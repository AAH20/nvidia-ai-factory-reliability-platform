# NVIDIA AI Factory Reliability and Capacity Control Plane

**AI Infrastructure · NVIDIA NIM · GPU Cluster Management · Kubernetes GPU Operator · RoCEv2 RDMA · InfiniBand · NVLink · LangGraph · CrewAI · Paperclip · OpenClaw · Temporal GraphRAG · OpenTofu · Terraform · Ansible · Compliance as Code · OPA Rego · NIST 800-53 · AIOps · FinOps · SRE · LLM Inference Optimization**

[![CI](https://github.com/AAH20/nvidia-ai-factory-reliability-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/AAH20/nvidia-ai-factory-reliability-platform/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](pyproject.toml)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-NIM%20Compatible-76B900?logo=nvidia)](https://docs.nvidia.com/nim/)
[![Compliance](https://img.shields.io/badge/Compliance-NIST%20800--53%20%7C%20OSCAL-red)](docs/)

A topology-aware, autonomous self-healing and continuous compliance control plane that correlates **NVIDIA NIM inference behavior** with **GPU cluster allocation, Kubernetes GPU Operator states, RoCEv2/InfiniBand network fabric health, declarative OpenTofu/Terraform infrastructure mutations, and verified business economics**.

---

## The Urgent Commercial Problem: The Day-2 AI Factory Yield Crisis

Enterprises spend millions acquiring high-density GPU clusters (NVIDIA DGX H100/B200), yet purchased capacity routinely fails to convert into reliable, revenue-generating model throughput.

Modern AI factories face acute, high-frequency operational bottlenecks:
- **RoCEv2 PFC Deadlocks & Buffer Microbursts**: Priority Flow Control storms halt distributed NCCL all-reduce operations and spike Time to First Token (TTFT).
- **Inference KV-Cache Saturation**: Fragmented batching and cold starts degrade model latency and evict active customer sessions.
- **Silent Compliance Breaches**: Autoscaling policies cross-route restricted or sovereign data (HIPAA, FedRAMP High, EU AI Act) into non-compliant cloud regions.
- **Uncontrolled Cloud Burst Costs**: Agents spawn expensive cloud GPU fallbacks that violate margin floors.

```text
The Executive Question:
"How much revenue-producing, SLO-compliant model output does each purchased GPU-hour deliver—and can the infrastructure heal itself when network fabrics or inference endpoints degrade?"
```

---

## The Primary North Star KPI

$$\text{AI Factory Yield} = \frac{\text{SLO-Compliant Billable Model Output (Tokens)}}{\text{GPU-Hours Purchased}}$$

The platform tracks and optimizes:
- **GPU Capacity**: Active compute fraction, memory fragmentation, stranded GPU-hours.
- **NVIDIA NIM Performance**: P95/P99 TTFT, inter-token latency (ITL), KV-cache allocation, queue saturation.
- **Fabric Health**: RoCEv2 pause frame duration, ECN marking rate, packet loss, RDMA buffer pool utilization.
- **Unit Economics**: Gross margin per model endpoint, cost per verified remediation, protected revenue.

---

## Architecture & Multi-Tier Agentic Orchestration

To prevent non-deterministic agent conflicts, orchestration is structured into strictly bounded, hierarchical layers:

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           1. ECONOMIC GOVERNOR (PAPERCLIP)                       │
│ - Enforces macro token budgets, capital expenditure caps, and minimum 3x ROI.    │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   2. PERSISTENT OPERATOR GATEWAY (OPENCLAW-COMPATIBLE)           │
│ - Event-driven Prometheus trigger listeners (RoCE PFC breaches, TTFT spikes).    │
│ - Reusable, versioned operational skill mesh.                                    │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   3. DURABLE TWO-PHASE COMMIT ENGINE (LANGGRAPH)                 │
│ - State machine: Draft -> Batfish_Simulate -> Invariant_Proof -> Canary -> Commit│
│ - Reversible 15-minute leases with automated rollback upon health failure.       │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    4. BOUNDED SPECIALIST CREWS (CREWAI + LANGCHAIN)              │
│ - NIM Performance Specialist (KV-cache, Tensor Parallelism)                      │
│ - Network Fabric Specialist (RoCEv2, ECN, PFC, MTU 9000)                        │
│ - Compliance Auditor (Sovereignty, NIST 800-53, FIPS 140-3)                      │
│ - IaC Synthesizer (OpenTofu HCL & Ansible YAML)                                  │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     5. TEMPORAL CAUSAL GRAPH (TEMPORAL GRAPHRAG)                 │
│ - 5-layer time-indexed property graph: Hardware ↔ Fabric ↔ Workload ↔ History    │
│ - Temporal traversal evaluating state at incident time vs. desired state.       │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│               6. PHYSICAL EXECUTION & COMPLIANCE-AS-CODE ENFORCEMENT             │
│ - NVIDIA NIM API (/v1/health, /v1/metrics, Prometheus DCGM metrics)              │
│ - OpenTofu / Terraform (Kubernetes GPU Operator node pools, affinity, limits)   │
│ - Ansible (NVIDIA Cumulus Linux & SONiC switch buffer/QoS tuning)                │
│ - OPA / Rego & Machine-Readable NIST OSCAL System Security Plans                 │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start: Run Locally (Zero GPUs Required)

You can validate the full control plane locally using deterministic simulation fixtures without physical GPU hardware:

```bash
# 1. Run the Autonomous Self-Healing Pipeline on a RoCEv2 PFC Deadlock Incident:
PYTHONPATH=src python3 -m ai_factory_reliability.cli self-heal examples/roce-pfc-deadlock-llama3.json

# 2. Analyze a Cross-Layer AI Factory Telemetry Snapshot:
PYTHONPATH=src python3 -m ai_factory_reliability.cli analyze examples/synthetic-ai-factory-incident.json

# 3. Export Machine-Readable NIST OSCAL System Security Plan (SSP):
PYTHONPATH=src python3 -m ai_factory_reliability.cli export-oscal

# 4. Execute the Full Automated Test Suite:
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

---

## Implemented Proof & Key Modules

| Module | Core Responsibility |
| :--- | :--- |
| [`graphrag.py`](src/ai_factory_reliability/graphrag.py) | **Temporal GraphRAG Engine**: 5-layer causal graph evaluating time-stamped hardware, fabric, and compliance state. |
| [`paperclip.py`](src/ai_factory_reliability/orchestration/paperclip.py) | **Financial Governor**: Enforces budget headroom and mandatory $\ge 3\times$ ROI thresholds on actions. |
| [`openclaw.py`](src/ai_factory_reliability/orchestration/openclaw.py) | **Persistent Operator Gateway**: Event-driven alert listener and hot-reloadable skill mesh. |
| [`langgraph_engine.py`](src/ai_factory_reliability/orchestration/langgraph_engine.py) | **Durable 2PC State Machine**: Reversible 15-minute canary leases with automatic rollback. |
| [`crew.py`](src/ai_factory_reliability/orchestration/crew.py) | **CrewAI Specialist Debate**: Multi-agent consensus between NIM, Network, Compliance, and IaC engineers. |
| [`opentofu_generator.py`](src/ai_factory_reliability/automation/opentofu_generator.py) | **OpenTofu / Terraform HCL**: Synthesizes declarative Kubernetes GPU Operator & NIM patches. |
| [`ansible_generator.py`](src/ai_factory_reliability/automation/ansible_generator.py) | **Ansible Network Automation**: Configures RoCEv2 ECN thresholds, PFC lossless queues, and MTU 9000. |
| [`compliance_gate.py`](src/ai_factory_reliability/automation/compliance_gate.py) | **Compliance as Code**: OPA/Rego invariants (NIST 800-53, EU AI Act) and OSCAL SSP export. |
| [`receipts.py`](src/ai_factory_reliability/receipts.py) | **Cryptographic Action Receipts**: SHA-256 tamper-evident tokens binding telemetry, patches, and approvals. |

---

## Evidence Boundary

- **Implemented**: All topology graph traversal, Paperclip financial evaluations, LangGraph 2PC state transitions, CrewAI consensus logic, OpenTofu HCL generation, Ansible YAML synthesis, and OPA compliance gates are fully implemented in code and tested in CI.
- **Simulated**: The RoCEv2 PFC deadlock telemetry and AI factory metric streams are deterministic synthetic fixtures modeled directly on official **NVIDIA DCGM and NIM Prometheus schemas**.
- **Contract**: Network switch configuration commands and physical cloud cluster APIs are integration contracts until executed against authorized hardware environments.

---

## Official Technical Basis

- [NVIDIA NIM Logging & Per-Request Observability](https://docs.nvidia.com/nim/large-language-models/latest/nim-per-request-metrics.html)
- [NVIDIA NIM Latency & Throughput Benchmarking Guide](https://docs.nvidia.com/nim/benchmarking/llm/latest/index.html)
- [NVIDIA Base Command Manager Documentation](https://docs.nvidia.com/base-command-manager/)
- [NVIDIA AI Enterprise Reference Architecture](https://docs.nvidia.com/enterprise-reference-architectures/observability-guide/latest/abstract.html)
- [NIST SP 800-53 Rev. 5 Security Controls](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [NIST OSCAL (Open Security Controls Assessment Language)](https://pages.nist.gov/OSCAL/)

---

## Commercial Engagements & Assessments

For enterprise AI factory capacity reviews, RoCEv2 fabric optimization retainers, and autonomous agent invariant audits:

[Request an AI Factory Architecture & GPU-Capacity Review at A2Z SOC](https://a2zsoc.com/contact?topic=nvidia-ai-factory-reliability&utm_source=github&utm_medium=repository).
