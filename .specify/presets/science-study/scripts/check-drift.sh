#!/usr/bin/env bash
# Report whether projects' vendored copies of this preset have drifted.
#
# specify copies the preset in at install time and nothing links the copy back
# here, so improving the preset leaves every installed copy frozen. Passing
# --preset to `specify init` does NOT refresh an existing install: it reports
# success and leaves the old copy in place. So drift is silent by default, and
# this is the thing that makes it visible.
#
#   scripts/check-drift.sh ~/dev/acoustics/*
#   scripts/check-drift.sh                     # defaults to ~/dev
#
# Exit 0 if every copy matches this repo's HEAD, 1 otherwise.

set -o pipefail
# Deliberately no `set -u`: bash 3.2, which macOS ships, treats an empty
# array as unset, so every ${#arr[@]} on a clean project would abort the run.

SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PRESET_ID="$(basename "$SOURCE" | sed 's/^speckit-preset-//')"

# Files that are ours to ship. Anything else in the copy is spec-kit's business.
# Built with a read loop, not mapfile: macOS ships bash 3.2, which
# predates it, and the script dies on line 21 otherwise.
TRACKED=()
while IFS= read -r line; do TRACKED+=("$line"); done < <(
  git -C "$SOURCE" ls-files | grep -vE '^(scripts|\.github)/')

PROJECTS=()
if [[ $# -gt 0 ]]; then
  PROJECTS=("$@")
else
  while IFS= read -r line; do PROJECTS+=("$line"); done < <(
    find ~/dev -maxdepth 3 -type d -name '.specify' -not -path '*/.venv/*' -exec dirname {} \;)
fi

bold=$'\033[1m'; red=$'\033[31m'; yellow=$'\033[33m'; green=$'\033[32m'; off=$'\033[0m'
drift=0
checked=0

for project in "${PROJECTS[@]}"; do
  copy="$project/.specify/presets/$PRESET_ID"
  [[ -d "$copy" ]] || continue
  checked=$((checked + 1))
  name="$(basename "$project")"

  behind=(); modified=(); missing=()
  n_behind=0; n_modified=0; n_missing=0
  for f in "${TRACKED[@]}"; do
    if [[ ! -f "$copy/$f" ]]; then
      missing+=("$f"); n_missing=$((n_missing + 1)); continue
    fi
    if git -C "$SOURCE" diff --quiet HEAD -- "$f" 2>/dev/null &&
       [[ "$(git -C "$SOURCE" hash-object "$copy/$f")" == "$(git -C "$SOURCE" rev-parse "HEAD:$f" 2>/dev/null)" ]]; then
      continue
    fi
    # Differs from HEAD. Is this an older version of ours, or someone's edit?
    hash="$(git -C "$SOURCE" hash-object "$copy/$f")"
    if [[ -n "$(git -C "$SOURCE" log --all --oneline --find-object="$hash" -- "$f" 2>/dev/null | head -1)" ]]; then
      behind+=("$f"); n_behind=$((n_behind + 1))
    else
      modified+=("$f"); n_modified=$((n_modified + 1))
    fi
  done

  # The gitlink trap: --dev and init --preset both copy this repo's own .git,
  # so a plain `git add` records a submodule and a clone gets an empty preset.
  gitlink=""
  [[ -d "$copy/.git" ]] && gitlink="nested .git present"
  if git -C "$project" ls-files --stage "$copy" 2>/dev/null | grep -q '^160000'; then
    gitlink="tracked as a gitlink (mode 160000); a clone gets an empty preset"
  fi

  if [[ $n_behind -eq 0 && $n_modified -eq 0 && $n_missing -eq 0 && -z "$gitlink" ]]; then
    printf '%s  %-28s%s %sup to date%s\n' "$bold" "$name" "$off" "$green" "$off"
    continue
  fi

  drift=1
  printf '%s  %-28s%s ' "$bold" "$name" "$off"
  if [[ $n_modified -gt 0 ]]; then
    printf '%sLOCALLY MODIFIED%s\n' "$red" "$off"
  else
    printf '%sbehind%s\n' "$yellow" "$off"
  fi
  for f in ${missing[@]+"${missing[@]}"};   do printf '      missing   %s\n' "$f"; done
  for f in ${behind[@]+"${behind[@]}"};    do printf '      older     %s\n' "$f"; done
  for f in ${modified[@]+"${modified[@]}"}; do printf '      %sedited    %s%s  (not any version in this repo)\n' "$red" "$f" "$off"; done
  [[ -n "$gitlink" ]] && printf '      %sgitlink   %s%s\n' "$red" "$gitlink" "$off"
  printf '      refresh:  cd %s && specify preset remove %s && specify preset add --dev %s && rm -rf %s/.git\n' \
         "$project" "$PRESET_ID" "$SOURCE" "$copy"
done

echo
if [[ $checked -eq 0 ]]; then
  echo "No project has this preset installed."
elif [[ $drift -eq 0 ]]; then
  echo "All $checked copies match $(git -C "$SOURCE" rev-parse --short HEAD)."
else
  echo "Drift found against $(git -C "$SOURCE" rev-parse --short HEAD)."
  echo "\"behind\" is safe to refresh. \"LOCALLY MODIFIED\" means someone edited the copy;"
  echo "salvage that change into this repo first, or refreshing will discard it."
fi
exit $drift
