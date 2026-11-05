import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_marketplace as validator


class MarketplaceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "repository"
        self.catalog_path = self.root / ".github/plugin/marketplace.json"
        self.catalog_path.parent.mkdir(parents=True)
        self.catalog = validator.read_json(validator.ROOT / ".github/plugin/marketplace.json")
        self.plugin = self.root / "plugins/senzing-bootcamp"
        shutil.copytree(validator.ROOT / "plugins/senzing-bootcamp", self.plugin)
        self.write(self.catalog_path, self.catalog)

    def write(self, path, value):
        path.write_text(json.dumps(value), encoding="utf-8")

    def invalid(self, expected):
        with self.assertRaisesRegex(validator.InvalidPackage, expected):
            validator.validate(self.root)

    def test_public_package_and_optional_matching_version(self):
        validator.validate(self.root)
        self.catalog["plugins"][0]["version"] = "0.6.1"
        self.write(self.catalog_path, self.catalog)
        validator.validate(self.root)

    def test_invalid_catalog_shape_and_identity(self):
        for field, value, message in (
            ("name", "senzing-bootcamp-development", "marketplace name"),
            ("owner", {"name": "docktermj"}, "owner must be"),
            ("metadata", {}, "metadata.description"),
            ("plugins", [], "nonempty array"),
            ("plugins", [False], "entry must be an object"),
        ):
            with self.subTest(field=field, value=value):
                self.write(self.catalog_path, {**self.catalog, field: value})
                self.invalid(message)
        self.write(self.catalog_path, [])
        self.invalid("catalog must be an object")

    def test_missing_and_malformed_catalog_are_reported_by_cli(self):
        for content in ("{", '{"name":"one","name":"two"}'):
            with self.subTest(content=content):
                self.catalog_path.write_text(content, encoding="utf-8")
                output = io.StringIO()
                with patch.object(validator, "ROOT", self.root):
                    with contextlib.redirect_stderr(output):
                        self.assertEqual(validator.main(), 1)
                self.assertIn("Marketplace validation failed:", output.getvalue())
        self.catalog_path.unlink()
        with self.assertRaisesRegex(validator.InvalidPackage, "missing file"):
            validator.validate(self.root)

    def test_duplicate_and_invalid_names(self):
        self.catalog["plugins"] *= 2
        self.write(self.catalog_path, self.catalog)
        self.invalid("duplicate plugin name")
        for name in (None, {}, "", "Invalid Name", "another-plugin"):
            with self.subTest(name=name):
                self.catalog["plugins"] = [{**self.catalog["plugins"][0], "name": name}]
                self.write(self.catalog_path, self.catalog)
                self.invalid("plugin name|name mismatch")

    def test_unsafe_and_missing_sources(self):
        for source in ("/tmp/outside", "C:/outside", r"..\outside", "../outside", "./missing"):
            with self.subTest(source=source):
                self.catalog["plugins"][0]["source"] = source
                self.write(self.catalog_path, self.catalog)
                self.invalid("relative file|escapes package|missing file")
        self.catalog["plugins"][0]["source"] = "./plugins/senzing-bootcamp/."
        self.write(self.catalog_path, self.catalog)
        self.invalid("source must be")

    def test_manifest_symlink_escape(self):
        manifest = self.plugin / "plugin.json"
        outside = self.root.parent / "outside.json"
        shutil.copyfile(manifest, outside)
        manifest.unlink()
        manifest.symlink_to(outside)
        self.invalid("escapes package")

    def test_source_symlink_escape(self):
        outside = self.root.parent / "outside"
        shutil.move(self.plugin, outside)
        self.plugin.symlink_to(outside, target_is_directory=True)
        self.invalid("escapes package")

    def test_manifest_schema_and_public_references(self):
        path = self.plugin / "plugin.json"
        original = validator.read_json(path)
        for changes, message in (
            ({"skills": ["skills"]}, "plugin schema"),
            ({"version": 1}, "plugin schema"),
            ({"version": "broken"}, "stable SemVer"),
            ({"repository": "https://github.com/docktermj/development"}, "public repository"),
            ({"homepage": ""}, "public repository"),
            ({"keywords": ["senzing-bootcamp-development"]}, "development distribution"),
        ):
            with self.subTest(changes=changes):
                self.write(path, {**original, **changes})
                self.invalid(message)

    def test_catalog_manifest_mismatch(self):
        for field, value in (("description", "other"), ("version", "0.0.0"), ("version", None)):
            with self.subTest(field=field, value=value):
                catalog = json.loads(json.dumps(self.catalog))
                catalog["plugins"][0][field] = value
                self.write(self.catalog_path, catalog)
                self.invalid(f"{field} mismatch")

    def test_mcp_schema_and_endpoint(self):
        path = self.plugin / "mcp.json"
        original = validator.read_json(path)
        for server, message in (
            ({"type": "http", "url": "https://mcp.senzing.com/mcp"}, "mcp schema"),
            ({"type": "streamable-http"}, "mcp schema"),
            ({"type": "streamable-http", "url": "https://example.com"}, "public Senzing"),
        ):
            with self.subTest(server=server):
                self.write(path, {**original, "mcpServers": {"senzing": server}})
                self.invalid(message)

    def test_skill_discovery_and_frontmatter(self):
        path = self.plugin / "skills/bootcamp-onboarding/SKILL.md"
        original = path.read_text(encoding="utf-8")
        for content in ("no header", "---\nname: wrong\n---\nbody", "---\n[]\n---\nbody"):
            with self.subTest(content=content):
                path.write_text(content, encoding="utf-8")
                self.invalid("frontmatter|invalid skill")
        path.write_text(original, encoding="utf-8")
        path.unlink()
        self.invalid("missing file")

    def test_hooks_require_installed_paths_and_files(self):
        path = self.plugin / "com.github.copilot/hooks/hooks.json"
        original = validator.read_json(path)
        for command in (
            "python3 /checkout/scripts/copilot-hooks.py session-start",
            'python3 "${PLUGIN_ROOT}/missing.py" session-start',
            'python3 "${PLUGIN_ROOT}/../outside.py" session-start',
        ):
            with self.subTest(command=command):
                hooks = json.loads(json.dumps(original))
                hooks["hooks"]["sessionStart"][0]["command"] = command
                self.write(path, hooks)
                self.invalid("plugin-root|missing file|escapes package")
        self.write(path, {**original, "hooks": {}})
        self.invalid("hook events")

    def test_bundled_resource_missing(self):
        for name in ("scripts/vendor/d3.v7.min.js", "scripts/secret_patterns.py"):
            with self.subTest(name=name):
                path = self.plugin / name
                original = path.read_bytes()
                path.unlink()
                self.invalid("missing file")
                path.write_bytes(original)

    def test_sibling_curriculum_reference_is_not_a_distribution_leak(self):
        path = self.plugin / "skills/bootcamp-onboarding/ground-rules.md"
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\nSee docktermj/senzing-bootcamp-claude-plugin-development.\n")
        validator.validate(self.root)


if __name__ == "__main__":
    unittest.main()
