from .models import WorkloadSLO


def diagnose(kpis: dict, topology: dict, slo: WorkloadSLO) -> list[dict]:
    findings = []
    if topology["unhealthy_links"] or topology["lossy_links"]:
        findings.append({"cause": "fabric-degradation", "confidence": .96, "evidence": ["unhealthy_links", "lossy_links"]})
    if topology["congested_links"]:
        findings.append({"cause": "fabric-congestion", "confidence": .9, "evidence": ["congested_links"]})
    inference = kpis["inference"]
    if inference["p95_ttft_ms"] > slo.p95_ttft_ms and inference["queue_depth"] > 0:
        findings.append({"cause": "inference-queue-saturation", "confidence": .88, "evidence": ["p95_ttft_ms", "queue_depth"]})
    if inference["kv_cache_fraction"] >= .9:
        findings.append({"cause": "kv-cache-pressure", "confidence": .85, "evidence": ["kv_cache_fraction"]})
    if inference["nim_readiness_rate"] < 1:
        findings.append({"cause": "nim-replica-unavailable", "confidence": .98, "evidence": ["nim_readiness_rate"]})
    if kpis["capacity"]["stranded_gpu_hours"] > 0:
        findings.append({"cause": "stranded-gpu-capacity", "confidence": 1.0, "evidence": ["stranded_gpu_hours"]})
    return sorted(findings, key=lambda finding: (-finding["confidence"], finding["cause"]))
