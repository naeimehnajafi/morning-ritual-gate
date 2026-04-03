#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# Morning Ritual Gate — Setup
# Triggers on wake from sleep (lid open) AND on login.
# Uses sleepwatcher for wake-from-sleep detection.
# ─────────────────────────────────────────────────────────────────────────────
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$(which python3)"
WAKEUP_SCRIPT="$HOME/.wakeup"
LOGIN_PLIST="$HOME/Library/LaunchAgents/com.morningritual.gate.plist"
LOG="$HOME/Library/Logs/morningritual.log"

echo ""
echo "🌅  Morning Ritual Gate — Setup"
echo "──────────────────────────────────────────────────────"

# ── 1. Check Python ───────────────────────────────────────────────────────────
if [ -z "$PYTHON" ]; then
    echo "❌  python3 not found."
    echo "    Install it with:  brew install python3"
    exit 1
fi
echo "✅  Python found: $PYTHON"

# ── 2. Check / install Homebrew & sleepwatcher ────────────────────────────────
echo ""
echo "🔍  Checking for sleepwatcher (wake-from-sleep trigger)..."

if ! command -v brew &>/dev/null; then
    echo ""
    echo "⚠️   Homebrew not found — installing it first..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Add Homebrew to PATH for this session (needed on Apple Silicon Macs)
if [ -x "/opt/homebrew/bin/brew" ]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x "/usr/local/bin/brew" ]; then
    eval "$(/usr/local/bin/brew shellenv)"
fi

if ! brew list sleepwatcher &>/dev/null; then
    echo "📦  Installing sleepwatcher..."
    brew install sleepwatcher
else
    echo "✅  sleepwatcher already installed"
fi

# ── 3. Create the ~/.wakeup script (runs on every lid-open / wake) ────────────
cat > "$WAKEUP_SCRIPT" <<WAKEUP
#!/bin/bash
# Called by sleepwatcher every time the Mac wakes from sleep.
# Only show the ritual gate once per day (the Python app handles this check).
$PYTHON "$SCRIPT_DIR/morning_ritual.py" &
WAKEUP

chmod +x "$WAKEUP_SCRIPT"
echo "✅  Wake script written to: $WAKEUP_SCRIPT"

# ── 4. Start sleepwatcher (runs ~/.wakeup on wake) ────────────────────────────
# sleepwatcher ships with its own LaunchAgent — just enable it
SLEEP_PLIST="$(brew --prefix)/opt/sleepwatcher/de.bernhard-baehr.sleepwatcher-20compatibility-localuser.plist"

if [ -f "$SLEEP_PLIST" ]; then
    cp "$SLEEP_PLIST" "$HOME/Library/LaunchAgents/" 2>/dev/null || true
    launchctl unload "$HOME/Library/LaunchAgents/$(basename "$SLEEP_PLIST")" 2>/dev/null || true
    launchctl load   "$HOME/Library/LaunchAgents/$(basename "$SLEEP_PLIST")"
    echo "✅  sleepwatcher LaunchAgent loaded"
else
    # Fallback: write our own sleepwatcher plist
    SW_PLIST="$HOME/Library/LaunchAgents/com.morningritual.sleepwatcher.plist"
    SW_BIN="$(brew --prefix)/bin/sleepwatcher"
    cat > "$SW_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.morningritual.sleepwatcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>$SW_BIN</string>
        <string>-w</string>
        <string>$WAKEUP_SCRIPT</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$LOG</string>
    <key>StandardErrorPath</key>
    <string>$LOG</string>
</dict>
</plist>
EOF
    launchctl unload "$SW_PLIST" 2>/dev/null || true
    launchctl load   "$SW_PLIST"
    echo "✅  Custom sleepwatcher LaunchAgent loaded"
fi

# ── 5. Also install a login-time trigger (covers fresh logins/reboots) ─────────
cat > "$LOGIN_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.morningritual.gate</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON</string>
        <string>$SCRIPT_DIR/morning_ritual.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>$LOG</string>
    <key>StandardErrorPath</key>
    <string>$LOG</string>
</dict>
</plist>
EOF

launchctl unload "$LOGIN_PLIST" 2>/dev/null || true
launchctl load   "$LOGIN_PLIST"
echo "✅  Login trigger installed (covers full restarts too)"

# ── 6. Summary ────────────────────────────────────────────────────────────────
ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Documents/MorningRitual"
if [ -d "$HOME/Library/Mobile Documents/com~apple~CloudDocs" ]; then
    JOURNAL_PATH="$ICLOUD/blessings_journal.txt  (syncs to iPhone via iCloud)"
else
    JOURNAL_PATH="$HOME/Documents/MorningRitual/blessings_journal.txt"
fi

echo ""
echo "──────────────────────────────────────────────────────"
echo "✨  All done! Morning Ritual Gate is active."
echo ""
echo "   🔁  Triggers on:  lid open / wake from sleep"
echo "   🔁            +   every fresh login / reboot"
echo "   📓  Journal:      $JOURNAL_PATH"
echo "   📋  Log file:     $LOG"
echo ""
echo "   Test now:      python3 \"$SCRIPT_DIR/morning_ritual.py\""
echo ""
echo "   To uninstall:"
echo "     launchctl unload \"$LOGIN_PLIST\" && rm \"$LOGIN_PLIST\""
echo "     launchctl unload \"\$HOME/Library/LaunchAgents/$(basename "$SLEEP_PLIST" 2>/dev/null || echo 'com.morningritual.sleepwatcher.plist')\""
echo "     rm \"$WAKEUP_SCRIPT\""
echo "──────────────────────────────────────────────────────"
echo ""
