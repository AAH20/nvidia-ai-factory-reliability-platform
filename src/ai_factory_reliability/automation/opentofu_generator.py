"""OpenTofu / Terraform HCL Synthesis for GPU Clusters and NVIDIA NIM Deployments."""

from dataclasses import dataclass
from typing import Any


@dataclass
class IaCPatch:
    target_file: str
    hcl_content: str
    rollback_hcl: str
    resource_type: str


class OpenTofuSynthesizer:
    """Generates deterministic OpenTofu HCL patches for GPU clusters and NIM workloads."""

    def generate_nim_scaling_patch(
        self,
        service_name: str,
        current_replicas: int,
        target_replicas: int,
        gpu_type: str = "nvidia.com/gpu",
        gpus_per_replica: int = 8,
    ) -> IaCPatch:
        hcl = f"""# Autonomous OpenTofu Patch: Scale {service_name}
resource "kubernetes_deployment" "{service_name}" {{
  metadata {{
    name      = "{service_name}"
    namespace = "ai-services"
    labels = {{
      "app.kubernetes.io/name"       = "{service_name}"
      "app.kubernetes.io/managed-by" = "aegis-factory-control-plane"
    }}
  }}

  spec {{
    replicas = {target_replicas}

    template {{
      spec {{
        container {{
          name  = "nim-worker"
          image = "nvcr.io/nim/{service_name}:latest"

          resources {{
            limits = {{
              "{gpu_type}" = "{gpus_per_replica}"
              "memory"          = "128Gi"
            }}
            requests = {{
              "{gpu_type}" = "{gpus_per_replica}"
              "memory"          = "64Gi"
            }}
          }}

          volume_mount {{
            name       = "dshm"
            mount_path = "/dev/shm"
          }}
        }}

        volume {{
          name = "dshm"
          empty_dir {{
            medium     = "Memory"
            size_limit = "64Gi"
          }}
        }}
      }}
    }}
  }}
}}
"""
        rollback = f"""# Automated Rollback HCL
resource "kubernetes_deployment" "{service_name}" {{
  spec {{
    replicas = {current_replicas}
  }}
}}
"""
        return IaCPatch(
            target_file=f"deployments/{service_name}.tf",
            hcl_content=hcl.strip(),
            rollback_hcl=rollback.strip(),
            resource_type="kubernetes_deployment",
        )
