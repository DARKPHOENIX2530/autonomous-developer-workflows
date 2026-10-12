"""
Video 3: Stop Copy-Pasting Code in 2026
Part 3 of 20: Autonomous Developer Workflows Series
Agent Workflows: systemzero.dev
Author: Autonomous Developer Workflows (System Zero)

Autonomous Code Verification & Self-Healing Loop.
Automatically detects test failures, formulates patches, applies fixes directly
to the file on disk, and verifies until all tests pass — eliminating manual copy-pasting.
"""

import os
import sys
import io
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import subprocess
import time
import argparse
from typing import Tuple, Dict, Any

def run_test_suite(target_file: str) -> Tuple[bool, str]:
    """Runs the target test/script and captures stderr/stdout."""
    print(f"  🔍 [VERIFY] Running verification suite on '{target_file}'...")
    result = subprocess.run(
        [sys.executable, target_file],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        return True, result.stdout
    else:
        error_log = result.stderr if result.stderr else result.stdout
        return False, error_log

def autonomous_patch_generator(error_trace: str, code_content: str) -> str:
    """
    Simulates the autonomous agent repair loop (System Zero workflow).
    Parses the error trace and generates the precise replacement patch.
    """
    print("  🧠 [AGENT] Diagnosing traceback and generating targeted patch...")
    time.sleep(1.0) # Simulating agent reasoning loop
    
    # Auto-healing rule demonstration for sample bug:
    # Fixes ZeroDivisionError and TypeError in sample_broken_app.py
    patched_code = code_content
    if "ZeroDivisionError" in error_trace:
        print("  🛠️ [PATCH] Detected ZeroDivisionError -> injecting guard clause.")
        patched_code = patched_code.replace(
            "return total / count",
            "return total / count if count > 0 else 0.0"
        )
    if "TypeError" in error_trace:
        print("  🛠️ [PATCH] Detected TypeError -> type-casting input array.")
        patched_code = patched_code.replace(
            "total = sum(items)",
            "total = sum(float(x) for x in items)"
        )
    return patched_code

def self_healing_loop(target_file: str, max_attempts: int = 3):
    """Executes the autonomous loop: Test -> Detect -> Patch -> Re-test."""
    print("=" * 65)
    print(" 🚀 Autonomous Verification Loop (Stop Copy-Pasting in 2026)")
    print("    Agent Workflows: systemzero.dev")
    print("=" * 65)

    if not os.path.exists(target_file):
        print(f"❌ Error: Target file '{target_file}' not found.")
        return

    for attempt in range(1, max_attempts + 1):
        print(f"\n--- Iteration {attempt}/{max_attempts} ---")
        passed, log = run_test_suite(target_file)

        if passed:
            print(f"✅ [SUCCESS] All verification tests passed cleanly!")
            print("🎉 No copy-pasting required. The autonomous agent patched the file directly on disk.")
            return

        print(f"❌ [TEST FAILED] Error output captured:\n{'-'*40}\n{log.strip()}\n{'-'*40}")
        
        with open(target_file, "r", encoding="utf-8") as f:
            code = f.read()

        patched_code = autonomous_patch_generator(log, code)

        if patched_code == code:
            print("⚠️ [WARNING] Autonomous agent could not resolve this specific failure automatically.")
            break

        # Apply patch directly to file
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(patched_code)
        print(f"💾 [APPLIED] Patch successfully written directly to '{target_file}'.")

    print("\n❌ Verification loop reached maximum attempts without full resolution.")

def main():
    parser = argparse.ArgumentParser(description="Autonomous Verification Loop - System Zero")
    parser.add_argument("--target", default="sample_broken_app.py", help="Python file to verify and auto-patch")
    parser.add_argument("--max-retries", type=int, default=3, help="Maximum patch iterations")
    args = parser.parse_args()

    self_healing_loop(args.target, max_attempts=args.max_retries)

if __name__ == "__main__":
    main()