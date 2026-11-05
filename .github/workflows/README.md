# Workflows

## add-labels-standardized.yaml

When issues are opened,
this action adds appropriate labels to the issue.
(e.g. "triage", "customer-submission")

- [Add Labels Standardized GitHub Action]
  - Uses: [senzing-factory/build-resources/.../add-labels-to-issue.yaml]

## add-to-project-senzing-dependabot.yaml

When a Dependabot Pull Request (PR) is made against `main` branch,
this action adds the PR to the Senzing organization project board as "In Progress".

- [Add to Project Senzing Dependabot GitHub Action]
  - Uses: [senzing-factory/build-resources/.../add-to-project-dependabot.yaml]

## add-to-project-senzing.yaml

When an issue is created,
this action adds the issue to the Senzing organization project board as "Backlog".

- [Add to Project Senzing GitHub Action]
  - Uses: [senzing-factory/build-resources/.../add-to-project.yaml]

## claude-pr-review.yaml

When a Pull Request is opened or updated,
this action posts an automated review of the diff as a comment on the PR.

- [Claude PR Review GitHub Action]
  - Uses: [senzing-factory/build-resources/.../claude-pr-review.yaml]

## dependabot-approve-and-merge.yaml

When a Dependabot Pull Request (PR) is made against the `main` branch,
this action determines if it should be automatically approved and merged into the `main` branch.
Once this action occurs [move-pr-to-done-dependabot.yaml] moves the PR on the project board to "Done".

- [Dependabot Approve and Merge GitHub Action]
  - Uses: [senzing-factory/build-resources/.../dependabot-approve-and-merge.yaml]

## link-issues-to-pr-post-merge.yaml

When a Pull Request is merged into the `main` branch,
this action links the issues the PR references so they close with it.

- [Link Issues to PR Post Merge GitHub Action]
  - Uses: [senzing-factory/build-resources/.../link-issues-to-pr-post-merge.yaml]

## lint-workflows.yaml

When a change is committed to GitHub or a Pull Request is made against the `main` branch,
this action runs [super-linter] to run multiple linters against the code.

- [Lint Workflows GitHub Action]
  - Configuration:
    - [.checkov.yaml]
    - [.jscpd.json]
    - [.yaml-lint.yml]
  - Uses: [senzing-factory/build-resources/.../lint-workflows.yaml]

## move-pr-to-done-dependabot.yaml

When a Pull Request is merged into the `main` branch,
this action moves the PR on the project board to "Done".

- [Move PR to Done Dependabot GitHub Action]
  - Uses: [senzing-factory/build-resources/.../move-pr-to-done-dependabot.yaml]

## spellcheck.yaml

When a Pull Request is made against the `main` branch,
this action runs [cspell] against the repository.

- [Spellcheck GitHub Action]
  - Configuration:
    - [.vscode/cspell.json]
  - Uses: [senzing-factory/build-resources/.../cspell.yaml]

## validate-marketplace.yaml

On pull requests and pushes to `main`, this model-free workflow validates the
public marketplace catalog and bundled plugin, then runs the validator's focused
unit tests. It uses `tools/requirements.txt`; run the same commands from
[development and validation](../../docs/development.md) before opening a PR.
It does not certify remote installation or app runtime behavior.

[.checkov.yaml]: ../linters/README.md#checkovyaml
[.jscpd.json]: ../linters/README.md#jscpdjson
[.vscode/cspell.json]: ../../.vscode/cspell.json
[.yaml-lint.yml]: ../linters/README.md#yaml-lintyml
[Add Labels Standardized GitHub Action]: add-labels-standardized.yaml
[Add to Project Senzing Dependabot GitHub Action]: add-to-project-senzing-dependabot.yaml
[Add to Project Senzing GitHub Action]: add-to-project-senzing.yaml
[Claude PR Review GitHub Action]: claude-pr-review.yaml
[cspell]: https://cspell.org/
[Dependabot Approve and Merge GitHub Action]: dependabot-approve-and-merge.yaml
[Link Issues to PR Post Merge GitHub Action]: link-issues-to-pr-post-merge.yaml
[Lint Workflows GitHub Action]: lint-workflows.yaml
[Move PR to Done Dependabot GitHub Action]: move-pr-to-done-dependabot.yaml
[move-pr-to-done-dependabot.yaml]: move-pr-to-done-dependabot.yaml
[senzing-factory/build-resources/.../add-labels-to-issue.yaml]: https://github.com/senzing-factory/build-resources/blob/main/.github/workflows/add-labels-to-issue.yaml
[senzing-factory/build-resources/.../add-to-project-dependabot.yaml]: https://github.com/senzing-factory/build-resources/blob/main/.github/workflows/add-to-project-dependabot.yaml
[senzing-factory/build-resources/.../add-to-project.yaml]: https://github.com/senzing-factory/build-resources/blob/main/.github/workflows/add-to-project.yaml
[senzing-factory/build-resources/.../claude-pr-review.yaml]: https://github.com/senzing-factory/build-resources/blob/main/.github/workflows/claude-pr-review.yaml
[senzing-factory/build-resources/.../cspell.yaml]: https://github.com/senzing-factory/build-resources/blob/main/.github/workflows/cspell.yaml
[senzing-factory/build-resources/.../dependabot-approve-and-merge.yaml]: https://github.com/senzing-factory/build-resources/blob/main/.github/workflows/dependabot-approve-and-merge.yaml
[senzing-factory/build-resources/.../link-issues-to-pr-post-merge.yaml]: https://github.com/senzing-factory/build-resources/blob/main/.github/workflows/link-issues-to-pr-post-merge.yaml
[senzing-factory/build-resources/.../lint-workflows.yaml]: https://github.com/senzing-factory/build-resources/blob/main/.github/workflows/lint-workflows.yaml
[senzing-factory/build-resources/.../move-pr-to-done-dependabot.yaml]: https://github.com/senzing-factory/build-resources/blob/main/.github/workflows/move-pr-to-done-dependabot.yaml
[Spellcheck GitHub Action]: spellcheck.yaml
[super-linter]: https://github.com/super-linter/super-linter
