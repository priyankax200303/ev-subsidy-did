#!/usr/bin/env bash
set -euo pipefail
python3 scripts/build_panel.py
python3 scripts/build_notebooks.py 1 2 3
python3 scripts/reconcile.py
