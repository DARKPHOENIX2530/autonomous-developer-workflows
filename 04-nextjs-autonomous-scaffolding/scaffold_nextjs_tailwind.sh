#!/usr/bin/env bash
# Autonomous Scaffolding Script for Next.js 14 + Tailwind CSS
# Part 4 of 20: Autonomous Developer Workflows Series
# Pipeline: vercel.com

set -e
PROJECT_NAME=${1:-"autonomous-nextjs-app"}

echo "🚀 Scaffolding Next.js 14 project: $PROJECT_NAME..."
npx create-next-app@latest "$PROJECT_NAME" --typescript --tailwind --eslint --app --no-src-dir --import-alias "@/*" --use-npm

cd "$PROJECT_NAME"
echo "🌐 Deploying to Vercel..."
if command -v vercel &> /dev/null; then
    vercel --yes
else
    echo "💡 Install vercel CLI (npm i -g vercel) or import repo at vercel.com"
fi