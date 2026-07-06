================================================================================
      ▄▄▄▄▄▄        ▄▄▄▄   ▄▄▄▄▄▄▄  
██  █▄   ▓▒▒░        ▒▓▀▒▒▌   ███░▀ ▀▄
▐░▌ ▐░   ▐░ ▌       ▐░  ▐▒░   ▐░█▌   ░
 ▒▌  ▒░▌   ░           ▄░░ ▌   ░░ ▄▄▀ 
 ▓    ▒█  ░▒  ▀░▄  ▐░▄▀▀▄ █░   ▒▒ ▀▀▄ 
 █     ▒  ▒▓▌   ▒░ ▓▒▌   ░░▒▌  ▓▌    ▒
▐█▌   ▓█ ▐▓██▌ ▐▓▓▌█▓    ▐▒▓▌ ▐█▓   █▓
 ▐█▄▄█▌  ▐██▄█▓▓█  ▐█▓    ▓█  ████▄█▓▌
   ▀▀    ▀▀▀▀▀▀▀    ▀▀▀  ▀▀  ▀▀▀▀▀▀▀▀ 

       V LAB — REAL-TIME AUDIO LABORATORY [v2.2.0 Master Edition]
================================================================================

V LAB is a high-performance, real-time digital signal processing (DSP) 
environment, soundboard, synthesizer, and audio modifier built entirely 
in Python. Featuring ultra-low latency processing, global hotkeys, 
real-time Text-to-Speech injection, an advanced song sequencer, and a 
fully extensible Modding SDK.

┌──────────────────────────────────────────────────────────────────────────────┐
│  [1] KEY FEATURES                                                            │
└──────────────────────────────────────────────────────────────────────────────┘
 [+] REAL-TIME DSP ENGINE: Vectorized high-fidelity effects including Phase 
     Vocoder Pitch Shifting, Schroeder Reverb, Lookahead Compression, 
     3-Band EQ, Flanger/Chorus, Delay, and Harmonic Exciters.
 
 [+] 100-SLOT SOUNDBOARD: Hotkeyable, loopable, and trimmable sound slots 
     with integrated sample-rate matching and on-the-fly micro-recording.
 
 [+] ADVANCED SYNTHESIZER: Multi-waveform synth featuring unison detuning, 
     portamento, FM, and built-in arpeggiator step-sequencing.
 
 [+] LIVE TTS INJECTION: Zero-file, real-time Text-to-Speech rendering 
     piped straight into your live microphone stream.
 
 [+] MODULAR ARCHITECTURE: Advanced Python-driven theme configuration and 
     hot-swappable user mod slots via the built-in SDK.


┌──────────────────────────────────────────────────────────────────────────────┐
│  [2] PREREQUISITES & INSTALLATION                                            │
└──────────────────────────────────────────────────────────────────────────────┘
 V LAB leverages specialized libraries for low-latency audio capture and UI.

 > STEP 1: INSTALL DEPENDENCIES
   Open your terminal/command prompt and run:
   $ pip install customtkinter keyboard numpy sounddevice soundfile pillow

 > STEP 2: OPTIONAL ENHANCEMENTS (Highly Recommended)
   Enable full TTS engines, visualizers, and advanced filters:
   $ pip install pyttsx3 pystray matplotlib scipy

   /!\ WINDOWS USERS: To use the global hotkey feature ('keyboard'), 
   run the main script as Administrator so it can capture keystrokes system-wide.

 > STEP 3: IGNITION
   Launch the core interface:
   $ python main.py


┌──────────────────────────────────────────────────────────────────────────────┐
│  [3] ROUTING AUDIO VIA VIRTUAL CABLE (Discord, OBS, Games)                   │
└──────────────────────────────────────────────────────────────────────────────┘
 To pipe your processed voice and soundboard into communication apps, 
 you MUST use a Virtual Audio Cable (VAC).

     [ Physical Hardware Mic ]
                │
                ▼
      ( V LAB Input Device )
                │
    ░▒▓█[ DSP PROCESSING ]█▓▒░
                │
                ▼
      ( V LAB Output Device )
                │
                ▼
  [ Virtual Audio Cable INPUT ]
                │
        ( Virtual Driver )
                │
                ▼
  [ Virtual Audio Cable OUTPUT ]
                │
                ▼
  [ Discord / Zoom / OBS Input ]


 > STEP-BY-STEP SETUP:
   1. INSTALL DRIVER: Download and install "VB-AUDIO Virtual Cable" or similar.
      Restart your PC.
   
   2. CONFIGURE V LAB: 
      - Set INPUT to your physical microphone.
      - Set OUTPUT to "CABLE Input (VB-Audio Virtual Cable)".
      - Start the engine!

   3. CONFIGURE APP (e.g., Discord):
      - Go to User Settings -> Voice & Video.
      - Set INPUT DEVICE to "CABLE Output (VB-Audio Virtual Cable)".
      - Set OUTPUT DEVICE to your normal headphones.

   *PRO TIP*: Turn OFF Discord's built-in processing (Echo Cancellation, 
   Noise Suppression, Krisp) to prevent it from destroying V LAB's pristine 
   audio gating and effects!


┌──────────────────────────────────────────────────────────────────────────────┐
│  [4] MODDING & THEME SDK                                                     │
└──────────────────────────────────────────────────────────────────────────────┘
 V LAB monitors specific folders for runtime loading (no restart required):
 
   > mods/themes/basic/     --> Drop .json color configurations here.
   > mods/themes/advanced/  --> Drop .py scripts for full hook APIs.
   > mods/songs/            --> Drop .json sequencer mapping patterns.

   Check 'mods/SDK_README.md' for full syntax, hooks, and examples.


┌──────────────────────────────────────────────────────────────────────────────┐
│  [5] SUPPORT & COMMUNITY                                                     │
└──────────────────────────────────────────────────────────────────────────────┘
 Buffer underruns? DSP math making your head spin? Need custom scripts?
 Join the development lab:

   _____   _____   _____  
  |  _  \ |  _  \ |  _  \ 
  | | | | | |_| | | | | |   > DISCORD SERVER:
  | | | | |  ___/ | | | |   > https://discord.gg/thPHeJJkH
  | |_| | | |     | |_| | 
  |_____/ |_|     |_____/ 

================================================================================
