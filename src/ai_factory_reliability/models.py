from dataclasses import dataclass, field


@dataclass(frozen=True)
class FabricLink:
    source: str
    target: str
    kind: str
    capacity_gbps: float
    utilization: float
    packet_loss_rate: float
    healthy: bool


@dataclass(frozen=True)
class WorkloadSLO:
    workload_id: str
    requests_per_second: float
    p95_ttft_ms: float
    p95_itl_ms: float
    availability: float
    max_cost_per_request_usd: float
    revenue_per_request_usd: float


@dataclass(frozen=True)
class FactorySnapshot:
    timestamp: str
    gpu_count: int
    allocated_gpus: int
    active_gpu_fraction: float
    gpu_memory_fraction: float
    stranded_gpu_hours: float
    gpu_hour_cost_usd: float
    successful_requests: int
    failed_requests: int
    input_tokens: int
    output_tokens: int
    measured_rps: float
    p95_ttft_ms: float
    p95_itl_ms: float
    queue_depth: int
    kv_cache_fraction: float
    nim_ready_replicas: int
    nim_desired_replicas: int
    model_cache_hits: int
    model_cache_requests: int
    incidents: int
    repeated_incidents: int
    mttr_minutes: float
    baseline_mttr_minutes: float
    changes: int
    failed_changes: int
    rollback_attempts: int
    successful_rollbacks: int
    unauthorized_actions: int
    evaluation_passes: int
    evaluation_total: int
    policy_passes: int
    policy_total: int
    context_relevant_tokens: int
    context_total_tokens: int
    dependencies_known: int
    dependencies_total: int
    operating_cost_usd: float
    engineering_hours_saved: float
    hourly_cost_usd: float
    verified: bool
    tags: tuple[str, ...] = field(default_factory=tuple)
