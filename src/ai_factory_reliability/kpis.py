from .models import FactorySnapshot, WorkloadSLO


def _rate(numerator: float, denominator: float) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def calculate(snapshot: FactorySnapshot, slo: WorkloadSLO) -> dict:
    total_requests = snapshot.successful_requests + snapshot.failed_requests
    tokens = snapshot.input_tokens + snapshot.output_tokens
    gpu_cost = snapshot.gpu_count * snapshot.gpu_hour_cost_usd
    stranded_cost = snapshot.stranded_gpu_hours * snapshot.gpu_hour_cost_usd
    request_cost = _rate(snapshot.operating_cost_usd, snapshot.successful_requests)
    revenue = snapshot.successful_requests * slo.revenue_per_request_usd if snapshot.verified else 0.0
    labor_value = snapshot.engineering_hours_saved * snapshot.hourly_cost_usd if snapshot.verified else 0.0
    verified_value = revenue + labor_value
    return {
        "capacity": {
            "gpu_allocation_rate": _rate(snapshot.allocated_gpus, snapshot.gpu_count),
            "active_gpu_fraction": snapshot.active_gpu_fraction,
            "gpu_memory_fraction": snapshot.gpu_memory_fraction,
            "stranded_gpu_hours": snapshot.stranded_gpu_hours,
            "stranded_capacity_cost_usd": round(stranded_cost, 2),
            "useful_tokens_per_gpu_hour": round(tokens / max(snapshot.allocated_gpus, 1), 2),
        },
        "inference": {
            "request_success_rate": _rate(snapshot.successful_requests, total_requests),
            "measured_rps": snapshot.measured_rps,
            "rps_slo_attainment": _rate(snapshot.measured_rps, slo.requests_per_second),
            "p95_ttft_ms": snapshot.p95_ttft_ms,
            "p95_itl_ms": snapshot.p95_itl_ms,
            "queue_depth": snapshot.queue_depth,
            "kv_cache_fraction": snapshot.kv_cache_fraction,
            "nim_readiness_rate": _rate(snapshot.nim_ready_replicas, snapshot.nim_desired_replicas),
            "model_cache_hit_rate": _rate(snapshot.model_cache_hits, snapshot.model_cache_requests),
            "cost_per_request_usd": request_cost,
        },
        "reliability": {
            "availability": _rate(snapshot.successful_requests, total_requests),
            "change_failure_rate": _rate(snapshot.failed_changes, snapshot.changes),
            "incident_recurrence_rate": _rate(snapshot.repeated_incidents, snapshot.incidents),
            "mttr_minutes": snapshot.mttr_minutes,
            "mttr_reduction_rate": _rate(max(snapshot.baseline_mttr_minutes - snapshot.mttr_minutes, 0), snapshot.baseline_mttr_minutes),
            "rollback_success_rate": _rate(snapshot.successful_rollbacks, snapshot.rollback_attempts),
        },
        "agent": {
            "evaluation_pass_rate": _rate(snapshot.evaluation_passes, snapshot.evaluation_total),
            "policy_pass_rate": _rate(snapshot.policy_passes, snapshot.policy_total),
            "context_precision": _rate(snapshot.context_relevant_tokens, snapshot.context_total_tokens),
            "dependency_coverage": _rate(snapshot.dependencies_known, snapshot.dependencies_total),
            "unauthorized_actions": snapshot.unauthorized_actions,
        },
        "economics": {
            "gpu_capacity_cost_usd": round(gpu_cost, 2),
            "operating_cost_usd": round(snapshot.operating_cost_usd, 2),
            "verified_revenue_usd": round(revenue, 2),
            "verified_labor_value_usd": round(labor_value, 2),
            "verified_net_value_usd": round(verified_value - snapshot.operating_cost_usd, 2),
            "roi": round((verified_value - snapshot.operating_cost_usd) / snapshot.operating_cost_usd, 4) if snapshot.operating_cost_usd else None,
            "revenue_per_gpu_hour_usd": round(revenue / max(snapshot.allocated_gpus, 1), 2),
        },
    }
