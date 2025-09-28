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
<div style="text-align:center; margin-bottom:10px;">
  <h2 style="font-family:sans-serif; font-weight:700; color:#ffffff; margin-bottom:25px;">
    FluxTape — Lyrics Toggle
  </h2>
  <button id="playBtn" class="play-btn">▶</button>
</div>

<div id="waveform" style="margin:25px auto; width:85%;"></div>

<!-- Knob + orbiting labels -->
<div class="knob-wrap">
  <div id="knob" class="knob" title="Click to switch Lyrics version">
    <div id="pointer" class="pointer"></div>
    <div class="center-dot"></div>
  </div>
  <div class="label labelA" data-idx="0">Lyrics A</div>
  <div class="label labelB" data-idx="1">Lyrics B</div>
  <div class="label labelC" data-idx="2">Lyrics C</div>
</div>

<div style="margin-top:16px; text-align:center;">
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
    width: 82px;
    height: 82px;
    border-radius: 50%;
    border: none;
    font-size: 34px;
    cursor: pointer;
    color: #fff;
    background: var(--accent);
    transition: background 0.25s ease, transform 0.2s ease, box-shadow .3s ease;
    box-shadow: 0 6px 20px rgba(76,175,80,.4);
  }}
  .play-btn:hover {{ transform: scale(1.1); }}
  .play-btn.pause {{
    background: #FBC02D;
    box-shadow: 0 6px 20px rgba(251,192,45,.4);
  }}

  .knob-wrap {{
    position: relative;
    width: 260px;
    height: 260px;
    margin: 50px auto;
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
    width: 12px;
    height: 12px;
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
    transition: transform 0.4s ease; /* smooth motion */
  }}

  .label {{
    position: absolute;
    background: #2a2f3a;
    color: var(--text);
    padding: 7px 14px;
    border-radius: 14px;
    font-family: sans-serif;
    font-size: 14px;
    cursor: pointer;
    transition: background .25s ease, box-shadow .25s ease;
  }}
  .label:hover {{ background: #3a4150; }}
  .label.active {{
    background: #b71c1c;
    box-shadow: 0 0 14px rgba(183,28,28,0.9);
  }}

  /* Positions: A=9pm, B=12, C=3pm */
  .labelA {{ top: 50%; left: -57px; transform: translateY(-50%); }}
  .labelB {{ top: -20px; left: 50%; transform: translateX(-50%); }}
  .labelC {{ top: 50%; right: -57px; transform: translateY(-50%); }}
</style>

<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  const audioMap = {audio_map};
  const labels = ["A","B","C"];
  const angles = [270, 0, 90]; // A=left, B=top, C=right

  const ws = WaveSurfer.create({{
    container: '#waveform',
    waveColor: '#c9cbd3',
    progressColor: '#5f6bff',
    height: 120,
    backend: 'WebAudio',
    cursorWidth: 2,
  }});

  let currentIdx = 0;
  let current = labels[currentIdx];

  const activeEl = document.getElementById('active');
  const playBtn = document.getElementById('playBtn');
  const pointer = document.getElementById('pointer');
  const labelEls = Array.from(document.querySelectorAll('.label'));

  function setLabelActive(idx) {{
    labelEls.forEach((el,i)=> el.classList.toggle('active', i===idx));
  }}

  function setPointer(idx) {{
    pointer.style.transform = 'translate(-50%, 0) rotate(' + angles[idx] + 'deg)';
  }}

  function loadVersion(idx, keepTime=true) {{
    const label = labels[idx];
    const t = ws.getCurrentTime();
    const playing = ws.isPlaying();
    ws.load(audioMap[label]);
    ws.once('ready', () => {{
      if (keepTime) ws.setTime(Math.min(t, ws.getDuration()-0.01));
      if (playing) ws.play();
      activeEl.textContent = 'Active: Lyrics ' + label;
    }});
    currentIdx = idx;
    current = label;
    setPointer(idx);
    setLabelActive(idx);
  }}

  // Init
  ws.load(audioMap[current]);
  activeEl.textContent = 'Active: Lyrics ' + current;
  setPointer(currentIdx);
  setLabelActive(currentIdx);

  // Play/pause
  playBtn.addEventListener('click', () => ws.playPause());
  ws.on('play', () => {{ playBtn.textContent = '⏸'; playBtn.classList.add('pause'); }});
  ws.on('pause', () => {{ playBtn.textContent = '▶'; playBtn.classList.remove('pause'); }});

  // Click knob cycles A→B→C
  document.getElementById('knob').addEventListener('click', () => {{
    const next = (currentIdx + 1) % 3;
    loadVersion(next);
  }});

  // Click labels directly
  labelEls.forEach(el => {{
    el.addEventListener('click', () => {{
      const idx = parseInt(el.getAttribute('data-idx'));
      if (idx !== currentIdx) loadVersion(idx);
    }});
  }});
</script>
"""

st.components.v1.html(html, height=640)