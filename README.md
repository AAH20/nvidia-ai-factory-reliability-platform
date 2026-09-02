# NVIDIA AI Factory Reliability and Capacity Control Plane

**AI infrastructure · GPU cluster · NVIDIA NIM · Kubernetes · inference optimization · InfiniBand · RoCE · RDMA · NVLink · Terraform · OpenTofu · Ansible · AIOps · platform engineering · SRE · FinOps · GraphRAG**

[![CI](https://github.com/AAH20/nvidia-ai-factory-reliability-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/AAH20/nvidia-ai-factory-reliability-platform/actions/workflows/ci.yml) [![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](pyproject.toml) [![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A topology-aware reliability and capacity reference platform that correlates NVIDIA NIM inference behavior with GPU allocation, Kubernetes state, network-fabric health, infrastructure changes and verified business economics.

> **Evidence boundary:** topology analysis, KPI calculations, diagnosis, action ranking and release gating are implemented and tested. The included AI-factory incident and economics are synthetic. NVIDIA NIM, GPU hardware, Kubernetes, cloud, Terraform/OpenTofu, Ansible and network tools are integration contracts until executed against corresponding systems.

## Business problem

Purchased GPU-hours do not automatically become SLO-compliant, revenue-producing model output. Capacity is lost through scheduling fragmentation, unavailable replicas, KV-cache pressure, queue saturation, model-cache misses, fabric degradation, storage bottlenecks and unsafe infrastructure changes.

The platform asks:

> How much billable, SLO-compliant model output is produced by every GPU-hour purchased—and which verified change improves that yield?

## Run locally without GPUs

```bash
PYTHONPATH=src python3 -m ai_factory_reliability.cli examples/synthetic-ai-factory-incident.json
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Implemented proof

- Dependency-aware AI-factory topology traversal
- Fabric degradation, congestion and loss detection
- NIM replica readiness, latency, queue and cache analysis
- GPU allocation, utilization and stranded-capacity KPIs
- Cross-layer diagnosis across inference, GPU capacity and network fabric
- Expected-value remediation ranking
- Deterministic simulation-eligibility gate
- SHA-256 analysis receipt
- Explicit evidence tiers for code, scenario, integrations and economics

## Architecture

```text
NIM + DCGM + Kubernetes + Slurm + fabric + storage + billing
                             ↓
          temporal AI-factory topology and GraphRAG
                             ↓
     context compiler → specialist agents → deterministic policy
                             ↓
      digital twin → benchmark → approval → canary → verify
                             ↓
        capacity, reliability and verified-economics data flywheel
```

See [architecture](docs/architecture.md), [KPI dictionary](docs/kpi-dictionary.md) and [local validation path](docs/local-validation.md).

## Orchestration boundaries

| Component | Exact responsibility |
|---|---|
| Paperclip | Programs, budgets, priorities and assignments |
| OpenClaw-compatible gateway | Persistent operations interface, schedules and skills |
| LangGraph | Sole durable workflow-state owner |
| CrewAI | Specialist collaboration within bounded stages |
| LangChain | Model, retriever and tool adapters |
| NeMo Agent Toolkit | Agent profiling, evaluation and observability |
| Temporal GraphRAG | GPU, network, workload, change and incident context |
| Deterministic policy engine | Authorization |

## Automation scope

- **IaC:** Terraform, OpenTofu, Bicep, CloudFormation, Pulumi, Helm and Kustomize
- **Network:** Ansible, Nornir, Netmiko, NAPALM, Batfish, pyATS, containerlab, gNMI, NETCONF and RESTCONF
- **Configuration:** Ansible, Chef and Puppet
- **Compliance as Code:** OPA, Conftest, Checkov, InSpec, Kyverno, Gatekeeper and cloud-native policy services

## Primary KPI

```text
AI Factory Yield = SLO-compliant billable model output / purchased GPU-hours
```

Supporting metrics cover GPU utilization, inference latency and throughput, fabric health, reliability, agent quality, operating cost and verified value.

## Official technical basis

- [NVIDIA NIM logging and observability](https://docs.nvidia.com/nim/large-language-models/latest/nim-per-request-metrics.html)
- [NVIDIA NIM latency-throughput benchmarking](https://docs.nvidia.com/nim/benchmarking/llm/latest/index.html)
- [NVIDIA NIM architecture](https://docs.nvidia.com/nim/large-language-models/latest/reference/architecture.html)
- [NVIDIA Base Command Manager](https://docs.nvidia.com/base-command-manager/)
- [NVIDIA AI Factory observability guide](https://docs.nvidia.com/enterprise-reference-architectures/observability-guide/latest/abstract.html)

## Engage

[Request an AI factory reliability and GPU-capacity assessment](https://a2zsoc.com/contact?topic=nvidia-ai-factory-reliability&utm_source=github&utm_medium=repository).
