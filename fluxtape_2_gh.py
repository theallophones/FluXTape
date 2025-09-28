import streamlit as st
import base64

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
  <h2 style="font-family:sans-serif; font-weight:600; color:#ffffff; margin-bottom:20px;">
    FluxTape — Lyrics Versions
  </h2>
  <button id="playBtn" class="play-btn">▶</button>
</div>

<div id="waveform" style="margin-top:20px;"></div>

<!-- 🎛 NexusUI knob -->
<div style="display:flex; justify-content:center; margin-top:25px;">
  <div id="knob" style="width:100px; height:100px;"></div>
</div>

<div style="margin-top:14px; text-align:center;">
  <span id="active" style="font-weight:600; color:#ffffff; font-size:16px;"></span>
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
</style>

<!-- load NexusUI + WaveSurfer -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/nexusui/2.0.12/nexusUI.min.js"></script>
<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  const audioMap = {audio_map};
  const labels = ["A", "B", "C"];

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
  playBtn.addEventListener("click", () => {{ wavesurfer.playPause(); }});

  wavesurfer.on("play", () => {{
    playBtn.textContent = "⏸";
    playBtn.classList.add("pause");
  }});

  wavesurfer.on("pause", () => {{
    playBtn.textContent = "▶";
    playBtn.classList.remove("pause");
  }});

  // 🎛 NexusUI Knob
  const knob = new Nexus.Knob('#knob', {{
    'size': [100,100],
    'min': 0,
    'max': 2,
    'step': 1,
    'value': 0
  }});

  knob.on('change', (val) => {{
    const label = labels[Math.round(val)];
    if (label === current) return;
    const time = wavesurfer.getCurrentTime();
    const playing = wavesurfer.isPlaying();
    current = label;
    wavesurfer.load(audioMap[label]);
    wavesurfer.once("ready", () => {{
      wavesurfer.setTime(time);
      if (playing) wavesurfer.play();
      document.getElementById("active").textContent = "Active: Lyrics " + label;
    }});
  }});
</script>
"""

st.components.v1.html(html, height=500)