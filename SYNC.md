# Automatic release synchronization

This repository follows the healthy deployed Infraveil release, not every private
development commit. A server-side job checks every five minutes; the owner's PC
does not need to be running. Scheduling and network failures can delay updates.

`SOURCE-RELEASE.json` identifies the release and exact exported file hashes.
The runtime repository contains the seven generic sources already published at
https://repo.infraveil.com/. The dashboard repository contains only its frontend
templates, controllers, styles, shared UI modules and named supporting assets.
The hosted backend, administrative console, private Git history, environment,
workspace data, credentials and release archives are not mirrored.

Publication checks the active API health/readiness, installed release file hashes,
and prepared/public runtime consistency. Release signature approval remains the
normal deployer's responsibility; this observer never receives its signing key.

Updates use normal parent-linked commits and non-forced pushes. No-change checks
create no commits. A failure retains the last good public revision and reports a
failed/partial synchronization; it does not roll back healthy application code.
Each repository records its own release because two Git pushes are not atomic.

Do not edit mirrored source files here as the source of truth. Make changes through
Infraveil's normal source review and release process. Repository documentation and
license notices retain their own ownership; publication does not change licensing.
