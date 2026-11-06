# App verification checklist

Use this checklist with the [0.6.1 test record](test-records/0.6.1.md).
It is a procedure, not evidence that checks passed. Record observed controls,
commands, outcomes, and failures under the same app version/OS; do not mark a
row passing from a static script test or a different client.

## Preparation and installation

1. Record the date, exact GitHub Copilot app version, OS, Python version, public
   default-branch revision, and plugin version. Confirm the app is signed in,
   policy permits the plugin, and `python3` is available to app hook processes.
2. Use a fresh app profile or supported isolated configuration and empty synthetic
   project A. Obtain authorization before modifying any personal app settings.
   Record how isolation is achieved; do not assume `COPILOT_HOME` controls the app.
3. In Customize, use the marketplace settings control to add
   `https://github.com/Senzing/senzing-bootcamp-copilot-plugin`. Record the actual
   UI labels. Stop and record unsupported controls or access restrictions.
4. Search `senzing-bootcamp`, record its displayed/searchable name, install it, and
   confirm Installed/enabled using actual app controls.
5. Disable and re-enable it using app controls; confirm each resulting state.
   Start a new session where the client requires one.

## Runtime in project A

1. Record discovery and a safe invocation outcome for each of the 12 skills in
   `plugins/senzing-bootcamp/skills/`. Enumerate their actual installed names in
   the record; installation reporting a count is insufficient.
2. Start the bootcamp. Use app diagnostics/logs to establish that hooks resolve
   `${PLUGIN_ROOT}` to the installed/cache directory, not this source checkout.
   Record the resolved root and observed hook events without exposing secrets.
3. Make a live Senzing MCP call from the app. Record the server/tool, sanitized
   inputs, and meaningful result. An external CLI/MCP call is not app evidence.
4. Complete one representative module. Record its name, live MCP interaction,
   completion evidence, and that each yielding turn asks only one question.
5. End and reopen a session in project A. Verify progress and resume data persist.
   Open unrelated empty synthetic project B and verify no progress or session
   information from A appears. Check notes/feedback handling with and without an
   active bootcamp, recording whether any files or submissions were produced.
6. With synthetic content only, request an allowed in-project write, an
   out-of-project write to a disposable test location, and an obvious-secret
   write containing only a clearly fake test value. Record allowed/denied
   outcomes and hook diagnostics. A client permission denial alone does not
   demonstrate the plugin write guard; do not broaden permissions to force it.
7. Verify stop handling with a closing question and without one. Record whether
   the former ends normally and the latter requests the intended continuation.
   End the session and verify cleanup without deleting persisted progress.
8. Exercise the plugin's documented checkpoint fallback and resume from it.
   Automatic pre-compaction is not configured; do not claim it was tested.

## Update and removal

1. Use the actual app update controls. Record the available control, starting
   version/revision, target version/revision, and resulting installed version.
   An unchanged-version/no-op result is not proof of a changed-version upgrade.
   If no changed public version is available, record that limitation rather
   than fabricating a release or replacing the remote catalog with a local one.
2. Remove the plugin and marketplace using the app controls. Record the labels,
   absence from Installed/catalog selection, and whether a restart is required.
   Restore only test-owned settings; do not remove pre-existing user resources.

Record each required check as passed, failed, unsupported, blocked, or unrun.
Keep parent issue #5 open while any required check has not passed. Issue #7 was
closed before all checks passed; do not treat closure as acceptance evidence or
reopen it without authorization. Publish only sanitized observations; never
include credentials, private transcripts, or real sensitive data.
