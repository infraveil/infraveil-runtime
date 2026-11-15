# Infraveil customer-side runtime source

Infraveil is a backend operations control plane. Its hosted dashboard coordinates
operations; the installer, launcher, and service agents run on supported customer
infrastructure. This public repository contains those customer-side components,
not the proprietary hosted backend or customer workspace data.

## Follow the operating path

1. **Connect a server:** `payload_templates/infraveil.py` implements the Trust
   Console setup, enrollment, review, and verified launcher installation flow.
2. **Manage agents:** `payload_templates/launcher.py.j2` reconciles assigned agent
   lifecycles, verifies runtime releases, supervises agent processes, and reports
   host/runtime state to the control plane.
3. **Operate services:** `payload_templates/professional_agent.py.j2` prepares
   configured application releases, runs and supervises service processes, checks
   health, applies bounded restart/recovery behavior, and operates configured
   managed gateway routes and policy.

For supported supervised services, configuration describes the commands, health
checks, persistent paths, and routes. Business logic does not need an Infraveil
SDK. Process supervision is not instruction-level containment or an application
sandbox. External-process observation has different ownership and recovery
boundaries from managed-package supervision.

## Files

- [Installer / Trust Console](payload_templates/infraveil.py)
- [Launcher template](payload_templates/launcher.py.j2)
- [Service-agent template](payload_templates/professional_agent.py.j2)
- [Starter application example](payload_templates/starter_server.js.j2)
- [Supporting local-ledger inspection tool](tools/verify-ledger.py)
- [License](LICENSE)

Browse these files at <https://repo.infraveil.com/> or clone this public scope:

```sh
git clone https://repo.infraveil.com/runtime.git
```

## Published source versus installed software

The `.j2` files are templates. The public installer contains setup placeholders.
Use the supported portal setup flow to enroll a server; copying these unconfigured
files is not a personalized installation.

Workspace settings, host identity, approved versions, rendering, and release
selection affect installed bytes. A periodically synchronized public template is
not proof that every host is running the same version. Compare your installation
against its selected release and exact source/hash receipts. The public
`source-manifest.json` identifies published file bytes; it is not an independent
signature, security audit, or customer deployment attestation.

## Operating documentation

- [Platform and runtime operating model](https://infraveil.com/platform)
- [Architecture](https://infraveil.com/how-it-works)
- [Setup and operation](https://infraveil.com/documentation)
- [Source and product boundaries](https://infraveil.com/transparency)
- [Detailed architecture](https://whitepaper.infraveil.com/architecture)

Gateway protection covers configured managed routes, not every listener on a
host. Recovery depends on service configuration, available known-good releases,
application data compatibility, and infrastructure. Selected operational data
reaches the hosted control plane; customer-hosted applications do not imply that
all information remains local. See the current website and privacy notice for
the applicable data-handling and product boundaries.

## License

See the existing `LICENSE` file. Publishing inspectable source is not a claim of
an independent external audit or universal recovery guarantees.
