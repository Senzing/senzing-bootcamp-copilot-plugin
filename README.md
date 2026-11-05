# Senzing Bootcamp for GitHub Copilot

A guided, hands-on introduction to Senzing entity resolution. Start with a business
problem and work through setup, data preparation, loading, querying, and graduation.
This repository hosts both the Copilot plugin and its public marketplace catalog.

[Read the Copilot quick-start guide](https://hub.senzing.com/senzing-bootcamp-copilot-plugin/).

## Availability and prerequisites

The marketplace name is `senzing-bootcamp`; its plugin identifier is
`senzing-bootcamp@senzing-bootcamp`.

**Publication and verification are pending.** The catalog and payload must be on
this repository's default branch before remote marketplace installation works.
[Issue #6](https://github.com/Senzing/senzing-bootcamp-copilot-plugin/issues/6)
tracks publication; [issue #7](https://github.com/Senzing/senzing-bootcamp-copilot-plugin/issues/7)
tracks remote installation and app runtime verification. The instructions below
follow documented client controls, not a successful public installation test.
Existing development CLI evidence does not certify the public marketplace or app.

You need:

- A signed-in GitHub account with Copilot access and read access to this repository.
- A client with plugin support and organization/enterprise policy permitting this
  marketplace, plugin, and its tools.
- Network access to the Senzing MCP server at `https://mcp.senzing.com/mcp`.
- Python 3 available as **`python3` on `PATH`**, including on Windows. The hooks
  invoke that command; a `python` or `py` alias alone does not satisfy it.
- A new, empty project folder for bootcamp work.

Review the plugin's skills, scripts, hooks, MCP configuration, and requested tool
permissions before trusting or enabling it. Hook commands execute local Python.
Do not grant access beyond what you intend to use.

## Install in the GitHub Copilot app

1. Open the app and sign in; open your empty bootcamp project folder.
2. Open **Customize**, then the marketplace settings control beside the
   marketplace dropdown.
3. Add `https://github.com/Senzing/senzing-bootcamp-copilot-plugin`.
4. Search for `senzing-bootcamp` (Senzing Bootcamp) and select **Install**.
5. Open **Installed** and confirm the plugin is enabled.

These are [GitHub's documented app controls](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app#adding-a-plugin-marketplace).
Actual display names, update/removal controls, and runtime behavior remain
unverified until #7 records them. Manage the app's activation under
**Customize → Installed**; do not assume CLI commands manage the app configuration.

## Install through the CLI marketplace

After default-branch publication:

```sh
copilot plugin marketplace add Senzing/senzing-bootcamp-copilot-plugin
copilot plugin marketplace browse senzing-bootcamp
copilot plugin install senzing-bootcamp@senzing-bootcamp
copilot plugin enable senzing-bootcamp@senzing-bootcamp
copilot plugin list
```

Start a new session after installing or enabling the plugin. Open your empty
project folder and enter **Start the bootcamp** in Copilot chat.

To refresh the catalog and update the plugin:

```sh
copilot plugin marketplace update senzing-bootcamp
copilot plugin update senzing-bootcamp@senzing-bootcamp
```

To disable it, re-enable it, or remove it and the catalog:

```sh
copilot plugin disable senzing-bootcamp@senzing-bootcamp
copilot plugin enable senzing-bootcamp@senzing-bootcamp
# Only when you want to remove the installation:
copilot plugin uninstall senzing-bootcamp@senzing-bootcamp
copilot plugin marketplace remove senzing-bootcamp
```

**Optional direct installation:** CLI can also install from the repository
subdirectory. This bypasses marketplace discovery and is not a marketplace test.

```sh
copilot plugin install Senzing/senzing-bootcamp-copilot-plugin:plugins/senzing-bootcamp
```

Do not install both routes merely to test discovery; use a clean or isolated
configuration. Direct installations use the unqualified name `senzing-bootcamp`
for management rather than the marketplace-qualified identifier.

## Troubleshooting and support status

If the marketplace cannot be added or the plugin is absent, check that the catalog
and payload are published on the default branch, GitHub authentication/read access,
client plugin support, and organization policy. Report restrictions rather than
bypassing managed settings.

If installation succeeds but bootcamp features do not load, confirm the plugin is
enabled, start a new session, check `python3 --version`, and verify access to
`mcp.senzing.com`. Installation, activation, skills, MCP, and lifecycle hooks are
separate checks. Do not treat successful installation as runtime certification.

The app's tested version/OS and limitations will be recorded in #7. The existing
checkpoint fallback remains in place; automatic pre-compaction is not configured.
This is a Senzing Garage project, not a production-readiness guarantee.

## Maintain the marketplace

See [development and validation](docs/development.md) for local checks, schema
provenance, ownership, and how public distribution differs from payload propagation.
See [contributing](CONTRIBUTING.md) and [security reporting](SECURITY.md).
