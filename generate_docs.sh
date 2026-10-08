#!/usr/bin/env bash
set -euo pipefail

script_src=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
uv run --project "$script_src" --group docs sphinx-build -b html "${script_src}/docs_source" "${script_src}/docs"
