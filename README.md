# Senzing Bootcamp for GitHub Copilot

A guided, hands-on introduction to Senzing entity resolution. Start with a business
problem and work through setup, data preparation, loading, querying, and graduation.
This repository hosts both the Copilot plugin and its public marketplace catalog.

[Read the Copilot quick-start guide](https://hub.senzing.com/senzing-bootcamp-copilot-plugin/).

## Availability and prerequisites

The marketplace name is `senzing-bootcamp`; its plugin identifier is
`senzing-bootcamp@senzing-bootcamp`.

**Published; remote CLI lifecycle verified; app runtime verification partial.**
The catalog and payload are on this repository's default branch.
The [0.6.1 test record](docs/test-records/0.6.1.md) records remote marketplace
installation and management with CLI 1.0.105 on Ubuntu 24.04.5 LTS.
The update check used the same published version, not a changed-version upgrade.
Selected installation, management, MCP, module, and same-checkout resume flows
were also observed in Copilot app 1.1.35. An initial secret-like write check
failed on an earlier revision; after the merged hook fix, synthetic write
probes on `9d72e36` were allowed or denied as intended. Several required checks
remain unrun. [Issue
#7](https://github.com/Senzing/senzing-bootcamp-copilot-plugin/issues/7) was
closed before those checks were complete; the parent [issue
#5](https://github.com/Senzing/senzing-bootcamp-copilot-plugin/issues/5)
remains open. Neither CLI installation nor partial app testing certifies all
skills, hooks, write guards, or app compatibility.

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
The observed display name and selected runtime results are in the test record;
some app checks remain incomplete. Manage the app's activation under
**Customize → Installed**; do not assume CLI commands manage the app configuration.

## Install through the CLI marketplace

The remote marketplace lifecycle below was verified in an isolated CLI configuration:

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

The [test record](docs/test-records/0.6.1.md) documents the tested app version/OS
and limitations. Issue #7 is closed, but app acceptance remains incomplete and
parent issue #5 remains open. The checkpoint fallback remains in place;
automatic pre-compaction is not configured.
This is a Senzing Garage project, not a production-readiness guarantee.

## Maintain the marketplace

See [development and validation](docs/development.md) for local checks, schema
provenance, ownership, and how public distribution differs from payload propagation.
See [contributing](CONTRIBUTING.md) and [security reporting](SECURITY.md).
