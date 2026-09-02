"""Command Line Interface for NVIDIA AI Factory Reliability & Capacity Control Plane."""

import argparse
import json
import sys
from pathlib import Path

from .engine import analyze
from .io import load_case
from .self_heal import run_self_healing_pipeline
from .automation.compliance_gate import ComplianceGate, OSCALExporter, PolicyEvaluationResult


def main() -> None:
    parser = argparse.ArgumentParser(
        description="NVIDIA AI Factory Reliability & Capacity Control Plane (Aegis-Factory)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # 1. analyze subcommand
    analyze_parser = subparsers.add_parser("analyze", help="Analyze synthetic/measured telemetry snapshot")
    analyze_parser.add_argument("case", help="Path to JSON snapshot case")
    analyze_parser.add_argument("--output", help="Optional output JSON file")

    # 2. self-heal subcommand
    heal_parser = subparsers.add_parser("self-heal", help="Run autonomous self-healing & compliance pipeline")
    heal_parser.add_argument("incident", help="Path to incident fixture JSON")
    heal_parser.add_argument("--output", help="Optional output JSON file")

    # 3. export-oscal subcommand
    oscal_parser = subparsers.add_parser("export-oscal", help="Export NIST OSCAL System Security Plan")
    oscal_parser.add_argument("--system-id", default="sovereign-ai-cluster-01", help="System Identifier")
    oscal_parser.add_argument("--output", help="Optional output JSON file")

    # Support backward compatibility: if first arg is a JSON file, default to analyze
    raw_args = sys.argv[1:]
    if raw_args and not raw_args[0].startswith("-") and raw_args[0] not in ("analyze", "self-heal", "export-oscal"):
        raw_args = ["analyze"] + raw_args

    args = parser.parse_args(raw_args)

    if args.command == "analyze":
        result = analyze(*load_case(json.loads(Path(args.case).read_text())))
        rendered = json.dumps(result, indent=2, sort_keys=True)
        if args.output:
            Path(args.output).write_text(rendered + "\n")
        else:
            print(rendered)

    elif args.command == "self-heal":
        incident_data = json.loads(Path(args.incident).read_text())
        result = run_self_healing_pipeline(incident_data)
        rendered = json.dumps(result, indent=2, sort_keys=True)
        if args.output:
            Path(args.output).write_text(rendered + "\n")
        else:
            print(rendered)

    elif args.command == "export-oscal":
        exporter = OSCALExporter()
        mock_eval = PolicyEvaluationResult(
            passed=True,
            evaluated_controls=["NIST-800-53-AC-4", "NIST-800-53-SC-7", "NIST-800-53-SC-8", "EU-AI-ACT-ART-15"],
            violations=[],
        )
        oscal_data = exporter.export_ssp(system_id=args.system_id, compliance_result=mock_eval, topology_state={})
        rendered = json.dumps(oscal_data, indent=2, sort_keys=True)
        if args.output:
            Path(args.output).write_text(rendered + "\n")
        else:
            print(rendered)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
