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

<!-- Knob (no external UI libs; pure CSS/JS; click to cycle A→B→C) -->
<div class="knob-wrap">
  <div id="knob" class="knob" title="Click to switch Lyrics version">
    <div id="pointer" class="pointer"></div>
    <div class="center-dot"></div>
  </div>
  <div class="ticks">
    <span data-idx="0">Lyrics A</span>
    <span data-idx="1">Lyrics B</span>
    <span data-idx="2">Lyrics C</span>
  </div>
</div>

<div style="margin-top:14px; text-align:center;">
  <span id="active" style="font-weight:600; color:#ffffff; font-size:16px;"></span>
</div>

<style>
  :root {{
    --bg: #0f1115;
    --panel: #171a21;
    --ring: #2a2f3a;
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

  /* Knob wrapper and labels */
  .knob-wrap {{
    margin-top: 26px;
    display: grid;
    place-items: center;
    gap: 12px;
  }}
  .ticks {{
    display: flex;
    gap: 22px;
    font-family: sans-serif;
    font-size: 14px;
    color: var(--text);
  }}
  .ticks span {{
    padding: 6px 12px;
    border-radius: 12px;
    background: #2a2f3a;
    cursor: pointer;
    user-select: none;
    transition: background .2s ease, box-shadow .2s ease;
  }}
  .ticks span.active {{
    background: #b71c1c;
    box-shadow: 0 0 0 2px #ffebee inset;
  }}
  .ticks span:hover {{ background: #3a4150; }}

  /* Knob face */
  .knob {{
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #2b313c, #1b1f27 70%);
    position: relative;
    box-shadow: inset 0 6px 14px rgba(0,0,0,.5), 0 8px 24px rgba(0,0,0,.35);
    border: 1px solid #2e3440;
    display: grid;
    place-items: center;
  }}
  .center-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #cfd8dc;
    position: absolute;
  }}
  .pointer {{
    position: absolute;
    width: 4px;
    height: 44px;
    background: #ffffff;
    border-radius: 2px;
    transform-origin: bottom center;
    bottom: 50%;
    left: 50%;
    translate: -50% 0;
    box-shadow: 0 0 8px rgba(255,255,255,.35);
  }}
</style>

<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  const audioMap = {audio_map};
  const labels = ["A","B","C"];
  const angles = [-90, 0, 90]; // pointer positions for A/B/C

  // Wavesurfer
  const ws = WaveSurfer.create({{
    container: '#waveform',
    waveColor: '#c9cbd3',
    progressColor: '#5f6bff',
    height: 160,
    backend: 'WebAudio',
    cursorWidth: 2,
  }});

  let currentIdx = 0; // 0=A, 1=B, 2=C
  let current = labels[currentIdx];

  const activeEl = document.getElementById('active');
  const playBtn = document.getElementById('playBtn');
  const pointer = document.getElementById('pointer');
  const tickEls = Array.from(document.querySelectorAll('.ticks span'));

  function setTickActive(idx) {{
    tickEls.forEach((el,i)=> el.classList.toggle('active', i===idx));
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
    setTickActive(idx);
  }}

  // Init
  ws.load(audioMap[current]);
  activeEl.textContent = 'Active: Lyrics ' + current;
  setPointer(currentIdx);
  setTickActive(currentIdx);

  // Play/pause
  playBtn.addEventListener('click', () => ws.playPause());
  ws.on('play', () => {{ playBtn.textContent = '⏸'; playBtn.classList.add('pause'); }});
  ws.on('pause', () => {{ playBtn.textContent = '▶'; playBtn.classList.remove('pause'); }});

  // Click knob to cycle A→B→C
  document.getElementById('knob').addEventListener('click', () => {{
    const next = (currentIdx + 1) % 3;
    loadVersion(next);
  }});

  // Click labels under knob to jump directly
  tickEls.forEach(el => {{
    el.addEventListener('click', () => {{
      const idx = parseInt(el.getAttribute('data-idx'));
      if (idx !== currentIdx) loadVersion(idx);
    }});
  }});

  // Optional: arrow keys to switch
  window.addEventListener('keydown', (e) => {{
    if (e.key === 'ArrowRight') loadVersion((currentIdx+1)%3);
    if (e.key === 'ArrowLeft') loadVersion((currentIdx+2)%3);
  }});
</script>
"""

st.components.v1.html(html, height=520)