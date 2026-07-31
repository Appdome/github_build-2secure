#!/bin/bash
#
# Installs the Firebase CLI (firebase-tools) when Crashlytics deobfuscation
# upload is requested via FIREBASE_APP_ID.
#
# Behavior:
#   - Skips install if FIREBASE_APP_ID is not set (Crashlytics not used).
#   - Tries the official Firebase installer first (firebase.tools), with retries.
#   - On failure, downloads the standalone binary from Firebase GitHub Releases.
#   - If both fail, logs a clear warning that mapping was NOT uploaded,
#     but exits 0 so Appdome fuse/sign still runs.
#
# Logging:
#   - Default: only key outcomes (installed / fallback / warning).
#   - Set VERBOSE=true (or 1) for attempt/retry/download detail.
#

set -u

FIREBASE_APP_ID="${FIREBASE_APP_ID:-None}"
VERBOSE="${VERBOSE:-false}"

log() {
  echo "$1"
}

vlog() {
  case "$VERBOSE" in
    true|TRUE|1|yes|YES) echo "$1" ;;
  esac
}

# Crashlytics mapping upload is optional — only needed when FIREBASE_APP_ID is provided.
if [ -z "$FIREBASE_APP_ID" ] || [ "$FIREBASE_APP_ID" = "None" ]; then
  vlog "FIREBASE_APP_ID not provided; skipping firebase-tools install."
  exit 0
fi

firebase_works() {
  command -v firebase >/dev/null 2>&1 && firebase --version >/dev/null 2>&1
}

run_primary_install() {
  if [ "$VERBOSE" = "true" ] || [ "$VERBOSE" = "TRUE" ] || [ "$VERBOSE" = "1" ]; then
    curl -sL firebase.tools | bash
  else
    curl -sL firebase.tools | bash >/dev/null 2>&1
  fi
}

vlog "Installing firebase-tools (needed for Crashlytics mapping upload)..."

# Step 1: official Firebase install script (retry before fallback)
MAX_PRIMARY_ATTEMPTS=3
PRIMARY_RETRY_DELAY_SEC=2

for attempt in $(seq 1 "$MAX_PRIMARY_ATTEMPTS"); do
  vlog "Primary install attempt ${attempt}/${MAX_PRIMARY_ATTEMPTS}..."
  if run_primary_install; then
    if firebase_works; then
      log "firebase-tools installed via firebase.tools: $(firebase --version)"
      exit 0
    fi
  fi
  if [ "$attempt" -lt "$MAX_PRIMARY_ATTEMPTS" ]; then
    vlog "Primary install failed; retrying in ${PRIMARY_RETRY_DELAY_SEC}s..."
    sleep "$PRIMARY_RETRY_DELAY_SEC"
  fi
done

log "Primary install failed; trying GitHub Releases binary..."

# Step 2: fallback — standalone binary from https://github.com/firebase/firebase-tools/releases
UNAME="$(uname -s | tr '[:upper:]' '[:lower:]')"
case "$UNAME" in
  linux*)  ASSET="firebase-tools-linux" ;;
  darwin*) ASSET="firebase-tools-macos" ;;
  *)
    echo "::warning::Unsupported OS ($UNAME): cannot install firebase-tools. Crashlytics mapping upload will NOT run. Appdome fuse/sign will continue."
    exit 0
    ;;
esac

DOWNLOAD_URL="https://github.com/firebase/firebase-tools/releases/latest/download/${ASSET}"
TMP_BIN="/tmp/firebase_standalone"

vlog "Downloading $DOWNLOAD_URL ..."
if curl -fsSL -o "$TMP_BIN" "$DOWNLOAD_URL"; then
  sudo=""
  if [ ! -w /usr/local/bin ]; then
    sudo="sudo"
  fi
  $sudo mv -f "$TMP_BIN" /usr/local/bin/firebase
  $sudo chmod +rx /usr/local/bin/firebase

  if firebase_works; then
    log "firebase-tools installed via GitHub Releases: $(firebase --version)"
    exit 0
  fi
  vlog "Downloaded binary but firebase --version failed."
else
  vlog "Failed to download $DOWNLOAD_URL"
fi

# Step 3: clear warning for Crashlytics path, but do not fail fuse/sign
echo "::warning::firebase-tools install failed (official installer and GitHub Releases). Crashlytics mapping upload will NOT run. Appdome fuse/sign will continue."
log "WARNING: firebase-tools is not available — do not assume Crashlytics deobfuscation mapping was uploaded."
exit 0
