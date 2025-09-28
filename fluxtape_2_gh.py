import streamlit as st
import base64

st.set_page_config(layout="wide")

st.markdown("""
<style>
/* make the whole app use the gradient */
[data-testid="stAppViewContainer"] {
  background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%) fixed !important;
}

/* hide the default header bar background so gradient shows through */
[data-testid="stHeader"] {
  background: rgba(0,0,0,0) !important;
}

/* optional: sidebar tint (remove if you don't use sidebar) */
[data-testid="stSidebar"] {
  background: rgba(0,0,0,0.15) !important;
}
</style>
""", unsafe_allow_html=True)

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
  <h1 style="font-family:sans-serif; font-weight:800; color:#ffffff; font-size:40px; margin-bottom:5px;">
    FluX-Tape
  </h1>
  <h3 style="font-family:sans-serif; font-weight:500; color:#cccccc; font-size:18px; margin-top:0;">
    Lyrics Versions
  </h3>
  <button id="playBtn" class="play-btn">▶</button>
</div>

<div id="waveform" style="margin:25px auto; width:85%;"></div>

<!-- Time counter -->
<div id="time-display" style="text-align:center; margin-top:6px; color:#ccc; font-family:sans-serif; font-size:14px;">
  0:00 / 0:00
</div>

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

<!-- Volume slider -->
<div style="text-align:center; margin-top:20px;">
  <input id="volumeSlider" type="range" min="0" max="1" step="0.01" value="1" class="slider">
</div>

<style>
  /* ... keep your existing styles ... */

  /* Volume slider styling */
  .slider {{
    -webkit-appearance: none;
    width: 220px;
    height: 6px;
    border-radius: 3px;
    background: #444;
    outline: none;
    margin-top: 10px;
  }}
  .slider::-webkit-slider-thumb {{
    -webkit-appearance: none;
    appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #4CAF50;
    cursor: pointer;
    box-shadow: 0 0 6px rgba(76,175,80,.8);
    transition: transform 0.2s ease;
  }}
  .slider::-webkit-slider-thumb:hover {{
    transform: scale(1.2);
  }}
  .slider::-moz-range-thumb {{
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #4CAF50;
    cursor: pointer;
    box-shadow: 0 0 6px rgba(76,175,80,.8);
  }}
</style>

<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  const audioMap = {audio_map};
  const labels = ["A","B","C"];
  const angles = [270, 0, 90];

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

  const playBtn = document.getElementById('playBtn');
  const pointer = document.getElementById('pointer');
  const labelEls = Array.from(document.querySelectorAll('.label'));
  const timeDisplay = document.getElementById('time-display');
  const volSlider = document.getElementById('volumeSlider');

  function formatTime(sec) {{
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60).toString().padStart(2, '0');
    return `${{m}}:${{s}}`;
  }}

  function updateTime() {{
    const cur = ws.getCurrentTime();
    const total = ws.getDuration();
    timeDisplay.textContent = formatTime(cur) + ' / ' + formatTime(total);
  }}

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
      updateTime();
    }});
    currentIdx = idx;
    current = label;
    setPointer(idx);
    setLabelActive(idx);
  }}

  // Init
  ws.load(audioMap[current]);
  setPointer(currentIdx);
  setLabelActive(currentIdx);

  ws.on('ready', updateTime);
  ws.on('audioprocess', updateTime);

  // Play/pause
  playBtn.addEventListener('click', () => ws.playPause());
  ws.on('play', () => {{ playBtn.textContent = '⏸'; playBtn.classList.add('pause'); }});
  ws.on('pause', () => {{ playBtn.textContent = '▶'; playBtn.classList.remove('pause'); }});

  // Volume slider
  volSlider.addEventListener('input', e => {{
    ws.setVolume(parseFloat(e.target.value));
  }});

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

st.components.v1.html(html, height=700)