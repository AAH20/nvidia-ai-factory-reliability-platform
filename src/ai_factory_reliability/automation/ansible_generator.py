"""Ansible Network Automation Playbook Synthesis for RoCEv2 & Switch Fabrics."""

from dataclasses import dataclass


@dataclass
class NetworkPlaybook:
    target_hosts: str
    playbook_yaml: str
    rollback_yaml: str
    qos_profile: str


class AnsibleNetworkSynthesizer:
    """Generates deterministic Ansible playbooks for NVIDIA Cumulus / SONiC RoCEv2 fabrics."""

    def generate_roce_qos_playbook(
        self,
        switch_group: str = "leaf_switches",
        pfc_cos_priority: int = 3,
        ecn_min_threshold_kb: int = 150,
        ecn_max_threshold_kb: int = 1500,
        mtu: int = 9000,
    ) -> NetworkPlaybook:
        playbook = f"""---
- name: Autonomous RoCEv2 QoS & PFC Tuning
  hosts: {switch_group}
  become: yes
  tasks:
    - name: Configure MTU 9000 Jumbo Frames for RoCEv2
      ansible.builtin.lineinfile:
        path: /etc/network/interfaces
        regexp: '^mtu '
        line: 'mtu {mtu}'
      notify: Reload Networking

    - name: Tune RoCEv2 Priority Flow Control (PFC) Lossless Queue
      ansible.builtin.copy:
        dest: /etc/cumulus/datapath/traffic.conf
        content: |
          # Aegis Factory Control Plane QoS Profile
          pfc.pfc_enable = true
          pfc.lossless_priorities = {pfc_cos_priority}
          ecn.wred_enable = true
          ecn.min_threshold_bytes = {ecn_min_threshold_kb * 1024}
          ecn.max_threshold_bytes = {ecn_max_threshold_kb * 1024}
          ecn.drop_probability = 10
      notify: Restart Switch Daemon

  handlers:
    - name: Reload Networking
      ansible.builtin.command: ifreload -a
    - name: Restart Switch Daemon
      ansible.builtin.service:
        name: switchd
        state: restarted
"""
        rollback = f"""---
- name: Rollback RoCEv2 QoS Settings
  hosts: {switch_group}
  become: yes
  tasks:
    - name: Revert to Default Factory QoS Profile
      ansible.builtin.copy:
        src: /etc/cumulus/datapath/traffic.conf.bak
        dest: /etc/cumulus/datapath/traffic.conf
        remote_src: yes
      notify: Restart Switch Daemon
"""
        return NetworkPlaybook(
            target_hosts=switch_group,
            playbook_yaml=playbook.strip(),
            rollback_yaml=rollback.strip(),
            qos_profile="RoCEv2-Lossless-PFC3",
        )
