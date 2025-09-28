import streamlit as st
import base64

# --- Audio files (must sit next to this script) ---
audio_files = {
    "A": "H1A.mp3",
    "B": "H1B.mp3",
    "C": "H1C.mp3",
}

def file_to_data_url(path, mime="audio/mpeg"):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

audio_map = {k: file_to_data_url(v) for k, v in audio_files.items()}

html = f"""
<div style="text-align:center; margin-bottom:20px;">
  <h2 style="font-family:sans-serif; font-weight:700; color:#ffffff; margin-bottom:20px;">
    FluxTape — Lyrics Versions
  </h2>
  <button id="playBtn" class="play-btn">▶</button>
</div>

<div id="waveform" style="margin-top:20px;"></div>

<!-- Knob + orbiting labels (A=9pm, B=12, C=3pm) -->
<div class="knob-wrap">
  <div id="knob" class="knob" title="Click to switch Lyrics version">
    <div id="pointer" class="pointer"></div>
    <div class="center-dot"></div>
  </div>
  <div class="label labelA" data-label="A">Lyrics A</div>
  <div class="label labelB" data-label="B">Lyrics B</div>
  <div class="label labelC" data-label="C">Lyrics C</div>
</div>

<div style="margin-top:14px; text-align:center;">
  <span id="active" style="font-weight:600; color:#ffffff; font-size:16px;"></span>
</div>

<style>
  :root {{
    --bg: #0f1115;
    --accent: #4CAF50;
    --text: #ffffff;
  }}
  body {{ background: var(--bg); }}

  .play-btn {{
    width: 78px;
    height: 78px;
    border-radius: 50%;
    border: none;
    font-size: 30px;
    cursor: pointer;
    color: #fff;
    background: var(--accent);
    transition: background 0.25s ease, transform 0.1s ease, box-shadow .2s ease;
    box-shadow: 0 6px 18px rgba(76,175,80,.35);
  }}
  .play-btn:hover {{ transform: scale(1.05); }}
  .play-btn.pause {{
    background: #FBC02D;
    box-shadow: 0 6px 18px rgba(251,192,45,.35);
  }}

  .knob-wrap {{
    position: relative;
    width: 260px;
    height: 260px;
    margin: 40px auto;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .knob {{
    width: 160px;
    height: 160px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #2b313c, #1b1f27 70%);
    position: relative;
    box-shadow: inset 0 6px 14px rgba(0,0,0,.5), 0 8px 24px rgba(0,0,0,.35);
    border: 1px solid #2e3440;
  }}
  .center-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #cfd8dc;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
  }}
  .pointer {{
    position: absolute;
    width: 4px;
    height: 55px;
    background: #ffffff;
    border-radius: 2px;
    transform-origin: bottom center;
    bottom: 50%;
    left: 50%;
    translate: -50% 0;
    box-shadow: 0 0 8px rgba(255,255,255,.35);
  }}

  .label {{
    position: absolute;
    background: #2a2f3a;
    color: var(--text);
    padding: 6px 12px;
    border-radius: 12px;
    font-family: sans-serif;
    font-size: 14px;
    cursor: pointer;
    transition: background .2s ease, box-shadow .2s ease;
  }}
  .label:hover {{ background: #3a4150; }}
  .label.active {{
    background: #b71c1c;
    box-shadow: 0 0 0 2px #ffebee inset;
  }}

  /* Positions: A=9pm, B=12, C=3pm */
  .labelA {{ top: 50%; left: -60px; transform: translateY(-50%); }}
  .labelB {{ top: -40px; left: 50%; transform: translateX(-50%); }}
  .labelC {{ top: 50%; right: -60px; transform: translateY(-50%); }}
</style>

<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  const audioMap = {audio_map};

  // Correct pointer angles for each label
  const angleByLabel = {{ A: 90, B: -90, C: 0 }}; 
  // A=left (9pm), B=top (12), C=right (3)

  const ws = WaveSurfer.create({{
    container: '#waveform',
    waveColor: '#c9cbd3',
    progressColor: '#5f6bff',
    height: 160,
    backend: 'WebAudio',
    cursorWidth: 2,
  }});

  let currentLabel = "A";

  const activeEl = document.getElementById('active');
  const playBtn  = document.getElementById('playBtn');
  const pointer  = document.getElementById('pointer');
  const labelEls = Array.from(document.querySelectorAll('.label'));

  function setLabelActive(label) {{
    labelEls.forEach(el => {{
      el.classList.toggle('active', el.dataset.label === label);
    }});
  }}

  function setPointer(label) {{
    const deg = angleByLabel[label];
    pointer.style.transform = 'translate(-50%, 0) rotate(' + deg + 'deg)';
  }}

  function loadVersion(label, keepTime=true) {{
    const t = ws.getCurrentTime();
    const playing = ws.isPlaying();
    ws.load(audioMap[label]);
    ws.once('ready', () => {{
      if (keepTime) ws.setTime(Math.min(t, ws.getDuration()-0.01));
      if (playing) ws.play();
      activeEl.textContent = 'Active: Lyrics ' + label;
    }});
    currentLabel = label;
    setPointer(label);
    setLabelActive(label);
  }}

  // Init
  ws.load(audioMap[currentLabel]);
  activeEl.textContent = 'Active: Lyrics ' + currentLabel;
  setPointer(currentLabel);
  setLabelActive(currentLabel);

  // Play/pause
  playBtn.addEventListener('click', () => ws.playPause());
  ws.on('play', ()  => {{ playBtn.textContent = '⏸'; playBtn.classList.add('pause'); }});
  ws.on('pause', () => {{ playBtn.textContent = '▶';  playBtn.classList.remove('pause'); }});

  // Knob cycles in order A → B → C
  const cycle = ['A','B','C'];
  document.getElementById('knob').addEventListener('click', () => {{
    const i = cycle.indexOf(currentLabel);
    const next = cycle[(i+1)%cycle.length];
    loadVersion(next);
  }});

  // Labels click directly
  labelEls.forEach(el => {{
    el.addEventListener('click', () => {{
      const label = el.dataset.label;
      if (label !== currentLabel) loadVersion(label);
    }});
  }});
</script>
"""

st.components.v1.html(html, height=620)