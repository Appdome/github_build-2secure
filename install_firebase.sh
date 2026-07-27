#!/bin/bash
#
# Installs the Firebase CLI (firebase-tools) when Crashlytics deobfuscation
# upload is requested via FIREBASE_APP_ID.
#
# Behavior:
#   - Skips install if FIREBASE_APP_ID is not set (Crashlytics not used).
#   - Tries the official Firebase installer first (firebase.tools).
#   - On failure, downloads the standalone binary from Firebase GitHub Releases.
#   - If both fail, logs a warning and continues so Appdome fuse/sign still runs.
#

set -u

FIREBASE_APP_ID="${FIREBASE_APP_ID:-None}"

# Crashlytics mapping upload is optional — only needed when FIREBASE_APP_ID is provided.
if [ -z "$FIREBASE_APP_ID" ] || [ "$FIREBASE_APP_ID" = "None" ]; then
  echo "FIREBASE_APP_ID not provided; skipping firebase-tools install."
  exit 0
fi

firebase_works() {
  command -v firebase >/dev/null 2>&1 && firebase --version >/dev/null 2>&1
}

echo "-- Installing firebase-tools (needed for Crashlytics mapping upload)..."

# Step 1: official Firebase install script
if curl -sL firebase.tools | bash; then
  if firebase_works; then
    echo "-- firebase-tools installed via firebase.tools: $(firebase --version)"
    exit 0
  fi
fi

echo "-- Primary install failed; trying GitHub Releases binary..."

# Step 2: fallback — standalone binary from https://github.com/firebase/firebase-tools/releases
UNAME="$(uname -s | tr '[:upper:]' '[:lower:]')"
case "$UNAME" in
  linux*)  ASSET="firebase-tools-linux" ;;
  darwin*) ASSET="firebase-tools-macos" ;;
  *)
    echo "::warning::Unsupported OS ($UNAME) for firebase-tools fallback. Continuing without firebase CLI."
    exit 0
    ;;
esac

DOWNLOAD_URL="https://github.com/firebase/firebase-tools/releases/latest/download/${ASSET}"
TMP_BIN="/tmp/firebase_standalone"

if curl -fsSL -o "$TMP_BIN" "$DOWNLOAD_URL"; then
  sudo=""
  if [ ! -w /usr/local/bin ]; then
    sudo="sudo"
  fi
  $sudo mv -f "$TMP_BIN" /usr/local/bin/firebase
  $sudo chmod +rx /usr/local/bin/firebase

  if firebase_works; then
    echo "-- firebase-tools installed via GitHub Releases: $(firebase --version)"
    exit 0
  fi
else
  echo "-- Failed to download $DOWNLOAD_URL"
fi

# Step 3: do not fail the job — protection build should still complete
echo "::warning::Could not install firebase-tools. The Appdome build will continue, but Crashlytics mapping upload may fail or be skipped."
exit 0
