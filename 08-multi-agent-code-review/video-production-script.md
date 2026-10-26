# 🎬 Short 08: Video Production Script
## "Stop Reviewing PRs Manually. Deploy Agent Fleets."

> **Series**: [Autonomous Developer Workflows](../../README.md) (Part 8 of 20)  
> **Channel**: [@SystemZeroTech](https://www.youtube.com/@SystemZeroTech)  
> **Format**: 9:16 Vertical Video (1080x1920, 30fps)  
> **Target Runtime**: `36.0 seconds`  
> **Aesthetic**: System Zero Dark Cyberpunk, Glass HUD, Animated Terminal & Diffs

---

## ⏱️ Scene & Beat Breakdown

```
================================================================================
TIME        BADGE & COLOR      VISUAL MOCKUP                  SPOKEN NARRATION
================================================================================
```

### 🔹 Beat 1: The Problem Hook (0.0s – 5.5s)
* **Badge**: `CRITICAL CODE REVIEW RISK` (Neon Red: `#FF5050`)
* **Title**: `TIRED REVIEWERS MISS\nLEAKED STRIPE SECRETS`
* **Visual Mockup**:
  * Red warning pulse in top corner.
  * Git unified diff displaying line 16 highlighted in red:
    ```diff
    + self.admin_api_key = "sk_live_9941a8e2b84c81"
    + query = f"SELECT * FROM users WHERE email='{email}'"
    ```
  * Subtitle in Safe Zone: *"A tired reviewer at 6 PM will easily miss an SQL injection."*
* **Voiceover**:
  *"Human code reviews miss things. A tired reviewer at 6 PM will easily skim past an SQL injection or a leaked live Stripe secret."*

---

### 🔹 Beat 2: The Autonomous Shift (5.5s – 11.5s)
* **Badge**: `SYSTEM ZERO // AGENT FLEET` (Neon Blue: `#2DB9FF`)
* **Title**: `DEPLOY 3 PARALLEL\nSPECIALIZED REVIEW BOTS`
* **Visual Mockup**:
  * 3 glowing agent badges appear in parallel:
    1. `[🛡️ Security-Sentry-01]`
    2. `[⚡ Perf-Profiler-02]`
    3. `[📐 Arch-Auditor-03]`
  * Subtitle in Safe Zone: *"Deploy autonomous review fleets to audit PRs in parallel."*
* **Voiceover**:
  *"Stop doing manual reviews. Deploy an autonomous review fleet where specialized agents audit code in parallel before merge."*

---

### 🔹 Beat 3: Live Agent Inspection (11.5s – 19.5s)
* **Badge**: `PARALLEL SENTRY IN ACTION` (Neon Green: `#50F078`)
* **Title**: `INSTANT DETECTION:\nCWE-798 & CWE-89`
* **Visual Mockup**:
  * Terminal running `$ python review_fleet.py` with typing cursor.
  * Rapid output lines popping up:
    * `[🔴 CRITICAL] CWE-798: Hardcoded Stripe API Secret`
    * `[🔴 CRITICAL] CWE-89: SQL Injection in user_service.py`
    * `[🟡 MEDIUM] PERF-01: Unbounded SELECT * table scan`
  * Subtitle in Safe Zone: *"Security Sentry flags hardcoded keys and raw SQL formatting."*
* **Voiceover**:
  *"Security Sentry intercepts hardcoded credentials and SQL injections, while Performance Profiler flags unbounded table scans."*

---

### 🔹 Beat 4: Automated GitHub Verdict (19.5s – 27.5s)
* **Badge**: `GITHUB ACTIONS VERDICT` (Neon Purple: `#F56ED2`)
* **Title**: `MERGE BLOCKED:\nAUTOMATED PR REVIEW POSTED`
* **Visual Mockup**:
  * GitHub Pull Request interface mockup:
    * Status: `❌ REQUEST_CHANGES (Blocked)`
    * Comment posted with markdown table: `3 Critical | 2 Medium | 0 Leaks Allowed`
  * Subtitle in Safe Zone: *"The fleet blocks the merge and posts line-by-line fixes."*
* **Voiceover**:
  *"The fleet blocks the pull request, outputs exact line-by-line fixes, and prevents broken code from ever reaching your main branch."*

---

### 🔹 Beat 5: Outro & Seamless Loop (27.5s – 36.0s)
* **Badge**: `SYSTEM ZERO` (Neon Gold: `#FFD71E`)
* **Title**: `CLONE THE REPO\nPART 8 OF 20 SERIES`
* **Visual Mockup**:
  * Glowing System Zero terminal card:
    * `github.com/DARKPHOENIX2530/autonomous-developer-workflows`
    * `SUBSCRIBE TO @SystemZeroTech`
  * Subtitle in Safe Zone: *"Clone the review fleet code on GitHub. And remember..."*
* **Voiceover**:
  *"Grab the complete review fleet script on our GitHub repo in the pinned comment. Subscribe to System Zero, because..."*
  *(Seamless loop flows directly into 0:00: "Human code reviews miss things...")*

```
================================================================================
END OF SCRIPT (Exact Duration: 36.0s)
================================================================================
```
