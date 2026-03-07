#!/usr/bin/env bash
set -euo pipefail
SOURCE_ROOT="${1:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESTINATION_ROOT="${2:-$(cd "$SCRIPT_DIR/.." && pwd)}"
LOG_DIR="$DESTINATION_ROOT/scripts/logs"
LOG_PATH="$LOG_DIR/organize_repo_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$LOG_DIR"
folders=(knowledge knowledge/business knowledge/products knowledge/operations knowledge/technical knowledge/commercial knowledge/ai knowledge/branding projects prompts prompts/generation prompts/analysis prompts/coding prompts/image prompts/business prompts/marketing datasets datasets/structured datasets/extracted datasets/candidates docs docs/architecture docs/systems docs/flows docs/ui-ux docs/api references references/technical references/commercial references/contracts references/inspirations references/external assets assets/catalogs assets/visual-assets assets/product-assets assets/diagrams archive scripts)
ignored_dirs=(node_modules .git .next dist build coverage vendor venv .venv target out .turbo .cache)
log(){ printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" | tee -a "$LOG_PATH"; }
for folder in "${folders[@]}"; do mkdir -p "$DESTINATION_ROOT/$folder"; done
category(){ local lower="${1,,}"; if [[ "$lower" == *prompt* ]]; then echo prompts; elif [[ "$lower" == *"mercado livre"* || "$lower" == *petala* ]]; then echo knowledge/commercial; elif [[ "$lower" == *.csv || "$lower" == *.xlsx || "$lower" == *.json ]]; then echo datasets/candidates; else echo archive; fi; }
unique_target(){ local c="$1"; [[ ! -e "$c" ]] && { printf '%s\n' "$c"; return; }; local dir stem ext i next; dir="$(dirname "$c")"; stem="$(basename "$c")"; ext=""; [[ "$stem" == *.* ]] && ext=".${stem##*.}" && stem="${stem%.*}"; i=1; while true; do next="$dir/${stem}-$(printf '%03d' "$i")$ext"; [[ ! -e "$next" ]] && { printf '%s\n' "$next"; return; }; i=$((i+1)); done; }
log "organization started | source=$SOURCE_ROOT | destination=$DESTINATION_ROOT"
while IFS= read -r -d '' file_path; do
  [[ "$file_path" == "$DESTINATION_ROOT"* ]] && { log "ignored destination self-scan | source=$file_path"; continue; }
  skip=false; for ignored in "${ignored_dirs[@]}"; do [[ "$file_path" == *"/$ignored/"* || "$file_path" == *"\\$ignored\\"* ]] && skip=true; done; [[ "$skip" == true ]] && { log "ignored by directory rule | source=$file_path"; continue; }
  [[ "${file_path##*.}" != md ]] && { log "ignored by extension | source=$file_path"; continue; }
  rel="${file_path#$SOURCE_ROOT/}"; catdir="$(category "$rel")"; mkdir -p "$DESTINATION_ROOT/$catdir"; target="$(unique_target "$DESTINATION_ROOT/$catdir/$(basename "$file_path")")"; cp -n "$file_path" "$target"; log "copied | source=$file_path | target=$target"
done < <(find "$SOURCE_ROOT" -type f -print0)
log 'organization finished'
