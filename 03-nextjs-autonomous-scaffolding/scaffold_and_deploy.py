"""
Video 3: System Zero Autonomous Full Stack (Never Manually Scaffold Next.js Again)
Part 3 of 20: Autonomous Developer Workflows Series
Published on YouTube: Oct 17, 2026 (https://youtu.be/guFYzxngsXE)
Author: Autonomous Developer Workflows (System Zero)

Autonomous Scaffolding & Local Project Generator for Next.js 14 + Tailwind CSS.
Eliminates 30 minutes of repetitive manual configuration and optionally hooks into Vercel.
"""

import os
import sys
import io
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import json
import subprocess
import argparse
from pathlib import Path

def scaffold_nextjs_project(target_dir: str, project_name: str):
    """Generates a clean Next.js 14 + Tailwind CSS project structure."""
    print(f"\n🚀 [SCAFFOLD] Creating autonomous Next.js 14 boilerplate at '{target_dir}'...")
    root = Path(target_dir)
    root.mkdir(parents=True, exist_ok=True)
    
    # 1. package.json
    package_json = {
        "name": project_name,
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "^14.2.0",
            "react": "^18.3.0",
            "react-dom": "^18.3.0",
            "lucide-react": "^0.378.0"
        },
        "devDependencies": {
            "typescript": "^5.4.0",
            "@types/node": "^20.0.0",
            "@types/react": "^18.3.0",
            "@types/react-dom": "^18.3.0",
            "postcss": "^8.4.0",
            "tailwindcss": "^3.4.0"
        }
    }
    with open(root / "package.json", "w", encoding="utf-8") as f:
        json.dump(package_json, f, indent=2)

    # 2. Tailwind & PostCSS configs
    tailwind_cfg = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: { extend: {} },
  plugins: [],
};
"""
    with open(root / "tailwind.config.js", "w", encoding="utf-8") as f:
        f.write(tailwind_cfg)

    postcss_cfg = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
"""
    with open(root / "postcss.config.js", "w", encoding="utf-8") as f:
        f.write(postcss_cfg)

    # 3. Next.js 14 App Router layout & page
    app_dir = root / "app"
    app_dir.mkdir(exist_ok=True)

    layout_tsx = """import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Autonomous Next.js 14 App',
  description: 'Built with System Zero autonomous local scaffolding',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100 min-h-screen">{children}</body>
    </html>
  );
}
"""
    with open(app_dir / "layout.tsx", "w", encoding="utf-8") as f:
        f.write(layout_tsx)

    globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;
"""
    with open(app_dir / "globals.css", "w", encoding="utf-8") as f:
        f.write(globals_css)

    page_tsx = f"""export default function Home() {{
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="max-w-xl text-center space-y-4">
        <div className="inline-block px-3 py-1 bg-cyan-950 text-cyan-400 rounded-full text-xs font-mono uppercase tracking-wider">
          Part 3: Autonomous Full Stack Scaffolding
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl text-white">
          {project_name}
        </h1>
        <p className="text-slate-400">
          Generated automatically without manual boilerplate. Next.js 14 + Tailwind CSS + App Router ready for instant development.
        </p>
      </div>
    </main>
  );
}}
"""
    with open(app_dir / "page.tsx", "w", encoding="utf-8") as f:
        f.write(page_tsx)

    print(f"✅ [COMPLETED] Next.js 14 project scaffolded successfully in '{target_dir}'.")

def deploy_to_vercel(project_dir: str):
    """Triggers optional autonomous cloud deployment to Vercel via Vercel CLI."""
    print(f"\n🌐 [DEPLOY] Connecting to Vercel deployment pipeline (vercel.com)...")
    try:
        res = subprocess.run(["vercel", "--version"], capture_output=True, text=True)
        if res.returncode == 0:
            print("  --> Vercel CLI detected. Initiating autonomous preview deployment...")
            subprocess.run(["vercel", "--yes"], cwd=project_dir)
        else:
            print("  ⚠️ Vercel CLI not authenticated locally. Connect via 'vercel login' or git push to deploy.")
    except FileNotFoundError:
        print("  ℹ️ Vercel CLI not found in PATH. Install with: npm i -g vercel")
        print("  ℹ️ Link your GitHub repository directly to vercel.com for 1-click CI/CD deployment!")

def main():
    parser = argparse.ArgumentParser(description="Autonomous Next.js 14 Scaffolder - System Zero")
    parser.add_argument("--name", default="autonomous-nextjs-app", help="Name of the project")
    parser.add_argument("--out", default="./generated-app", help="Output directory")
    parser.add_argument("--deploy", action="store_true", help="Automatically trigger Vercel deployment")
    args = parser.parse_args()

    print("=" * 65)
    print(" 🚀 Autonomous Next.js 14 + Tailwind Scaffolder")
    print("    Part 3: System Zero Autonomous Full Stack")
    print("=" * 65)

    scaffold_nextjs_project(args.out, args.name)

    if args.deploy:
        deploy_to_vercel(args.out)

if __name__ == "__main__":
    main()
