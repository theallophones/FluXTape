import streamlit as st
import base64

st.title("FluxTape — Lyrics Versions")



print("hey this is a test")

# Audio files (relative paths — must be in same folder as this script)
audio_files = {
    "A": "H1A.mp3",
    "B": "H1B.mp3",
    "C": "H1C.mp3",
}

# Convert files to base64 for embedding in WaveSurfer.js
def file_to_data_url(path, mime="audio/mpeg"):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

audio_map = {k: file_to_data_url(v) for k, v in audio_files.items()}

html = f"""
<div style="text-align:center; margin-bottom:20px;">
  <h2 style="font-family:sans-serif; font-weight:600; color:#ffffff; margin-bottom:15px;">
    FluxTape — Lyrics Versions
  </h2>
  <button id="playBtn" class="play-btn">▶</button>
</div>

<div id="waveform" style="margin-top:20px;"></div>

<div style="display:flex; justify-content:space-evenly; margin-top:18px;">
  <button class="toggle" data-key="A">Lyrics A</button>
  <button class="toggle" data-key="B">Lyrics B</button>
  <button class="toggle" data-key="C">Lyrics C</button>
</div>

<div style="margin-top:14px; text-align:center;">
  <span id="active" style="font-weight:600; color:#ffffff; font-size:15px;"></span>
</div>

<style>
  body {{
    background-color: #111;
  }}

  h2 {{
    margin: 0;
  }}

  .play-btn {{
    width: 75px;
    height: 75px;
    border-radius: 50%;
    border: none;
    font-size: 30px;
    cursor: pointer;
    color: #fff;
    background: #4CAF50; /* green */
    transition: background 0.25s ease, transform 0.1s ease;
  }}
  .play-btn:hover {{ transform: scale(1.05); }}
  .play-btn.pause {{ background: #FBC02D; }} /* yellow when paused */

  .toggle {{
    border: none;
    background: #e53935;
    color: #fff;
    padding: 10px 24px;
    border-radius: 24px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.25s ease;
  }}
  .toggle:hover {{
    background: #d32f2f;
  }}
  .toggle.active {{
    background: #b71c1c;
    box-shadow: 0 0 0 2px #ffebee inset;
  }}
</style>
"""

st.components.v1.html(html, height=350)


#this is for you Peyman - now here whatever you do is gonna appear remotley too. This is really great. 


