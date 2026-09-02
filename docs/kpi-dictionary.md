# KPI dictionary

## Capacity

| KPI | Formula |
|---|---|
| GPU allocation | allocated GPUs / GPUs available |
| Active GPU fraction | measured active compute time / observation time |
| Stranded capacity cost | stranded GPU-hours × GPU-hour price |
| Useful tokens per GPU-hour | successful input + output tokens / allocated GPU-hours |
| AI Factory Yield | SLO-compliant billable output / purchased GPU-hours |

## Inference

- Request success rate
- Requests and tokens per second
- Time to first token (TTFT)
- Inter-token latency (ITL)
- End-to-end latency
- Queue depth and queue time
- KV-cache utilization
- NIM readiness rate
- Model-cache hit rate
- Cost per successful request

## Fabric and storage

- Link availability and utilization
- Packet loss and retransmission
- InfiniBand/RoCE congestion events
- RDMA throughput
- NCCL collective bandwidth
- East-west latency
- Model and checkpoint throughput
- Network-attributed job failures

## Reliability and agents

- Availability and SLO attainment
- Change failure and incident recurrence rates
- MTTR and reduction against a comparable baseline
- Rollback success
- Evaluation and policy pass rates
- Context precision and dependency coverage
- Unauthorized actions
- Human intervention and override rates
- Remediation success and regression escape rates

## Economics

- Purchased and stranded GPU cost
- GPU cost per million successful tokens
- Revenue per GPU-hour
- Cost per verified remediation
- Verified revenue and labor value
- Verified net value and ROI

Identified, forecast, approved and realized values must remain separate. The synthetic case is not a customer result.
