#!/usr/bin/env bash
# Проверка: страница showcase не содержит контактов (правила Kwork).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILE="$ROOT/public/showcase/index.html"
FAIL=0

patterns=(
  't\.me/'
  'mailto:'
  'tel:'
  'TELEGRAM_USERNAME'
  'data-site-link="telegram"'
  'id="leadForm"'
  'Полное портфолио'
)

for p in "${patterns[@]}"; do
  if rg -q "$p" "$FILE"; then
    echo "FAIL: showcase содержит запрещённый паттерн: $p"
    FAIL=1
  fi
done

if [[ "$FAIL" -eq 0 ]]; then
  echo "OK: showcase проходит проверку контактов для Kwork"
fi
exit "$FAIL"
