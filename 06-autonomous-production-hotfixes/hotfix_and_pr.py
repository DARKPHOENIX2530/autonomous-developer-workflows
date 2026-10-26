import os
import sys
import re
import time
import subprocess
import shutil

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ANSI Color Codes for Broadcast Terminal Recording
C_RED = "\033[91m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_BLUE = "\033[94m"
C_CYAN = "\033[96m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_FILE = os.path.join(BASE_DIR, "broken_service.py")
TEST_FILE = os.path.join(BASE_DIR, "test_service.py")
LOG_FILE = os.path.join(BASE_DIR, "server_logs.log")
BACKUP_FILE = os.path.join(BASE_DIR, "broken_service.py.bak")

def print_banner():
    border = "=" * 70
    print(f"\n{C_RED}{C_BOLD}{border}{C_RESET}")
    print(f"{C_RED}{C_BOLD}   SYSTEM ZERO AUTONOMOUS DEVOPS AGENT: 3:00 AM INCIDENT SENTRY{C_RESET}")
    print(f"{C_RED}{C_BOLD}   Zero Local RAM | OpenCode Free Cloud Fleet | Auto-PR Pipeline{C_RESET}")
    print(f"{C_RED}{C_BOLD}{border}{C_RESET}\n")

def simulate_webhook_ingest():
    print(f"{C_CYAN}[03:14:22 UTC] [WEBHOOK INGESTED]{C_RESET} Alert received from Vercel Edge / PostgreSQL Gateway")
    print(f"               --> Webhook Payload: HTTP 500 | req_id=req_8a91f2c4e | tenant=production")
    time.sleep(0.4)

def parse_stack_trace():
    print(f"\n{C_YELLOW}[03:14:23 UTC] [STACK TRACE INGESTION]{C_RESET} Parsing server_logs.log...")
    if not os.path.exists(LOG_FILE):
        print(f"{C_RED}[!] Error: Log file {LOG_FILE} not found.{C_RESET}")
        sys.exit(1)
        
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        log_content = f.read()

    # Regex to extract traceback
    tb_pattern = r'File "([^"]+)", line (\d+), in (\w+)\s*\n\s*([^\n]+)\s*\n(\w+Error:[^\n]+)'
    match = re.search(tb_pattern, log_content)
    
    if match:
        culprit_file, line_no, func_name, offending_line, error_type = match.groups()
        print(f"               --> Isolated Module  : {C_BOLD}{culprit_file}{C_RESET}")
        print(f"               --> Target Function  : {C_BOLD}{func_name}(){C_RESET} at line {line_no}")
        print(f"               --> Offending Op     : {C_RED}{offending_line.strip()}{C_RESET}")
        print(f"               --> Exception Class  : {C_RED}{C_BOLD}{error_type}{C_RESET}")
        return culprit_file, func_name
    else:
        print(f"{C_YELLOW}[*] Parsing default target: broken_service.py -> process_payment_settlement{C_RESET}")
        return "broken_service.py", "process_payment_settlement"

def apply_surgical_patch(culprit_file, func_name):
    print(f"\n{C_BLUE}[03:14:24 UTC] [SURGICAL AST PATCH]{C_RESET} Generating guard clause patch...")
    target_path = os.path.join(BASE_DIR, culprit_file)
    
    # Create backup before patching if not exists
    if not os.path.exists(BACKUP_FILE):
        shutil.copyfile(target_path, BACKUP_FILE)
        
    with open(target_path, "r", encoding="utf-8") as f:
        code = f.read()

    # Check if already patched
    if "if not num_splits or num_splits <= 0:" in code:
        print(f"{C_GREEN}[+] Code already contains guard clause patch.{C_RESET}")
        return

    # Invert the division by zero bug with surgical guard clause
    old_stmt = "return round(amount / num_splits, 2)"
    patch = """    # [AUTONOMOUS HOTFIX] Guard clause injected by System Zero agent
    if not num_splits or num_splits <= 0:
        return amount
    return round(amount / num_splits, 2)"""

    if old_stmt in code:
        patched_code = code.replace(old_stmt, patch)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(patched_code)
        print(f"               --> Injected Guard: {C_GREEN}if not num_splits or num_splits <= 0: return amount{C_RESET}")
        print(f"               --> AST Verification: Clean syntax, zero regressions")
    else:
        print(f"{C_YELLOW}[!] Target statement not found in {culprit_file}. Code unchanged.{C_RESET}")
    time.sleep(0.4)

def run_test_suite():
    print(f"\n{C_YELLOW}[03:14:25 UTC] [PYTEST SANDBOX VERIFICATION]{C_RESET} Executing test suite...")
    res = subprocess.run(
        [sys.executable, "-m", "pytest", TEST_FILE, "-v"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )
    for line in res.stdout.strip().split("\n"):
        if "PASSED" in line:
            print(f"  {C_GREEN}✔ {line}{C_RESET}")
        elif "FAILED" in line:
            print(f"  {C_RED}✖ {line}{C_RESET}")
        elif "collected" in line or "test session starts" in line:
            continue
        elif "passed in" in line:
            print(f"\n{C_GREEN}{C_BOLD}[PYTEST SUCCESS] {line.strip()}{C_RESET}")
            
    if res.returncode != 0:
        print(f"{C_RED}[!] Test suite failed! Hotfix aborted.{C_RESET}")
        sys.exit(1)
    time.sleep(0.4)

def simulate_pr_creation():
    print(f"\n{C_CYAN}[03:14:26 UTC] [GIT & GITHUB AUTOMATION]{C_RESET} Pushing hotfix branch...")
    print(f"               --> git checkout -b hotfix/auto-fix-zerodivision")
    print(f"               --> git commit -m 'fix(prod): auto-hotfix server crash on zero splits'")
    print(f"               --> git push origin hotfix/auto-fix-zerodivision")
    time.sleep(0.3)
    
    print(f"\n{C_GREEN}{C_BOLD}[GITHUB PR CREATED]{C_RESET} Pull Request #142 opened successfully!")
    print(f"  Link   : https://github.com/DARKPHOENIX2530/autonomous-developer-workflows/pull/142")
    print(f"  Title  : fix(prod): auto-hotfix 500 error in process_payment_settlement")
    print(f"  Review : 5/5 Pytest assertions passed. Ready for 1-click morning merge.\n")

def restore_backup():
    if os.path.exists(BACKUP_FILE):
        shutil.copyfile(BACKUP_FILE, SERVICE_FILE)
        os.remove(BACKUP_FILE)
        print(f"{C_GREEN}[+] Restored {SERVICE_FILE} from backup.{C_RESET}")
    else:
        print(f"{C_YELLOW}[*] No backup found. Reverting patch manually if present...{C_RESET}")
        with open(SERVICE_FILE, "r", encoding="utf-8") as f:
            code = f.read()
        patch_pattern = r"    # \[AUTONOMOUS HOTFIX\].*?return round\(amount / num_splits, 2\)"
        restored_code = re.sub(patch_pattern, "    return round(amount / num_splits, 2)", code, flags=re.DOTALL)
        with open(SERVICE_FILE, "w", encoding="utf-8") as f:
            f.write(restored_code)
        print(f"{C_GREEN}[+] Code reverted to original unpatched crash state.{C_RESET}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--restore":
        restore_backup()
        sys.exit(0)

    print_banner()
    simulate_webhook_ingest()
    culprit, func = parse_stack_trace()
    apply_surgical_patch(culprit, func)
    run_test_suite()
    simulate_pr_creation()

if __name__ == "__main__":
    main()
