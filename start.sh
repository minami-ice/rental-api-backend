#!/bin/bash
set -e

# 加载环境变量（宝塔/Ubuntu 常用）
set -a
source /www/wwwroot/rental-api/.env
set +a

cd /www/wwwroot/rental-api || exit 1

# 自动识别虚拟环境目录（venv 或 .venv）
PY=""
if [ -x "/www/wwwroot/rental-api/.venv/bin/python" ]; then
  PY="/www/wwwroot/rental-api/.venv/bin/python"
elif [ -x "/www/wwwroot/rental-api/venv/bin/python" ]; then
  PY="/www/wwwroot/rental-api/venv/bin/python"
fi

if [ -z "$PY" ]; then
  echo "找不到虚拟环境 python：请确认 /www/wwwroot/rental-api/venv 或 .venv 是否存在"
  exit 1
fi

exec "$PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
