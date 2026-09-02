ACTION_LIBRARY = {
    "fabric-degradation": ("drain-affected-path-and-run-fabric-validation", 8000, 350, .91),
    "fabric-congestion": ("validate-roce-pfc-ecn-or-infiniband-qos", 5000, 250, .82),
    "inference-queue-saturation": ("benchmark-and-adjust-replicas-batching-or-routing", 7000, 500, .86),
    "kv-cache-pressure": ("evaluate-context-bounds-cache-policy-or-model-profile", 4500, 300, .79),
    "nim-replica-unavailable": ("replace-unready-replica-after-readiness-diagnostics", 6000, 180, .94),
    "stranded-gpu-capacity": ("repack-workloads-or-repartition-mig-after-simulation", 4000, 200, .76),
}


def rank_actions(findings: list[dict]) -> list[dict]:
    actions = []
    for finding in findings:
        action, value, cost, success = ACTION_LIBRARY[finding["cause"]]
        expected_value = success * value - cost
        actions.append({
            "cause": finding["cause"],
            "action": action,
            "success_probability": success,
            "estimated_value_usd": value,
            "estimated_execution_cost_usd": cost,
            "expected_net_value_usd": round(expected_value, 2),
            "requires": ["independent-evaluation", "human-approval", "canary", "verification", "rollback"],
            "evidence_tier": "reference-assumption",
        })
    return sorted(actions, key=lambda item: (-item["expected_net_value_usd"], item["action"]))
