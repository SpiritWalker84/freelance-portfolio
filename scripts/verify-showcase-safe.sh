#!/usr/bin/env bash
# Проверка: showcase-страницы не содержат контактов (правила Kwork).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FILES=(
  "$ROOT/public/showcase/index.html"
  "$ROOT/public/showcase/mp/index.html"
)
FAIL=0

patterns=(
  't\.me/'
  'mailto:'
  'tel:'
  'TELEGRAM_USERNAME'
  'data-site-link="telegram"'
  'id="leadForm"'
  'Полное портфолио'
  'apply-site-config'
  'site-config\.js'
)

for FILE in "${FILES[@]}"; do
  if [[ ! -f "$FILE" ]]; then
    echo "FAIL: нет файла $FILE"
    FAIL=1
    continue
  fi
  for p in "${patterns[@]}"; do
    if rg -q "$p" "$FILE"; then
      echo "FAIL: $(basename "$(dirname "$FILE")")/$(basename "$FILE") — паттерн: $p"
      FAIL=1
    fi
  done
done

if [[ "$FAIL" -eq 0 ]]; then
  echo "OK: showcase и showcase/mp проходят проверку контактов для Kwork"
fi
exit "$FAIL"
