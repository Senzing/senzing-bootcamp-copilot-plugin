# Marketplace development and validation

The public catalog is `.github/plugin/marketplace.json`. It points to the
bootcamper package at `plugins/senzing-bootcamp/`. Keep marketplace name
`senzing-bootcamp`, owner `Senzing`, and identifier
`senzing-bootcamp@senzing-bootcamp` stable.

## Local checks

Use Python 3.10 or later for validation tooling (the plugin has its own runtime
prerequisites). From the repository root:

```sh
python3 -m pip install -r tools/requirements.txt
python3 tools/validate_marketplace.py
python3 -m unittest discover -s tools/tests -v
cspell lint --config .vscode/cspell.json --no-progress '**'
git diff --check
```

The model-free validator checks public catalog identity, unique plugin names,
repository-contained paths (including symlinks), manifest agreement, Agent Plugins
schemas, MCP configuration, all 12 skill entry points, hook command paths, and
bundled resources. It never imports or executes plugin code or contacts MCP.
Errors exit nonzero with a diagnostic.

`tools/schemas/` contains the validation rules from the
[Agent Plugins 1.0 plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
and [MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json),
retrieved 2026-11-05; descriptive annotations are omitted, validation rules are
unchanged. These local copies keep validation independent of network availability.
Review schema updates deliberately alongside package compatibility and tests.
`tools/requirements.txt` contains only validation dependencies, not plugin runtime
dependencies. Unit tests use Python's standard library.

The validator deliberately checks the current public package contract, not every
possible marketplace or plugin format. Intentional changes to skill count, MCP,
hooks, public identity, or distribution layout need corresponding tests and review.
Curriculum references to sibling repositories are not distribution metadata leaks.

## Ownership and propagation

Existing `.github/CODEOWNERS` assigns `.github/` (including catalog and workflow)
to `@Senzing/senzing-devsecops`; other paths use `@Senzing/senzing-community`.
No ownership change is needed for this catalog.

Development propagation copies only the generated bootcamper payload. Public
catalog metadata, documentation, validation tools, and CI are maintained here,
outside that payload. Do not overwrite or remove them during a payload update.
After propagation, rerun validation and review catalog/manifest agreement,
resources, README, and Hub instructions before publication. No development
marketplace name or repository URL belongs in public distribution metadata.
Changes to the development propagation contract belong in a separate issue there.

## Publication versus verification

Merge/publish only through normal maintainer approval. Confirm that the catalog
and payload are readable on remote `main` before marking
[issue #6](https://github.com/Senzing/senzing-bootcamp-copilot-plugin/issues/6) complete.
A feature-branch/local catalog does not establish public availability.

[Issue #7](https://github.com/Senzing/senzing-bootcamp-copilot-plugin/issues/7)
owns remote CLI/app installation, management, and app runtime verification.
Static CI is not evidence that hooks execute, MCP connects, or app skills work.
Record exact revision, plugin/client versions, OS, date, and outcomes there;
failures, unsupported operations, and unrun checks must not be reported passing.
Keep availability and support notices in README and the Hub page until evidence
justifies updating them. Do not claim support for untested versions or OSes.
