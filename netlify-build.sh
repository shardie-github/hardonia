#!/usr/bin/env bash
set -euo pipefail

echo "===== Netlify Build: Start ====="

# Show toolchain
echo "Node: $(node -v || true)"
echo "NPM:  $(npm -v || true)"
echo "Python: $(python --version 2>/dev/null || true)"
echo "Pip: $(python -m pip --version 2>/dev/null || true)"

# --- Python setup ---
if [ -f "requirements.txt" ]; then
  echo ">> Python: creating venv .venv"
  python -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip setuptools wheel

  if [ -f "constraints.txt" ]; then
    echo ">> Python: installing requirements with constraints"
    python -m pip install --only-binary=:all: -r requirements.txt -c constraints.txt
  else
    echo ">> Python: installing requirements (no constraints.txt present)"
    python -m pip install --only-binary=:all: -r requirements.txt
  fi

  # Optional: Playwright for Python (browsers download)
  if [ "${USE_PY_PLAYWRIGHT:-0}" = "1" ]; then
    echo ">> Python: installing Playwright browsers"
    python -m playwright install
  fi
else
  echo ">> Python: no requirements.txt found, skipping Python deps"
fi

# If you have a Python pre-step (e.g., building data), run it here:
if [ -f "main.py" ]; then
  echo ">> Python: running main.py prebuild task"
  python main.py
fi

# --- Node setup ---
if [ -f "package.json" ]; then
  echo ">> Node: installing dependencies"
  if [ -f "package-lock.json" ]; then
    npm ci
  else
    npm i
  fi

  # Optional: Playwright for Node (browsers download)
  if [ "${USE_NODE_PLAYWRIGHT:-0}" = "1" ]; then
    echo ">> Node: installing Playwright browsers (chromium only)"
    npx playwright install chromium
  fi

  # Run your JS build if present
  if npm run | grep -qE ' build'; then
    echo ">> Node: running npm run build"
    npm run build
  else
    echo ">> Node: no build script found, skipping"
  fi
else
  echo ">> Node: no package.json found, skipping"
fi

# Ensure publish dir exists
mkdir -p public

echo "===== Netlify Build: Done ====="
