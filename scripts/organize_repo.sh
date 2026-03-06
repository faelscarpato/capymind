#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="${1:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESTINATION_ROOT="${2:-$(cd "$SCRIPT_DIR/.." && pwd)}"
MAX_FILE_SIZE_KB="${MAX_FILE_SIZE_KB:-1024}"
LOG_DIR="$DESTINATION_ROOT/scripts/logs"
LOG_PATH="$LOG_DIR/organize_repo_$(date +%Y%m%d_%H%M%S).log"

folders=(knowledge docs prompts datasets data schemas references indexes projects scripts archive)
allowed_ext=(md txt json jsonl csv)
ignored_dirs=(node_modules .git .next dist build coverage release out bin obj .wrangler .turbo .cache vendor target)

mkdir -p "$LOG_DIR"

log() {
  local message="$1"
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$message" | tee -a "$LOG_PATH"
}

ensure_structure() {
  for folder in "${folders[@]}"; do
    mkdir -p "$DESTINATION_ROOT/$folder"
  done
}

resolve_category() {
  local relative="$1"
  local lower
  lower="$(printf '%s' "$relative" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    prompts/*|*/prompts/*) echo "prompts" ;;
    datasets/*|*/datasets/*) echo "datasets" ;;
    schemas/*|*/schemas/*) echo "schemas" ;;
    references/*|*/references/*) echo "references" ;;
    knowledge/*|*/knowledge/*) echo "knowledge" ;;
    docs/*|*/docs/*) echo "docs" ;;
    data/*|*/data/*|json/*|*/json/*|sql/*|*/sql/*) echo "data" ;;
    *) echo "docs" ;;
  esac
}

unique_target() {
  local candidate="$1"
  if [[ ! -e "$candidate" ]]; then
    printf '%s\n' "$candidate"
    return
  fi
  local dir stem ext counter next
  dir="$(dirname "$candidate")"
  stem="$(basename "$candidate")"
  ext=""
  if [[ "$stem" == *.* ]]; then
    ext=".${stem##*.}"
    stem="${stem%.*}"
  fi
  counter=1
  while true; do
    next="$dir/${stem}-$(printf '%03d' "$counter")$ext"
    if [[ ! -e "$next" ]]; then
      printf '%s\n' "$next"
      return
    fi
    counter=$((counter + 1))
  done
}

is_ignored_path() {
  local full_path="$1"
  for ignored in "${ignored_dirs[@]}"; do
    if [[ "$full_path" == *"/$ignored/"* ]] || [[ "$full_path" == *"\\$ignored\\"* ]]; then
      return 0
    fi
  done
  return 1
}

ensure_structure
log "organization started | source=$SOURCE_ROOT | destination=$DESTINATION_ROOT"

while IFS= read -r -d '' file_path; do
  if [[ "$file_path" == "$DESTINATION_ROOT"* ]]; then
    log "ignored destination self-scan | source=$file_path"
    continue
  fi
  if is_ignored_path "$file_path"; then
    log "ignored by directory rule | source=$file_path"
    continue
  fi
  extension="${file_path##*.}"
  extension="${extension,,}"
  allowed=false
  for item in "${allowed_ext[@]}"; do
    if [[ "$extension" == "$item" ]]; then
      allowed=true
      break
    fi
  done
  if [[ "$allowed" != true ]]; then
    log "ignored by extension | source=$file_path"
    continue
  fi
  size_kb=$(( ($(wc -c < "$file_path") + 1023) / 1024 ))
  if (( size_kb > MAX_FILE_SIZE_KB )); then
    log "ignored by size | source=$file_path | size_kb=$size_kb"
    continue
  fi
  relative_path="${file_path#$SOURCE_ROOT/}"
  category="$(resolve_category "$relative_path")"
  target_dir="$DESTINATION_ROOT/$category"
  mkdir -p "$target_dir"
  target_path="$target_dir/$(basename "$file_path")"
  safe_target="$(unique_target "$target_path")"
  cp -n "$file_path" "$safe_target"
  if [[ "$safe_target" != "$target_path" ]]; then
    log "copied with rename | source=$file_path | target=$safe_target"
  else
    log "copied | source=$file_path | target=$safe_target"
  fi
done < <(find "$SOURCE_ROOT" -type f -print0)

log 'organization finished'
