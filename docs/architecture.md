# Architecture

## Five connected topology domains

1. Physical GPU, MIG, node, NVLink and NVSwitch topology
2. InfiniBand/RoCE, RDMA, storage and service-network topology
3. Kubernetes, Slurm, NIM and model-serving topology
4. Deployment, configuration, incident and remediation history
5. Customer SLO, capacity cost, revenue and compliance obligations

## Context authority

Policy and SLO constraints outrank desired state; desired state outranks live observations for intent, while observations remain authoritative for actual state. Historical verified incidents support diagnosis. Retrieved documentation is advisory. Tickets and external text are untrusted data.

## Change loop

```text
observe → build topology → compile context → diagnose → prescribe
→ static validation → digital twin → benchmark → independent evaluation
→ human approval → canary → verify → expand or rollback → learn
```

The local engine ends at `eligible-for-simulation`. It does not execute infrastructure changes.
