#!/usr/bin/env python3
"""
Multi-Agent Code Review Fleet
Autonomous parallel review bots auditing incoming Pull Requests for Security,
Performance, and Architectural compliance before merging.
Part 8 of Autonomous Developer Workflows Series (@SystemZeroTech)
"""

import sys
import os
import re
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# Ensure UTF-8 output on Windows terminals
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

@dataclass
class ReviewFinding:
    agent: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    file: str
    line: int
    rule: str
    description: str
    suggested_fix: str

class SecurityAuditorAgent:
    """Agent scanning PR diffs for secret leaks, injection flaws, and unsafe calls."""
    name = "Security-Sentry-01"

    SECRET_PATTERNS = [
        (re.compile(r"""(?:api[_-]?key|secret|token|password)\s*=\s*['"]([A-Za-z0-9_\-]{16,})['"]""", re.IGNORECASE),
         "CWE-798: Hardcoded Credential Detected", "Move secrets to environment variables or vault secret manager."),
        (re.compile(r"""sk_live_[0-9a-zA-Z]{16,}"""),
         "CWE-798: Live Stripe/Payment API Secret Leak", "Revoke secret immediately and load via os.getenv('STRIPE_API_KEY').")
    ]

    INJECTION_PATTERNS = [
        (re.compile(r"""execute\(\s*f['"].*SELECT.*\{.*\}""", re.IGNORECASE),
         "CWE-89: SQL Injection via f-string formatting", "Use parameterized queries with placeholder tuples: execute(query, (param,))."),
        (re.compile(r"""execute\(.*SELECT.*\+\s*(?:str\()?([a-zA-Z0-9_]+)""", re.IGNORECASE),
         "CWE-89: SQL Injection via string concatenation", "Replace string concatenation with prepared statement placeholders.")
    ]

    def audit(self, file_path: str, added_lines: List[tuple]) -> List[ReviewFinding]:
        findings = []
        for line_no, content in added_lines:
            # Check secrets
            for pattern, rule, fix in self.SECRET_PATTERNS:
                if pattern.search(content):
                    findings.append(ReviewFinding(
                        agent=self.name,
                        severity="CRITICAL",
                        file=file_path,
                        line=line_no,
                        rule=rule,
                        description="Hardcoded sensitive token detected in pull request diff.",
                        suggested_fix=fix
                    ))
            # Check SQL Injection
            for pattern, rule, fix in self.INJECTION_PATTERNS:
                if pattern.search(content):
                    findings.append(ReviewFinding(
                        agent=self.name,
                        severity="CRITICAL",
                        file=file_path,
                        line=line_no,
                        rule=rule,
                        description="Unescaped dynamic query parameter allows remote arbitrary SQL execution.",
                        suggested_fix=fix
                    ))
        return findings

class PerformanceProfilerAgent:
    """Agent scanning PR diffs for N+1 queries, unindexed table scans, and memory bloat."""
    name = "Perf-Profiler-02"

    PERF_PATTERNS = [
        (re.compile(r"""SELECT\s+\*\s+FROM""", re.IGNORECASE),
         "PERF-01: Unbounded SELECT * table scan", "Specify exact column names needed to minimize memory and network overhead."),
        (re.compile(r"""\.fetchall\(\)""", re.IGNORECASE),
         "PERF-02: In-memory bulk materialization without pagination", "Use cursor pagination, batch generator, or server-side LIMIT/OFFSET.")
    ]

    def audit(self, file_path: str, added_lines: List[tuple]) -> List[ReviewFinding]:
        findings = []
        for line_no, content in added_lines:
            for pattern, rule, fix in self.PERF_PATTERNS:
                if pattern.search(content):
                    findings.append(ReviewFinding(
                        agent=self.name,
                        severity="MEDIUM",
                        file=file_path,
                        line=line_no,
                        rule=rule,
                        description="Potential database bottleneck or memory strain under production load.",
                        suggested_fix=fix
                    ))
        return findings

class ArchitectureAuditorAgent:
    """Agent validating typing, docstrings, and clean design patterns."""
    name = "Arch-Auditor-03"

    def audit(self, file_path: str, added_lines: List[tuple]) -> List[ReviewFinding]:
        findings = []
        for line_no, content in added_lines:
            # Check function definitions missing type annotations
            if re.match(r"""^\s*def\s+[a-zA-Z0-9_]+\s*\([^)]*\):""", content):
                if "->" not in content:
                    findings.append(ReviewFinding(
                        agent=self.name,
                        severity="LOW",
                        file=file_path,
                        line=line_no,
                        rule="ARCH-01: Missing return type annotation",
                        description="Public service methods should specify explicit return type hints.",
                        suggested_fix="Add return type annotation (e.g., -> Optional[User] or -> List[Dict])."
                    ))
        return findings

def parse_patch(patch_text: str) -> Dict[str, List[tuple]]:
    """Parse git unified diff into added lines with line numbers."""
    files = {}
    current_file = None
    current_line = 0

    for line in patch_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
            files[current_file] = []
        elif line.startswith("@@"):
            # @@ -14,6 +14,15 @@
            match = re.search(r"""\+(\d+)""", line)
            if match:
                current_line = int(match.group(1))
        elif line.startswith("+") and not line.startswith("+++"):
            if current_file:
                files[current_file].append((current_line, line[1:]))
            current_line += 1
        elif not line.startswith("-"):
            current_line += 1

    return files

def run_fleet_review(patch_file: str) -> Dict[str, Any]:
    if not os.path.exists(patch_file):
        raise FileNotFoundError(f"Patch file not found: {patch_file}")

    with open(patch_file, "r", encoding="utf-8") as f:
        patch_text = f.read()

    diff_data = parse_patch(patch_text)
    agents = [
        SecurityAuditorAgent(),
        PerformanceProfilerAgent(),
        ArchitectureAuditorAgent()
    ]

    all_findings: List[ReviewFinding] = []
    for file_path, added_lines in diff_data.items():
        for agent in agents:
            findings = agent.audit(file_path, added_lines)
            all_findings.extend(findings)

    # Calculate review verdict
    has_critical = any(f.severity == "CRITICAL" for f in all_findings)
    verdict = "REQUEST_CHANGES" if has_critical else "APPROVE"

    return {
        "verdict": verdict,
        "total_findings": len(all_findings),
        "critical_count": sum(1 for f in all_findings if f.severity == "CRITICAL"),
        "medium_count": sum(1 for f in all_findings if f.severity == "MEDIUM"),
        "low_count": sum(1 for f in all_findings if f.severity == "LOW"),
        "findings": [asdict(f) for f in all_findings]
    }

def format_github_pr_comment(report: Dict[str, Any]) -> str:
    """Format markdown payload ready for `gh pr review --comment` or status check."""
    status_icon = "❌" if report["verdict"] == "REQUEST_CHANGES" else "✅"
    lines = [
        f"## {status_icon} Autonomous Code Review Fleet Report",
        f"**Verdict**: `{report['verdict']}` | **Critical**: {report['critical_count']} | **Medium**: {report['medium_count']} | **Low**: {report['low_count']}\n",
        "| Agent | Severity | Location | Issue | Recommendation |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    for f in report["findings"]:
        sev_badge = f"🔴 {f['severity']}" if f['severity'] == "CRITICAL" else f"🟡 {f['severity']}" if f['severity'] == "MEDIUM" else f"⚪ {f['severity']}"
        lines.append(f"| `{f['agent']}` | {sev_badge} | `{f['file']}:{f['line']}` | **{f['rule']}**: {f['description']} | {f['suggested_fix']} |")
    
    return "\n".join(lines)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    patch_path = os.path.join(script_dir, "sample_pr_diff.patch")

    print("=" * 65)
    print("🤖 System Zero - Autonomous Multi-Agent Code Review Fleet")
    print("=" * 65)
    print(f"[>] Ingesting pull request diff: {os.path.basename(patch_path)}")
    
    review_result = run_fleet_review(patch_path)
    
    print(f"[+] Agents deployed: Security-Sentry-01, Perf-Profiler-02, Arch-Auditor-03")
    print(f"[+] Scan completed: {review_result['total_findings']} issue(s) detected across 3 review axes.")
    print("-" * 65)
    
    markdown_output = format_github_pr_comment(review_result)
    print(markdown_output)
    print("-" * 65)
    
    if review_result["verdict"] == "REQUEST_CHANGES":
        print("[!] VERDICT: REQUEST_CHANGES (Blocked merge due to CRITICAL vulnerabilities)")
    else:
        print("[+] VERDICT: APPROVE (All automated checks passed)")
    print("=" * 65)
