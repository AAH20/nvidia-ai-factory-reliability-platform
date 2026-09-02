# Hardware-free validation path

The initial architecture can be evaluated without an NVIDIA GPU:

1. Replay synthetic NIM, DCGM, Kubernetes and fabric telemetry.
2. Run a mock OpenAI-compatible inference service.
3. Model Kubernetes with kind or k3d.
4. Model Ethernet/RoCE topologies with containerlab.
5. Validate network intent with Batfish.
6. test Terraform/OpenTofu plans and Ansible check-mode output.
7. Inject node, link, replica, cache and traffic failures.
8. Verify diagnosis, proposed actions, gates, KPIs and evidence receipts.

Later validation should use a time-bounded rented GPU environment to measure real NIM metrics. Results must record hardware, model, precision, input/output length distributions, concurrency, batching, software versions and cost.
