# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository packages the Senzing bootcamp for GitHub Copilot. It is one of
several per-assistant repositories carrying the same curriculum.

The repository currently holds only its community artifacts — README,
CONTRIBUTING, CODE_OF_CONDUCT, LICENSE, CHANGELOG, SECURITY, docs and the
GitHub workflows. The bootcamp content itself is added by the development team.

## CI/CD and Automation

GitHub Actions workflows use reusable workflows from [senzing-factory/build-resources](https://github.com/senzing-factory/build-resources).
Each one is described in [.github/workflows/README.md](../.github/workflows/README.md):

- **add-labels-standardized.yaml**: adds labels to new issues
- **add-to-project-senzing-dependabot.yaml**: adds Dependabot PRs to the Senzing organization project board
- **add-to-project-senzing.yaml**: adds issues to the Senzing organization project board
- **claude-pr-review.yaml**: automated review comment on opened and updated PRs
- **dependabot-approve-and-merge.yaml**: auto-approves and merges Dependabot PRs
- **link-issues-to-pr-post-merge.yaml**: links referenced issues when a PR merges
- **lint-workflows.yaml**: runs super-linter on pushes to non-main branches and PRs to main
- **move-pr-to-done-dependabot.yaml**: moves a merged PR to "Done" on the project board
- **spellcheck.yaml**: runs cspell on PRs to main

## Spelling

Spellcheck runs on every pull request against [.vscode/cspell.json](../.vscode/cspell.json).
New project vocabulary belongs in that word list rather than in a linter suppression.

## CHANGELOG Convention

CHANGELOG.md follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format with [Semantic Versioning](https://semver.org/). Changes are manually curated (not auto-generated) to describe user-facing impacts.

## Claude Slash Commands

- `/senzing` - Runs steps from the centralized senzing command
