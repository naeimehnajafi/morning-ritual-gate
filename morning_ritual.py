#!/usr/bin/env python3
"""
Morning Ritual Gate
Blocks your Mac at login until you've meditated and written 10 blessings.
Saves a dated journal entry with your streak to ~/Documents/MorningRitual/
"""

import tkinter as tk
import json
from datetime import datetime, date
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
HOME        = Path.home()
ICLOUD_DOCS = HOME / "Library/Mobile Documents/com~apple~CloudDocs/Documents"
LOCAL_DOCS  = HOME / "Documents"

BASE        = (ICLOUD_DOCS if ICLOUD_DOCS.exists() else LOCAL_DOCS) / "MorningRitual"
JOURNAL     = BASE / "blessings_journal.txt"
STREAK_FILE = BASE / "streak.json"

# ── Streak helpers ────────────────────────────────────────────────────────────
def load_streak():
    """Return (streak_count, already_completed_today)."""
    if not STREAK_FILE.exists():
        return 0, False
    with open(STREAK_FILE) as f:
        data = json.load(f)
    last   = date.fromisoformat(data.get("last_date", "2000-01-01"))
    streak = data.get("streak", 0)
    today  = date.today()
    if last == today:
        return streak, True         # already done today — don't block
    if (today - last).days == 1:
        return streak, False        # yesterday done — streak continues
    return 0, False                 # missed a day — streak resets

def save_streak(new_streak):
    BASE.mkdir(parents=True, exist_ok=True)
    with open(STREAK_FILE, "w") as f:
        json.dump({"last_date": date.today().isoformat(), "streak": new_streak}, f)

# ── Journal writer ────────────────────────────────────────────────────────────
def save_journal(blessings):
    streak, _ = load_streak()
    new_streak = streak + 1
    now = datetime.now()

    # ── Header line ──
    # Wednesday, April 2, 2026  ·  7:34 AM  ·  Day 5 🔥
    header = (
        f"\n{'─' * 64}\n"
        f"  {now.strftime('%A, %B %-d, %Y')}  ·  "
        f"{now.strftime('%-I:%M %p')}  ·  "
        f"Day {new_streak} 🔥\n"
        f"{'─' * 64}\n"
    )
    body = "".join(f"  {i:2}. {b}\n" for i, b in enumerate(blessings, 1))

    BASE.mkdir(parents=True, exist_ok=True)
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(header + body)

    save_streak(new_streak)
    return new_streak

# ── Colour palette ────────────────────────────────────────────────────────────
BG     = "#0f0f1a"
CARD   = "#1c1c30"
ACCENT = "#7c6af7"
GREEN  = "#4ade80"
TEXT   = "#e8e8f0"
DIM    = "#6868a0"
ERR    = "#f87171"
GOLD   = "#fbbf24"
FONT   = "SF Pro Display"

# ── Main window ───────────────────────────────────────────────────────────────
class MorningGate(tk.Tk):
    def __init__(self):
        super().__init__()
        self._lock_window()

        streak, done_today = load_streak()

        if done_today:
            self._already_done(streak)
        else:
            self.streak = streak
            self._build()

    # ── Window locking ────────────────────────────────────────────────────────
    def _lock_window(self):
        self.attributes("-fullscreen", True)
        self.attributes("-topmost", True)
        # Note: overrideredirect is intentionally NOT used — on macOS it breaks
        # keyboard input. Fullscreen mode hides the title bar anyway.
        self.configure(bg=BG)
        self.title("Morning Ritual")
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        for chord in ("<Command-q>", "<Command-w>", "<Command-h>",
                      "<Command-m>", "<Escape>"):
            self.bind(chord, lambda e: None)
        # Force keyboard focus to this window after it renders
        self.after(200, self._grab_focus)

    # ── Focus grabbing ────────────────────────────────────────────────────────
    def _grab_focus(self):
        self.lift()
        self.focus_force()
        # If entries exist, focus the first one
        if hasattr(self, "b_entries") and self.b_entries:
            self.b_entries[0].focus_set()

    # ── Already done screen ───────────────────────────────────────────────────
    def _already_done(self, streak):
        tk.Label(
            self,
            text=f"Already done today  ✅\nDay {streak} streak maintained  🔥",
            font=(FONT, 30, "bold"), fg=GREEN, bg=BG, justify="center"
        ).pack(expand=True)
        self.after(1800, self.destroy)

    # ── Main UI ───────────────────────────────────────────────────────────────
    def _build(self):
        # Scrollable canvas so it works on any screen height
        canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        vsb    = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.f = tk.Frame(canvas, bg=BG)
        win   = canvas.create_window((0, 0), window=self.f, anchor="n")

        self.f.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(win, width=e.width)
        )
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-e.delta / 60), "units")
        )

        self._header()
        self._meditation_card()
        self._blessings()
        self._footer()
        # Focus first blessing field once everything is rendered
        self.after(300, self._grab_focus)

    # ── Header ────────────────────────────────────────────────────────────────
    def _lbl(self, text, size, bold=False, color=TEXT, pady=0, parent=None):
        p = parent or self.f
        w = "bold" if bold else ""
        tk.Label(p, text=text, font=(FONT, size, w), fg=color, bg=BG).pack(
            pady=pady, padx=80
        )

    def _header(self):
        now = datetime.now()
        self._lbl(
            now.strftime("%A, %B %-d, %Y"), 18,
            color=DIM, pady=(50, 0)
        )
        self._lbl("Good morning  ✨", 46, bold=True, pady=(6, 2))
        if self.streak > 0:
            streak_msg = (
                f"You're on a {self.streak}-day streak  🔥  "
                f"→  finish today to reach Day {self.streak + 1}"
            )
        else:
            streak_msg = "Start your streak today  🌱"
        self._lbl(streak_msg, 15, color=GOLD, pady=(0, 34))

    # ── Meditation checkbox card ──────────────────────────────────────────────
    def _meditation_card(self):
        card = tk.Frame(self.f, bg=CARD)
        card.pack(fill="x", padx=80, pady=(0, 30))

        self.med_var = tk.BooleanVar()
        tk.Checkbutton(
            card,
            text="  I have meditated today  🧘",
            variable=self.med_var,
            font=(FONT, 19, "bold"),
            fg=GREEN, bg=CARD,
            selectcolor=BG,
            activebackground=CARD, activeforeground=GREEN,
            cursor="hand2",
        ).pack(pady=18, padx=26)

    # ── 10 Blessings fields ───────────────────────────────────────────────────
    def _blessings(self):
        self._lbl("10 Blessings", 26, bold=True, pady=(0, 4))
        self._lbl("What are you grateful for today?", 14, color=DIM, pady=(0, 16))

        self.b_vars   = []
        self.b_entries = []

        for i in range(1, 11):
            row = tk.Frame(self.f, bg=BG)
            row.pack(fill="x", padx=80, pady=4)

            tk.Label(
                row, text=f"{i:2}.",
                font=("SF Mono", 15), fg=DIM, bg=BG, width=3
            ).pack(side="left")

            var = tk.StringVar()
            self.b_vars.append(var)

            e = tk.Entry(
                row, textvariable=var,
                font=(FONT, 16), fg=TEXT, bg=CARD,
                insertbackground=TEXT,
                relief="flat", bd=0,
                highlightthickness=1,
                highlightcolor=ACCENT,
                highlightbackground="#2c2c50",
            )
            e.pack(side="left", fill="x", expand=True, ipady=10, padx=(6, 0))
            self.b_entries.append(e)

            # Return/Enter jumps to next field
            e.bind("<Return>",  lambda ev, idx=i:   self._next_field(idx))
            e.bind("<KP_Enter>", lambda ev, idx=i:  self._next_field(idx))

    def _next_field(self, current):
        if current < 10:
            self.b_entries[current].focus_set()
        else:
            self.unlock_btn.focus_set()

    # ── Submit area ───────────────────────────────────────────────────────────
    def _footer(self):
        self.unlock_btn = tk.Button(
            self.f,
            text="Unlock My Mac  →",
            font=(FONT, 19, "bold"),
            fg=BG, bg=ACCENT,
            activebackground="#9d8fff",
            relief="flat", cursor="hand2",
            command=self._submit,
            padx=44, pady=14,
        )
        self.unlock_btn.pack(pady=(38, 8))
        self.unlock_btn.bind("<Return>", lambda e: self._submit())

        self.err = tk.Label(
            self.f, text="", font=(FONT, 13), fg=ERR, bg=BG
        )
        self.err.pack(pady=(0, 60))

    # ── Validation & save ─────────────────────────────────────────────────────
    def _submit(self):
        if not self.med_var.get():
            self.err.config(text="Please check that you've meditated first  ☝️")
            return

        blessings = [v.get().strip() for v in self.b_vars]
        missing   = [i + 1 for i, b in enumerate(blessings) if not b]

        if missing:
            nums = ", ".join(str(n) for n in missing)
            self.err.config(text=f"Please fill in blessing{'s' if len(missing)>1 else ''}:  {nums}")
            return

        new_streak = save_journal(blessings)

        # Success screen
        for w in self.winfo_children():
            w.destroy()

        tk.Label(
            self,
            text=f"Beautiful  🌟\nDay {new_streak} complete — your Mac is unlocked.",
            font=(FONT, 34, "bold"), fg=GREEN, bg=BG, justify="center",
        ).pack(expand=True)

        self.after(2200, self.destroy)


if __name__ == "__main__":
    MorningGate().mainloop()
