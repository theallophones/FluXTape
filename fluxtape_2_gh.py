import streamlit as st
import base64

# Remove default Streamlit title since we'll add a custom one in HTML
# st.title("FluxTape — Lyrics Versions")

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
<div style="text-align:center; margin-bottom:15px;">
  <h2 style="font-family:sans-serif; font-weight:600; color:#ffffff; margin-bottom:20px;">
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
    background: #4CAF50; /* green default */
    transition: background 0.25s ease, transform 0.1s ease;
  }}
  .play-btn:hover {{ transform: scale(1.05); }}
  .play-btn.pause {{ background: #FBC02D; }} /* yellow when paused */

  .toggle {{
    border: none;
    background: #e53935;  /* red */
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

<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>
<script>
  const audioMap = {audio_map};

  const wavesurfer = WaveSurfer.create({{
    container: '#waveform',
    waveColor: '#bbb',
    progressColor: '#333',
    height: 140,
    backend: 'WebAudio'
  }});

  let current = "A";
  wavesurfer.load(audioMap[current]);
  document.getElementById("active").textContent = "Active: Lyrics " + current;

  const playBtn = document.getElementById("playBtn");

  playBtn.addEventListener("click", () => {{
    wavesurfer.playPause();
  }});

  wavesurfer.on("play", () => {{
    playBtn.textContent = "⏸";
    playBtn.classList.add("pause");
  }});

  wavesurfer.on("pause", () => {{
    playBtn.textContent = "▶";
    playBtn.classList.remove("pause");
  }});

  const buttons = document.querySelectorAll(".toggle");
  function updateActive(label) {{
    buttons.forEach(btn => {{
      btn.classList.toggle("active", btn.dataset.key === label);
    }});
  }}
  updateActive(current);

  buttons.forEach(btn => {{
    btn.addEventListener("click", () => {{
      const label = btn.dataset.key;
      if (label === current) return;
      const time = wavesurfer.getCurrentTime();
      const playing = wavesurfer.isPlaying();
      current = label;
      wavesurfer.load(audioMap[label]);
      wavesurfer.once("ready", () => {{
        wavesurfer.setTime(time);
        if (playing) wavesurfer.play();
        document.getElementById("active").textContent = "Active: Lyrics " + label;
        updateActive(label);
      }});
    }});
  }});
</script>
"""

st.components.v1.html(html, height=400)