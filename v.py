"""      ▄▄▄▄▄▄        ▄▄▄▄   ▄▄▄▄▄▄▄  
██  █▄   ▓▒▒░        ▒▓▀▒▒▌   ███░▀ ▀▄
▐░▌ ▐░   ▐░ ▌       ▐░  ▐▒░   ▐░█▌   ░
 ▒▌  ▒░▌   ░           ▄░░ ▌   ░░ ▄▄▀ 
 ▓    ▒█  ░▒  ▀░▄  ▐░▄▀▀▄ █░   ▒▒ ▀▀▄ 
 █     ▒  ▒▓▌   ▒░ ▓▒▌   ░░▒▌  ▓▌    ▒
▐█▌   ▓█ ▐▓██▌ ▐▓▓▌█▓    ▐▒▓▌ ▐█▓   █▓
 ▐█▄▄█▌  ▐██▄█▓▓█  ▐█▓    ▓█  ████▄█▓▌
   ▀▀    ▀▀▀▀▀▀▀    ▀▀▀  ▀▀  ▀▀▀▀▀▀▀▀ 
Real-time audio processing, DSP, soundboard, synth, song sequencer, TTS, full Modding SDK.

WHAT'S NEW IN v2.0.3
  • Advanced Theme System — Full UI control for theme mod creators
  • Extended color palette with 11 customizable colors (sidebar, card, text, borders, etc.)
  • Font customization for main text, headings, and mono text
  • Widget styling controls (corner radius, border width, hover animations)
  • Custom mouse cursor support with image loading
  • Background image support with opacity and blur effects
  • Visual effects including rainbow animation and glow intensity
  • Backward compatible with simple theme format
  • Comprehensive SDK documentation with theme examples
  • RGB Rainbow theme with animated color cycling
"""

# ─────────────────────────────────────────────────────────────────────────────
# Standard library
# ─────────────────────────────────────────────────────────────────────────────
import importlib.util
import json
import math
import os
import queue
import random
import socket
import sys
import textwrap
import threading
import time
import webbrowser
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Third-party
# ─────────────────────────────────────────────────────────────────────────────
import customtkinter as ctk
import keyboard
import numpy as np
import sounddevice as sd
import soundfile as sf
import tkinter as tk
from PIL import Image
from tkinter import filedialog, messagebox, colorchooser

# ─────────────────────────────────────────────────────────────────────────────
# Optional
# ─────────────────────────────────────────────────────────────────────────────
try:
    import pyttsx3
    HAS_TTS = True
except ImportError:
    pyttsx3 = None
    HAS_TTS = False

try:
    import pystray
    from pystray import MenuItem as item
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    HAS_MPL = True
except Exception:
    HAS_MPL = False
    plt = None
    FigureCanvasTkAgg = None

try:
    from scipy import signal as scipy_signal
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# ═════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═════════════════════════════════════════════════════════════════════════════
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

APP_NAME       = "V LAB"
VERSION        = "v2.2.0 Master Edition"
SR             = 44100
CHANNELS       = 2
SOUND_LIMIT    = 100
HISTORY_MAX    = 50

CONFIG_FILE    = "soundboard_config.json"
MOD_CONFIG     = "mods_config.json"
SETTINGS_FILE  = "user_settings.json"
PRESETS_FILE   = "fx_presets.json"
SONGS_FILE     = "arp_songs.json"
REC_FOLDER     = "saved_recordings"
MODS_FOLDER    = "mods"
THEMES_FOLDER  = os.path.join(MODS_FOLDER, "themes")
SONGS_FOLDER   = os.path.join(MODS_FOLDER, "songs")
SAMPLES_FOLDER = "samples"

# ─────────────────────────────────────────────────────────────────────────────
# Theme folders — v11.0
#   mods/themes/basic/    → JSON files (color palette overrides)
#   mods/themes/advanced/ → Python files (full hooks, custom renderers)
# ─────────────────────────────────────────────────────────────────────────────
THEMES_BASIC_FOLDER    = os.path.join(MODS_FOLDER, "themes", "basic")
THEMES_ADVANCED_FOLDER = os.path.join(MODS_FOLDER, "themes", "advanced")

for _d in [REC_FOLDER, MODS_FOLDER, THEMES_BASIC_FOLDER, THEMES_ADVANCED_FOLDER, SONGS_FOLDER, SAMPLES_FOLDER]:
    Path(_d).mkdir(parents=True, exist_ok=True)

# Keep the old path working so nothing else in the file breaks
THEMES_FOLDER = THEMES_BASIC_FOLDER

SPLASHES = [
    "v2.1.0 — Revolutionary Pitch System!",
    "Phase vocoder pitch shifting with formant preservation.",
    "Theme Creator UI — No coding required!",
    "Rainbow effects with speed and intensity controls.",
    "RGB effects: cycle, pulse, and wave modes.",
    "Gradient support for backgrounds and widgets.",
    "Themes can now customize ANY UI element.",
    "Live theme preview while you edit.",
    "Export and share your custom themes.",
    "High-quality pitch shifting for larger changes.",
    "Time-domain pitch shifting for small changes.",
    "Widget-level customization available.",
    "Animation system with smooth transitions.",
    "More knobs than a recording studio.",
    "Unison detuning hits different.",
    "Buffer underrun? Never heard of her.",
    "Your mods belong in a museum.",
    "Portamento is a vibe.",
    "Waveform shaping is an art form.",
    "Latency so low it's basically telepathy.",
    "Your voice, but better.",
    "Real-time processing is the only way.",
    "Modular or nothing.",
    "Sample rate matters.",
    "Bit depth is not a suggestion.",
    "Compression is your friend.",
    "Reverb adds space to your life.",
    "Delay creates echoes of greatness.",
    "Distortion adds character.",
    "EQ is the surgeon of audio.",
    "Filter out the noise.",
    "Modulate everything.",
    "LFOs make it move.",
    "Envelopes shape the sound.",
    "Oscillators are the heart.",
    "Filters are the soul.",
    "FX are the spice.",
    "Mix it like you mean it.",
    "Master it with precision.",
    "Your ears will thank you.",
    "Audio engineering is my passion.",
    "Sound design is life.",
    "Make some noise.",
    "Break the rules.",
    "Push the limits.",
    "Experiment freely.",
    "Create without fear.",
    "Your sound is unique.",
    "Express yourself.",
    "Be heard.",
    "Make waves.",
    "Ride the frequency.",
    "Catch the vibe.",
    "Feel the beat.",
    "Hear the difference.",
    "Listen closely.",
    "Pay attention to detail.",
    "Quality over quantity.",
    "Simplicity is elegance.",
    "Less is more.",
    "Do more with less.",
    "Efficiency is key.",
    "Optimize everything.",
    "Streamline your workflow.",
    "Work smarter, not harder.",
    "Let the tools work for you.",
    "Automate the boring stuff.",
    "Focus on creativity.",
    "Let inspiration flow.",
    "Capture the moment.",
    "Preserve the magic.",
    "Share your sound.",
    "Connect with others.",
    "Build a community.",
    "Learn from each other.",
    "Grow together.",
    "Evolve constantly.",
    "Never stop learning.",
    "Stay curious.",
    "Keep exploring.",
    "thats good.",
    "Find your voice.",
    "Define your style.",
    "Create your legacy.",
]

# ─────────────────────────────────────────────────────────────────────────────
# Built-in themes — v11.0
# Each entry is a "basic" theme: a flat palette the engine resolves into a full
# ThemeData dict.  Advanced themes (Python) live in mods/themes/advanced/.
# ─────────────────────────────────────────────────────────────────────────────

def _mk_theme(accent, hover, glow, sidebar="#0D0D0D", card="#161616",
              card2="#1E1E1E", text="#E8E8E8", subtext="#848484",
              border="#2A2A2A", input_bg="#111111", rainbow=False, rgb=False):
    """Build a complete basic-theme dict from key colors."""
    return {
        "accent": accent, "hover": hover, "glow": glow,
        "sidebar": sidebar, "card": card, "card2": card2,
        "text": text, "subtext": subtext, "border": border,
        "input_bg": input_bg, "dropdown_bg": card2,
        "progress": accent, "switch_active": accent, "switch_inactive": border,
        "checkbox": accent, "segmented": accent, "tabview": accent,
        "scrollbar": "#303030", "scrollbar_button": "#404040", "tooltip": "#0A0A0A",
        "rainbow": rainbow, "rgb": rgb,
    }

DEFAULT_THEMES = {
    # ── Dark-background precision palettes ───────────────────────────────────
    "Crimson":  _mk_theme("#D12020", "#E84040", "#D1202044",
                           sidebar="#0E0A0A", card="#180E0E", card2="#231212", border="#3A1515"),
    "Cobalt":   _mk_theme("#2D6EE8", "#4D8CFF", "#2D6EE844",
                           sidebar="#09090F", card="#101424", card2="#171C30", border="#1E2A50"),
    "Emerald":  _mk_theme("#24CC8E", "#3EE8A8", "#24CC8E44",
                           sidebar="#090E0C", card="#0F1A14", card2="#15231B", border="#1A3526"),
    "Amethyst": _mk_theme("#9640D8", "#B060F0", "#9640D844",
                           sidebar="#0C090F", card="#160E20", card2="#1D142C", border="#30185A"),
    "Amber":    _mk_theme("#E8900A", "#FFA828", "#E8900A44",
                           sidebar="#0F0C07", card="#1A1408", card2="#231B0A", border="#3A2A0A"),
    "Neon":     _mk_theme("#00F040", "#33FF66", "#00F04044",
                           sidebar="#060A06", card="#0C120C", card2="#111811", border="#1A3A1A"),
    "Sakura":   _mk_theme("#E83078", "#FF4D96", "#E8307844",
                           sidebar="#0F0809", card="#1A0D10", card2="#221016", border="#3D1828"),
    "Gold":     _mk_theme("#D4AA10", "#F0CC28", "#D4AA1044",
                           sidebar="#0E0C07", card="#181408", card2="#201A0A", border="#38300A"),
    "Ice":      _mk_theme("#18B8D4", "#30D4EE", "#18B8D444",
                           sidebar="#07090F", card="#0C1018", card2="#111820", border="#183040"),
    "Void":     _mk_theme("#7C70FF", "#9C92FF", "#7C70FF44",
                           sidebar="#08070F", card="#100E20", card2="#16142C", border="#2A2660"),
    "Blood":    _mk_theme("#E01040", "#FF2855", "#E0104044",
                           sidebar="#0F0608", card="#1A0A0C", card2="#230E10", border="#3E1018"),
    "Mint":     _mk_theme("#00D4B8", "#1AF0D2", "#00D4B844",
                           sidebar="#060E0C", card="#0A1614", card2="#0E1E1C", border="#163830"),
    # ── Special effect themes ─────────────────────────────────────────────────
    "Rainbow":  _mk_theme("#D12020", "#E84040", "#D1202044", rainbow=True),
    "Space Nebula": {
        "accent": "#8A5CFF", "hover": "#B084FF", "glow": "#8A5CFF55",
        "sidebar": "#06040F", "card": "#110C24", "card2": "#18123A",
        "text": "#E4DCFF", "subtext": "#9080C4", "border": "#261E58",
        "input_bg": "#0C0918", "dropdown_bg": "#18123A",
        "progress": "#8A5CFF", "switch_active": "#8A5CFF", "switch_inactive": "#261E58",
        "checkbox": "#8A5CFF", "segmented": "#8A5CFF", "tabview": "#8A5CFF",
        "scrollbar": "#2A1E6C", "scrollbar_button": "#3E2E90", "tooltip": "#06040F",
        "rainbow": False, "rgb": False, "_space": True,
    },
    "RGB Pulse": _mk_theme("#FF2020", "#FF4040", "#FF202055", rgb=True),
}

# Advanced theme schema with full UI control - v2.1.0 Enhanced
ADVANCED_THEME_SCHEMA = {
    "version": "2.1",  # Theme format version
    "meta": {
        "name": "Theme Name",
        "author": "Author Name",
        "description": "Theme description"
    },
    "colors": {
        "accent": "#D00000",
        "hover": "#FF2020",
        "glow": "#D0000033",
        "sidebar": "#0C0C0C",
        "card": "#181818",
        "card2": "#222222",
        "text": "#E8E8E8",
        "subtext": "#888888",
        "border": "#333333",
        "scrollbar": "#444444",
        "input_bg": "#1A1A1A",
        "dropdown_bg": "#222222"
    },
    "fonts": {
        "main": {"family": "Consolas", "size": 10},
        "heading": {"family": "Consolas", "size": 12, "weight": "bold"},
        "mono": {"family": "Consolas", "size": 9}
    },
    "widgets": {
        "button": {
            "corner_radius": 8,
            "border_width": 0,
            "hover_animation": True
        },
        "card": {
            "corner_radius": 10,
            "border_width": 0
        },
        "input": {
            "corner_radius": 6,
            "border_width": 1
        },
        "slider": {
            "corner_radius": 0,
            "button_size": 20
        }
    },
    "cursor": {
        "enabled": False,
        "default": "arrow",
        "custom_path": ""
    },
    "background": {
        "enabled": False,
        "path": "",
        "opacity": 1.0,
        "blur": 0
    },
    "effects": {
        "rainbow": {
            "enabled": False,
            "speed": 1.0,
            "intensity": 1.0,
            "targets": ["accent", "hover", "glow"]
        },
        "rgb": {
            "enabled": False,
            "mode": "cycle",  # cycle, pulse, wave
            "speed": 1.0,
            "intensity": 1.0,
            "targets": ["accent"]
        },
        "gradients": {
            "enabled": False,
            "sidebar": {
                "enabled": False,
                "type": "linear",  # linear, radial
                "direction": "vertical",  # horizontal, vertical, diagonal
                "colors": ["#0C0C0C", "#1A1A1A"],
                "stops": [0.0, 1.0]
            },
            "card": {
                "enabled": False,
                "type": "linear",
                "direction": "vertical",
                "colors": ["#181818", "#222222"],
                "stops": [0.0, 1.0]
            }
        },
        "glow_intensity": 1.0,
        "animation_speed": 1.0
    }
}


def _seed_basic_themes():
    """Write built-in palettes into basic/ if the folder is empty."""
    if any(f.endswith(".json") for f in os.listdir(THEMES_BASIC_FOLDER)):
        return
    for name, data in DEFAULT_THEMES.items():
        fname = name.replace(" ", "_") + ".json"
        with open(os.path.join(THEMES_BASIC_FOLDER, fname), "w", encoding="utf-8") as f:
            # Serialise — strip internal flags that aren't user-facing
            out = {k: v for k, v in data.items() if not k.startswith("_")}
            json.dump(out, f, indent=4)


def _load_basic_themes():
    """Return dict of name → palette-dict from basic/ JSON files."""
    result = {}
    for fn in sorted(os.listdir(THEMES_BASIC_FOLDER)):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(THEMES_BASIC_FOLDER, fn)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                continue
            name = fn[:-5].replace("_", " ")   # filename → display name
            # Ensure required keys exist (fill from defaults if partial)
            merged = {
                "accent": "#D12020", "hover": "#E84040", "glow": "#D1202044",
                "sidebar": "#0D0D0D", "card": "#161616", "card2": "#1E1E1E",
                "text": "#E8E8E8", "subtext": "#848484", "border": "#2A2A2A",
                "input_bg": "#111111", "dropdown_bg": "#1E1E1E",
                "progress": data.get("accent", "#D12020"),
                "switch_active": data.get("accent", "#D12020"),
                "switch_inactive": "#2A2A2A",
                "checkbox": data.get("accent", "#D12020"),
                "segmented": data.get("accent", "#D12020"),
                "tabview": data.get("accent", "#D12020"),
                "scrollbar": "#303030", "scrollbar_button": "#404040",
                "tooltip": "#0A0A0A", "rainbow": False, "rgb": False,
            }
            merged.update(data)
            result[name] = merged
        except Exception as e:
            print(f"[Themes] Failed to load {fn}: {e}")
    return result


def _load_advanced_themes():
    """Return dict of name → advanced-theme-module from advanced/ Python files.

    Each .py file must define:
        THEME = {"name": "...", "accent": "#RRGGBB", "hover": "...", "glow": "...",
                 "sidebar": "...", "card": "...", "card2": "...", ...}

    And may optionally define:
        def apply(app):   ...   # called when theme becomes active
        def remove(app):  ...   # called when theme is deactivated
        def tick(app):    ...   # called every theme-tick (~120ms) if defined
    """
    result = {}
    for fn in sorted(os.listdir(THEMES_ADVANCED_FOLDER)):
        if not fn.endswith(".py"):
            continue
        path = os.path.join(THEMES_ADVANCED_FOLDER, fn)
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(f"adv_theme_{fn[:-3]}", path)
            mod  = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            theme_data = getattr(mod, "THEME", None)
            if not isinstance(theme_data, dict) or "name" not in theme_data:
                print(f"[Themes] {fn}: missing THEME dict with 'name' key — skipped")
                continue
            name = theme_data["name"]
            result[name] = {
                "_advanced": True,
                "_module": mod,
                "colors": theme_data,
                # Flatten for compatibility with the simple _apply_theme path
                **theme_data,
            }
        except Exception as e:
            print(f"[Themes] Failed to load advanced theme {fn}: {e}")
    return result


def init_themes():
    """Load all themes (built-in + basic JSON + advanced Python)."""
    _seed_basic_themes()
    loaded = {}
    # Built-ins first so mods can override them by name
    loaded.update(DEFAULT_THEMES)
    loaded.update(_load_basic_themes())
    loaded.update(_load_advanced_themes())
    return loaded


THEMES = init_themes()

DEFAULT_PRESETS = {
    "Clean":      {"gain": 0, "pitch": 0, "pan": 0, "distortion": 0, "chorus_mix": 0, "delay_mix": 0, "reverb_mix": 0, "noise_gate": 0},
    "Radio":      {"gain": 6, "pitch": 0, "distortion": 0.35, "chorus_mix": 0, "delay_mix": 0, "reverb_mix": 0, "noise_gate": 0.05, "eq_lo": -12, "eq_hi": -8},
    "Megaphone":  {"gain": 12, "pitch": 1, "distortion": 0.6, "chorus_mix": 0, "delay_mix": 0, "reverb_mix": 0},
    "Deep Voice": {"gain": 4, "pitch": -5, "distortion": 0, "chorus_mix": 0, "delay_mix": 0, "reverb_mix": 0.15},
    "Chipmunk":   {"gain": 0, "pitch": 8, "distortion": 0, "chorus_mix": 0.1, "delay_mix": 0, "reverb_mix": 0},
    "Cave":       {"gain": 2, "pitch": 0, "distortion": 0, "chorus_mix": 0, "delay_mix": 0.4, "reverb_mix": 0.8, "reverb_decay": 0.9},
    "Robot":      {"gain": 0, "pitch": 0, "distortion": 0.9, "chorus_mix": 0.4, "delay_mix": 0.2, "reverb_mix": 0},
    "Telephone":  {"gain": 8, "pitch": 0, "distortion": 0.4, "eq_lo": -15, "eq_hi": -10, "noise_gate": 0.08},
    "Stadium":    {"gain": 3, "pitch": 0, "distortion": 0, "chorus_mix": 0.2, "delay_mix": 0.3, "reverb_mix": 0.7, "reverb_decay": 0.85},
}


# ═════════════════════════════════════════════════════════════════════════════
# ARP SONGS — note name → MIDI number helper
# ═════════════════════════════════════════════════════════════════════════════
_NOTE_MAP = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4,
             "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9,
             "A#": 10, "Bb": 10, "B": 11}

def note_to_midi(name: str) -> int:
    """Convert 'C4', 'F#5', etc. to MIDI number. C4 = 60."""
    name = name.strip()
    if len(name) >= 2 and name[-1].isdigit():
        octave = int(name[-1])
        n = name[:-1]
    elif len(name) >= 3 and name[-1].isdigit():
        octave = int(name[-1])
        n = name[:-1]
    else:
        return 60
    pc = _NOTE_MAP.get(n, 0)
    return (octave + 1) * 12 + pc

def midi_to_freq(midi: int) -> float:
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)

def note_name_to_freq(name: str) -> float:
    return midi_to_freq(note_to_midi(name))


# Song format:
# A "song" is a list of steps. Each step is:
#   {"note": "C4", "dur": 0.25, "vel": 1.0, "rest": false}
# dur = duration in beats (1.0 = one beat at current BPM)
# vel = velocity 0-1
# rest = if true, plays silence for that duration

def _make_song(notes_dur_pairs, vel=0.8):
    """Helper: list of (note_name, dur_beats) → song steps."""
    return [{"note": n, "dur": d, "vel": vel, "rest": False} for n, d in notes_dur_pairs]

def _make_rest(dur):
    return {"note": "C4", "dur": dur, "vel": 0.0, "rest": True}

# ── Built-in songs ────────────────────────────────────────────────────────────
BUILTIN_SONGS = {
    "Major Triad Up":   {"steps": _make_song([("C4",0.25),("E4",0.25),("G4",0.25),("C5",0.25)]), "loop": True},
    "Minor Triad Up":   {"steps": _make_song([("C4",0.25),("Eb4",0.25),("G4",0.25),("C5",0.25)]), "loop": True},
    "Octave Bounce":    {"steps": _make_song([("C4",0.25),("C5",0.25),("G4",0.25),("C5",0.25)]), "loop": True},
    "Pentatonic Up":    {"steps": _make_song([("C4",0.2),("D4",0.2),("E4",0.2),("G4",0.2),("A4",0.2)]), "loop": True},
    "Blues Scale":      {"steps": _make_song([("C4",0.2),("Eb4",0.2),("F4",0.2),("Gb4",0.2),("G4",0.2),("Bb4",0.2)]), "loop": True},
    "Chromatic Run":    {"steps": _make_song([(f"{n}{o}",0.125) for o in [4] for n in ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]], vel=0.7), "loop": True},
    "Major Scale":      {"steps": _make_song([("C4",0.25),("D4",0.25),("E4",0.25),("F4",0.25),("G4",0.25),("A4",0.25),("B4",0.25),("C5",0.25)]), "loop": True},
    "Phrygian Mode":    {"steps": _make_song([("E4",0.25),("F4",0.25),("G4",0.25),("A4",0.25),("B4",0.25),("C5",0.25),("D5",0.25),("E5",0.25)]), "loop": True},
    "Power Chord":      {"steps": _make_song([("E4",0.25),("B4",0.25),("E5",0.25),("B4",0.25)]), "loop": True},
    "Jazz ii-V-I":      {"steps": _make_song([("D4",0.33),("F4",0.33),("A4",0.33),("G4",0.33),("B4",0.33),("D5",0.33),("C4",0.33),("E4",0.33),("G4",0.33)]), "loop": True},
    "Alberti Bass":     {"steps": _make_song([("C4",0.25),("G4",0.25),("E4",0.25),("G4",0.25),("C4",0.25),("G4",0.25),("E4",0.25),("G4",0.25)]), "loop": True},
    "Whole Tone":       {"steps": _make_song([("C4",0.25),("D4",0.25),("E4",0.25),("F#4",0.25),("G#4",0.25),("A#4",0.25)]), "loop": True},
    # ── Famous melodies ───────────────────────────────────────────────────────
    "Mary Had a Little Lamb": {
        "steps": _make_song([
            ("E4",0.25),("D4",0.25),("C4",0.25),("D4",0.25),
            ("E4",0.25),("E4",0.25),("E4",0.5),
            ("D4",0.25),("D4",0.25),("D4",0.5),
            ("E4",0.25),("G4",0.25),("G4",0.5),
            ("E4",0.25),("D4",0.25),("C4",0.25),("D4",0.25),
            ("E4",0.25),("E4",0.25),("E4",0.25),("E4",0.25),
            ("D4",0.25),("D4",0.25),("E4",0.25),("D4",0.25),("C4",0.5),
        ]),
        "loop": True,
    },
    "Dance of the Sugar Plum Fairy": {
        "steps": _make_song([
            ("E5",0.25),("D#5",0.25),("E5",0.25),("D#5",0.25),
            ("E5",0.25),("B4",0.25),("D5",0.25),("C5",0.25),
            ("A4",0.5),("A4",0.5),
            ("C4",0.25),("E4",0.25),("A4",0.25),("B4",0.25),
            ("D4",0.25),("F4",0.25),("B4",0.25),("C5",0.25),
            ("E5",0.25),("D#5",0.25),("E5",0.25),("D#5",0.25),
            ("E5",0.25),("B4",0.25),("D5",0.25),("C5",0.25),
            ("A4",0.75),
        ]),
        "loop": True,
    },
    "Ode to Joy": {
        "steps": _make_song([
            ("E4",0.25),("E4",0.25),("F4",0.25),("G4",0.25),
            ("G4",0.25),("F4",0.25),("E4",0.25),("D4",0.25),
            ("C4",0.25),("C4",0.25),("D4",0.25),("E4",0.25),
            ("E4",0.33),("D4",0.17),("D4",0.5),
            ("E4",0.25),("E4",0.25),("F4",0.25),("G4",0.25),
            ("G4",0.25),("F4",0.25),("E4",0.25),("D4",0.25),
            ("C4",0.25),("C4",0.25),("D4",0.25),("E4",0.25),
            ("D4",0.33),("C4",0.17),("C4",0.5),
        ]),
        "loop": True,
    },
    "Für Elise (Theme)": {
        "steps": _make_song([
            ("E5",0.125),("D#5",0.125),("E5",0.125),("D#5",0.125),
            ("E5",0.125),("B4",0.125),("D5",0.125),("C5",0.125),
            ("A4",0.375),
            ("C4",0.125),("E4",0.125),("A4",0.125),
            ("B4",0.375),
            ("E4",0.125),("G#4",0.125),("B4",0.125),
            ("C5",0.375),
            ("E4",0.125),("E5",0.125),("D#5",0.125),
            ("E5",0.125),("D#5",0.125),("E5",0.125),("B4",0.125),("D5",0.125),("C5",0.125),
            ("A4",0.375),
        ]),
        "loop": True,
    },
    "Twinkle Twinkle": {
        "steps": _make_song([
            ("C4",0.25),("C4",0.25),("G4",0.25),("G4",0.25),
            ("A4",0.25),("A4",0.25),("G4",0.5),
            ("F4",0.25),("F4",0.25),("E4",0.25),("E4",0.25),
            ("D4",0.25),("D4",0.25),("C4",0.5),
            ("G4",0.25),("G4",0.25),("F4",0.25),("F4",0.25),
            ("E4",0.25),("E4",0.25),("D4",0.5),
            ("G4",0.25),("G4",0.25),("F4",0.25),("F4",0.25),
            ("E4",0.25),("E4",0.25),("D4",0.5),
            ("C4",0.25),("C4",0.25),("G4",0.25),("G4",0.25),
            ("A4",0.25),("A4",0.25),("G4",0.5),
            ("F4",0.25),("F4",0.25),("E4",0.25),("E4",0.25),
            ("D4",0.25),("D4",0.25),("C4",0.5),
        ]),
        "loop": True,
    },
    "Jingle Bells (Hook)": {
        "steps": _make_song([
            ("E4",0.25),("E4",0.25),("E4",0.5),
            ("E4",0.25),("E4",0.25),("E4",0.5),
            ("E4",0.25),("G4",0.25),("C4",0.25),("D4",0.125),("E4",0.875),
            ("F4",0.25),("F4",0.25),("F4",0.25),("F4",0.25),
            ("F4",0.25),("E4",0.25),("E4",0.25),("E4",0.125),("E4",0.125),
            ("E4",0.25),("D4",0.25),("D4",0.25),("E4",0.25),("D4",0.5),("G4",0.5),
        ]),
        "loop": True,
    },
    "Happy Birthday": {
        "steps": _make_song([
            ("G4",0.125),("G4",0.125),("A4",0.25),("G4",0.25),("C5",0.25),("B4",0.5),
            ("G4",0.125),("G4",0.125),("A4",0.25),("G4",0.25),("D5",0.25),("C5",0.5),
            ("G4",0.125),("G4",0.125),("G5",0.25),("E5",0.25),("C5",0.25),("B4",0.25),("A4",0.5),
            ("F5",0.125),("F5",0.125),("E5",0.25),("C5",0.25),("D5",0.25),("C5",0.5),
        ]),
        "loop": True,
    },
    "Tetris (Korobeiniki)": {
        "steps": _make_song([
            ("E5",0.25),("B4",0.125),("C5",0.125),("D5",0.25),("C5",0.125),("B4",0.125),
            ("A4",0.25),("A4",0.125),("C5",0.125),("E5",0.25),("D5",0.125),("C5",0.125),
            ("B4",0.375),("C5",0.125),("D5",0.25),("E5",0.25),
            ("C5",0.25),("A4",0.25),("A4",0.5),
            ("D5",0.375),("F5",0.125),("A5",0.25),("G5",0.125),("F5",0.125),
            ("E5",0.375),("C5",0.125),("E5",0.25),("D5",0.125),("C5",0.125),
            ("B4",0.25),("B4",0.125),("C5",0.125),("D5",0.25),("E5",0.25),
            ("C5",0.25),("A4",0.25),("A4",0.5),
        ]),
        "loop": True,
    },
    "Super Mario (Theme)": {
        "steps": _make_song([
            ("E5",0.125),("E5",0.125),("E5",0.0),("E5",0.125),
            ("C5",0.125),("E5",0.25),("G5",0.25),("G4",0.25),
            ("C5",0.375),("G4",0.125),("E4",0.375),("A4",0.25),
            ("B4",0.25),("Bb4",0.125),("A4",0.25),("G4",0.2),("E5",0.2),("G5",0.2),
            ("A5",0.25),("F5",0.125),("G5",0.125),("E5",0.25),("C5",0.125),("D5",0.125),("B4",0.25),
        ]),
        "loop": True,
    },
    "Greensleeves": {
        "steps": _make_song([
            ("A4",0.25),("C5",0.375),("D5",0.125),("E5",0.25),
            ("F5",0.375),("E5",0.125),("D5",0.375),("B4",0.125),
            ("G4",0.25),("A4",0.375),("B4",0.125),("C5",0.25),
            ("A4",0.5),
            ("A4",0.25),("C5",0.375),("D5",0.125),("E5",0.25),
            ("F5",0.375),("E5",0.125),("D5",0.375),("B4",0.125),
            ("G4",0.25),("A4",0.375),("B4",0.125),("C5",0.25),
            ("A4",0.5),
        ]),
        "loop": True,
    },
    "Moonlight Sonata (Opening)": {
        "steps": _make_song([
            ("C#4",0.33),("E4",0.33),("G#4",0.33),
            ("C#4",0.33),("E4",0.33),("G#4",0.33),
            ("D4",0.33),("F#4",0.33),("A4",0.33),
            ("D4",0.33),("F#4",0.33),("A4",0.33),
            ("B3",0.33),("D4",0.33),("G#4",0.33),
            ("B3",0.33),("D4",0.33),("G#4",0.33),
        ]),
        "loop": True,
    },
}


def load_songs():
    """Load all songs: built-ins + user songs from JSON files in songs/ folder."""
    songs = dict(BUILTIN_SONGS)
    # Load user songs from SONGS_FOLDER
    for fn in os.listdir(SONGS_FOLDER):
        if fn.endswith(".json"):
            try:
                with open(os.path.join(SONGS_FOLDER, fn)) as f:
                    data = json.load(f)
                name = data.get("name", fn[:-5])
                songs[name] = data
            except Exception:
                pass
    # Also load top-level SONGS_FILE if it exists
    if os.path.exists(SONGS_FILE):
        try:
            with open(SONGS_FILE) as f:
                user = json.load(f)
            songs.update(user)
        except Exception:
            pass
    return songs


# ═════════════════════════════════════════════════════════════════════════════
# SDK README (auto-generated)
# ═════════════════════════════════════════════════════════════════════════════
SDK_README = textwrap.dedent("""
# V LAB Modding SDK — v11.0
## Open Source — MIT License

---

## What's new in v11.0
- **Two-tier theme system.** Basic themes (JSON, `mods/themes/basic/`) for
  simple palette edits.  Advanced themes (Python, `mods/themes/advanced/`)
  for full control: custom animations, tick hooks, dynamic recoloring.
- **Theme hooks:** `apply(app)`, `remove(app)`, `tick(app)` — the engine
  calls them automatically; you never schedule your own `after()` loop.
- **CPU savings:** rainbow/RGB animation now batches widget recolors and runs
  at 120ms intervals.  Space Nebula starfield runs at 80ms, no pixel loops.
- Theme SDK is separate from FX/instrument mods — drop theme files into the
  correct subfolder and V LAB picks them up on next reload.

---

## Module Types

### 1. FX Mod  (category = "fx")
Real-time audio processor. Receives audio blocks and returns processed audio.

```python
import numpy as np

META = {
    "name":     "my_effect",        # unique ID — no spaces
    "label":    "My Effect",        # shown in UI
    "version":  "1.0",
    "author":   "YourName",
    "desc":     "Does something cool.",
    "category": "fx",
}

CONTROLS = [
    {"key": "my_effect_amount", "label": "Amount", "type": "slider",
     "min": 0.0, "max": 1.0, "default": 0.5, "unit": ""},
    {"key": "my_effect_on",     "label": "Enabled", "type": "toggle",  "default": True},
    {"key": "my_effect_mode",   "label": "Mode",    "type": "dropdown",
     "options": ["Soft", "Hard", "Clip"], "default": "Soft"},
]

def process(audio: np.ndarray, params: dict) -> np.ndarray:
    \"\"\"
    audio  : float32 ndarray (N, 2) — stereo audio block, ~1024 frames
    params : dict — CONTROLS values with META["name"]_ prefix stripped
    return : float32 ndarray same shape
    PERFORMANCE: Keep this fast. Avoid Python loops. Use numpy ops.
    \"\"\"
    amount = params.get("amount", 0.0)
    if amount <= 0:
        return audio
    return np.tanh(audio * (1 + amount * 4)) / (1 + amount * 0.3)
```

---

### 2. Instrument Mod  (category = "instrument")
Adds a custom sound generator. Override `get_audio(frames, params)` to produce audio.

```python
import numpy as np, time

META = {"name": "my_inst", "label": "My Instrument", "category": "instrument",
        "version": "1.0", "author": "You", "desc": "Custom oscillator"}

_phase = 0.0

def get_audio(frames: int, params: dict) -> np.ndarray:
    \"\"\"Return (frames, 2) float32 audio. Called every block when synth is on.\"\"\"
    global _phase
    freq = params.get("freq", 440)
    vol  = params.get("master_vol", 0.5)
    t = np.arange(frames)
    inc = 2 * np.pi * freq / 44100
    audio = np.sin(_phase + t * inc) * vol
    _phase = (_phase + frames * inc) % (2 * np.pi)
    stereo = np.column_stack((audio, audio)).astype(np.float32)
    return stereo
```

---

### 3. Song Mod  (external JSON in mods/songs/)
Define an arpeggiator song as a JSON file. Drop it in `mods/songs/`.

```json
{
    "name": "My Song",
    "loop": true,
    "steps": [
        {"note": "C4",  "dur": 0.25, "vel": 1.0, "rest": false},
        {"note": "E4",  "dur": 0.25, "vel": 0.9, "rest": false},
        {"note": "G4",  "dur": 0.25, "vel": 0.8, "rest": false},
        {"note": "C4",  "dur": 0.25, "vel": 0.0, "rest": true}
    ]
}
```

Fields:
- `note` : note name e.g. "C4", "F#5", "Bb3" (C4 = middle C)
- `dur`  : duration in beats (1.0 = one beat at current BPM)
- `vel`  : velocity 0.0–1.0
- `rest` : if true, silence for this step

---

### 4. Sequencer Pattern Mod  (category = "sequencer")
Add a pattern to the Song Sequencer's pattern library.

```python
META = {"name": "my_pattern", "label": "My Pattern",
        "category": "sequencer", "version": "1.0", "author": "You",
        "desc": "A drum-like pattern"}

PATTERN = {
    "name": "My Pattern",
    "bpm":  120,
    "rows": [
        {"name": "Kick",   "freq": 60,  "beats": [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0]},
        {"name": "Snare",  "freq": 200, "beats": [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0]},
        {"name": "Hi-Hat", "freq": 800, "beats": [1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0]},
    ]
}
```

---

### 5a. Basic Theme Mod  (`mods/themes/basic/mytheme.json`)

Drop a `.json` file into `mods/themes/basic/`. The filename becomes the
theme name (underscores → spaces). Only the keys you include override the
defaults — anything you omit is filled from the base palette.

**Minimum viable basic theme:**
```json
{
    "accent":  "#FF6600",
    "hover":   "#FF8833",
    "glow":    "#FF660033"
}
```

**Full basic theme** (all supported color keys):
```json
{
    "accent":           "#FF6600",
    "hover":            "#FF8833",
    "glow":             "#FF660033",
    "sidebar":          "#0D0907",
    "card":             "#181008",
    "card2":            "#22160A",
    "text":             "#F0E8D8",
    "subtext":          "#908070",
    "border":           "#3A2810",
    "input_bg":         "#120D06",
    "dropdown_bg":      "#22160A",
    "progress":         "#FF6600",
    "switch_active":    "#FF6600",
    "switch_inactive":  "#3A2810",
    "checkbox":         "#FF6600",
    "scrollbar":        "#2A1E0A",
    "scrollbar_button": "#3A2A10",
    "tooltip":          "#080500",
    "rainbow":          false,
    "rgb":              false
}
```

Supported extra flags:
- `"rainbow": true` — accent cycles through the full hue spectrum
- `"rgb": true` — accent/hover/glow cycle through the full RGB spectrum at a faster rate

---

### 5b. Advanced Theme Mod  (`mods/themes/advanced/mytheme.py`)

Drop a `.py` file into `mods/themes/advanced/`. Define a `THEME` dict and
any combination of the three optional hooks.

The engine calls `apply(app)` once when the theme is selected, `remove(app)` 
when it is deselected, and `tick(app)` every ~120ms while it is active.
You do **not** schedule your own `after()` loop — the engine handles timing.

```python
# mods/themes/advanced/lava.py
import colorsys, math

THEME = {
    "name":    "Lava",              # required — display name in the theme picker
    "accent":  "#FF4500",
    "hover":   "#FF6028",
    "glow":    "#FF450055",
    "sidebar": "#100600",
    "card":    "#1A0800",
    "card2":   "#240C00",
    "text":    "#FFD0B0",
    "subtext": "#A06040",
    "border":  "#3A1000",
    "input_bg":"#120600",
    # Any extra keys are stored and accessible as app.col_* after apply()
}

_phase = 0.0

def apply(app):
    \"\"\"Called once when Lava becomes the active theme.\"\"\"
    # Example: set a custom window title badge
    pass

def remove(app):
    \"\"\"Called when user switches away from Lava.\"\"\"
    pass

def tick(app):
    \"\"\"Called every ~120ms while Lava is active. Keep it fast.\"\"\"
    global _phase
    _phase += 0.04
    # Pulse the accent between deep orange and bright yellow-orange
    t = (math.sin(_phase) + 1) / 2
    r = int(0xFF)
    g = int(0x20 + t * 0x60)
    b = 0
    hex_col = f"#{r:02x}{g:02x}{b:02x}"
    app.col_accent = hex_col
    # Recolor key widgets — call app's batch recolor helper
    try:
        app._batch_recolor_accent(hex_col)
    except Exception:
        pass
```

**`app._batch_recolor_accent(color)`** — recolors all registered accent
widgets in one pass with no individual widget traversal.  Use it inside
`tick()` instead of iterating `winfo_children()` yourself.

**Available `app` attributes inside hooks:**
```
app.col_accent, app.col_hover, app.col_glow
app.col_sidebar, app.col_card, app.col_card2
app.col_text, app.col_sub, app.col_border
app.engine.params          # live FX params dict
app.sb                     # SoundboardCore
app.synth                  # RealtimeSynth
app.show_toast(msg, color) # non-blocking toast
app.log.add(msg, level)    # activity log (INFO / WARN / ERROR)
app.SONGS                  # loaded songs dict
```

---

## App API available inside all mods

```python
app.engine.params          # live FX params dict
app.sb                     # SoundboardCore
app.synth                  # RealtimeSynth
app.synth_params           # synth params dict
app.col_accent             # current accent colour string
app.show_toast(msg, color) # non-blocking toast notification
app.log.add(msg, level)    # activity log: level = "INFO"|"WARN"|"ERROR"
app.SONGS                  # currently loaded songs dict
```

---

## Performance Rules

1. **No Python `for` loops over audio samples.** Use numpy vectorised ops.
2. Keep `process()` under ~0.5ms per call on average.
3. Do not allocate large arrays every call — pre-allocate in module scope.
4. Do not call `time.sleep()` or blocking I/O in `process()`.
5. Catch all exceptions inside `process()` — a crash stops your effect silently.
6. **Theme `tick()` must complete in under 2ms.** The 120ms tick budget is
   shared across all active advanced themes.
7. Never call `winfo_children()` recursively inside `tick()` — use
   `app._batch_recolor_accent()` instead.

---

## Example: Full Flanger Mod

```python
import numpy as np

META = {"name": "flanger", "label": "Flanger", "category": "fx",
        "version": "1.0", "author": "SDK Example", "desc": "Classic flanger"}

CONTROLS = [
    {"key": "flanger_rate",  "label": "Rate",  "type": "slider", "min": 0.1, "max": 10.0, "default": 2.0, "unit": "Hz"},
    {"key": "flanger_depth", "label": "Depth", "type": "slider", "min": 0.0, "max": 1.0,  "default": 0.5},
    {"key": "flanger_mix",   "label": "Mix",   "type": "slider", "min": 0.0, "max": 1.0,  "default": 0.4},
]

SR = 44100
_buf = np.zeros((int(SR * 0.05), 2), dtype=np.float32)
_wptr = 0
_phase = 0.0

def process(audio, params):
    global _buf, _wptr, _phase
    rate  = params.get("rate", 2.0)
    depth = params.get("depth", 0.5)
    mix   = params.get("mix", 0.4)
    if mix <= 0:
        return audio
    n = len(audio)
    max_d = int(0.005 * SR)
    lfo = (np.sin(_phase + np.arange(n) * 2 * np.pi * rate / SR) + 1) * 0.5
    delays = (lfo * max_d * depth).astype(int).clip(1, len(_buf) - 1)
    out = np.zeros_like(audio)
    for i in range(n):
        d = delays[i]
        ri = (_wptr - d) % len(_buf)
        _buf[_wptr] = audio[i]
        out[i] = audio[i] * (1 - mix) + _buf[ri] * mix
        _wptr = (_wptr + 1) % len(_buf)
    _phase = (_phase + n * 2 * np.pi * rate / SR) % (2 * np.pi)
    return out
```

Happy modding! Docs: mods/SDK_README.md | Songs: mods/songs/*.json
""").strip()

def _write_sdk_readme():
    path = os.path.join(MODS_FOLDER, "SDK_README.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(SDK_README)

_write_sdk_readme()


# ═════════════════════════════════════════════════════════════════════════════
# DSP — ALL VECTORISED (zero Python sample loops in hot paths)
# ═════════════════════════════════════════════════════════════════════════════
def apply_gain(buf, gain_db):
    if gain_db == 0:
        return buf
    return buf * (10.0 ** (gain_db / 20.0))

def apply_pan(buf, pan):
    if pan == 0.0:
        return buf
    theta = (pan + 1.0) * (np.pi / 4.0)
    out = buf.copy()
    out[:, 0] *= np.cos(theta)
    out[:, 1] *= np.sin(theta)
    return out

def apply_distortion(buf, amount):
    if amount <= 0:
        return buf
    t = 1.0 / (1.0 + amount * 10)
    return np.tanh(buf / t) * t * (1.0 + amount * 0.5)

def apply_bitcrush(buf, bits):
    if bits <= 0:
        return buf
    steps = 2 ** max(1, int(bits))
    return np.round(buf * steps) / steps

def apply_tremolo(buf, rate, depth):
    if depth <= 0:
        return buf
    n = len(buf)
    lfo = 1.0 - depth * 0.5 * (1.0 + np.sin(2.0 * np.pi * rate * np.arange(n) / SR))
    return buf * lfo.reshape(-1, 1)

def apply_distortion_soft(buf, drive):
    """Soft clip — preserves more character than tanh."""
    if drive <= 0:
        return buf
    x = buf * (1.0 + drive * 5.0)
    return x / (1.0 + np.abs(x))


class VectorisedReverb:
    """Schroeder reverb — allpass + comb filters, fully numpy."""
    def __init__(self):
        # Comb filter delays (prime-ish sample counts for diffusion)
        self._comb_d = [int(SR * t) for t in [0.0297, 0.0371, 0.0411, 0.0437]]
        self._comb_buf = [np.zeros((d, CHANNELS), dtype=np.float32) for d in self._comb_d]
        self._comb_ptr = [0] * 4
        # Allpass
        self._ap_d = [int(SR * t) for t in [0.005, 0.0017]]
        self._ap_buf = [np.zeros((d, CHANNELS), dtype=np.float32) for d in self._ap_d]
        self._ap_ptr = [0] * 2

    def process(self, data, mix, decay=0.5):
        if mix <= 0:
            return data
        wet = np.zeros_like(data)
        for i, (d, buf, ptr) in enumerate(zip(self._comb_d, self._comb_buf, self._comb_ptr)):
            n = len(data)
            out_c = np.zeros_like(data)
            # Vectorised comb: each sample reads from circular buffer
            read_idx = (ptr + np.arange(n) - d) % d
            feedback = buf[read_idx] * decay
            write_data = data + feedback
            write_idx = (ptr + np.arange(n)) % d
            buf[write_idx] = write_data
            out_c = feedback
            self._comb_ptr[i] = (ptr + n) % d
            wet += out_c
        wet /= len(self._comb_d)
        # Allpass passes
        for i, (d, buf, ptr) in enumerate(zip(self._ap_d, self._ap_buf, self._ap_ptr)):
            n = len(data)
            read_idx = (ptr + np.arange(n) - d) % d
            delayed = buf[read_idx]
            output = -wet + delayed
            buf[(ptr + np.arange(n)) % d] = wet + delayed * 0.5
            wet = output
            self._ap_ptr[i] = (ptr + n) % d
        return data * (1.0 - mix) + wet * mix


class VectorisedChorus:
    def __init__(self):
        self._maxd = int(SR * 0.04)
        self._buf  = np.zeros((self._maxd, CHANNELS), dtype=np.float32)
        self._wptr = 0
        self._lph  = 0.0

    def process(self, data, rate, depth, mix):
        if mix <= 0:
            return data
        n = len(data)
        lfo = (np.sin(self._lph + np.arange(n) * 2 * np.pi * rate / SR) + 1) * 0.5
        delays = ((0.01 + 0.02 * depth) * SR * lfo).astype(int).clip(1, self._maxd - 1)
        out = np.zeros_like(data)
        wptr = self._wptr
        for i in range(n):  # bounded ~1024, OK
            self._buf[wptr % self._maxd] = data[i]
            ri = (wptr - delays[i]) % self._maxd
            out[i] = data[i] * (1 - mix) + self._buf[ri] * mix
            wptr += 1
        self._wptr = wptr % self._maxd
        self._lph = (self._lph + n * 2 * np.pi * rate / SR) % (2 * np.pi)
        return out


class VectorisedDelay:
    def __init__(self):
        self._maxd = int(SR * 2.0)
        self._buf  = np.zeros((self._maxd, CHANNELS), dtype=np.float32)
        self._wptr = 0

    def process(self, data, t1, t2, fb, mix):
        if mix <= 0:
            return data
        d1 = max(1, int(t1 * SR))
        d2 = max(1, int(t2 * SR))
        n = len(data)
        out = np.zeros_like(data)
        wp = self._wptr
        for i in range(n):  # bounded
            r1 = self._buf[(wp - d1) % self._maxd]
            r2 = self._buf[(wp - d2) % self._maxd]
            pp = np.array([r1[0], r2[1]], dtype=np.float32)
            self._buf[wp % self._maxd] = data[i] + pp * fb
            out[i] = data[i] * (1 - mix) + pp * mix
            wp += 1
        self._wptr = wp % self._maxd
        return out


class VectorisedPhaser:
    def __init__(self):
        self._z = np.zeros((4, CHANNELS), dtype=np.float32)
        self._ph = 0.0

    def process(self, data, rate, depth, mix):
        if mix <= 0:
            return data
        n = len(data)
        lfo = 200 + (np.sin(self._ph + np.arange(n) * 2 * np.pi * rate / SR) + 1) * 0.5 * depth * 4000
        a = (np.tan(np.pi * lfo / SR) - 1) / (np.tan(np.pi * lfo / SR) + 1)
        out = np.zeros_like(data)
        z = self._z.copy()
        for i in range(n):
            ap = a[i] * data[i] + z[0]
            z[0] = data[i] - a[i] * ap
            out[i] = data[i] * (1 - mix) + ap * mix
        self._z = z
        self._ph = (self._ph + n * 2 * np.pi * rate / SR) % (2 * np.pi)
        return out


class PitchShifter:
    """High-quality pitch shifter with formant preservation using phase vocoder."""
    BUF = 8192
    FFT_SIZE = 2048
    HOP_SIZE = 512
    
    def __init__(self):
        self._b = np.zeros((self.BUF, CHANNELS), dtype=np.float32)
        self._w = 0
        self._r = 0.0
        self._phase_accum = np.zeros((self.FFT_SIZE // 2 + 1, CHANNELS), dtype=np.float32)
        self._prev_phase = np.zeros((self.FFT_SIZE // 2 + 1, CHANNELS), dtype=np.float32)
        
    def _stft(self, data):
        """Short-time Fourier transform."""
        n = len(data)
        if n < self.FFT_SIZE:
            padded = np.zeros((self.FFT_SIZE, CHANNELS), dtype=np.float32)
            padded[:n] = data
            data = padded
        
        # Window
        window = np.hanning(self.FFT_SIZE)
        result = []
        for ch in range(CHANNELS):
            fft_data = np.fft.rfft(data[:, ch] * window)
            result.append(fft_data)
        return np.array(result).T  # Shape: (freq_bins, channels)
    
    def _istft(self, stft_data):
        """Inverse short-time Fourier transform."""
        freq_bins, channels = stft_data.shape
        result = np.zeros((self.FFT_SIZE, channels), dtype=np.float32)
        window = np.hanning(self.FFT_SIZE)
        
        for ch in range(channels):
            time_data = np.fft.irfft(stft_data[:, ch])
            result[:, ch] = time_data * window
        
        return result
    
    def process(self, data, semitones):
        if abs(semitones) < 0.05:
            return data
        
        n = len(data)
        rate = 2.0 ** (semitones / 12.0)
        
        # For small pitch shifts, use time-domain method (faster)
        if abs(semitones) < 2:
            return self._time_domain_pitch(data, rate)
        
        # For larger shifts, use phase vocoder (better quality)
        return self._phase_vocoder_pitch(data, rate)
    
    def _time_domain_pitch(self, data, rate):
        """Time-domain pitch shifting with overlap-add."""
        n = len(data)
        end = self._w + n
        if end <= self.BUF:
            self._b[self._w:end] = data
        else:
            f = self.BUF - self._w
            self._b[self._w:] = data[:f]
            self._b[:n - f] = data[f:]
        self._w = (self._w + n) % self.BUF
        
        # Vectorised read with fractional indexing
        read_positions = (self._r + np.arange(n) * rate)
        read_int = read_positions.astype(int) % self.BUF
        read_frac = read_positions - np.floor(read_positions)
        read_next = (read_int + 1) % self.BUF
        out = (self._b[read_int] * (1 - read_frac.reshape(-1, 1)) +
               self._b[read_next] * read_frac.reshape(-1, 1))
        self._r = (self._r + n * rate) % self.BUF
        
        # Resync if drift
        dist = (self._w - self._r) % self.BUF
        if dist < 256 or dist > self.BUF - 256:
            self._r = (self._w - self.BUF // 4) % self.BUF
        
        return out.astype(np.float32)
    
    def _phase_vocoder_pitch(self, data, rate):
        """Phase vocoder-based pitch shifting for high quality."""
        n = len(data)
        
        # Buffer management
        end = self._w + n
        if end <= self.BUF:
            self._b[self._w:end] = data
        else:
            f = self.BUF - self._w
            self._b[self._w:] = data[:f]
            self._b[:n - f] = data[f:]
        self._w = (self._w + n) % self.BUF
        
        # Process in overlapping windows
        output = np.zeros_like(data)
        num_frames = (n - self.FFT_SIZE) // self.HOP_SIZE + 1
        
        for i in range(num_frames):
            start = i * self.HOP_SIZE
            end_frame = start + self.FFT_SIZE
            
            if end_frame > n:
                break
            
            # Get window
            window_data = self._b[(self._w - n + start):(self._w - n + end_frame)]
            if len(window_data) < self.FFT_SIZE:
                continue
            
            # STFT
            stft = self._stft(window_data)
            magnitude = np.abs(stft)
            phase = np.angle(stft)
            
            # Pitch shift by frequency bin interpolation
            shifted_magnitude = np.zeros_like(magnitude)
            num_bins = magnitude.shape[0]
            
            for bin_idx in range(num_bins):
                # Map to new frequency
                new_bin = int(bin_idx * rate)
                if new_bin < num_bins:
                    shifted_magnitude[new_bin] += magnitude[bin_idx]
            
            # Phase reconstruction
            expected_phase_diff = 2 * np.pi * np.arange(num_bins) * self.HOP_SIZE / self.FFT_SIZE
            phase_diff = phase - self._prev_phase
            phase_diff = phase_diff - expected_phase_diff
            phase_diff = np.angle(np.exp(1j * phase_diff))  # Wrap to [-π, π]
            
            self._phase_accum += phase_diff
            reconstructed_phase = self._phase_accum + expected_phase_diff
            
            # Reconstruct STFT
            shifted_stft = shifted_magnitude * np.exp(1j * reconstructed_phase)
            self._prev_phase = phase.copy()
            
            # ISTFT
            time_domain = self._istft(shifted_stft)
            
            # Overlap-add
            output[start:start + self.FFT_SIZE] += time_domain[:self.FFT_SIZE]
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(output))
        if max_val > 0:
            output = output / max_val * 0.9
        
        return output.astype(np.float32)


class SimpleCompressor:
    """Lookahead compressor — vectorised envelope follower."""
    def __init__(self):
        self._env = 0.0

    def process(self, buf, threshold, ratio, attack, release):
        if ratio <= 1:
            return buf
        n = len(buf)
        levels = np.max(np.abs(buf), axis=1)
        ac = np.exp(-1.0 / (max(1e-4, attack) * SR))
        rc = np.exp(-1.0 / (max(1e-4, release) * SR))
        env = self._env
        envs = np.zeros(n)
        for i in range(n):
            coeff = ac if levels[i] > env else rc
            env = env + (levels[i] - env) * (1 - coeff)
            envs[i] = env
        self._env = env
        over = np.maximum(0, envs - threshold)
        gr = np.where(envs > threshold, 1.0 / (1.0 + (ratio - 1) * over / np.maximum(threshold, 1e-6)), 1.0)
        return buf * gr.reshape(-1, 1)


def apply_3band_eq(buf, lo_db, mid_db, hi_db):
    if lo_db == 0 and mid_db == 0 and hi_db == 0:
        return buf
    if HAS_SCIPY and len(buf) > 64:
        try:
            lo_g  = 10 ** (lo_db / 20)
            mid_g = 10 ** (mid_db / 20)
            hi_g  = 10 ** (hi_db / 20)
            b_lo, a_lo = scipy_signal.butter(2, 300 / (SR / 2), btype='low')
            b_hi, a_hi = scipy_signal.butter(2, 3000 / (SR / 2), btype='high')
            lo  = scipy_signal.lfilter(b_lo, a_lo, buf, axis=0) * lo_g
            hi  = scipy_signal.lfilter(b_hi, a_hi, buf, axis=0) * hi_g
            mid = (buf - scipy_signal.lfilter(b_lo, a_lo, buf, axis=0) -
                   scipy_signal.lfilter(b_hi, a_hi, buf, axis=0)) * mid_g
            return lo + mid + hi
        except Exception:
            pass
    return buf


# ═════════════════════════════════════════════════════════════════════════════
# SOUNDBOARD
# ═════════════════════════════════════════════════════════════════════════════
class ActiveSound:
    __slots__ = ("data", "volume", "speed", "loop", "reverse", "finished", "pos", "slot_idx")
    def __init__(self, data, volume, speed, loop, reverse, slot_idx=None):
        self.data     = data
        self.volume   = volume
        self.speed    = speed
        self.loop     = loop
        self.reverse  = reverse
        self.finished = False
        self.pos      = len(data) - 1 if reverse else 0
        self.slot_idx = slot_idx


class SoundboardCore:
    def __init__(self):
        self.slots = [
            {"data": None, "name": "Empty", "path": "", "hotkey": None,
             "color": None, "tags": [], "trim_start": 0.0, "trim_end": 1.0}
            for _ in range(SOUND_LIMIT)
        ]
        self.active_sounds   = []
        self.tts_queue       = []
        self.lock            = threading.Lock()
        self.is_recording    = False
        self.rec_buffer      = []
        self.rec_target      = -1
        self.pending_updates = {}
        self.app_ref         = None
        self.load_config()
        threading.Thread(target=self.auto_load_recordings, daemon=True).start()

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return
        try:
            with open(CONFIG_FILE) as f:
                data = json.load(f)
            for k, v in data.items():
                idx = int(k)
                if idx < len(self.slots):
                    if v.get("path"):
                        self.load_file(idx, v["path"], save=False)
                    if v.get("hotkey"):
                        self.slots[idx]["hotkey"] = v["hotkey"]
                        try:
                            keyboard.add_hotkey(v["hotkey"], lambda i=idx: self.play(i, 1.0, 1.0, False, False))
                        except Exception:
                            pass
                    for k2 in ("color", "tags", "trim_start", "trim_end"):
                        if k2 in v:
                            self.slots[idx][k2] = v[k2]
        except Exception:
            pass

    def save_config(self):
        data = {
            str(i): {"path": s["path"], "hotkey": s["hotkey"], "color": s.get("color"),
                     "tags": s.get("tags", []), "trim_start": s.get("trim_start", 0.0),
                     "trim_end": s.get("trim_end", 1.0)}
            for i, s in enumerate(self.slots) if s["path"] or s["hotkey"]
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def auto_load_recordings(self):
        if not os.path.exists(REC_FOLDER):
            return
        for fn in os.listdir(REC_FOLDER):
            if not fn.lower().endswith((".wav", ".mp3")):
                continue
            full = os.path.join(REC_FOLDER, fn)
            if any(s["path"] == full for s in self.slots):
                continue
            for i, s in enumerate(self.slots):
                if s["data"] is None:
                    self.load_file(i, full, save=False)
                    break

    def load_file(self, idx, filepath, save=True):
        if not os.path.exists(filepath):
            return False
        try:
            data, sr = sf.read(filepath, dtype="float32")
            if data.ndim == 1:
                data = np.column_stack((data, data))
            elif data.shape[1] > 2:
                data = data[:, :2]
            if sr != SR:
                fac = SR / sr
                n_out = int(len(data) * fac)
                idx_in = np.linspace(0, len(data) - 1, n_out)
                data = np.array([np.interp(idx_in, np.arange(len(c)), c) for c in data.T]).T.astype(np.float32)
            with self.lock:
                self.slots[idx].update({"data": data, "path": filepath, "name": os.path.basename(filepath)[:20]})
            if save:
                self.save_config()
            return True
        except Exception:
            return False

    def save_recording(self, idx):
        if not self.rec_buffer:
            return
        data = np.concatenate(self.rec_buffer)
        path = os.path.join(REC_FOLDER, f"rec_{idx}_{int(time.time())}.wav")
        sf.write(path, data, SR)
        self.load_file(idx, path)

    def play(self, idx, speed, vol, loop, reverse):
        with self.lock:
            s = self.slots[idx]
            if s["data"] is not None:
                data = s["data"]
                ts, te = s.get("trim_start", 0.0), s.get("trim_end", 1.0)
                if ts > 0 or te < 1.0:
                    n = len(data)
                    data = data[int(ts * n):max(1, int(te * n))]
                self.active_sounds.append(ActiveSound(data, vol, speed, loop, reverse, slot_idx=idx))

    def stop_slot(self, idx):
        with self.lock:
            self.active_sounds = [s for s in self.active_sounds if s.slot_idx != idx]

    def stop_all(self):
        with self.lock:
            self.active_sounds.clear()
            self.tts_queue.clear()

    def update_playbars(self):
        if self.pending_updates:
            with self.lock:
                updates = dict(self.pending_updates)
                self.pending_updates.clear()
            for si, prog in updates.items():
                if si < len(self.slots):
                    s = self.slots[si]
                    if "progress_var" in s:
                        try:
                            s["progress_var"].set(prog)
                        except Exception:
                            pass
        if self.app_ref:
            self.app_ref.after(50, self.update_playbars)

    def get_audio_mix(self, frame_size, include_sb=True, include_tts=True):
        out = np.zeros((frame_size, CHANNELS), dtype=np.float32)
        try:
            with self.lock:
                self.active_sounds = [s for s in self.active_sounds if not s.finished]
                self.tts_queue     = [s for s in self.tts_queue     if not s.finished]
                targets = []
                if include_sb:  targets.extend(self.active_sounds)
                if include_tts: targets.extend(self.tts_queue)
                for s in targets:
                    try:
                        needed = int(frame_size * s.speed)
                        chunk  = np.zeros((needed, CHANNELS), dtype=np.float32)
                        if not s.reverse:
                            rem = len(s.data) - s.pos
                            if rem >= needed:
                                chunk = s.data[s.pos:s.pos + needed].copy()
                                s.pos += needed
                            else:
                                chunk[:rem] = s.data[s.pos:]
                                if s.loop:
                                    fade = min(256, rem)
                                    chunk[:fade] *= np.linspace(1, 0, fade).reshape(-1, 1)
                                    lc = s.data[:needed - rem]
                                    lc = lc.copy()
                                    lc[:min(fade, len(lc))] *= np.linspace(0, 1, min(fade, len(lc))).reshape(-1, 1)
                                    chunk[rem:rem + len(lc)] = lc
                                    s.pos = needed - rem
                                else:
                                    s.finished = True
                        else:
                            start = s.pos - needed
                            if start >= 0:
                                chunk = s.data[start:s.pos][::-1].copy()
                                s.pos -= needed
                            else:
                                avail = s.pos
                                chunk[:avail] = s.data[:s.pos][::-1]
                                if s.loop:
                                    s.pos = len(s.data)
                                    extra = needed - avail
                                    chunk[avail:avail + extra] = s.data[max(0, s.pos - extra):][::-1]
                                    s.pos -= extra
                                else:
                                    s.finished = True
                        if len(chunk) != frame_size and len(chunk) > 0:
                            chunk = np.array(
                                [np.interp(np.linspace(0, len(c), frame_size), np.arange(len(c)), c)
                                 for c in chunk.T]).T
                        if s.speed < 1.0:
                            chunk *= min(3.0, 1.0 / max(0.01, s.speed))
                        if np.all(np.isfinite(chunk)):
                            out += chunk * s.volume
                        if s.slot_idx is not None and s.slot_idx < len(self.slots):
                            sl = self.slots[s.slot_idx]
                            if "progress_var" in sl and sl["data"] is not None:
                                self.pending_updates[s.slot_idx] = (s.pos / len(sl["data"])) * 100
                    except Exception:
                        continue
        except Exception:
            pass
        return out


# ═════════════════════════════════════════════════════════════════════════════
# TTS — LIVE (no temp files, injected directly as audio)
# ═════════════════════════════════════════════════════════════════════════════
class LiveTTS:
    """Renders TTS audio in a background thread and pushes it to the SB tts_queue."""
    def __init__(self, sb_core: SoundboardCore):
        self.sb       = sb_core
        self._q       = queue.Queue()
        self._running = True
        self._thread  = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()
        self.rate     = 150
        self.voice_id = None  # None = system default

    def speak(self, text: str):
        if text.strip():
            self._q.put(text)

    def stop(self):
        self._running = False

    def _worker(self):
        if not HAS_TTS:
            return
        while self._running:
            try:
                text = self._q.get(timeout=0.5)
            except queue.Empty:
                continue
            try:
                self._render_and_inject(text)
            except Exception:
                pass

    def _render_and_inject(self, text: str):
        """Render TTS to PCM via sounddevice capture trick or pyttsx3 wav bytes."""
        import io as _io
        import tempfile, wave

        try:
            eng = pyttsx3.init()
            eng.setProperty("rate", self.rate)
            if self.voice_id:
                eng.setProperty("voice", self.voice_id)

            # Render to a temp wav in memory via a temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name

            eng.save_to_file(text, tmp_path)
            eng.runAndWait()

            if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
                data, sr = sf.read(tmp_path, dtype="float32")
                os.unlink(tmp_path)
                if data.ndim == 1:
                    data = np.column_stack((data, data))
                if sr != SR:
                    n_out = int(len(data) * SR / sr)
                    ix = np.linspace(0, len(data) - 1, n_out)
                    data = np.array([np.interp(ix, np.arange(len(c)), c) for c in data.T]).T.astype(np.float32)
                with self.sb.lock:
                    self.sb.tts_queue.append(ActiveSound(data, 1.0, 1.0, False, False))
            else:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
        except Exception:
            pass

    def get_voices(self):
        if not HAS_TTS:
            return []
        try:
            eng = pyttsx3.init()
            vs  = eng.getProperty("voices")
            eng.stop()
            return vs
        except Exception:
            return []


# ═════════════════════════════════════════════════════════════════════════════
# SYNTHESIZER — with portamento, unison, filter
# ═════════════════════════════════════════════════════════════════════════════
class RealtimeSynth:
    UNISON_MAX = 7

    def __init__(self):
        self.running        = False
        self.env_time       = 0.0
        self.env_stage      = 0
        self.release_lvl    = 0.0
        self._phases        = np.zeros(self.UNISON_MAX)
        self._phase2        = 0.0
        self._cur_freq      = 440.0   # portamento current
        self._filter_state  = np.zeros((2, CHANNELS), dtype=np.float32)
        # Song/arp state
        self.song_steps     = []
        self.song_step_idx  = 0
        self.song_time_acc  = 0.0
        self.song_note_freq = 0.0
        self.song_note_vel  = 1.0
        self.song_note_on   = False
        self.song_loop      = True
        self.song_active    = False

    def _envelope(self, p, dt):
        a, d, s, r = p.get("env_a", 0.05), p.get("env_d", 0.2), p.get("env_s", 0.7), p.get("env_r", 0.3)
        if self.env_stage == 0:
            return 0.0
        self.env_time += dt
        if self.env_stage == 1:
            if self.env_time >= a:
                self.env_stage, self.env_time = 2, 0.0
                return 1.0
            return self.env_time / max(a, 1e-5)
        if self.env_stage == 2:
            if self.env_time >= d:
                self.env_stage, self.env_time = 3, 0.0
                return s
            return 1.0 - (self.env_time / max(d, 1e-5)) * (1.0 - s)
        if self.env_stage == 3:
            return p.get("env_s", 0.7)
        if self.env_stage == 4:
            lvl = self.release_lvl * max(0.0, 1.0 - self.env_time / max(r, 1e-5))
            if self.env_time >= r:
                self.env_stage = 0
                self.running   = False
            return lvl
        return 0.0

    def _wave(self, phases, wave_type):
        if wave_type == "Sine":     return np.sin(phases)
        if wave_type == "Square":   return np.sign(np.sin(phases))
        if wave_type == "Saw":      return 2 * (phases / (2*np.pi) - np.floor(phases/(2*np.pi) + 0.5))
        if wave_type == "Triangle": return 2*np.abs(2*(phases/(2*np.pi) - np.floor(phases/(2*np.pi)+0.5))) - 1
        if wave_type == "Pulse":    return ((phases % (2*np.pi)) / (2*np.pi) < 0.3).astype(float)*2 - 1
        if wave_type == "SuperSaw":
            saws = [2*(p/(2*np.pi)-np.floor(p/(2*np.pi)+0.5)) for p in [phases*0.99, phases, phases*1.01]]
            return sum(saws) / 3
        return np.sin(phases)

    def _advance_song(self, frames, params):
        """Advance song/arp sequencer, return (freq, vel, note_on)."""
        if not self.song_steps:
            return self.song_note_freq, self.song_note_vel, self.song_note_on
        bpm = params.get("arp_bpm", 120.0)
        beat_secs = 60.0 / bpm
        dt = frames / SR
        self.song_time_acc += dt
        step = self.song_steps[self.song_step_idx % len(self.song_steps)]
        step_dur = float(step.get("dur", 0.25)) * beat_secs
        if self.song_time_acc >= step_dur:
            self.song_time_acc -= step_dur
            self.song_step_idx += 1
            if self.song_step_idx >= len(self.song_steps):
                if self.song_loop:
                    self.song_step_idx = 0
                else:
                    self.song_active = False
                    return self.song_note_freq, 0.0, False
            step = self.song_steps[self.song_step_idx % len(self.song_steps)]
            if step.get("rest", False):
                self.song_note_on  = False
                self.song_note_vel = 0.0
            else:
                self.song_note_freq = note_name_to_freq(step.get("note", "C4"))
                self.song_note_vel  = float(step.get("vel", 1.0))
                self.song_note_on   = True
        return self.song_note_freq, self.song_note_vel, self.song_note_on

    def load_song(self, song_def: dict):
        self.song_steps    = song_def.get("steps", [])
        self.song_loop     = song_def.get("loop", True)
        self.song_step_idx = 0
        self.song_time_acc = 0.0
        self.song_note_on  = False
        self.song_active   = bool(self.song_steps)

    def process(self, frames, params):
        if not self.running:
            return np.zeros((frames, CHANNELS), dtype=np.float32)

        # Portamento
        target_freq = params.get("freq", 440.0) * (2 ** (params.get("detune", 0) / 1200))
        porta = params.get("portamento", 0.0)
        if porta > 0 and self._cur_freq != target_freq:
            k = np.exp(-1.0 / max(1e-4, porta * SR / frames))
            self._cur_freq = self._cur_freq * k + target_freq * (1 - k)
        else:
            self._cur_freq = target_freq

        freq = self._cur_freq

        # Song/arp sequencer
        if self.song_active and self.song_steps:
            sf_freq, sf_vel, sf_on = self._advance_song(frames, params)
            if sf_on:
                freq = sf_freq
            else:
                freq = 0.0  # rest
        else:
            # Simple arp
            arp_on = params.get("arp_on", False)
            if arp_on:
                freq *= (2 ** (params.get("_arp_offset", 0) / 12.0))

        # LFO
        lfo_rate  = params.get("mod_lfo_rate", 5)
        lfo_depth = params.get("mod_lfo_depth", 0)
        lfo = np.sin(2 * np.pi * lfo_rate * time.time()) * lfo_depth
        if params.get("mod_target", "None") == "Pitch":
            freq *= 1.0 + lfo * 0.1

        # Unison
        u_count  = max(1, int(params.get("unison", 1)))
        u_detune = params.get("unison_detune", 10)  # cents spread total
        offsets  = np.linspace(-u_detune / 2, u_detune / 2, u_count) if u_count > 1 else [0.0]

        wave_type = params.get("wave", "Sine")
        osc_sum = np.zeros(frames)
        for ui, off in enumerate(offsets):
            f = freq * 2 ** (off / 1200) if freq > 0 else 0
            pinc = 2 * np.pi * f / SR if f > 0 else 0
            phases = self._phases[ui] + np.arange(frames) * pinc
            self._phases[ui] = (self._phases[ui] + frames * pinc) % (2 * np.pi)
            # FM
            fm_depth = params.get("fm_depth", 0)
            if fm_depth > 0:
                fm_inc = 2 * np.pi * params.get("fm_freq", 440) / SR
                fm_ph  = self._phases[ui] + np.arange(frames) * fm_inc
                phases += np.sin(fm_ph) * fm_depth
            osc_sum += self._wave(phases, wave_type)
        audio = osc_sum / u_count

        # OSC2
        osc2_mix = params.get("osc2_mix", 0)
        if osc2_mix > 0:
            f2   = freq * 2 ** (params.get("osc2_detune", 7) / 1200)
            inc2 = 2 * np.pi * f2 / SR
            ph2  = self._phase2 + np.arange(frames) * inc2
            self._phase2 = (self._phase2 + frames * inc2) % (2 * np.pi)
            audio = audio * (1 - osc2_mix) + self._wave(ph2, params.get("osc2_wave", "Saw")) * osc2_mix

        # Sub + noise
        sub_mix = params.get("sub_mix", 0)
        if sub_mix > 0:
            audio = audio * (1 - sub_mix) + np.sin(
                self._phases[0] * 0.5 + np.arange(frames) * np.pi * freq / SR) * sub_mix

        noise_mix = params.get("noise_mix", 0)
        if noise_mix > 0:
            audio = audio * (1 - noise_mix) + np.random.uniform(-1, 1, frames) * noise_mix

        # Envelope
        env = self._envelope(params, frames / SR)
        audio *= env
        if params.get("mod_target") == "Amp":
            audio *= 1.0 + lfo

        # Simple one-pole lowpass filter
        fcut = params.get("filter_cutoff", 1.0)
        if fcut < 1.0:
            fc = max(0.001, fcut) * 0.499
            alpha = 1.0 - np.exp(-2.0 * np.pi * fc)
            for i in range(frames):  # filter needs sequential state
                self._filter_state[0, 0] += alpha * (audio[i] - self._filter_state[0, 0])
                audio[i] = self._filter_state[0, 0]

        # Synth FX
        dist = params.get("fx_dist", 0)
        if dist > 0:
            audio = np.tanh(audio * (1 + dist)) / (1 + dist * 0.1)

        bits = params.get("fx_bitcrush", 0)
        if bits > 0:
            steps = 2 ** int(max(1, bits))
            audio = np.round(audio * steps) / steps

        audio *= params.get("master_vol", 0.5)
        stereo = np.column_stack((audio, audio))
        stereo = apply_pan(stereo, params.get("mod_pan", 0))
        return stereo.astype(np.float32)


# ═════════════════════════════════════════════════════════════════════════════
# AUDIO ENGINE — with CPU guard
# ═════════════════════════════════════════════════════════════════════════════
class AudioEngine:
    def __init__(self, sb, synth, synth_params):
        self.sb           = sb
        self.synth        = synth
        self.synth_params = synth_params
        self.monitoring   = False
        self.vis_data     = np.zeros(1024)
        self.vu_peak_l    = 0.0
        self.vu_peak_r    = 0.0
        # DSP objects
        self.shifter   = PitchShifter()
        self.reverb    = VectorisedReverb()
        self.chorus    = VectorisedChorus()
        self.delay     = VectorisedDelay()
        self.phaser    = VectorisedPhaser()
        self.comp      = SimpleCompressor()
        self.mods      = []
        # CPU guard
        self._cb_times    = []
        self._overload    = False
        self._overload_cb = None  # callable(bool) for UI feedback
        self.params = {
            "gain": 0.0, "pitch": 0.0, "pan": 0.0,
            "master_out_gain": 0.0, "noise_gate": 0.0,
            "sb_speed": 1.0, "sb_vol": 1.0,
            "sb_loop": False, "sb_reverse": False, "sb_reverb": 0.0,
            "distortion": 0.0,
            "chorus_rate": 1.0, "chorus_depth": 0.5, "chorus_mix": 0.0,
            "phaser_rate": 1.0, "phaser_depth": 0.5, "phaser_mix": 0.0,
            "tremolo_rate": 5.0, "tremolo_depth": 0.0,
            "delay_time": 0.3, "delay2_time": 0.6,
            "delay_feedback": 0.3, "delay_mix": 0.0,
            "reverb_mix": 0.0, "reverb_decay": 0.5,
            "comp_threshold": 0.7, "comp_ratio": 4.0,
            "comp_attack": 0.01, "comp_release": 0.1,
            "eq_lo": 0.0, "eq_mid": 0.0, "eq_hi": 0.0,
            "bitcrush": 0.0,
            "loud_mic_bypass": False,
            "limiter_threshold": 0.95, "pre_limiter_gain": 1.0,
            "post_limiter_gain": 1.0, "adaptive_headroom": 0.05,
            # ── Experimental features (toggled via Settings → Experimental) ──
            "exp_echo_enabled":       False,  # desktop echo
            "exp_echo_vol":           0.85,
            "exp_echo_mix":           1.0,
            "exp_noise_suppress":     False,  # spectral noise suppression
            "exp_ns_strength":        0.6,
            "exp_transient_enhance":  False,  # transient sharpener
            "exp_transient_amount":   0.5,
            "exp_stereo_width":       False,  # mid-side stereo widener
            "exp_stereo_width_amt":   0.5,
            "exp_voice_morph":        False,  # crude formant-shift voice morpher
            "exp_morph_gender":       0.0,    # -1 = more masculine, +1 = more feminine
            "exp_exciter":            False,  # harmonic exciter
            "exp_exciter_amount":     0.4,
            "exp_gate_duck":          False,  # auto-ducker: sb audio ducks mic
            "exp_gate_duck_depth":    0.7,
            "exp_gate_duck_speed":    0.05,
        }
        # loopback capture buffer for desktop echo
        self._lb_buf  = np.zeros((1024, 2), dtype=np.float32)
        self._lb_lock = threading.Lock()
        self._duck_gain = 1.0   # state for gate_duck

    def _budget_ms(self, frames):
        """Return allowed ms per callback (80% of block duration)."""
        return (frames / SR) * 1000 * 0.8

    def process(self, indata):
        t0 = time.perf_counter()
        x = indata.astype(np.float32)
        if x.shape[1] == 1:
            x = np.column_stack((x, x))

        if self.sb.is_recording:
            self.sb.rec_buffer.append(x.copy())

        # Gate (vectorised)
        gate = self.params["noise_gate"]
        if gate > 0:
            amps = np.abs(x)
            mask = amps < gate
            x = np.where(mask, x * (amps / np.maximum(gate, 1e-9)), x)

        # TTS + Synth
        x = x + self.sb.get_audio_mix(len(x), include_sb=False, include_tts=True)
        if self.synth.running:
            x = x + self.synth.process(len(x), self.synth_params)

        x = apply_gain(x, self.params["gain"])

        # EQ
        x = apply_3band_eq(x, self.params["eq_lo"], self.params["eq_mid"], self.params["eq_hi"])

        # Dynamics
        if self.params["comp_ratio"] > 1:
            x = self.comp.process(x, self.params["comp_threshold"], self.params["comp_ratio"],
                                   self.params["comp_attack"], self.params["comp_release"])

        # Pitch shift
        x = self.shifter.process(x, self.params["pitch"])

        # FX chain — check budget between each and skip if overloaded
        budget = self._budget_ms(len(x))
        elapsed = (time.perf_counter() - t0) * 1000

        if self.params["distortion"] > 0:
            x = apply_distortion(x, self.params["distortion"])
        if self.params["bitcrush"] > 0:
            x = apply_bitcrush(x, self.params["bitcrush"])
        if self.params["tremolo_depth"] > 0:
            x = apply_tremolo(x, self.params["tremolo_rate"], self.params["tremolo_depth"])

        elapsed = (time.perf_counter() - t0) * 1000
        if elapsed < budget * 0.6:
            if self.params["chorus_mix"] > 0:
                x = self.chorus.process(x, self.params["chorus_rate"], self.params["chorus_depth"], self.params["chorus_mix"])
            if self.params["phaser_mix"] > 0:
                x = self.phaser.process(x, self.params["phaser_rate"], self.params["phaser_depth"], self.params["phaser_mix"])

        elapsed = (time.perf_counter() - t0) * 1000
        if elapsed < budget * 0.75:
            if self.params["delay_mix"] > 0:
                x = self.delay.process(x, self.params["delay_time"], self.params["delay2_time"],
                                       self.params["delay_feedback"], self.params["delay_mix"])

        # Limiter pre
        if self.params["loud_mic_bypass"]:
            h = self.params["adaptive_headroom"]
            th = self.params["limiter_threshold"]
            x = x * self.params["pre_limiter_gain"]
            x = np.tanh(x * 0.8 / (th + h)) * (th + h)
            x = x * self.params["post_limiter_gain"]

        # Mod plugins
        for mod in self.mods:
            if hasattr(mod, "process"):
                try:
                    pfx = mod.META["name"] + "_"
                    p = {k[len(pfx):]: v for k, v in self.params.items() if k.startswith(pfx)}
                    res = mod.process(x, p)
                    if res is not None and res.shape == x.shape and np.all(np.isfinite(res)):
                        x = res
                except Exception:
                    pass
            # Instrument mods
            if hasattr(mod, "get_audio") and self.synth.running:
                try:
                    ia = mod.get_audio(len(x), self.synth_params)
                    if ia is not None and ia.shape == x.shape:
                        x = x + ia
                except Exception:
                    pass

        # ── EXPERIMENTAL FEATURES ─────────────────────────────────────────────
        # Desktop Echo: mix loopback capture into the mic output
        if self.params.get("exp_echo_enabled"):
            with self._lb_lock:
                lb = self._lb_buf
            n     = len(x)
            chunk = lb[:n] if lb.shape[0] >= n else np.pad(lb, ((0, n - lb.shape[0]), (0, 0)))
            vol   = float(self.params.get("exp_echo_vol", 0.85))
            mix   = float(self.params.get("exp_echo_mix", 1.0))
            x     = x * (1.0 - mix) + chunk * vol * mix

        # Spectral Noise Suppression: subtract estimated noise floor per-channel
        if self.params.get("exp_noise_suppress"):
            strength = float(self.params.get("exp_ns_strength", 0.6))
            for ch in range(x.shape[1]):
                spec = np.fft.rfft(x[:, ch])
                mag  = np.abs(spec)
                noise_floor = np.percentile(mag, 20) * strength
                gain_curve  = np.maximum(0.0, (mag - noise_floor) / np.maximum(mag, 1e-9))
                spec        = spec * gain_curve
                x[:, ch]    = np.fft.irfft(spec, n=len(x[:, ch]))

        # Transient Enhancer: boost onsets via high-pass envelope
        if self.params.get("exp_transient_enhance"):
            amt  = float(self.params.get("exp_transient_amount", 0.5))
            diff = np.diff(np.abs(x), axis=0, prepend=np.abs(x[:1]))
            pos  = np.maximum(diff, 0)
            x    = x + pos * amt * 3.0

        # Stereo Widener (mid-side)
        if self.params.get("exp_stereo_width"):
            w   = float(self.params.get("exp_stereo_width_amt", 0.5))
            mid = (x[:, 0] + x[:, 1]) * 0.5
            sid = (x[:, 0] - x[:, 1]) * 0.5
            sid_w = sid * (1.0 + w * 2.0)
            x = np.column_stack((mid + sid_w, mid - sid_w))

        # Voice Morpher (crude formant shift via resampling trick)
        if self.params.get("exp_voice_morph"):
            gender = float(self.params.get("exp_morph_gender", 0.0))
            factor = 1.0 + gender * 0.25
            for ch in range(x.shape[1]):
                n_out = max(1, int(len(x[:, ch]) * factor))
                stretched = np.interp(
                    np.linspace(0, len(x[:, ch]) - 1, n_out),
                    np.arange(len(x[:, ch])),
                    x[:, ch]
                )
                if len(stretched) >= len(x[:, ch]):
                    x[:, ch] = stretched[:len(x[:, ch])]
                else:
                    x[:len(stretched), ch] = stretched
                    x[len(stretched):, ch] = 0.0

        # Harmonic Exciter: add soft-clipped harmonics to highs
        if self.params.get("exp_exciter"):
            amt = float(self.params.get("exp_exciter_amount", 0.4))
            for ch in range(x.shape[1]):
                spec  = np.fft.rfft(x[:, ch])
                freqs = np.fft.rfftfreq(len(x[:, ch]), 1.0 / SR)
                hi    = freqs > 4000
                spec_hi          = spec.copy()
                spec_hi[~hi]     = 0
                harmonics        = np.fft.irfft(spec_hi, n=len(x[:, ch]))
                harmonics        = np.tanh(harmonics * 3.0) * amt * 0.3
                x[:, ch]         = x[:, ch] + harmonics

        # Auto-Ducker: attenuate mic when soundboard is loud
        if self.params.get("exp_gate_duck"):
            sb_level = float(np.max(np.abs(
                self.sb.get_audio_mix(len(x), include_sb=True, include_tts=False)
            )))
            depth = float(self.params.get("exp_gate_duck_depth", 0.7))
            speed = float(self.params.get("exp_gate_duck_speed", 0.05))
            target = max(0.0, 1.0 - sb_level * depth * 6)
            self._duck_gain += (target - self._duck_gain) * speed
            x = x * max(0.0, self._duck_gain)

        # SB mix
        sb_audio = self.sb.get_audio_mix(len(x), include_sb=True, include_tts=False)
        if self.params["sb_reverb"] > 0:
            sb_audio = self.reverb.process(sb_audio, self.params["sb_reverb"] * 0.5)
        x = x + sb_audio * self.params["sb_vol"]

        x = apply_pan(x, self.params["pan"])

        elapsed = (time.perf_counter() - t0) * 1000
        if elapsed < budget * 0.85:
            if self.params["reverb_mix"] > 0:
                x = self.reverb.process(x, self.params["reverb_mix"], self.params["reverb_decay"])

        x = apply_gain(x, self.params["master_out_gain"])
        if self.params["loud_mic_bypass"]:
            ceiling = self.params["limiter_threshold"] - self.params["adaptive_headroom"]
            x = np.tanh(x / max(0.001, ceiling)) * ceiling

        x = np.clip(x, -1.0, 1.0)

        # VU + vis
        self.vu_peak_l = float(np.max(np.abs(x[:, 0])))
        self.vu_peak_r = float(np.max(np.abs(x[:, 1])))
        self.vis_data  = x[:, 0].copy()

        # CPU guard bookkeeping
        elapsed = (time.perf_counter() - t0) * 1000
        self._cb_times.append(elapsed)
        if len(self._cb_times) > 20:
            self._cb_times.pop(0)
        was_overload = self._overload
        self._overload = (len(self._cb_times) == 20 and
                          sum(self._cb_times[-5:]) / 5 > budget * 0.9)
        if self._overload != was_overload and self._overload_cb:
            try:
                self._overload_cb(self._overload)
            except Exception:
                pass

        return x


# ═════════════════════════════════════════════════════════════════════════════
# MOD LOADER
# ═════════════════════════════════════════════════════════════════════════════
class ModLoader:
    def __init__(self, app=None):
        self.app    = app
        self.states = self._load()
        self.loaded = {}

    def _load(self):
        if os.path.exists(MOD_CONFIG):
            try:
                with open(MOD_CONFIG) as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def save(self):
        with open(MOD_CONFIG, "w") as f:
            json.dump(self.states, f)

    def load_mods(self):
        lst = []
        for fn in os.listdir(MODS_FOLDER):
            if not fn.endswith(".py"):
                continue
            if fn not in self.states:
                self.states[fn] = True
            if not self.states[fn]:
                continue
            try:
                spec = importlib.util.spec_from_file_location(fn[:-3], os.path.join(MODS_FOLDER, fn))
                mod  = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "META"):
                    lst.append(mod)
                    self.loaded[mod.META["name"]] = mod
                    for hook in ("init", "init_ui"):
                        if hasattr(mod, hook) and self.app:
                            try:
                                getattr(mod, hook)(self.app)
                            except Exception:
                                pass
                            break
            except Exception as e:
                print(f"[Mod] {fn}: {e}")
        self.save()
        return lst


# ═════════════════════════════════════════════════════════════════════════════
# PRESETS
# ═════════════════════════════════════════════════════════════════════════════
CAPTURE_KEYS = [
    "gain","pitch","pan","distortion","chorus_mix","chorus_rate","chorus_depth",
    "delay_mix","delay_time","delay_feedback","reverb_mix","reverb_decay",
    "noise_gate","comp_threshold","comp_ratio","comp_attack","comp_release",
    "eq_lo","eq_mid","eq_hi","master_out_gain","phaser_mix","tremolo_depth",
    "bitcrush","sb_vol","sb_speed","sb_reverb",
]

class PresetsManager:
    def __init__(self):
        self.presets = dict(DEFAULT_PRESETS)
        if os.path.exists(PRESETS_FILE):
            try:
                with open(PRESETS_FILE) as f:
                    self.presets.update(json.load(f))
            except Exception:
                pass

    def save(self):
        user = {k: v for k, v in self.presets.items() if k not in DEFAULT_PRESETS}
        with open(PRESETS_FILE, "w") as f:
            json.dump(user, f, indent=2)

    def apply(self, name, params):
        if name in self.presets:
            params.update(self.presets[name])
            return True
        return False

    def capture(self, name, params):
        self.presets[name] = {k: params[k] for k in CAPTURE_KEYS if k in params}
        self.save()

    def delete(self, name):
        if name not in DEFAULT_PRESETS:
            self.presets.pop(name, None)
            self.save()
            return True
        return False


# ═════════════════════════════════════════════════════════════════════════════
# ACTIVITY LOG
# ═════════════════════════════════════════════════════════════════════════════
class ActivityLog:
    def __init__(self):
        self.entries = []
        self._cbs    = []

    def add(self, msg, level="INFO"):
        e = f"[{time.strftime('%H:%M:%S')}] [{level}] {msg}"
        self.entries.append(e)
        if len(self.entries) > 300:
            self.entries.pop(0)
        for cb in self._cbs:
            try:
                cb(e)
            except Exception:
                pass

    def on_entry(self, cb):
        self._cbs.append(cb)


# ═════════════════════════════════════════════════════════════════════════════
# SONG SEQUENCER
# ═════════════════════════════════════════════════════════════════════════════
class SongSequencer:
    """Step sequencer that drives the synth's song playback."""
    def __init__(self, synth: RealtimeSynth, synth_params: dict):
        self.synth        = synth
        self.synth_params = synth_params
        self.current_song = None
        self.songs        = load_songs()

    def reload_songs(self):
        self.songs = load_songs()

    def play_song(self, name: str):
        if name not in self.songs:
            return False
        self.current_song = name
        self.synth.load_song(self.songs[name])
        if not self.synth.running:
            self.synth.env_stage = 1
            self.synth.env_time  = 0.0
            self.synth.running   = True
        return True

    def stop(self):
        self.synth.song_active = False
        self.synth.song_steps  = []


# ═════════════════════════════════════════════════════════════════════════════
# LOADING SCREEN
# ═════════════════════════════════════════════════════════════════════════════
LOADING_TIPS = [
    "Tip: Drop a .py file into mods/ and V LAB loads it automatically — no restart needed for most mod types.",
    "Tip: Open the Theme Creator from Settings to build a full custom theme with live preview.",
    "Tip: Try the Space Nebula theme for an animated purple/blue starfield background.",
    "Tip: RGB Pulse cycles every accent color through the full spectrum in real time.",
    "Tip: Gradients support up to 5 color stops — linear, radial, or conic.",
    "Tip: Use the SDK Readme button to see worked examples for every mod type.",
    "Tip: FX mods should avoid Python for-loops over audio — use numpy ops for speed.",
    "Tip: You can export and share your custom theme as a single JSON file.",
    "Tip: Song mods are just JSON — drop one in mods/songs/ and it shows up in the sequencer.",
    "Tip: Press the Mods tab to enable/disable any installed mod without deleting it.",
    "Tip: Theme presets in the Theme Creator are a fast starting point — tweak from there.",
    "Tip: Animated gradients support shift, pulse, reverse, and hue-rotate modes.",
]

class LoadingScreen(ctk.CTkToplevel):
    """Rebuilt loading screen: animated gradient backdrop, twinkling stars,
    rotating tips, and a smoother progress bar."""

    WIDTH, HEIGHT = 560, 360

    def __init__(self):
        super().__init__()
        self.title("Loading V LAB...")
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.WIDTH) // 2
        y = (screen_height - self.HEIGHT) // 2
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")
        self.configure(fg_color="#05040F")

        # ── Animated background canvas (gradient + stars) ──────────────────
        self.bg_canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT,
                                    highlightthickness=0, bd=0)
        self.bg_canvas.place(x=0, y=0)

        self._stars = []
        self._grad_phase = 0.0
        self._anim_job = None
        self._build_starfield()
        self._draw_background()

        # ── Foreground content (on top of canvas) ──────────────────────────
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center", relwidth=1.0, relheight=1.0)

        ctk.CTkLabel(content, text="V LAB", font=("Consolas", 36, "bold"),
                     text_color="#B388FF").pack(pady=(46, 2))
        ctk.CTkLabel(content, text=f"{VERSION}", font=("Consolas", 12),
                     text_color="#9C90C4").pack(pady=(0, 28))

        self.progress_bar = ctk.CTkProgressBar(content, width=440, height=12,
                                                progress_color="#8A5CFF",
                                                fg_color="#1C1740",
                                                corner_radius=6)
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(content, text="Initializing...",
                                          font=("Consolas", 10),
                                          text_color="#B388FF")
        self.status_label.pack(pady=(0, 26))

        # ── Tip box ──────────────────────────────────────────────────────
        tip_frame = ctk.CTkFrame(content, fg_color="#13102B", corner_radius=10)
        tip_frame.pack(side="bottom", fill="x", padx=24, pady=24)
        ctk.CTkLabel(tip_frame, text="💡", font=("Consolas", 14)).pack(side="left", padx=(14, 6), pady=10)
        self.tip_label = ctk.CTkLabel(tip_frame, text="", font=("Consolas", 10),
                                       text_color="#E6E0FF", wraplength=460,
                                       justify="left", anchor="w")
        self.tip_label.pack(side="left", fill="x", expand=True, padx=(0, 14), pady=10)

        self._tip_pool = LOADING_TIPS[:]
        random.shuffle(self._tip_pool)
        self._tip_index = 0
        self._rotate_tip()
        self._tip_job = self.after(3200, self._tip_loop)

        self._animate_background()

    # -- starfield -----------------------------------------------------
    def _build_starfield(self, count=90):
        self._stars = []
        for _ in range(count):
            self._stars.append({
                "x": random.uniform(0, self.WIDTH),
                "y": random.uniform(0, self.HEIGHT),
                "r": random.uniform(0.6, 1.8),
                "phase": random.uniform(0, 6.28318),
                "speed": random.uniform(0.03, 0.09),
            })

    def _draw_background(self):
        self.bg_canvas.delete("all")
        w, h = self.WIDTH, self.HEIGHT
        # Animated diagonal purple -> blue gradient
        top    = self._lerp_color("#05040F", "#1B1248", (math.sin(self._grad_phase) + 1) / 2)
        bottom = self._lerp_color("#3A2470", "#5A3FCF", (math.cos(self._grad_phase * 0.7) + 1) / 2)
        steps = 80
        for i in range(steps):
            t = i / (steps - 1)
            color = self._lerp_color(top, bottom, t)
            y0 = int(t * h)
            y1 = int((t + 1.0 / steps) * h) + 1
            self.bg_canvas.create_rectangle(0, y0, w, y1, fill=color, outline=color)
        # Stars on top
        for s in self._stars:
            tw = (math.sin(self._grad_phase * 2 + s["phase"]) + 1) / 2  # twinkle 0..1
            shade = int(180 + tw * 75)
            color = f"#{shade:02x}{shade:02x}{min(255, shade + 20):02x}"
            r = s["r"] * (0.7 + tw * 0.6)
            self.bg_canvas.create_oval(s["x"] - r, s["y"] - r, s["x"] + r, s["y"] + r,
                                        fill=color, outline="")

    def _lerp_color(self, c1, c2, t):
        c1 = c1.lstrip("#"); c2 = c2.lstrip("#")
        r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
        r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _animate_background(self):
        self._grad_phase += 0.04
        for s in self._stars:
            s["y"] += s["speed"]
            if s["y"] > self.HEIGHT:
                s["y"] = 0
                s["x"] = random.uniform(0, self.WIDTH)
        try:
            self._draw_background()
        except Exception:
            return
        self._anim_job = self.after(50, self._animate_background)

    # -- tips ------------------------------------------------------------
    def _rotate_tip(self):
        if not self._tip_pool:
            return
        tip = self._tip_pool[self._tip_index % len(self._tip_pool)]
        self._tip_index += 1
        self.tip_label.configure(text=tip)

    def _tip_loop(self):
        self._rotate_tip()
        self._tip_job = self.after(3200, self._tip_loop)

    # -- public API (unchanged signature) --------------------------------
    def update_progress(self, value, status):
        """Update progress bar and status text."""
        self.progress_bar.set(value)
        self.status_label.configure(text=status)
        self.update_idletasks()

    def close(self):
        """Close the loading screen."""
        for job in (getattr(self, "_anim_job", None), getattr(self, "_tip_job", None)):
            if job is not None:
                try:
                    self.after_cancel(job)
                except Exception:
                    pass
        self.destroy()


# ═════════════════════════════════════════════════════════════════════════════
# APP
# ═════════════════════════════════════════════════════════════════════════════
class App(ctk.CTk):
    def __init__(self):
        # Initialize loading screen first (before main window)
        self.loading_screen = LoadingScreen()
        self.loading_screen.update_progress(0.1, "Checking single instance...")
        self.loading_screen.update()
        
        self._single_instance()
        self.loading_screen.update_progress(0.2, "Initializing window...")
        super().__init__()
        self.title(f"{APP_NAME} {VERSION}")
        self.geometry("1480x940")
        self.minsize(1100, 700)
        if os.path.exists("icon.ico"):
            try:
                self.iconbitmap("icon.ico")
            except Exception:
                pass

        self.loading_screen.update_progress(0.3, "Loading splash text...")
        self.splash_text  = random.choice(SPLASHES)
        self.loading_screen.update_progress(0.4, "Initializing audio systems...")
        self.log          = ActivityLog()
        self.sb           = SoundboardCore()
        self.sb.app_ref   = self
        self.synth        = RealtimeSynth()
        self.synth_params = {
            "wave": "Sine", "osc2_wave": "Saw",
            "mod_target": "None", "lfo_shape": "Sine",
            "arp_bpm": 120.0,
        }
        self.loading_screen.update_progress(0.5, "Starting audio engine...")
        self.engine       = AudioEngine(self.sb, self.synth, self.synth_params)
        self.loading_screen.update_progress(0.6, "Loading mod system...")
        self.mod_loader   = ModLoader(self)
        self.presets      = PresetsManager()
        self.loading_screen.update_progress(0.7, "Initializing TTS...")
        self.tts          = LiveTTS(self.sb)
        self.loading_screen.update_progress(0.8, "Loading sequencer...")
        self.sequencer    = SongSequencer(self.synth, self.synth_params)
        self.SONGS        = self.sequencer.songs
        self.loading_screen.update_progress(0.85, "Loading settings...")
        self.settings     = self._load_settings()
        self.THEMES       = THEMES

        self.loading_screen.update_progress(0.9, "Setting up UI...")
        self.stream          = None
        self.monitor_stream  = None
        self.loopback_stream = None
        self.running         = False
        self.mon_q          = queue.Queue(maxsize=5)
        self.mon_thread_run = False
        self.tray_icon      = None

        self._fx_history    = []
        self._history_ptr   = -1
        self._slider_widgets = {}
        self._rainbow_hue    = 0.0
        self._rainbow_active = False
        
        # Advanced theme attributes
        self._theme_fonts = {}
        self._theme_widgets = {}

        self.loading_screen.update_progress(0.95, "Building interface...")
        self._apply_theme()
        self._apply_system_settings()
        self._load_bg()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.loading_screen.update_progress(0.97, "Building sidebar...")
        self._build_sidebar()
        self.loading_screen.update_progress(0.98, "Building main area...")
        self._build_main_area()
        self._build_vis_bar()
        self._apply_dynamic_theme(self.settings.get("theme", "Crimson"))

        self.loading_screen.update_progress(0.99, "Loading mods...")
        self.engine.mods = self.mod_loader.load_mods()
        self._init_mod_params()
        self._rebuild_mod_sections()

        # CPU guard → toast
        def _overload_cb(state):
            self.after(0, lambda: self.show_toast(
                "⚠ CPU overload — some effects skipped" if state else "✓ CPU load normal",
                "#880000" if state else "#228822"
            ))
        self.engine._overload_cb = _overload_cb

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.log.add(f"{APP_NAME} {VERSION} started.")
        
        # Close loading screen
        self.loading_screen.update_progress(1.0, "Complete!")
        self.after(100, self.loading_screen.close)
        
        self.after(800, self._init_visualizer)
        self.after(100, self._vu_loop)

    # ── instance ──────────────────────────────────────────────────────────────
    def _single_instance(self):
        self._inst_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self._inst_sock.bind(("127.0.0.1", 19347))
            threading.Thread(target=self._listen_wakeup, daemon=True).start()
        except OSError:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b"WAKEUP", ("127.0.0.1", 19347))
            sys.exit(0)

    def _listen_wakeup(self):
        while True:
            try:
                data, _ = self._inst_sock.recvfrom(1024)
                if data == b"WAKEUP":
                    self.after(0, self._show_window)
            except Exception:
                break

    def _show_window(self):
        self.deiconify(); self.lift(); self.focus_force()

    # ── settings ──────────────────────────────────────────────────────────────
    def _load_settings(self):
        d = {
            "theme": "Crimson", "minimize_to_tray": True, "startup": False,
            "always_on_top": False, "opacity": 1.0, "buffer_size": 1024,
            "high_priority": False, "sb_cols": 5, "vis_mode": "Waveform",
            "show_vu": True, "vu_color_bands": False, "tts_rate": 150,
            "seq_bpm": 120,
        }
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE) as f:
                    d.update(json.load(f))
            except Exception:
                pass
        return d

    def _save_settings(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f, indent=2)

    # ── theme ─────────────────────────────────────────────────────────────────
    def _apply_theme(self):
        t = self.THEMES.get(
            self.settings.get("theme", "Crimson"),
            next(iter(self.THEMES.values()))
        )

        # ── Stop any running advanced-theme tick from previous theme ──────────
        if getattr(self, "_adv_theme_module", None) is not None:
            try:
                rm = getattr(self._adv_theme_module, "remove", None)
                if rm:
                    rm(self)
            except Exception:
                pass
        self._adv_theme_module = None
        if getattr(self, "_adv_tick_job", None):
            try:
                self.after_cancel(self._adv_tick_job)
            except Exception:
                pass
        self._adv_tick_job = None

        # ── Pull colors (works for both basic and advanced themes) ────────────
        is_advanced_module = t.get("_advanced", False) and t.get("_module") is not None

        self.col_accent  = t.get("accent",  "#D12020")
        self.col_hover   = t.get("hover",   "#E84040")
        self.col_glow    = t.get("glow",    "#D1202044")
        self.col_sidebar = t.get("sidebar", "#0D0D0D")
        self.col_card    = t.get("card",    "#161616")
        self.col_card2   = t.get("card2",   "#1E1E1E")
        self.col_text    = t.get("text",    "#E8E8E8")
        self.col_sub     = t.get("subtext", "#848484")
        self.col_border  = t.get("border",  "#2A2A2A")
        self.col_input   = t.get("input_bg","#111111")

        # ── Rainbow effect ────────────────────────────────────────────────────
        self._rainbow_active = t.get("rainbow", False)
        self._rainbow_hue    = 0.0
        if self._rainbow_active:
            self._start_rainbow_animation()
        else:
            self._stop_rainbow_animation()

        # ── RGB effect ────────────────────────────────────────────────────────
        self._rgb_active = t.get("rgb", False)
        if self._rgb_active:
            self._start_rgb_animation()
        else:
            self._stop_rgb_animation()

        # ── Space Nebula special-case: draw starfield background ──────────────
        if t.get("_space", False):
            self._start_space_background()
        else:
            self._stop_space_background()

        # ── Advanced Python module hooks ──────────────────────────────────────
        if is_advanced_module:
            mod = t["_module"]
            self._adv_theme_module = mod
            try:
                apply_fn = getattr(mod, "apply", None)
                if apply_fn:
                    apply_fn(self)
            except Exception as e:
                print(f"[Themes] apply() error: {e}")

            # Schedule tick if the module provides one
            tick_fn = getattr(mod, "tick", None)
            if tick_fn:
                def _do_tick():
                    if self._adv_theme_module is not mod:
                        return
                    try:
                        tick_fn(self)
                    except Exception:
                        pass
                    self._adv_tick_job = self.after(120, _do_tick)
                self._adv_tick_job = self.after(120, _do_tick)

    def _hsv_to_hex(self, h, s, v):
        """Convert HSV to hex color."""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    def _apply_cursor(self, cursor_config):
        """Apply custom cursor from theme configuration."""
        if not cursor_config.get("enabled", False):
            return
        
        custom_path = cursor_config.get("custom_path", "")
        if custom_path and os.path.exists(custom_path):
            try:
                # Try to load custom cursor
                from PIL import Image
                img = Image.open(custom_path)
                # Resize to cursor size if needed
                if img.size != (32, 32):
                    img = img.resize((32, 32), Image.Resampling.LANCZOS)
                # Apply cursor (platform-specific)
                if sys.platform == "win32":
                    # Windows cursor support
                    try:
                        import ctypes
                        # Create cursor from image
                        cursor_data = img.tobytes()
                        # This is a simplified approach - full cursor creation requires more work
                        pass
                    except Exception:
                        pass
            except Exception:
                pass

    def _apply_starfield_overlay(self, effects_config):
        """Draw/remove a twinkling starfield canvas over the main window,
        used by themes that set effects.starfield.enabled = True (e.g. Space Nebula)."""
        want = effects_config.get("starfield", {}).get("enabled", False)

        if not want:
            if getattr(self, "_starfield_canvas", None) is not None:
                try:
                    self._starfield_job and self.after_cancel(self._starfield_job)
                except Exception:
                    pass
                self._starfield_canvas.destroy()
                self._starfield_canvas = None
            return

        density = effects_config.get("starfield", {}).get("density", 120)
        twinkle = effects_config.get("starfield", {}).get("twinkle", True)

        if getattr(self, "_starfield_canvas", None) is None:
            self._starfield_canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg="")
            try:
                self._starfield_canvas.configure(bg=self.col_sidebar)
            except Exception:
                pass
            self._starfield_canvas.place(x=0, y=0, relwidth=1, relheight=1)
            tk.Misc.lower(self._starfield_canvas)  # stays behind interactive widgets

            self._starfield_stars = []
            for _ in range(density):
                self._starfield_stars.append({
                    "x": random.uniform(0, 1), "y": random.uniform(0, 1),
                    "r": random.uniform(0.6, 1.6),
                    "phase": random.uniform(0, 6.28318),
                })
            self._starfield_phase = 0.0

            def _tick():
                if getattr(self, "_starfield_canvas", None) is None:
                    return
                try:
                    c = self._starfield_canvas
                    w = max(c.winfo_width(), 1)
                    h = max(c.winfo_height(), 1)
                    c.delete("star")
                    self._starfield_phase += 0.08
                    for s in self._starfield_stars:
                        tw = (math.sin(self._starfield_phase + s["phase"]) + 1) / 2 if twinkle else 1.0
                        shade = int(150 + tw * 100)
                        color = f"#{shade:02x}{shade:02x}{min(255, shade + 30):02x}"
                        r = s["r"] * (0.7 + tw * 0.5)
                        px, py = s["x"] * w, s["y"] * h
                        c.create_oval(px - r, py - r, px + r, py + r,
                                      fill=color, outline="", tags="star")
                except Exception:
                    pass
                self._starfield_job = self.after(70, _tick)

            _tick()

    # ─────────────────────────────────────────────────────────────────────────
    # Space Nebula background  (CPU-light: 70ms tick, no pixel loops)
    # ─────────────────────────────────────────────────────────────────────────
    def _start_space_background(self):
        """Lazy-init a starfield canvas behind the main UI."""
        if getattr(self, "_space_canvas", None) is not None:
            return  # already running

        import random, math as _math

        W = self.winfo_screenwidth()
        H = self.winfo_screenheight()
        STAR_COUNT = 80    # keep low — ovals are cheap but still cost
        TICK_MS    = 80    # ~12 fps for the starfield

        cvs = tk.Canvas(self, highlightthickness=0, bd=0, bg=self.col_sidebar)
        cvs.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        tk.Misc.lower(cvs)
        self._space_canvas = cvs

        stars = [
            {
                "x": random.uniform(0, 1),
                "y": random.uniform(0, 1),
                "r": random.uniform(0.8, 2.2),
                "phase": random.uniform(0, 6.2832),
                "vy": random.uniform(0.0002, 0.0007),
            }
            for _ in range(STAR_COUNT)
        ]
        self._space_stars = stars
        self._space_phase = 0.0
        self._space_job   = None

        def _tick():
            if getattr(self, "_space_canvas", None) is not cvs:
                return
            try:
                w = max(cvs.winfo_width(), 800)
                h = max(cvs.winfo_height(), 600)
                cvs.delete("star")
                self._space_phase += 0.06
                p = self._space_phase
                for s in stars:
                    s["y"] += s["vy"]
                    if s["y"] > 1.02:
                        s["y"] = -0.02
                        s["x"] = random.uniform(0, 1)
                    tw = (_math.sin(p + s["phase"]) + 1) / 2   # 0..1
                    shade = int(130 + tw * 110)
                    blue  = min(255, shade + 40)
                    col = f"#{shade:02x}{shade:02x}{blue:02x}"
                    r = s["r"] * (0.6 + tw * 0.6)
                    px, py = s["x"] * w, s["y"] * h
                    cvs.create_oval(px - r, py - r, px + r, py + r,
                                    fill=col, outline="", tags="star")
            except Exception:
                pass
            self._space_job = self.after(TICK_MS, _tick)

        _tick()

    def _stop_space_background(self):
        """Tear down the starfield canvas if it exists."""
        job = getattr(self, "_space_job", None)
        if job:
            try:
                self.after_cancel(job)
            except Exception:
                pass
        self._space_job = None

        cvs = getattr(self, "_space_canvas", None)
        if cvs is not None:
            try:
                cvs.destroy()
            except Exception:
                pass
        self._space_canvas = None

    def _apply_theme_background(self, background_config):
        """Apply background from theme configuration."""
        if not background_config.get("enabled", False):
            return
        
        bg_path = background_config.get("path", "")
        if bg_path and os.path.exists(bg_path):
            try:
                img = Image.open(bg_path)
                # Handle transparency
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGBA')
                    bg = Image.new('RGBA', img.size, (12, 12, 12, 255))
                    bg.paste(img, mask=img.split()[3])
                    img = bg.convert('RGB')
                else:
                    img = img.convert('RGB')
                
                # Apply opacity if specified
                opacity = background_config.get("opacity", 1.0)
                if opacity < 1.0:
                    from PIL import ImageEnhance
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(opacity)
                
                # Apply blur if specified
                blur = background_config.get("blur", 0)
                if blur > 0:
                    from PIL import ImageFilter
                    img = img.filter(ImageFilter.GaussianBlur(blur))
                
                self._bg = ctk.CTkImage(img, size=(1480, 940))
                lbl = ctk.CTkLabel(self, text="", image=self._bg)
                lbl.place(x=0, y=0, relwidth=1, relheight=1)
                lbl.lower()
            except Exception:
                pass

    def _start_rainbow_animation(self):
        """Start rainbow color cycling with advanced effects."""
        if not hasattr(self, '_rainbow_job') or self._rainbow_job is None:
            self._rainbow_job = self.after(50, self._animate_rainbow)

    def _stop_rainbow_animation(self):
        """Stop rainbow color cycling."""
        if hasattr(self, '_rainbow_job') and self._rainbow_job is not None:
            self.after_cancel(self._rainbow_job)
            self._rainbow_job = None

    def _animate_rainbow(self):
        """Animate rainbow colors with advanced effects."""
        if not self._rainbow_active:
            return
        
        theme_name = self.settings.get("theme", "Crimson")
        t = self.THEMES.get(theme_name, next(iter(self.THEMES.values())))
        
        # Check if it's an advanced theme with rainbow config
        if isinstance(t, dict) and "effects" in t:
            effects = t.get("effects", {})
            rainbow_config = effects.get("rainbow", {})
            
            if not rainbow_config.get("enabled", False):
                return
            
            speed = rainbow_config.get("speed", 1.0)
            intensity = rainbow_config.get("intensity", 1.0)
            targets = rainbow_config.get("targets", ["accent", "hover", "glow"])
            
            self._rainbow_hue = (self._rainbow_hue + 0.01 * speed) % 1.0
            
            # Apply rainbow to target colors
            if "accent" in targets:
                self.col_accent = self._hsv_to_hex(self._rainbow_hue, 1.0, intensity)
            if "hover" in targets:
                self.col_hover = self._hsv_to_hex((self._rainbow_hue + 0.1) % 1.0, 1.0, intensity)
            if "glow" in targets:
                glow_val = int(intensity * 0.8 * 255)
                self.col_glow = self._hsv_to_hex(self._rainbow_hue, 1.0, intensity * 0.8) + f"{glow_val:02x}"
        else:
            # Simple rainbow theme (backward compatible)
            self._rainbow_hue = (self._rainbow_hue + 0.01) % 1.0
            self.col_accent = self._hsv_to_hex(self._rainbow_hue, 1.0, 1.0)
            self.col_hover = self._hsv_to_hex((self._rainbow_hue + 0.1) % 1.0, 1.0, 1.0)
            self.col_glow = self._hsv_to_hex(self._rainbow_hue, 1.0, 0.8) + "33"
        
        self._apply_dynamic_theme(theme_name)
        self._rainbow_job = self.after(50, self._animate_rainbow)
    
    def _animate_rgb(self):
        """Animate RGB effects with different modes."""
        if not hasattr(self, '_rgb_active') or not self._rgb_active:
            return
        
        theme_name = self.settings.get("theme", "Crimson")
        t = self.THEMES.get(theme_name, next(iter(self.THEMES.values())))
        
        if isinstance(t, dict) and "effects" in t:
            effects = t.get("effects", {})
            rgb_config = effects.get("rgb", {})
            
            if not rgb_config.get("enabled", False):
                return
            
            mode = rgb_config.get("mode", "cycle")
            speed = rgb_config.get("speed", 1.0)
            intensity = rgb_config.get("intensity", 1.0)
            targets = rgb_config.get("targets", ["accent"])
            
            if not hasattr(self, '_rgb_hue'):
                self._rgb_hue = 0.0
            if not hasattr(self, '_rgb_phase'):
                self._rgb_phase = 0.0
            
            if mode == "cycle":
                self._rgb_hue = (self._rgb_hue + 0.02 * speed) % 1.0
                color = self._hsv_to_hex(self._rgb_hue, 1.0, intensity)
            elif mode == "pulse":
                self._rgb_phase = (self._rgb_phase + 0.05 * speed) % (2 * np.pi)
                pulse = (np.sin(self._rgb_phase) + 1) / 2  # 0 to 1
                color = self._hsv_to_hex(0.0, 1.0, 0.5 + pulse * 0.5 * intensity)
            elif mode == "wave":
                self._rgb_phase = (self._rgb_phase + 0.03 * speed) % (2 * np.pi)
                wave = (np.sin(self._rgb_phase) + 1) / 2
                self._rgb_hue = wave
                color = self._hsv_to_hex(self._rgb_hue, 1.0, intensity)
            else:
                color = self.col_accent
            
            # Apply RGB to target colors
            if "accent" in targets:
                self.col_accent = color
            if "hover" in targets:
                self.col_hover = self._hsv_to_hex((self._rgb_hue + 0.1) % 1.0, 1.0, intensity)
            
            self._apply_dynamic_theme(theme_name)
            self._rgb_job = self.after(50, self._animate_rgb)
    
    def _start_rgb_animation(self):
        """Start RGB animation."""
        if not hasattr(self, '_rgb_job') or self._rgb_job is None:
            self._rgb_job = self.after(50, self._animate_rgb)
    
    def _stop_rgb_animation(self):
        """Stop RGB animation."""
        if hasattr(self, '_rgb_job') and self._rgb_job is not None:
            self.after_cancel(self._rgb_job)
            self._rgb_job = None
    
    def _apply_gradients(self, gradient_config):
        """Apply gradient effects to UI elements."""
        if not gradient_config.get("enabled", False):
            return
        
        # Sidebar gradient
        sidebar_grad = gradient_config.get("sidebar", {})
        if sidebar_grad.get("enabled", False):
            self._apply_element_gradient("sidebar", sidebar_grad)
        
        # Card gradient
        card_grad = gradient_config.get("card", {})
        if card_grad.get("enabled", False):
            self._apply_element_gradient("card", card_grad)
    
    def _apply_element_gradient(self, element_name, grad_config):
        """Apply gradient to a specific UI element."""
        try:
            grad_type = grad_config.get("type", "linear")
            direction = grad_config.get("direction", "vertical")
            colors = grad_config.get("colors", ["#0C0C0C", "#1A1A1A"])
            stops = grad_config.get("stops", [0.0, 1.0])
            
            # Convert gradient to hex color for now (CustomTkinter limitation)
            # In a full implementation, this would use canvas gradients
            if element_name == "sidebar":
                self.col_sidebar = colors[0]  # Use first color as fallback
            elif element_name == "card":
                self.col_card = colors[0]  # Use first color as fallback
        except Exception:
            pass

    def _apply_dynamic_theme(self, name):
        t = self.THEMES.get(name, next(iter(self.THEMES.values())))
        self.col_accent = t.get("accent", "#D00000")
        self.col_hover  = t.get("hover",  "#FF2020")
        self.col_glow   = t.get("glow",   "#D0000033")

        def _r(w):
            try:
                if isinstance(w, ctk.CTkButton):
                    bg = str(w.cget("fg_color"))
                    if bg not in ("transparent","#333","#333333","#500","#500000","#800000","white","#222","#1a1a1a"):
                        w.configure(fg_color=self.col_accent, hover_color=self.col_hover)
                elif isinstance(w, ctk.CTkSlider):
                    w.configure(button_color=self.col_accent, progress_color=self.col_accent, button_hover_color=self.col_hover)
                elif isinstance(w, ctk.CTkSwitch):
                    w.configure(progress_color=self.col_accent)
                elif isinstance(w, (ctk.CTkComboBox, ctk.CTkOptionMenu)):
                    w.configure(button_color=self.col_accent, border_color=self.col_accent)
                elif isinstance(w, ctk.CTkSegmentedButton):
                    w.configure(selected_color=self.col_accent, selected_hover_color=self.col_hover)
                elif isinstance(w, ctk.CTkTabview):
                    w.configure(segmented_button_selected_color=self.col_accent,
                                segmented_button_selected_hover_color=self.col_hover)
                elif isinstance(w, ctk.CTkCheckBox):
                    w.configure(fg_color=self.col_accent, hover_color=self.col_hover)
                elif isinstance(w, ctk.CTkProgressBar):
                    w.configure(progress_color=self.col_accent)
            except Exception:
                pass
            for c in w.winfo_children():
                _r(c)

        _r(self)
        try:
            self.lbl_appname.configure(text_color=self.col_accent)
        except Exception:
            pass
        try:
            self.vis_line.set_color(self.col_accent)
            self.vis_canvas.draw_idle()
        except Exception:
            pass

    def _apply_system_settings(self):
        self.attributes("-alpha",   self.settings.get("opacity", 1.0))
        self.attributes("-topmost", self.settings.get("always_on_top", False))
        if self.settings.get("high_priority") and sys.platform == "win32":
            try:
                import ctypes
                ctypes.windll.kernel32.SetPriorityClass(
                    ctypes.windll.kernel32.GetCurrentProcess(), 0x00000080)
            except Exception:
                pass

    def _load_bg(self):
        for name in ["bg.jpg", "bg.png", "cat.jpg"]:
            if os.path.exists(name):
                try:
                    img = Image.open(name)
                    self._bg = ctk.CTkImage(img, size=(1480, 940))
                    lbl = ctk.CTkLabel(self, text="", image=self._bg)
                    lbl.place(x=0, y=0, relwidth=1, relheight=1)
                    lbl.lower()
                except Exception:
                    pass
                break

    def show_toast(self, msg, color=None):
        toast = ctk.CTkLabel(self, text=f"  {msg}  ",
                              fg_color=color or self.col_accent, text_color="white",
                              corner_radius=8, font=("Consolas", 11))
        toast.place(relx=0.5, rely=0.97, anchor="center")
        self.after(2800, toast.destroy)

    # ══════════════════════════════════════════════════════════════════════════
    # SIDEBAR
    # ══════════════════════════════════════════════════════════════════════════
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=265, corner_radius=0, fg_color=self.col_sidebar)
        sb.grid(row=0, column=0, rowspan=2, sticky="nsew")
        sb.grid_propagate(False)

        hdr = ctk.CTkFrame(sb, fg_color=self.col_card, corner_radius=0)
        hdr.pack(fill="x")
        self.lbl_appname = ctk.CTkLabel(hdr, text=APP_NAME,
            font=ctk.CTkFont(family="Courier New", size=30, weight="bold"),
            text_color=self.col_accent)
        self.lbl_appname.pack(pady=(16, 2))
        ctk.CTkLabel(hdr, text=self.splash_text, font=ctk.CTkFont(size=9),
                     text_color=self.col_sub, wraplength=220).pack(pady=(0, 4))
        ctk.CTkLabel(hdr, text=VERSION, font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=self.col_sub).pack(pady=(0, 10))

        dev = ctk.CTkFrame(sb, fg_color="transparent")
        dev.pack(fill="x", padx=12, pady=6)
        for lbl, attr in [("Microphone", "in_dev"), ("Output (Cable)", "out_dev"), ("Monitor", "mon_dev"),
                           ("Desktop Echo Input", "lb_dev")]:
            ctk.CTkLabel(dev, text=lbl, text_color=self.col_sub, font=("Consolas", 9)).pack(anchor="w")
            cb = ctk.CTkComboBox(dev, button_color=self.col_accent, border_color=self.col_card2,
                                  fg_color=self.col_card, height=26)
            cb.pack(fill="x", pady=(0, 4))
            setattr(self, attr, cb)

        ctk.CTkButton(sb, text="↻  Refresh Devices", command=self._refresh_devices,
                       fg_color="#222", hover_color="#333", height=26, font=("Consolas", 10)
                       ).pack(fill="x", padx=12, pady=(0, 6))

        self.btn_start = ctk.CTkButton(sb, text="▶  START ENGINE",
            command=self._toggle_audio, fg_color=self.col_accent, hover_color=self.col_hover,
            height=50, font=ctk.CTkFont(family="Courier New", size=13, weight="bold"))
        self.btn_start.pack(fill="x", padx=12, pady=6)

        # CPU load indicator
        self.cpu_lbl = ctk.CTkLabel(sb, text="● IDLE", font=("Consolas", 9), text_color="#444")
        self.cpu_lbl.pack(pady=2)

        sw_f = ctk.CTkFrame(sb, fg_color="transparent")
        sw_f.pack(fill="x", padx=12, pady=2)
        self.sw_mon = ctk.CTkSwitch(sw_f, text="Mic Monitor", command=self._toggle_mon,
                                     progress_color=self.col_accent, button_color="white")
        self.sw_mon.pack(side="left")

        # VU
        vu_f = ctk.CTkFrame(sb, fg_color=self.col_card, corner_radius=6)
        vu_f.pack(fill="x", padx=12, pady=6)
        ctk.CTkLabel(vu_f, text="VU", font=("Consolas", 9), text_color=self.col_sub).pack(pady=(4, 1))
        self.vu_l = ctk.CTkProgressBar(vu_f, height=8, progress_color=self.col_accent, fg_color="#111")
        self.vu_l.set(0); self.vu_l.pack(fill="x", padx=6, pady=1)
        self.vu_r = ctk.CTkProgressBar(vu_f, height=8, progress_color=self.col_accent, fg_color="#111")
        self.vu_r.set(0); self.vu_r.pack(fill="x", padx=6, pady=(1, 6))

        # Quick preset
        qp = ctk.CTkFrame(sb, fg_color=self.col_card, corner_radius=6)
        qp.pack(fill="x", padx=12, pady=4)
        ctk.CTkLabel(qp, text="QUICK PRESET", font=("Consolas", 9), text_color=self.col_sub).pack(pady=(4, 1))
        self.combo_preset = ctk.CTkComboBox(qp, values=list(self.presets.presets.keys()),
            button_color=self.col_accent, border_color=self.col_card2,
            fg_color="#111", command=self._apply_preset, height=26)
        self.combo_preset.pack(fill="x", padx=6, pady=(0, 6))

        # Quick song
        qs = ctk.CTkFrame(sb, fg_color=self.col_card, corner_radius=6)
        qs.pack(fill="x", padx=12, pady=4)
        ctk.CTkLabel(qs, text="QUICK SONG", font=("Consolas", 9), text_color=self.col_sub).pack(pady=(4, 1))
        self.combo_quick_song = ctk.CTkComboBox(qs, values=list(self.sequencer.songs.keys()),
            button_color=self.col_accent, border_color=self.col_card2,
            fg_color="#111", command=self._quick_play_song, height=26)
        self.combo_quick_song.pack(fill="x", padx=6, pady=(0, 6))
        ctk.CTkButton(qs, text="⏹ Stop Song", command=self.sequencer.stop,
                       fg_color="#500000", hover_color="#800000", height=24,
                       font=("Consolas", 9)).pack(fill="x", padx=6, pady=(0, 6))

        ctk.CTkButton(sb, text="⚠  Report Bug",
                       command=lambda: webbrowser.open("https://discord.gg/NJ4Ux5Pbm2"),
                       fg_color="transparent", text_color="#333", hover_color="#1a1a1a",
                       font=("Consolas", 9)).pack(side="bottom", pady=6)
        self._refresh_devices()

    def _refresh_devices(self):
        try:
            devs = sd.query_devices()
            ins  = [d["name"] for d in devs if d["max_input_channels"]  > 0]
            outs = [d["name"] for d in devs if d["max_output_channels"] > 0]
            self.in_dev.configure(values=ins)
            self.out_dev.configure(values=outs)
            self.mon_dev.configure(values=outs)
            self.lb_dev.configure(values=ins)
            if ins:  self.in_dev.set(ins[0]); self.lb_dev.set(ins[0])
            if outs: self.out_dev.set(outs[0]); self.mon_dev.set(outs[0])
        except Exception as e:
            self.log.add(f"Device refresh: {e}", "ERROR")

    def _quick_play_song(self, name):
        if not self.running:
            messagebox.showwarning("Engine Off", "Start the audio engine first.")
            return
        if self.sequencer.play_song(name):
            self.show_toast(f"♫  {name}")
            self.log.add(f"Playing song: {name}")
        else:
            self.show_toast(f"Song not found: {name}", "#880000")

    # ══════════════════════════════════════════════════════════════════════════
    # MAIN TABS
    # ══════════════════════════════════════════════════════════════════════════
    def _build_main_area(self):
        self.tabs = ctk.CTkTabview(self,
            segmented_button_selected_color=self.col_accent,
            segmented_button_selected_hover_color=self.col_hover,
            segmented_button_unselected_color=self.col_card,
            text_color=self.col_text)
        self.tabs.grid(row=0, column=1, sticky="nsew", padx=(0, 8), pady=8)

        self.tab_fx     = self.tabs.add("  FX Rack  ")
        self.tab_sb     = self.tabs.add("  Board  ")
        self.tab_synth  = self.tabs.add("  Synth  ")
        self.tab_seq    = self.tabs.add("  Sequencer  ")
        self.tab_mods   = self.tabs.add("  Mods  ")
        self.tab_tts    = self.tabs.add("  TTS  ")
        self.tab_preset = self.tabs.add("  Presets  ")
        self.tab_log    = self.tabs.add("  Log  ")
        self.tab_set    = self.tabs.add("  Settings  ")

        self._build_fx_tab()
        self._build_sb_tab()
        self._build_synth_tab()
        self._build_seq_tab()
        self._build_mods_tab()
        self._build_tts_tab()
        self._build_presets_tab()
        self._build_log_tab()
        self._build_settings_tab()

    def _build_vis_bar(self):
        self.vis_frame = ctk.CTkFrame(self, height=90, fg_color="#060606", corner_radius=0)
        self.vis_frame.grid(row=1, column=1, sticky="ew", padx=(0, 8), pady=(0, 6))

    def _init_visualizer(self):
        if not HAS_MPL:
            return
        try:
            self.vis_fig, self.vis_ax = plt.subplots(figsize=(10, 0.9), facecolor="#060606")
            self.vis_ax.set_facecolor("#060606")
            self.vis_ax.axis("off")
            self.vis_line, = self.vis_ax.plot([], [], color=self.col_accent, lw=1.0)
            self.vis_ax.set_ylim(-1, 1)
            self.vis_canvas = FigureCanvasTkAgg(self.vis_fig, master=self.vis_frame)
            self.vis_canvas.get_tk_widget().pack(fill="both", expand=True)
            self._vis_tick()
        except Exception as e:
            self.log.add(f"Vis init: {e}", "WARN")

    def _vis_tick(self):
        try:
            if self.running:
                d = self.engine.vis_data
                step = max(1, len(d) // 60)
                ds = d[::step]
                self.vis_line.set_data(np.arange(len(ds)), ds)
                self.vis_ax.set_xlim(0, max(1, len(ds)))
                self.vis_canvas.draw_idle()
        except Exception:
            pass
        self.after(80, self._vis_tick)

    def _vu_loop(self):
        try:
            lv = min(1.0, self.engine.vu_peak_l)
            rv = min(1.0, self.engine.vu_peak_r)
            self.vu_l.set(lv)
            self.vu_r.set(rv)
            if self.settings.get("vu_color_bands"):
                col = "#39FF14" if lv < 0.7 else ("#FFD700" if lv < 0.9 else "#FF2020")
                try:
                    self.vu_l.configure(progress_color=col)
                    self.vu_r.configure(progress_color=col)
                except Exception:
                    pass
            # CPU indicator
            if self.engine._cb_times:
                avg = sum(self.engine._cb_times) / max(1, len(self.engine._cb_times))
                budget = (self.settings.get("buffer_size", 1024) / SR) * 1000 * 0.8
                pct = int(min(100, avg / max(budget, 0.001) * 100))
                col_c = "#228822" if pct < 60 else ("#FFD700" if pct < 85 else "#FF2020")
                try:
                    self.cpu_lbl.configure(text=f"● CPU {pct}%", text_color=col_c)
                except Exception:
                    pass
        except Exception:
            pass
        self.after(60, self._vu_loop)

    # ══════════════════════════════════════════════════════════════════════════
    # FX RACK
    # ══════════════════════════════════════════════════════════════════════════
    def _build_fx_tab(self):
        self.fx_scroll = ctk.CTkScrollableFrame(self.tab_fx, fg_color="transparent")
        self.fx_scroll.pack(fill="both", expand=True)
        self._draw_fx(self.fx_scroll)

    def _draw_fx(self, p):
        def sec(title):
            f = ctk.CTkFrame(p, fg_color=self.col_card, corner_radius=8)
            f.pack(fill="x", padx=5, pady=(6, 0))
            hdr = ctk.CTkFrame(f, fg_color=self.col_card2, corner_radius=6)
            hdr.pack(fill="x", padx=3, pady=3)
            ctk.CTkLabel(hdr, text=title, font=("Consolas", 11, "bold"),
                         text_color=self.col_accent).pack(anchor="w", padx=8, pady=3)
            body = ctk.CTkFrame(f, fg_color="transparent")
            body.pack(fill="x", padx=6, pady=(0, 6))
            return body

        sl = self._sl  # shorthand
        sl(sec("⚡  MASTER"), "Master Out Gain (dB)", -30, 20, 0, "master_out_gain")
        sl(sec("⚡  MASTER"),"",0,0,0,"_skip") # don't double-create section
        # redo properly
        for w in self.fx_scroll.winfo_children():
            w.destroy()
        self._slider_widgets.clear()

        def S(title, *args):
            body = sec(title)
            for a in args:
                sl(body, *a)

        S("⚡  MASTER  &  GATE",
          ("Master Out Gain (dB)", -30, 20, 0, "master_out_gain"),
          ("Mic Input Gain (dB)", -20, 40, 0, "gain"),
          ("Noise Gate", 0.0, 0.5, 0.0, "noise_gate"))

        S("🎚  3-BAND EQ",
          ("Low Shelf (dB)", -18, 18, 0, "eq_lo"),
          ("Mid (dB)", -18, 18, 0, "eq_mid"),
          ("High Shelf (dB)", -18, 18, 0, "eq_hi"))

        S("📊  COMPRESSOR",
          ("Threshold", 0.1, 1.0, 0.7, "comp_threshold"),
          ("Ratio", 1.0, 20.0, 4.0, "comp_ratio"),
          ("Attack (s)", 0.001, 0.2, 0.01, "comp_attack"),
          ("Release (s)", 0.01, 2.0, 0.1, "comp_release"))

        S("🎛  TRANSFORM",
          ("Pitch (semitones)", -24, 24, 0, "pitch"),
          ("Pan", -1, 1, 0, "pan"),
          ("Bitcrush (bits)", 0, 16, 0, "bitcrush"))

        S("🔥  DISTORTION",
          ("Drive", 0.0, 1.0, 0.0, "distortion"))

        S("〰  TREMOLO",
          ("Rate (Hz)", 0.1, 20.0, 5.0, "tremolo_rate"),
          ("Depth", 0.0, 1.0, 0.0, "tremolo_depth"))

        S("🌊  CHORUS",
          ("Rate (Hz)", 0.1, 10.0, 1.0, "chorus_rate"),
          ("Depth", 0.0, 1.0, 0.5, "chorus_depth"),
          ("Mix", 0.0, 1.0, 0.0, "chorus_mix"))

        S("🔄  PHASER",
          ("Rate (Hz)", 0.1, 8.0, 1.0, "phaser_rate"),
          ("Depth", 0.0, 1.0, 0.5, "phaser_depth"),
          ("Mix", 0.0, 1.0, 0.0, "phaser_mix"))

        S("🏓  PING-PONG DELAY",
          ("Tap 1 (s)", 0.01, 1.5, 0.3, "delay_time"),
          ("Tap 2 (s)", 0.01, 2.0, 0.6, "delay2_time"),
          ("Feedback", 0.0, 0.95, 0.3, "delay_feedback"),
          ("Mix", 0.0, 1.0, 0.0, "delay_mix"))

        S("🏛  REVERB",
          ("Mix", 0.0, 1.0, 0.0, "reverb_mix"),
          ("Decay", 0.1, 1.0, 0.5, "reverb_decay"))

        # Limiter
        lim = sec("🔒  LIMITER / LOUD MIC BYPASS")
        chk = ctk.CTkCheckBox(lim, text="Enable Multi-Stage Limiter",
                               fg_color=self.col_accent, hover_color=self.col_hover,
                               command=lambda: self.engine.params.update({"loud_mic_bypass": bool(chk.get())}))
        chk.pack(anchor="w", pady=(3, 4))
        sl(lim, "Threshold", 0.5, 1.0, 0.95, "limiter_threshold")
        sl(lim, "Pre-Gain", 1.0, 10.0, 1.0, "pre_limiter_gain")
        sl(lim, "Post-Gain", 1.0, 10.0, 1.0, "post_limiter_gain")
        sl(lim, "Headroom", 0.01, 0.15, 0.05, "adaptive_headroom")

        # SB
        sbsec = sec("🎵  SOUNDBOARD MIX")
        sl(sbsec, "SB Volume", 0.0, 2.0, 1.0, "sb_vol")
        sl(sbsec, "SB Speed", 0.1, 3.0, 1.0, "sb_speed")
        sl(sbsec, "SB Reverb", 0.0, 0.9, 0.0, "sb_reverb")
        cr = ctk.CTkFrame(sbsec, fg_color="transparent")
        cr.pack(fill="x")
        self.chk_loop = ctk.CTkCheckBox(cr, text="Loop", fg_color=self.col_accent, hover_color=self.col_hover,
                                         command=lambda: self.engine.params.update({"sb_loop": bool(self.chk_loop.get())}))
        self.chk_loop.pack(side="left", padx=6)
        self.chk_rev = ctk.CTkCheckBox(cr, text="Reverse", fg_color=self.col_accent, hover_color=self.col_hover,
                                        command=lambda: self.engine.params.update({"sb_reverse": bool(self.chk_rev.get())}))
        self.chk_rev.pack(side="left", padx=6)

        ctrl = ctk.CTkFrame(p, fg_color="transparent")
        ctrl.pack(fill="x", padx=5, pady=8)
        ctk.CTkButton(ctrl, text="↩ Undo", command=self._undo_fx, fg_color="#333", hover_color="#444", width=75).pack(side="left", padx=3)
        ctk.CTkButton(ctrl, text="↺ Reset", command=self._reset_fx, fg_color="#333", hover_color="#500", width=75).pack(side="left", padx=3)

        self.fx_mod_section = ctk.CTkFrame(p, fg_color="transparent")
        self.fx_mod_section.pack(fill="x")

    def _sl(self, parent, text, mn, mx, default, key, steps=300):
        if key == "_skip":
            return
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", pady=1)
        val = self.engine.params.get(key, default)
        lbl = ctk.CTkLabel(f, text=f"{text}: {val:.3g}", font=("Consolas", 10))
        lbl.pack(anchor="w")
        def _ch(v):
            self._push_history()
            self.engine.params[key] = float(v)
            lbl.configure(text=f"{text}: {float(v):.3g}")
        sl = ctk.CTkSlider(f, from_=mn, to=mx, number_of_steps=steps, command=_ch,
                            button_color=self.col_accent, progress_color=self.col_accent,
                            button_hover_color=self.col_hover)
        sl.set(val)
        sl.pack(fill="x")
        self.engine.params[key] = val
        self._slider_widgets[key] = (sl, lbl, text, mn, mx)

    def _push_history(self):
        snap = dict(self.engine.params)
        if self._fx_history and self._fx_history[-1] == snap:
            return
        if self._history_ptr < len(self._fx_history) - 1:
            self._fx_history = self._fx_history[:self._history_ptr + 1]
        self._fx_history.append(snap)
        if len(self._fx_history) > HISTORY_MAX:
            self._fx_history.pop(0)
        self._history_ptr = len(self._fx_history) - 1

    def _undo_fx(self):
        if self._history_ptr > 0:
            self._history_ptr -= 1
            self._restore_fx(self._fx_history[self._history_ptr])
            self.show_toast("Undo")

    def _reset_fx(self):
        if messagebox.askyesno("Reset FX", "Reset all FX to defaults?"):
            self._push_history()
            DEFAULTS = {"comp_ratio": 4.0, "comp_threshold": 0.7, "limiter_threshold": 0.95,
                        "comp_attack": 0.01, "comp_release": 0.1, "sb_vol": 1.0,
                        "sb_speed": 1.0, "reverb_decay": 0.5, "pre_limiter_gain": 1.0,
                        "post_limiter_gain": 1.0, "adaptive_headroom": 0.05}
            for key, (sl, lbl, text, mn, mx) in self._slider_widgets.items():
                val = DEFAULTS.get(key, 0.0)
                self.engine.params[key] = val
                sl.set(val)
                lbl.configure(text=f"{text}: {val:.3g}")
            self.show_toast("FX reset")

    def _restore_fx(self, snap):
        self.engine.params.update(snap)
        for k, (sl, lbl, t, mn, mx) in self._slider_widgets.items():
            if k in snap and isinstance(snap[k], (int, float)):
                sl.set(snap[k])
                lbl.configure(text=f"{t}: {float(snap[k]):.3g}")

    def _apply_preset(self, name):
        self._push_history()
        if self.presets.apply(name, self.engine.params):
            self._restore_fx(self.engine.params)
            self.show_toast(f"Preset: {name}")

    # ══════════════════════════════════════════════════════════════════════════
    # SOUNDBOARD
    # ══════════════════════════════════════════════════════════════════════════
    def _build_sb_tab(self):
        ctrl = ctk.CTkFrame(self.tab_sb, fg_color=self.col_card, corner_radius=8)
        ctrl.pack(fill="x", padx=6, pady=(6, 3))
        top = ctk.CTkFrame(ctrl, fg_color="transparent")
        top.pack(fill="x", padx=6, pady=6)
        ctk.CTkButton(top, text="⏹ STOP ALL", command=self.sb.stop_all,
                       fg_color="#500000", hover_color="#800000", height=30).pack(side="right", padx=3)
        ctk.CTkLabel(top, text="Search:", text_color=self.col_sub, font=("Consolas", 10)).pack(side="left")
        self.sb_search = ctk.StringVar()
        self.sb_search.trace_add("write", lambda *_: self._draw_soundboard())
        ctk.CTkEntry(top, textvariable=self.sb_search, width=180, height=28).pack(side="left", padx=4)

        self.sb_scroll = ctk.CTkScrollableFrame(self.tab_sb, fg_color="transparent")
        self.sb_scroll.pack(fill="both", expand=True, padx=3)
        self._draw_soundboard()

    def _draw_soundboard(self):
        for w in self.sb_scroll.winfo_children():
            w.destroy()
        cols = self.settings.get("sb_cols", 5)
        for c in range(cols):
            self.sb_scroll.columnconfigure(c, weight=1)
        query = getattr(self, "sb_search", None)
        q = query.get().lower() if query else ""
        ri = 0
        for i in range(SOUND_LIMIT):
            slot = self.sb.slots[i]
            name = slot.get("name", "Empty")
            tags = " ".join(slot.get("tags", []))
            if q and q not in name.lower() and q not in tags.lower():
                continue
            ci = (i % cols)
            self._draw_slot(i, slot, ri // cols, ci)
            ri += 1

    def _draw_slot(self, i, slot, row_i, col_i):
        col = slot.get("color") or self.col_card
        fr = ctk.CTkFrame(self.sb_scroll, fg_color=col, corner_radius=7,
                           border_width=1, border_color=self.col_card2)
        fr.grid(row=row_i, column=col_i, padx=2, pady=2, sticky="nsew")
        lname = ctk.CTkLabel(fr, text=slot.get("name", "Empty"),
                              font=("Consolas", 9), wraplength=108)
        lname.pack(fill="x", padx=3, pady=(3, 1))
        lhk = ctk.CTkLabel(fr, text=f"[{slot['hotkey']}]" if slot.get("hotkey") else "[Bind]",
                             font=("Consolas", 8), text_color=self.col_sub)
        lhk.pack()
        pvar = tk.DoubleVar(value=0)
        slot["progress_var"] = pvar
        ctk.CTkProgressBar(fr, variable=pvar, height=3,
                            progress_color=self.col_accent, fg_color="#111").pack(fill="x", padx=3, pady=1)
        ctk.CTkButton(fr, text="▶", height=26, font=("Consolas", 11, "bold"),
                       fg_color=self.col_accent, hover_color=self.col_hover,
                       command=lambda idx=i: self.sb.play(
                           idx, self.engine.params["sb_speed"], self.engine.params["sb_vol"],
                           bool(self.engine.params.get("sb_loop")), bool(self.engine.params.get("sb_reverse")))
                       ).pack(fill="x", padx=3, pady=2)
        row = ctk.CTkFrame(fr, fg_color="transparent")
        row.pack(fill="x", padx=2, pady=(0, 3))
        def _b(t, cmd, hc="#444"):
            ctk.CTkButton(row, text=t, width=24, height=18, font=("Consolas", 9),
                           fg_color="#222", hover_color=hc, command=cmd).pack(side="left", padx=1)
        _b("📂", lambda idx=i, l=lname: self._sb_load(idx, l))
        _b("⏹",  lambda idx=i: self.sb.stop_slot(idx))
        _b("●",  lambda idx=i, l=lname: self._sb_rec(idx, l), "#5a0000")
        _b("⌨",  lambda idx=i, l=lhk: self._sb_bind(idx, l))
        _b("🎨", lambda idx=i: self._sb_color(idx))
        _b("✕",  lambda idx=i, l=lname: self._sb_clear(idx, l), "#5a0000")

    def _sb_load(self, i, lbl):
        p = filedialog.askopenfilename(filetypes=[("Audio", "*.wav *.mp3 *.ogg *.flac")])
        if p and self.sb.load_file(i, p):
            lbl.configure(text=self.sb.slots[i]["name"])
            self.log.add(f"Slot {i}: {os.path.basename(p)}")

    def _sb_rec(self, i, lbl):
        if self.sb.is_recording:
            self.sb.is_recording = False
            self.sb.save_recording(self.sb.rec_target)
            lbl.configure(text=self.sb.slots[self.sb.rec_target]["name"])
            self.show_toast("Saved")
        else:
            self.sb.rec_buffer = []; self.sb.rec_target = i; self.sb.is_recording = True
            lbl.configure(text="● REC"); self.show_toast("Recording…", "#880000")

    def _sb_bind(self, idx, lbl):
        lbl.configure(text="…", text_color="yellow"); self.update()
        def _w():
            try:
                k = keyboard.read_key(); time.sleep(0.3)
                old = self.sb.slots[idx]["hotkey"]
                if old:
                    try: keyboard.remove_hotkey(old)
                    except Exception: pass
                self.sb.slots[idx]["hotkey"] = k
                keyboard.add_hotkey(k, lambda i=idx: self.sb.play(i, 1, 1, False, False))
                lbl.configure(text=f"[{k}]", text_color=self.col_sub)
                self.sb.save_config()
            except Exception:
                lbl.configure(text="Err", text_color="red")
        threading.Thread(target=_w, daemon=True).start()

    def _sb_color(self, idx):
        r = colorchooser.askcolor(title="Slot Color")
        if r and r[1]:
            self.sb.slots[idx]["color"] = r[1]; self.sb.save_config(); self._draw_soundboard()

    def _sb_clear(self, i, lbl):
        if self.sb.slots[i]["hotkey"]:
            try: keyboard.remove_hotkey(self.sb.slots[i]["hotkey"])
            except Exception: pass
        self.sb.slots[i] = {"data": None, "name": "Empty", "path": "", "hotkey": None,
                             "color": None, "tags": [], "trim_start": 0.0, "trim_end": 1.0}
        lbl.configure(text="Empty"); self.sb.save_config()

    # ══════════════════════════════════════════════════════════════════════════
    # SYNTH TAB
    # ══════════════════════════════════════════════════════════════════════════
    def _build_synth_tab(self):
        info = ctk.CTkFrame(self.tab_synth, fg_color=self.col_card, corner_radius=6)
        info.pack(fill="x", padx=6, pady=(6, 3))
        ctk.CTkLabel(info, text="Synthesizer → Output Cable",
                     font=("Consolas", 10), text_color=self.col_sub).pack(pady=5)

        st = ctk.CTkTabview(self.tab_synth, height=420,
                             segmented_button_selected_color=self.col_accent,
                             segmented_button_selected_hover_color=self.col_hover)
        st.pack(fill="both", expand=True, padx=5, pady=4)

        osc  = st.add("OSC 1")
        osc2 = st.add("OSC 2")
        env  = st.add("ENV")
        flt  = st.add("FILTER")
        fx   = st.add("FX")
        mod  = st.add("MOD")
        arp  = st.add("ARP")
        uni  = st.add("UNISON")

        # OSC1
        self._ss(osc, "Frequency (Hz)", 20, 2000, 440, "freq")
        self._ss(osc, "Detune (cents)", -100, 100, 0, "detune")
        self._ss(osc, "Portamento", 0.0, 2.0, 0.0, "portamento")
        self._ss(osc, "Sub-Osc Mix", 0.0, 1.0, 0.0, "sub_mix")
        self._ss(osc, "FM Frequency", 1, 2000, 440, "fm_freq")
        self._ss(osc, "FM Depth", 0.0, 8.0, 0.0, "fm_depth")
        self._ss(osc, "Noise Mix", 0.0, 1.0, 0.0, "noise_mix")
        ctk.CTkLabel(osc, text="Waveform:", font=("Consolas", 9), text_color=self.col_sub).pack(anchor="w", padx=8)
        self.osc_wave = ctk.CTkSegmentedButton(osc, values=["Sine","Square","Saw","Triangle","Pulse","SuperSaw"],
            selected_color=self.col_accent, selected_hover_color=self.col_hover,
            command=lambda v: self.synth_params.update({"wave": v}))
        self.osc_wave.set("Sine"); self.osc_wave.pack(fill="x", padx=8, pady=3)

        # OSC2
        self._ss(osc2, "Detune (cents)", -1200, 1200, 7, "osc2_detune")
        self._ss(osc2, "Mix", 0.0, 1.0, 0.0, "osc2_mix")
        ctk.CTkLabel(osc2, text="Waveform:", font=("Consolas", 9), text_color=self.col_sub).pack(anchor="w", padx=8)
        osc2w = ctk.CTkSegmentedButton(osc2, values=["Sine","Square","Saw","Triangle","Pulse"],
            selected_color=self.col_accent, selected_hover_color=self.col_hover,
            command=lambda v: self.synth_params.update({"osc2_wave": v}))
        osc2w.set("Saw"); osc2w.pack(fill="x", padx=8, pady=3)

        # ENV
        self._ss(env, "Attack (s)",  0.0, 3.0, 0.05, "env_a")
        self._ss(env, "Decay (s)",   0.0, 3.0, 0.2,  "env_d")
        self._ss(env, "Sustain",     0.0, 1.0, 0.7,  "env_s")
        self._ss(env, "Release (s)", 0.0, 5.0, 0.3,  "env_r")

        # FILTER
        ctk.CTkLabel(flt, text="One-pole lowpass filter", font=("Consolas", 9), text_color=self.col_sub).pack(padx=8, pady=4)
        self._ss(flt, "Cutoff (0=closed, 1=open)", 0.01, 1.0, 1.0, "filter_cutoff")
        self._ss(flt, "Filter LFO Depth", 0.0, 1.0, 0.0, "filter_lfo_depth")

        # FX
        self._ss(fx, "Distortion", 0.0, 10.0, 0.0, "fx_dist")
        self._ss(fx, "Bitcrush (bits)", 0, 16, 0, "fx_bitcrush")

        # MOD
        self._ss(mod, "LFO Rate (Hz)", 0.1, 20.0, 5.0, "mod_lfo_rate")
        self._ss(mod, "LFO Depth", 0.0, 1.0, 0.0, "mod_lfo_depth")
        ctk.CTkLabel(mod, text="LFO Target:", font=("Consolas", 9), text_color=self.col_sub).pack(anchor="w", padx=8)
        tgt = ctk.CTkOptionMenu(mod, values=["None","Pitch","Amp","Detune"],
                                 fg_color=self.col_card, button_color=self.col_accent,
                                 command=lambda v: self.synth_params.update({"mod_target": v}))
        tgt.set("None"); tgt.pack(fill="x", padx=8, pady=3)
        self._ss(mod, "Pan", -1.0, 1.0, 0.0, "mod_pan")
        self._ss(mod, "Master Volume", 0.0, 2.0, 0.5, "master_vol")

        # ARP tab — built-in pattern arp + BPM
        arp_on = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(arp, text="Enable Simple Arp", variable=arp_on,
                      progress_color=self.col_accent,
                      command=lambda: self.synth_params.update({"arp_on": arp_on.get()})
                      ).pack(padx=8, pady=6)
        self._ss(arp, "BPM", 20, 300, 120, "arp_bpm")
        ctk.CTkLabel(arp, text="Pattern:", font=("Consolas", 9), text_color=self.col_sub).pack(anchor="w", padx=8)
        arp_patterns = {
            "Major":   [0,4,7,12], "Minor":   [0,3,7,12],
            "Dom7":    [0,4,7,10], "Dim":     [0,3,6,9],
            "Aug":     [0,4,8,12], "Sus4":    [0,5,7,12],
            "Octaves": [0,12],     "5ths":    [0,7,12,19],
            "Full":    [0,2,4,5,7,9,11,12],
        }
        def _set_arp(v):
            self.synth.arp_notes = arp_patterns.get(v, [0,4,7,12])
        arp_cb = ctk.CTkComboBox(arp, values=list(arp_patterns.keys()),
                                  button_color=self.col_accent, border_color=self.col_card2,
                                  command=_set_arp)
        arp_cb.set("Major"); arp_cb.pack(fill="x", padx=8, pady=3)

        # UNISON
        ctk.CTkLabel(uni, text="Unison stacks detuned copies of OSC1", font=("Consolas", 9), text_color=self.col_sub).pack(padx=8, pady=4)
        self._ss(uni, "Voices (1=off)", 1, 7, 1, "unison")
        self._ss(uni, "Detune Spread (cents)", 0, 100, 10, "unison_detune")

        ctrl = ctk.CTkFrame(self.tab_synth, fg_color="transparent")
        ctrl.pack(fill="x", pady=6)
        self.btn_synth = ctk.CTkButton(ctrl, text="▶  START SYNTH", width=160,
                                        fg_color=self.col_accent, hover_color=self.col_hover,
                                        font=("Consolas", 12, "bold"), command=self._toggle_synth)
        self.btn_synth.pack(side="left", padx=10)

    def _ss(self, parent, text, mn, mx, default, key):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=6, pady=1)
        val = self.synth_params.get(key, default)
        lbl = ctk.CTkLabel(f, text=f"{text}: {val:.3g}", font=("Consolas", 10))
        lbl.pack(anchor="w")
        def _ch(v):
            self.synth_params[key] = float(v)
            lbl.configure(text=f"{text}: {float(v):.3g}")
        sl = ctk.CTkSlider(f, from_=mn, to=mx, number_of_steps=300, command=_ch,
                            button_color=self.col_accent, progress_color=self.col_accent)
        sl.set(val); sl.pack(fill="x")
        self.synth_params[key] = val

    def _toggle_synth(self):
        if not self.running:
            messagebox.showwarning("Engine Off", "Start the audio engine first.")
            return
        if self.synth.running:
            self.synth.env_stage = 4
            self.synth.release_lvl = 0.5
            self.synth.env_time = 0.0
            self.btn_synth.configure(text="▶  START SYNTH", fg_color=self.col_accent)
        else:
            self.synth.env_stage = 1
            self.synth.env_time  = 0.0
            self.synth.running   = True
            self.btn_synth.configure(text="■  STOP SYNTH", fg_color="#500000")

    # ══════════════════════════════════════════════════════════════════════════
    # SONG SEQUENCER TAB
    # ══════════════════════════════════════════════════════════════════════════
    def _build_seq_tab(self):
        top = ctk.CTkFrame(self.tab_seq, fg_color=self.col_card, corner_radius=8)
        top.pack(fill="x", padx=6, pady=(6, 3))
        ctk.CTkLabel(top, text="SONG SEQUENCER",
                     font=("Consolas", 13, "bold"), text_color=self.col_accent).pack(pady=6)
        ctk.CTkLabel(top,
                     text="Select a song and play it through the synth. Add songs as JSON in mods/songs/.",
                     font=("Consolas", 9), text_color=self.col_sub, wraplength=800).pack(pady=(0, 8))

        # Song picker
        pick = ctk.CTkFrame(self.tab_seq, fg_color="transparent")
        pick.pack(fill="x", padx=6, pady=4)
        ctk.CTkLabel(pick, text="Song:", font=("Consolas", 10)).pack(side="left", padx=(0, 6))
        self.seq_song_combo = ctk.CTkComboBox(pick, values=list(self.sequencer.songs.keys()),
                                               button_color=self.col_accent, border_color=self.col_card2,
                                               fg_color=self.col_card, width=300)
        self.seq_song_combo.pack(side="left")

        bpm_f = ctk.CTkFrame(pick, fg_color="transparent")
        bpm_f.pack(side="left", padx=12)
        self.seq_bpm_lbl = ctk.CTkLabel(bpm_f, text="BPM: 120", font=("Consolas", 10))
        self.seq_bpm_lbl.pack()
        self.seq_bpm_sl = ctk.CTkSlider(bpm_f, from_=20, to=300, number_of_steps=280,
                                         button_color=self.col_accent, progress_color=self.col_accent,
                                         command=self._update_bpm, width=150)
        self.seq_bpm_sl.set(120); self.seq_bpm_sl.pack()

        btn_row = ctk.CTkFrame(self.tab_seq, fg_color="transparent")
        btn_row.pack(fill="x", padx=6, pady=6)
        ctk.CTkButton(btn_row, text="▶  Play Song", command=self._seq_play,
                       fg_color=self.col_accent, hover_color=self.col_hover, width=120).pack(side="left", padx=4)
        ctk.CTkButton(btn_row, text="⏹  Stop", command=self.sequencer.stop,
                       fg_color="#500000", hover_color="#800000", width=80).pack(side="left", padx=4)
        ctk.CTkButton(btn_row, text="↺  Reload Songs", command=self._reload_songs,
                       fg_color="#333", hover_color="#444", width=120).pack(side="left", padx=4)
        ctk.CTkButton(btn_row, text="📂  Open Songs Folder", command=self._open_songs_folder,
                       fg_color="#333", hover_color="#444", width=140).pack(side="left", padx=4)

        # Song list display
        self.seq_list_frame = ctk.CTkScrollableFrame(self.tab_seq, fg_color="transparent")
        self.seq_list_frame.pack(fill="both", expand=True, padx=4)
        self._draw_song_list()

        # JSON editor for new song
        edit_hdr = ctk.CTkFrame(self.tab_seq, fg_color=self.col_card2, corner_radius=6)
        edit_hdr.pack(fill="x", padx=6, pady=(4, 0))
        ctk.CTkLabel(edit_hdr, text="➕  Create / Edit Song (JSON)", font=("Consolas", 11, "bold"),
                     text_color=self.col_accent).pack(anchor="w", padx=8, pady=4)

        self.seq_name_entry = ctk.CTkEntry(edit_hdr, placeholder_text="Song name…", width=200)
        self.seq_name_entry.pack(side="left", padx=8, pady=(0, 6))
        ctk.CTkButton(edit_hdr, text="💾 Save to mods/songs/",
                       command=self._seq_save_song,
                       fg_color=self.col_accent, hover_color=self.col_hover, height=28).pack(side="left", padx=4)

        self.seq_editor = ctk.CTkTextbox(self.tab_seq, height=120, font=("Consolas", 10))
        self.seq_editor.pack(fill="x", padx=6, pady=(3, 6))
        self.seq_editor.insert("end", json.dumps({
            "name": "My Song", "loop": True,
            "steps": [
                {"note": "C4", "dur": 0.25, "vel": 1.0, "rest": False},
                {"note": "E4", "dur": 0.25, "vel": 0.9, "rest": False},
                {"note": "G4", "dur": 0.25, "vel": 0.8, "rest": False},
                {"note": "C4", "dur": 0.25, "vel": 0.0, "rest": True},
            ]
        }, indent=2))

    def _update_bpm(self, v):
        v = int(v)
        self.seq_bpm_lbl.configure(text=f"BPM: {v}")
        self.synth_params["arp_bpm"] = float(v)
        self.settings["seq_bpm"] = v
        self._save_settings()

    def _seq_play(self):
        if not self.running:
            messagebox.showwarning("Engine Off", "Start the audio engine first.")
            return
        name = self.seq_song_combo.get()
        if self.sequencer.play_song(name):
            if not self.synth.running:
                self._toggle_synth()
            self.show_toast(f"♫  {name}")
            self.log.add(f"Sequencer: playing {name}")
        else:
            self.show_toast("Song not found", "#880000")

    def _reload_songs(self):
        self.sequencer.reload_songs()
        self.SONGS = self.sequencer.songs
        names = list(self.sequencer.songs.keys())
        self.seq_song_combo.configure(values=names)
        self.combo_quick_song.configure(values=names)
        self._draw_song_list()
        self.show_toast(f"Loaded {len(names)} songs")
        self.log.add(f"Songs reloaded: {len(names)}")

    def _open_songs_folder(self):
        try:
            p = os.path.abspath(SONGS_FOLDER)
            if sys.platform == "win32":   os.startfile(p)
            elif sys.platform == "darwin": os.system(f'open "{p}"')
            else:                          os.system(f'xdg-open "{p}"')
        except Exception:
            pass

    def _seq_save_song(self):
        name = self.seq_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Name", "Enter a song name.")
            return
        txt = self.seq_editor.get("1.0", "end").strip()
        try:
            data = json.loads(txt)
            data["name"] = name
            fn = name.replace(" ", "_").replace("/", "-") + ".json"
            with open(os.path.join(SONGS_FOLDER, fn), "w") as f:
                json.dump(data, f, indent=2)
            self._reload_songs()
            self.show_toast(f"Saved: {name}")
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON Error", str(e))

    def _draw_song_list(self):
        for w in self.seq_list_frame.winfo_children():
            w.destroy()
        for name, song in self.sequencer.songs.items():
            row = ctk.CTkFrame(self.seq_list_frame, fg_color=self.col_card, corner_radius=6)
            row.pack(fill="x", pady=2, padx=3)
            is_builtin = name in BUILTIN_SONGS
            steps = len(song.get("steps", []))
            ctk.CTkLabel(row, text=f"♫  {name}", font=("Consolas", 10, "bold")).pack(side="left", padx=8, pady=5)
            ctk.CTkLabel(row, text=f"[{'built-in' if is_builtin else 'custom'}]  {steps} steps",
                         font=("Consolas", 9), text_color=self.col_sub).pack(side="left")
            ctk.CTkButton(row, text="▶", width=34, height=24, fg_color=self.col_accent,
                           hover_color=self.col_hover,
                           command=lambda n=name: self._quick_play_song(n)).pack(side="right", padx=4, pady=3)

    # ══════════════════════════════════════════════════════════════════════════
    # MODS TAB
    # ══════════════════════════════════════════════════════════════════════════
    def _build_mods_tab(self):
        top = ctk.CTkFrame(self.tab_mods, fg_color="transparent")
        top.pack(fill="x", padx=6, pady=5)
        ctk.CTkButton(top, text="↺ Reload", command=self._reload_mods,
                       fg_color=self.col_accent, hover_color=self.col_hover, height=30).pack(side="left", padx=3)
        ctk.CTkButton(top, text="📂 Mods Folder", command=self._open_mods_folder,
                       fg_color="#333", hover_color="#444", height=30).pack(side="left", padx=3)
        ctk.CTkButton(top, text="📖 SDK Readme", command=self._open_sdk,
                       fg_color="#333", hover_color="#444", height=30).pack(side="left", padx=3)
        ctk.CTkButton(top, text="🔄 Regen README", command=lambda: (_write_sdk_readme(), self.show_toast("README updated")),
                       fg_color="#333", hover_color="#444", height=30).pack(side="left", padx=3)

        self.mod_list_frame = ctk.CTkScrollableFrame(self.tab_mods, fg_color="transparent")
        self.mod_list_frame.pack(fill="both", expand=True, padx=3)
        self._draw_mods()

    def _draw_mods(self):
        for w in self.mod_list_frame.winfo_children():
            w.destroy()
        files = [f for f in os.listdir(MODS_FOLDER) if f.endswith(".py")]
        if not files:
            ctk.CTkLabel(self.mod_list_frame,
                         text="No mods found.\nDrop a .py file in mods/ and click Reload.",
                         text_color=self.col_sub, font=("Consolas", 11)).pack(pady=40)
            return
        for fn in files:
            row = ctk.CTkFrame(self.mod_list_frame, fg_color=self.col_card, corner_radius=8)
            row.pack(fill="x", pady=2, padx=3)
            mod_obj = self.mod_loader.loaded.get(fn[:-3])
            meta = getattr(mod_obj, "META", {})
            is_on = self.mod_loader.states.get(fn, True)
            var = ctk.BooleanVar(value=is_on)
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, padx=8, pady=5)
            ctk.CTkLabel(info, text=f"{meta.get('label', fn[:-3])}  [{meta.get('category','?').upper()}]  v{meta.get('version','?')}",
                         font=("Consolas", 11, "bold")).pack(anchor="w")
            ctk.CTkLabel(info, text=f"by {meta.get('author','?')}  —  {fn}",
                         font=("Consolas", 9), text_color=self.col_sub).pack(anchor="w")
            if meta.get("desc"):
                ctk.CTkLabel(info, text=meta["desc"], font=("Consolas", 9),
                             text_color=self.col_sub, wraplength=500).pack(anchor="w")
            ctk.CTkSwitch(row, text="", variable=var, progress_color=self.col_accent, width=48,
                           command=lambda f=fn, v=var: self._toggle_mod(f, v.get())).pack(side="right", padx=8)

    def _toggle_mod(self, fn, enabled):
        self.mod_loader.states[fn] = enabled; self.mod_loader.save()
        if not enabled:
            mod = self.mod_loader.loaded.get(fn[:-3])
            if mod and hasattr(mod, "on_disable"):
                try: mod.on_disable(self)
                except Exception: pass
        self.engine.mods = self.mod_loader.load_mods()
        self._init_mod_params(); self._rebuild_mod_sections()
        self.log.add(f"Mod {fn} {'on' if enabled else 'off'}")

    def _reload_mods(self):
        self.engine.mods = self.mod_loader.load_mods()
        self._init_mod_params(); self._rebuild_mod_sections(); self._draw_mods()
        self.show_toast("Mods reloaded"); self.log.add("Mods reloaded")

    def _open_mods_folder(self):
        try:
            p = os.path.abspath(MODS_FOLDER)
            if sys.platform == "win32":   os.startfile(p)
            elif sys.platform == "darwin": os.system(f'open "{p}"')
            else:                          os.system(f'xdg-open "{p}"')
        except Exception: pass

    def _open_sdk(self):
        p = os.path.abspath(os.path.join(MODS_FOLDER, "SDK_README.md"))
        try:
            if sys.platform == "win32":   os.startfile(p)
            elif sys.platform == "darwin": os.system(f'open "{p}"')
            else:                          os.system(f'xdg-open "{p}"')
        except Exception:
            messagebox.showinfo("SDK README", f"Open: {p}")

    def _init_mod_params(self):
        for mod in self.engine.mods:
            for ctrl in getattr(mod, "CONTROLS", []):
                k = ctrl.get("key","")
                if k and k not in self.engine.params:
                    self.engine.params[k] = ctrl.get("default", 0)

    def _rebuild_mod_sections(self):
        for w in self.fx_mod_section.winfo_children():
            w.destroy()
        for mod in self.engine.mods:
            ctrls = getattr(mod, "CONTROLS", [])
            if not ctrls: continue
            meta  = getattr(mod, "META", {})
            label = meta.get("label", meta.get("name","Mod"))
            f = ctk.CTkFrame(self.fx_mod_section, fg_color=self.col_card, corner_radius=8)
            f.pack(fill="x", padx=5, pady=3)
            ctk.CTkLabel(f, text=f"🔌  {label.upper()}",
                         font=("Consolas", 11, "bold"), text_color=self.col_accent).pack(anchor="w", padx=8, pady=4)
            body = ctk.CTkFrame(f, fg_color="transparent")
            body.pack(fill="x", padx=8, pady=(0, 6))
            for c in ctrls:
                key = c.get("key",""); lbl = c.get("label", key); unit = c.get("unit","")
                ct  = c.get("type","slider"); dflt = c.get("default", 0)
                if ct == "slider":
                    mn, mx = c.get("min",0), c.get("max",1)
                    val = self.engine.params.get(key, dflt)
                    cf  = ctk.CTkFrame(body, fg_color="transparent"); cf.pack(fill="x", pady=1)
                    lw  = ctk.CTkLabel(cf, text=f"{lbl}: {val:.3g}{unit}", font=("Consolas",10)); lw.pack(anchor="w")
                    def _ch(v, k=key, l=lw, t=lbl, u=unit):
                        self.engine.params[k]=float(v); l.configure(text=f"{t}: {float(v):.3g}{u}")
                    sl = ctk.CTkSlider(cf, from_=mn, to=mx, number_of_steps=200, command=_ch,
                                       button_color=self.col_accent, progress_color=self.col_accent)
                    sl.set(val); sl.pack(fill="x")
                elif ct == "toggle":
                    v = ctk.BooleanVar(value=self.engine.params.get(key, dflt))
                    ctk.CTkSwitch(body, text=lbl, variable=v, progress_color=self.col_accent,
                                  command=lambda k=key,vv=v: self.engine.params.update({k: vv.get()})
                                  ).pack(anchor="w", pady=2)
                elif ct == "dropdown":
                    opts = c.get("options", [])
                    val  = self.engine.params.get(key, dflt)
                    om   = ctk.CTkOptionMenu(body, values=opts, fg_color=self.col_card,
                                              button_color=self.col_accent,
                                              command=lambda v,k=key: self.engine.params.update({k:v}))
                    om.set(str(val)); om.pack(fill="x", pady=2)

    # ══════════════════════════════════════════════════════════════════════════
    # TTS TAB — live injection, no files
    # ══════════════════════════════════════════════════════════════════════════
    def _build_tts_tab(self):
        outer = ctk.CTkFrame(self.tab_tts, fg_color=self.col_card, corner_radius=10)
        outer.pack(fill="both", expand=True, padx=18, pady=18)
        ctk.CTkLabel(outer, text="TEXT  TO  SPEECH",
                     font=ctk.CTkFont(family="Courier New", size=16, weight="bold"),
                     text_color=self.col_accent).pack(pady=(18, 3))
        ctk.CTkLabel(outer, text="Live injection into your virtual microphone — no temp files.",
                     font=("Consolas", 9), text_color=self.col_sub).pack(pady=(0, 12))

        self.tts_box = ctk.CTkTextbox(outer, height=90, font=("Consolas", 12))
        self.tts_box.pack(fill="x", padx=18, pady=4)

        vrow = ctk.CTkFrame(outer, fg_color="transparent"); vrow.pack(fill="x", padx=18, pady=6)
        ctk.CTkLabel(vrow, text="Voice:", font=("Consolas", 10), text_color=self.col_sub).pack(side="left", padx=(0,6))
        self.tts_voice_combo = ctk.CTkComboBox(vrow, width=300, button_color=self.col_accent,
                                                border_color=self.col_card2, fg_color="#111")
        self.tts_voice_combo.pack(side="left")

        rrow = ctk.CTkFrame(outer, fg_color="transparent"); rrow.pack(fill="x", padx=18)
        self._tts_rate_lbl = ctk.CTkLabel(rrow, text=f"Rate: {self.settings.get('tts_rate',150)}", font=("Consolas",10))
        self._tts_rate_lbl.pack(anchor="w")
        self._tts_rate_sl = ctk.CTkSlider(rrow, from_=50, to=350, button_color=self.col_accent,
                                            progress_color=self.col_accent, command=self._upd_tts_rate)
        self._tts_rate_sl.set(self.settings.get("tts_rate", 150)); self._tts_rate_sl.pack(fill="x")
        self.tts.rate = int(self.settings.get("tts_rate", 150))

        btns = ctk.CTkFrame(outer, fg_color="transparent"); btns.pack(pady=10)
        ctk.CTkButton(btns, text="▶  SPEAK", command=self._do_tts,
                       fg_color=self.col_accent, hover_color=self.col_hover,
                       width=120, font=("Consolas",13,"bold")).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="⏹", command=lambda: self.sb.tts_queue.clear(),
                       fg_color="#500000", hover_color="#800000", width=50).pack(side="left", padx=4)

        if not HAS_TTS:
            ctk.CTkLabel(outer, text="⚠  pyttsx3 not installed — TTS unavailable.\nRun: pip install pyttsx3",
                         text_color="#FF4400", font=("Consolas", 10)).pack(pady=8)
        else:
            threading.Thread(target=self._load_tts_voices, daemon=True).start()

    def _load_tts_voices(self):
        voices = self.tts.get_voices()
        names  = ["System Default"] + [v.name for v in voices]
        self.tts_voice_combo.configure(values=names)
        self.tts_voice_combo.set(names[0])

    def _upd_tts_rate(self, v):
        self.tts.rate = int(v)
        self._tts_rate_lbl.configure(text=f"Rate: {int(v)}")
        self.settings["tts_rate"] = int(v); self._save_settings()

    def _do_tts(self):
        if not HAS_TTS:
            messagebox.showwarning("TTS", "Install pyttsx3: pip install pyttsx3")
            return
        text = self.tts_box.get("1.0", "end").strip()
        if not text:
            return
        # Set selected voice
        sel = self.tts_voice_combo.get()
        for v in self.tts.get_voices():
            if v.name == sel:
                self.tts.voice_id = v.id
                break
        self.tts.speak(text)
        self.show_toast("TTS queued")

    # ══════════════════════════════════════════════════════════════════════════
    # PRESETS TAB
    # ══════════════════════════════════════════════════════════════════════════
    def _build_presets_tab(self):
        top = ctk.CTkFrame(self.tab_preset, fg_color="transparent")
        top.pack(fill="x", padx=6, pady=6)
        self.preset_name = ctk.CTkEntry(top, placeholder_text="Preset name…", width=200)
        self.preset_name.pack(side="left", padx=3)
        ctk.CTkButton(top, text="💾 Save FX as Preset", command=self._save_preset,
                       fg_color=self.col_accent, hover_color=self.col_hover, height=30).pack(side="left", padx=3)

        self.preset_scroll = ctk.CTkScrollableFrame(self.tab_preset, fg_color="transparent")
        self.preset_scroll.pack(fill="both", expand=True, padx=3)
        self._draw_presets()

    def _draw_presets(self):
        for w in self.preset_scroll.winfo_children():
            w.destroy()
        for name in self.presets.presets:
            row = ctk.CTkFrame(self.preset_scroll, fg_color=self.col_card, corner_radius=7)
            row.pack(fill="x", pady=2, padx=3)
            is_def = name in DEFAULT_PRESETS
            ctk.CTkLabel(row, text=name, font=("Consolas", 11, "bold")).pack(side="left", padx=10, pady=6)
            ctk.CTkLabel(row, text="[built-in]" if is_def else "[custom]",
                         font=("Consolas", 9), text_color=self.col_sub).pack(side="left")
            ctk.CTkButton(row, text="▶ Load", width=68, height=24,
                           fg_color=self.col_accent, hover_color=self.col_hover,
                           command=lambda n=name: self._apply_preset(n)).pack(side="right", padx=3, pady=4)
            if not is_def:
                ctk.CTkButton(row, text="✕", width=28, height=24,
                               fg_color="#500000", hover_color="#800000",
                               command=lambda n=name: self._del_preset(n)).pack(side="right", padx=3, pady=4)

    def _save_preset(self):
        name = self.preset_name.get().strip()
        if not name:
            messagebox.showwarning("Preset", "Enter a name.")
            return
        self.presets.capture(name, self.engine.params)
        self.combo_preset.configure(values=list(self.presets.presets.keys()))
        self._draw_presets(); self.show_toast(f"Saved: {name}")

    def _del_preset(self, name):
        if messagebox.askyesno("Delete", f"Delete '{name}'?"):
            self.presets.delete(name); self._draw_presets()
            self.combo_preset.configure(values=list(self.presets.presets.keys()))

    # ══════════════════════════════════════════════════════════════════════════
    # LOG TAB
    # ══════════════════════════════════════════════════════════════════════════
    def _build_log_tab(self):
        top = ctk.CTkFrame(self.tab_log, fg_color="transparent")
        top.pack(fill="x", padx=6, pady=4)
        ctk.CTkButton(top, text="Clear", command=self._clear_log,
                       fg_color="#333", hover_color="#444", width=60, height=26).pack(side="right")
        self.log_box = ctk.CTkTextbox(self.tab_log, font=("Consolas", 10), state="disabled",
                                       fg_color="#080808")
        self.log_box.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        def _add(e):
            try:
                self.log_box.configure(state="normal")
                self.log_box.insert("end", e + "\n"); self.log_box.see("end")
                self.log_box.configure(state="disabled")
            except Exception:
                pass
        self.log.on_entry(_add)

    def _clear_log(self):
        self.log.entries.clear()
        try:
            self.log_box.configure(state="normal"); self.log_box.delete("1.0","end")
            self.log_box.configure(state="disabled")
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════════════════════
    # SETTINGS TAB
    # ══════════════════════════════════════════════════════════════════════════
    def _build_settings_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_set, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        f = ctk.CTkFrame(scroll, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=20, pady=10)

        def sec(t):
            ctk.CTkFrame(f, height=1, fg_color=self.col_border).pack(fill="x", pady=(12, 4))
            ctk.CTkLabel(f, text=t, font=("Consolas", 12, "bold"),
                         text_color=self.col_accent).pack(anchor="w", pady=(0, 4))

        def toggle(txt, key, cmd=None):
            var = ctk.BooleanVar(value=self.settings.get(key, False))
            def _t():
                self.settings[key] = var.get(); self._save_settings()
                if cmd: cmd()
            ctk.CTkSwitch(f, text=txt, variable=var, command=_t,
                           progress_color=self.col_accent,
                           font=("Consolas", 10)).pack(anchor="w", pady=3)

        def slider(lbl_text, key, mn, mx, default, steps=100, fmt="{:.0f}"):
            val  = self.settings.get(key, default)
            lbl  = ctk.CTkLabel(f, text=f"{lbl_text}: {fmt.format(val)}",
                                  font=("Consolas", 10), text_color=self.col_sub)
            lbl.pack(anchor="w")
            def _ch(v):
                self.settings[key] = float(v) if '.' in fmt else int(v)
                lbl.configure(text=f"{lbl_text}: {fmt.format(float(v))}")
                self._save_settings()
            sl = ctk.CTkSlider(f, from_=mn, to=mx, number_of_steps=steps,
                                command=_ch, button_color=self.col_accent,
                                progress_color=self.col_accent)
            sl.set(val); sl.pack(fill="x", pady=(0, 4))

        # ── Audio ──────────────────────────────────────────────────────────
        sec("🔊  AUDIO")
        slider("Buffer Size", "buffer_size", 64, 4096, 1024, 64, "{:.0f}")
        toggle("High Process Priority", "high_priority", self._apply_system_settings)

        # ── Window ─────────────────────────────────────────────────────────
        sec("🖥  WINDOW")
        toggle("Always on Top", "always_on_top", self._apply_system_settings)
        toggle("Minimize to Tray on Close", "minimize_to_tray")
        slider("Opacity", "opacity", 0.1, 1.0, 1.0, 100, "{:.2f}")

        # ── Appearance ─────────────────────────────────────────────────────
        sec("🎨  APPEARANCE")
        th_row = ctk.CTkFrame(f, fg_color="transparent"); th_row.pack(fill="x", pady=3)
        ctk.CTkLabel(th_row, text="Theme:", font=("Consolas", 10)).pack(side="left", padx=(0, 6))
        self.combo_theme = ctk.CTkComboBox(th_row, values=list(self.THEMES.keys()),
                                            button_color=self.col_accent,
                                            border_color=self.col_card2,
                                            command=self._change_theme)
        self.combo_theme.set(self.settings.get("theme", "Crimson"))
        self.combo_theme.pack(side="left")
        ctk.CTkButton(th_row, text="📂 Themes Folder", command=self._open_themes_folder,
                       fg_color=self.col_card2, hover_color=self.col_card,
                       height=26, corner_radius=8).pack(side="left", padx=8)

        # ── VU Meters ──────────────────────────────────────────────────────
        sec("📊  VU METERS")
        toggle("Colour Bands (green / yellow / red)", "vu_color_bands")

        # ── Soundboard ─────────────────────────────────────────────────────
        sec("🎵  SOUNDBOARD")
        slider("Columns", "sb_cols", 2, 10, 5, 8, "{:.0f}")

        # ── System ─────────────────────────────────────────────────────────
        sec("⚙  SYSTEM")
        startup_var = ctk.BooleanVar(value=self.settings.get("startup", False))
        ctk.CTkSwitch(f, text="Launch on Windows Startup", variable=startup_var,
                      command=lambda: self._toggle_startup(startup_var.get()),
                      progress_color=self.col_accent,
                      font=("Consolas", 10)).pack(anchor="w", pady=3)

        # ── EXPERIMENTAL ───────────────────────────────────────────────────
        ctk.CTkFrame(f, height=1, fg_color=self.col_border).pack(fill="x", pady=(16, 0))

        exp_hdr = ctk.CTkFrame(f, fg_color="#1a0000", corner_radius=8)
        exp_hdr.pack(fill="x", pady=(0, 6))
        warn_row = ctk.CTkFrame(exp_hdr, fg_color="transparent")
        warn_row.pack(fill="x", padx=12, pady=(10, 4))
        ctk.CTkLabel(warn_row, text="⚠  EXPERIMENTAL FEATURES",
                     font=("Consolas", 12, "bold"),
                     text_color="#ff4444").pack(side="left")
        ctk.CTkLabel(exp_hdr,
                     text="These features are unstable, unfinished, or may cause audio glitches, crashes,\n"
                          "or unexpected behaviour. Enable at your own risk. Restart the engine after toggling.",
                     font=("Consolas", 9), text_color="#cc6666",
                     justify="left").pack(anchor="w", padx=12, pady=(0, 10))

        # helper that writes directly to engine.params so features work live
        def exp_toggle(label, key, note=""):
            var = ctk.BooleanVar(value=self.engine.params.get(key, False))
            row = ctk.CTkFrame(f, fg_color="transparent")
            row.pack(fill="x", pady=2)
            def _t():
                self.engine.params[key] = var.get()
            sw = ctk.CTkSwitch(row, text=label, variable=var, command=_t,
                                progress_color="#cc3333",
                                font=("Consolas", 10))
            sw.pack(side="left")
            if note:
                ctk.CTkLabel(row, text=f"  ·  {note}",
                              font=("Consolas", 8), text_color="#666").pack(side="left")

        def exp_slider(lbl_text, key, mn, mx, default, steps=100, fmt="{:.2f}"):
            val = self.engine.params.get(key, default)
            lbl = ctk.CTkLabel(f, text=f"      {lbl_text}: {fmt.format(val)}",
                                font=("Consolas", 9), text_color="#aa5555")
            lbl.pack(anchor="w")
            def _ch(v):
                self.engine.params[key] = float(v)
                lbl.configure(text=f"      {lbl_text}: {fmt.format(float(v))}")
            sl = ctk.CTkSlider(f, from_=mn, to=mx, number_of_steps=steps,
                                command=_ch,
                                button_color="#cc3333", progress_color="#cc3333")
            sl.set(val); sl.pack(fill="x", padx=(20, 0), pady=(0, 6))

        # ── Desktop Echo ─────────────────────────────
        ctk.CTkLabel(f, text="🖥  Desktop Echo",
                     font=("Consolas", 11, "bold"),
                     text_color="#dd4444").pack(anchor="w", pady=(8, 2))
        ctk.CTkLabel(f, text="Routes your desktop audio (Spotify, YouTube, games…) through your virtual mic output.\n"
                              "Set 'Desktop Echo Input' in the sidebar to CABLE Output or any loopback device.",
                     font=("Consolas", 9), text_color="#885555",
                     justify="left").pack(anchor="w", padx=4, pady=(0, 4))

        def _toggle_echo_exp():
            enabled = self.engine.params.get("exp_echo_enabled", False)
            if self.running:
                if self.loopback_stream:
                    try: self.loopback_stream.stop(); self.loopback_stream.close()
                    except Exception: pass
                    self.loopback_stream = None
                if enabled:
                    self._start_loopback(int(self.settings.get("buffer_size", 1024)))

        exp_toggle("Enable Desktop Echo", "exp_echo_enabled", "restart engine after enabling")
        exp_slider("Echo Volume",  "exp_echo_vol",  0.0, 2.0, 0.85)
        exp_slider("Dry / Wet",    "exp_echo_mix",  0.0, 1.0, 1.0)

        # ── Noise Suppression ─────────────────────────
        ctk.CTkLabel(f, text="🔇  Spectral Noise Suppression",
                     font=("Consolas", 11, "bold"),
                     text_color="#dd4444").pack(anchor="w", pady=(8, 2))
        ctk.CTkLabel(f, text="FFT-based noise floor subtraction. May introduce metallic artefacts at high strength.",
                     font=("Consolas", 9), text_color="#885555").pack(anchor="w", padx=4, pady=(0, 4))
        exp_toggle("Enable Noise Suppression", "exp_noise_suppress", "adds CPU load")
        exp_slider("Strength", "exp_ns_strength", 0.0, 1.0, 0.6)

        # ── Transient Enhancer ────────────────────────
        ctk.CTkLabel(f, text="⚡  Transient Enhancer",
                     font=("Consolas", 11, "bold"),
                     text_color="#dd4444").pack(anchor="w", pady=(8, 2))
        ctk.CTkLabel(f, text="Sharpens attack transients — makes voice punchier. Can clip at high amounts.",
                     font=("Consolas", 9), text_color="#885555").pack(anchor="w", padx=4, pady=(0, 4))
        exp_toggle("Enable Transient Enhancer", "exp_transient_enhance")
        exp_slider("Amount", "exp_transient_amount", 0.0, 1.0, 0.5)

        # ── Stereo Widener ────────────────────────────
        ctk.CTkLabel(f, text="↔  Stereo Widener",
                     font=("Consolas", 11, "bold"),
                     text_color="#dd4444").pack(anchor="w", pady=(8, 2))
        ctk.CTkLabel(f, text="Mid-side width expansion. May cause mono compatibility issues.",
                     font=("Consolas", 9), text_color="#885555").pack(anchor="w", padx=4, pady=(0, 4))
        exp_toggle("Enable Stereo Widener", "exp_stereo_width")
        exp_slider("Width Amount", "exp_stereo_width_amt", 0.0, 1.0, 0.5)

        # ── Voice Morpher ─────────────────────────────
        ctk.CTkLabel(f, text="🎭  Voice Morpher",
                     font=("Consolas", 11, "bold"),
                     text_color="#dd4444").pack(anchor="w", pady=(8, 2))
        ctk.CTkLabel(f, text="Crude formant-shift morpher. Sounds robotic at extremes — intentionally experimental.",
                     font=("Consolas", 9), text_color="#885555").pack(anchor="w", padx=4, pady=(0, 4))
        exp_toggle("Enable Voice Morpher", "exp_voice_morph", "may stutter")
        exp_slider("Gender Shift  (−1 masc → +1 fem)", "exp_morph_gender", -1.0, 1.0, 0.0, 100, "{:.2f}")

        # ── Harmonic Exciter ──────────────────────────
        ctk.CTkLabel(f, text="✨  Harmonic Exciter",
                     font=("Consolas", 11, "bold"),
                     text_color="#dd4444").pack(anchor="w", pady=(8, 2))
        ctk.CTkLabel(f, text="Adds soft-clipped upper harmonics above 4 kHz for presence and air.",
                     font=("Consolas", 9), text_color="#885555").pack(anchor="w", padx=4, pady=(0, 4))
        exp_toggle("Enable Harmonic Exciter", "exp_exciter")
        exp_slider("Exciter Amount", "exp_exciter_amount", 0.0, 1.0, 0.4)

        # ── Auto-Ducker ───────────────────────────────
        ctk.CTkLabel(f, text="🔽  Auto-Ducker",
                     font=("Consolas", 11, "bold"),
                     text_color="#dd4444").pack(anchor="w", pady=(8, 2))
        ctk.CTkLabel(f, text="Ducks mic level when soundboard is playing. Useful for live commentary over sounds.",
                     font=("Consolas", 9), text_color="#885555").pack(anchor="w", padx=4, pady=(0, 4))
        exp_toggle("Enable Auto-Ducker", "exp_gate_duck")
        exp_slider("Duck Depth",  "exp_gate_duck_depth", 0.0, 1.0, 0.7)
        exp_slider("Duck Speed",  "exp_gate_duck_speed", 0.01, 0.3, 0.05, 100, "{:.3f}")

        # ── About ──────────────────────────────────────────────────────────
        ctk.CTkFrame(f, height=1, fg_color=self.col_border).pack(fill="x", pady=(16, 4))
        ctk.CTkLabel(f, text=f"{APP_NAME} {VERSION}\nOpen Source — MIT License\nModding SDK: mods/SDK_README.md",
                     font=("Consolas", 9), text_color=self.col_sub, justify="left").pack(anchor="w", pady=4)

    def _change_theme(self, name):
        self.settings["theme"] = name; self._save_settings()
        self._apply_theme(); self._apply_dynamic_theme(name)

    def _open_themes_folder(self):
        try:
            p = os.path.abspath(THEMES_FOLDER)
            if sys.platform == "win32":   os.startfile(p)
            elif sys.platform == "darwin": os.system(f'open "{p}"')
            else:                          os.system(f'xdg-open "{p}"')
        except Exception: pass

    # ══════════════════════════════════════════════════════════════════════════
    # AUDIO ENGINE CONTROL
    # ══════════════════════════════════════════════════════════════════════════
    def _toggle_startup(self, val):
        self.settings["startup"] = val; self._save_settings()
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_ALL_ACCESS)
            if val:
                exe = sys.executable
                v   = f'"{exe}" "{__file__}"' if not getattr(sys,"frozen",False) else f'"{exe}"'
                winreg.SetValueEx(key, "VLAB", 0, winreg.REG_SZ, v)
            else:
                try: winreg.DeleteValue(key, "VLAB")
                except Exception: pass
        except Exception as e:
            self.log.add(f"Startup: {e}", "WARN")

    def _toggle_audio(self):
        if self.running:
            self.running = False; self.mon_thread_run = False
            for s in [self.stream, self.monitor_stream, self.loopback_stream]:
                if s:
                    try: s.stop(); s.close()
                    except Exception: pass
            self.monitor_stream  = None
            self.loopback_stream = None
            self.btn_start.configure(text="▶  START ENGINE", fg_color=self.col_accent)
            self.log.add("Engine stopped"); return

        try:
            devs  = sd.query_devices()
            i_idx = next(i for i, d in enumerate(devs) if d["name"] == self.in_dev.get())
            o_idx = next(i for i, d in enumerate(devs) if d["name"] == self.out_dev.get())
            bs    = self.settings.get("buffer_size", 1024)

            if bool(self.sw_mon.get()):
                m_idx = next(i for i, d in enumerate(devs) if d["name"] == self.mon_dev.get())
                self.monitor_stream = sd.OutputStream(device=m_idx, samplerate=SR,
                                                       blocksize=bs, channels=CHANNELS, dtype="float32")
                self.monitor_stream.start()
                self.mon_q.queue.clear(); self.mon_thread_run = True
                threading.Thread(target=self._mon_worker, daemon=True).start()
                self.engine.monitoring = True
            else:
                self.engine.monitoring = False

            self.stream = sd.Stream(device=(i_idx, o_idx), samplerate=SR, blocksize=bs,
                                    channels=CHANNELS, callback=self._audio_cb)
            self.stream.start(); self.running = True
            if self.engine.params.get("exp_echo_enabled"):
                self._start_loopback(bs)
            self.btn_start.configure(text="■  STOP ENGINE", fg_color="#880000")
            self.sb.update_playbars()
            self.log.add(f"Engine started | SR={SR} BS={bs}")
        except Exception as e:
            messagebox.showerror("Audio Error", str(e))
            self.log.add(f"Engine failed: {e}", "ERROR")

    def _start_loopback(self, blocksize=1024):
        """Open a capture stream on the loopback device for Desktop Echo."""
        try:
            lb_name = getattr(self, "lb_dev", None)
            if lb_name is None:
                return
            lb_name = lb_name.get()
            devs    = sd.query_devices()
            lb_idx  = next(i for i, d in enumerate(devs) if d["name"] == lb_name)
            eng     = self.engine

            def _lb_cb(indata, frames, time_info, status):
                data = indata.astype(np.float32)
                if data.shape[1] == 1:
                    data = np.column_stack((data, data))
                with eng._lb_lock:
                    eng._lb_buf = data.copy()

            self.loopback_stream = sd.InputStream(
                device=lb_idx, samplerate=SR, blocksize=blocksize,
                channels=CHANNELS, dtype="float32", callback=_lb_cb)
            self.loopback_stream.start()
            self.log.add(f"Desktop Echo stream started: {lb_name}")
        except Exception as e:
            self.loopback_stream = None
            self.log.add(f"Desktop Echo stream failed: {e}", "WARN")

    def _toggle_mon(self):
        self.engine.monitoring = bool(self.sw_mon.get())
        if self.running:
            self._toggle_audio(); self._toggle_audio()

    def _mon_worker(self):
        while self.mon_thread_run and self.monitor_stream:
            try:
                data = self.mon_q.get(timeout=0.05)
                self.monitor_stream.write(data)
            except queue.Empty:
                pass
            except Exception:
                break

    def _audio_cb(self, indata, outdata, frames, time_info, status):
        try:
            p = self.engine.process(indata)
            outdata[:] = p if np.all(np.isfinite(p)) else np.zeros_like(p)
            if self.engine.monitoring and self.mon_thread_run and self.monitor_stream:
                if not self.mon_q.full():
                    self.mon_q.put_nowait(p.astype(np.float32))
        except Exception:
            outdata.fill(0)

    # ── lifecycle ─────────────────────────────────────────────────────────────
    def _on_close(self):
        self.synth.running = False
        self.tts.stop()
        if self.running:
            self._toggle_audio()
        if self.settings.get("minimize_to_tray", True):
            self.withdraw()
            if HAS_TRAY:
                self._setup_tray()
        else:
            self._quit()

    def _setup_tray(self):
        if self.tray_icon: return
        image = Image.new("RGB", (64, 64), (200, 0, 0))
        if os.path.exists("icon.ico"):
            try: image = Image.open("icon.ico")
            except Exception: pass
        def _show(icon, _): icon.stop(); self.tray_icon = None; self.after(0, self._show_window)
        def _quit(icon, _): icon.stop(); self.after(0, self._quit)
        self.tray_icon = pystray.Icon("VLAB", image, APP_NAME,
                                       pystray.Menu(item("Show V LAB", _show), item("Quit", _quit)))
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def _quit(self):
        if self.running: self._toggle_audio()
        self.destroy(); sys.exit(0)


# ═════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
