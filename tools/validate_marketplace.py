#!/usr/bin/env python3
"""Validate the public marketplace and its package without loading plugin code."""

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
NAME = "senzing-bootcamp"
REPOSITORY = "https://github.com/Senzing/senzing-bootcamp-copilot-plugin"
SOURCE = "./plugins/senzing-bootcamp"
SCHEMAS = Path(__file__).resolve().parent / "schemas"


class InvalidPackage(ValueError):
    """A validation error that can be presented without a traceback."""


def require(condition, message):
    if not condition:
        raise InvalidPackage(message)


def local_file(root, relative):
    require(
        isinstance(relative, str)
        and relative
        and "\\" not in relative
        and not re.match(r"^(?:/|[A-Za-z]:)", relative),
        f"expected a relative file path: {relative!r}",
    )
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), f"path escapes package: {relative}")
    require(path.is_file(), f"missing file: {relative}")
    return path


def read_json(path):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"{path}: duplicate JSON key {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def schema_check(value, name):
    schema = read_json(SCHEMAS / f"{name}.schema.json")
    errors = sorted(
        Draft202012Validator(schema).iter_errors(value), key=lambda error: error.json_path
    )
    require(not errors, f"{name} schema: " + "; ".join(error.message for error in errors))


def validate(root=ROOT):
    root = root.resolve()
    catalog = read_json(local_file(root, ".github/plugin/marketplace.json"))
    require(isinstance(catalog, dict), "catalog must be an object")
    require(catalog.get("name") == NAME, f"marketplace name must be {NAME}")
    owner = catalog.get("owner")
    require(isinstance(owner, dict) and owner.get("name") == "Senzing", "owner must be Senzing")
    metadata = catalog.get("metadata")
    require(
        isinstance(metadata, dict)
        and isinstance(metadata.get("description"), str)
        and metadata["description"].strip(),
        "catalog metadata.description must be a nonempty string",
    )
    entries = catalog.get("plugins")
    require(isinstance(entries, list) and entries, "plugins must be a nonempty array")
    names = set()
    for entry in entries:
        require(isinstance(entry, dict), "plugin entry must be an object")
        name = entry.get("name")
        require(
            isinstance(name, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name),
            "plugin name must be kebab-case",
        )
        require(name not in names, f"duplicate plugin name: {name}")
        names.add(name)
        source = entry.get("source")
        require(isinstance(source, str), "plugin source must be a relative string")
        manifest_path = local_file(root, source + "/plugin.json")
        require(source == SOURCE, f"plugin source must be {SOURCE}")
        plugin = manifest_path.parent
        manifest = read_json(manifest_path)
        schema_check(manifest, "plugin")
        require(name == manifest["name"] == NAME, "catalog/manifest name mismatch")
        require(
            isinstance(entry.get("description"), str)
            and bool(entry["description"].strip())
            and entry["description"] == manifest.get("description"),
            "catalog/manifest description mismatch",
        )
        if "version" in entry:
            require(entry["version"] == manifest.get("version"), "catalog/manifest version mismatch")
        require(
            isinstance(manifest.get("version"), str)
            and re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", manifest["version"]),
            "public plugin version must be stable SemVer",
        )
        require(
            manifest.get("homepage") == manifest.get("repository") == REPOSITORY,
            "plugin homepage/repository must use the public repository",
        )
        require(
            "senzing-bootcamp-copilot-plugin-development" not in json.dumps([catalog, manifest])
            and "senzing-bootcamp-development" not in json.dumps([catalog, manifest]),
            "development distribution metadata is not allowed",
        )
        mcp = read_json(local_file(plugin, "mcp.json"))
        schema_check(mcp, "mcp")
        require(
            mcp["mcpServers"] == {
                "senzing": {"type": "streamable-http", "url": "https://mcp.senzing.com/mcp"}
            },
            "expected the public Senzing Streamable HTTP MCP server",
        )
        skill_root = plugin / "skills"
        require(skill_root.resolve().is_relative_to(plugin), "skills directory escapes package")
        skills = sorted(skill_root.iterdir())
        require(len(skills) == 12, "expected 12 curriculum skill directories")
        for skill in skills:
            require(skill.is_dir(), f"unexpected skills entry: {skill.name}")
            text = local_file(plugin, f"skills/{skill.name}/SKILL.md").read_text(encoding="utf-8")
            parts = text.split("---", 2)
            require(len(parts) == 3 and not parts[0].strip(), f"{skill.name}: missing frontmatter")
            header = yaml.safe_load(parts[1])
            require(
                isinstance(header, dict)
                and header.get("name") == skill.name
                and isinstance(header.get("description"), str)
                and header["description"].strip()
                and parts[2].strip(),
                f"{skill.name}: invalid skill name, description, or body",
            )
        hooks = read_json(local_file(plugin, "com.github.copilot/hooks/hooks.json"))
        require(isinstance(hooks, dict) and hooks.get("version") == 1, "invalid hooks version")
        events = hooks.get("hooks")
        require(
            isinstance(events, dict)
            and set(events) == {"sessionStart", "userPromptSubmitted", "preToolUse", "Stop", "sessionEnd"},
            "unexpected or missing hook events",
        )
        for event, commands in events.items():
            require(isinstance(commands, list) and commands, f"{event}: missing hook commands")
            for command in commands:
                require(isinstance(command, dict), f"{event}: command must be an object")
                text = command.get("command", "")
                require(isinstance(text, str), f"{event}: command must be a string")
                match = re.fullmatch(r'python3 "\$\{PLUGIN_ROOT\}/([^"]+)" ([a-z-]+)', text)
                require(
                    command.get("type") == "command" and match and command.get("cwd") == ".",
                    f"{event}: expected a plugin-root Python command with project cwd",
                )
                local_file(plugin, match[1])
        for resource in (
            "LICENSE",
            "scripts/session-start.py",
            "scripts/session-end.py",
            "scripts/feedback-capture.py",
            "scripts/checkpoint-tick.py",
            "scripts/write-gate.py",
            "scripts/secret_patterns.py",
            "scripts/recap_checkpoint.py",
            "scripts/brand_tokens.py",
            "scripts/senzing_logo_light.png",
            "scripts/vendor/d3.v7.min.js",
            "docs/examples/bootcamp_recap.example.pdf",
        ):
            local_file(plugin, resource)
    require(len(entries) == 1 and names == {NAME}, "expected exactly the Senzing Bootcamp entry")


def main():
    try:
        validate(ROOT)
    except (InvalidPackage, OSError, ValueError, RuntimeError, yaml.YAMLError) as error:
        print(f"Marketplace validation failed: {error}", file=sys.stderr)
        return 1
    print("Public marketplace and plugin package validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
