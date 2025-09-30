import streamlit as st
import base64
import os

st.set_page_config(layout="wide", page_title="FluXTape", page_icon="🎵")

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

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Audio files (must sit next to this script) ---
audio_files = {
    "A": "H1A.mp3",
    "B": "H1B.mp3",
    "C": "H1C.mp3",
}

def file_to_data_url(path, mime="audio/mpeg"):
    """Convert audio file to base64 data URL with error handling"""
    try:
        if not os.path.exists(path):
            st.error(f"❌ Audio file not found: {path}")
            return None
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        st.error(f"❌ Error loading {path}: {str(e)}")
        return None

# Load audio files with error handling
audio_map = {}
for k, v in audio_files.items():
    data_url = file_to_data_url(v)
    if data_url:
        audio_map[k] = data_url

if len(audio_map) == 0:
    st.error("❌ No audio files could be loaded. Please ensure H1A.mp3, H1B.mp3, and H1C.mp3 are in the same directory as this script.")
    st.stop()

html = f"""
<div style="text-align:center; margin-bottom:10px;">
  <h1 style="font-family:'Inter', sans-serif; font-weight:800; color:#ffffff; font-size:48px; margin-bottom:5px; letter-spacing:-1px;">
    FluX-Tape
  </h1>
  <h3 style="font-family:'Inter', sans-serif; font-weight:400; color:#8b92a8; font-size:16px; margin-top:0; letter-spacing:0.5px;">
	Explore Alternate Takes Instantly
  </h3>
  <div style="margin-top:15px;">
    <button id="playBtn" class="play-btn" title="Play/Pause (Space)">▶</button>
  </div>
</div>

<div id="waveform" style="margin:30px auto; width:90%; max-width:1200px;"></div>

<!-- Time counter and speed control -->
<div style="display:flex; justify-content:center; align-items:center; gap:25px; margin-top:12px;">
  <div id="time-display" style="color:#8b92a8; font-family:'Inter', sans-serif; font-size:15px; font-weight:500; min-width:100px; text-align:right;">
    0:00 / 0:00
  </div>
  <div style="display:flex; align-items:center; gap:8px;">
    <span style="color:#8b92a8; font-size:13px; font-family:'Inter', sans-serif;">Speed:</span>
    <select id="speedSelect" class="speed-select">
      <option value="0.5">0.5x</option>
      <option value="0.75">0.75x</option>
      <option value="1" selected>1x</option>
      <option value="1.25">1.25x</option>
      <option value="1.5">1.5x</option>
      <option value="2">2x</option>
    </select>
  </div>
</div>

<!-- Volume control -->
<div style="text-align:center; margin:25px 0;">
  <div style="color:#8b92a8; font-size:22px; margin-bottom:8px;">🔊</div>
  <input id="volumeSlider" type="range" min="0" max="1" step="0.01" value="1" class="slider" title="Volume Control">
</div>

<!-- Current Version Display -->
<div id="versionDisplay" style="text-align:center; margin:15px 0;">
  <div style="display:inline-block; background:rgba(183,28,28,0.2); border:2px solid #b71c1c; border-radius:20px; padding:8px 20px;">
    <span style="color:#8b92a8; font-size:13px; font-family:'Inter', sans-serif; margin-right:8px;">NOW PLAYING:</span>
    <span id="currentVersion" style="color:#fff; font-size:15px; font-weight:700; font-family:'Inter', sans-serif;">Lyrics A</span>
  </div>
</div>

<!-- Knob + orbiting labels -->
<div class="knob-wrap">
  <div id="knob" class="knob" title="Click to cycle versions">
    <div id="pointer" class="pointer"></div>
    <div class="center-dot"></div>
  </div>
  <div class="label labelA" data-idx="0" title="Switch to Lyrics A (Key: 1)">Lyrics A</div>
  <div class="label labelB" data-idx="1" title="Switch to Lyrics B (Key: 2)">Lyrics B</div>
  <div class="label labelC" data-idx="2" title="Switch to Lyrics C (Key: 3)">Lyrics C</div>
</div>

<!-- Keyboard shortcuts info -->
<div style="text-align:center; margin-top:30px; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px; max-width:600px; margin-left:auto; margin-right:auto;">
  <div style="color:#8b92a8; font-size:13px; font-family:'Inter', sans-serif; margin-bottom:10px; font-weight:600;">
    ⌨️ KEYBOARD SHORTCUTS
  </div>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; color:#6b7280; font-size:12px; font-family:'Inter', sans-serif;">
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">Space</kbd> Play/Pause</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">←→</kbd> Seek ±5s</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">1/2/3</kbd> Switch Version</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">↑↓</kbd> Volume ±10%</div>
  </div>
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  
  :root {{
    --bg: #0f1115;
    --accent: #4CAF50;
    --accent-hover: #66BB6A;
    --text: #ffffff;
    --text-muted: #8b92a8;
  }}
  
  * {{
    font-family: 'Inter', sans-serif;
  }}

  html, body, .stApp {{
    height: 100%;
    margin: 0;
    background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%);
  }}

  .play-btn {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    border: none;
    font-size: 36px;
    cursor: pointer;
    color: #fff;
    background: var(--accent);
    transition: all 0.3s ease;
    box-shadow: 0 8px 24px rgba(76,175,80,.5);
  }}
  .play-btn:hover {{ 
    transform: scale(1.08); 
    background: var(--accent-hover);
    box-shadow: 0 12px 32px rgba(76,175,80,.6);
  }}
  .play-btn:active {{
    transform: scale(0.98);
  }}
  .play-btn.pause {{
    background: #FBC02D;
    box-shadow: 0 8px 24px rgba(251,192,45,.5);
  }}
  .play-btn.pause:hover {{
    background: #FDD835;
    box-shadow: 0 12px 32px rgba(251,192,45,.6);
  }}

  .speed-select {{
    background: #2a2f3a;
    color: #fff;
    border: 1px solid #3a4150;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 13px;
    cursor: pointer;
    outline: none;
    transition: all 0.2s ease;
  }}
  .speed-select:hover {{
    background: #3a4150;
    border-color: #4a5160;
  }}

  .knob-wrap {{
    position: relative;
    width: 280px;
    height: 280px;
    margin: 45px auto;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .knob {{
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #2b313c, #1b1f27 70%);
    position: relative;
    box-shadow: inset 0 6px 16px rgba(0,0,0,.6), 0 10px 28px rgba(0,0,0,.4);
    border: 2px solid #2e3440;
    cursor: pointer;
    transition: transform 0.2s ease;
  }}
  .knob:hover {{
    transform: scale(1.03);
  }}
  .knob:active {{
    transform: scale(0.98);
  }}
  
  .center-dot {{
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #cfd8dc;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
  }}
  
  .pointer {{
    position: absolute;
    width: 5px;
    height: 60px;
    background: linear-gradient(to top, #ffffff, #e0e0e0);
    border-radius: 3px;
    transform-origin: bottom center;
    bottom: 50%;
    left: 50%;
    translate: -50% 0;
    box-shadow: 0 0 12px rgba(255,255,255,.5);
    transition: transform 0.5s cubic-bezier(0.4, 0.0, 0.2, 1);
  }}

  .label {{
    position: absolute;
    background: #2a2f3a;
    color: var(--text);
    padding: 10px 18px;
    border-radius: 16px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    user-select: none;
  }}
  .label:hover {{ 
    background: #3a4150; 
    border-color: #4a5160;
  }}
  
  .labelA:hover {{ transform: translateY(-50%) scale(1.05); }}
  .labelB:hover {{ transform: translateX(-50%) scale(1.05); }}
  .labelC:hover {{ transform: translateY(-50%) scale(1.05); }}
  
  .label.active {{
    background: #b71c1c;
    box-shadow: 0 0 20px rgba(183,28,28,1), 0 4px 12px rgba(183,28,28,0.6);
    border-color: #d32f2f;
    transform: scale(1.1);
  }}

  /* Volume slider styling */
  .slider {{
    -webkit-appearance: none;
    width: 300px;
    height: 7px;
    border-radius: 4px;
    background: linear-gradient(to right, #5f6bff 100%, #3a4150 0%);
    outline: none;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .slider:hover {{
    height: 9px;
  }}
  .slider::-webkit-slider-thumb {{
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 8px rgba(200,200,200,.7);
    transition: transform 0.2s ease;
    cursor: grab;
  }}
  .slider::-webkit-slider-thumb:hover {{
    transform: scale(1.3);
  }}
  .slider::-webkit-slider-thumb:active {{
    cursor: grabbing;
  }}
  .slider::-moz-range-thumb {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 8px rgba(200,200,200,.7);
    cursor: pointer;
    border: none;
  }}

  /* Positions: A=9pm, B=12, C=3pm */
  .labelA {{ top: 50%; left: -50px; }}
  .labelB {{ top: -1px; left: 50%; }}
  .labelC {{ top: 50%; right: -50px; }}
  
  /* Fixed transforms to prevent movement */
  .labelA {{ transform: translateY(-50%); }}
  .labelB {{ transform: translateX(-50%); }}
  .labelC {{ transform: translateY(-50%); }}
  
  .labelA.active {{ transform: translateY(-50%) scale(1.1); }}
  .labelB.active {{ transform: translateX(-50%) scale(1.1); }}
  .labelC.active {{ transform: translateY(-50%) scale(1.1); }}
</style>

<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  const audioMap = {audio_map};
  const labels = ["A","B","C"];
  const angles = [270, 0, 90]; // A=left, B=top, C=right

  const ws = WaveSurfer.create({{
    container: '#waveform',
    waveColor: '#4a5568',
    progressColor: '#5f6bff',
    height: 140,
    backend: 'WebAudio',
    cursorWidth: 2,
    cursorColor: '#fff',
    barWidth: 3,
    barGap: 2,
    barRadius: 3,
    responsive: true,
    normalize: true,
  }});

  let currentIdx = 0;
  let current = labels[currentIdx];

  const playBtn = document.getElementById('playBtn');
  const pointer = document.getElementById('pointer');
  const labelEls = Array.from(document.querySelectorAll('.label'));
  const timeDisplay = document.getElementById('time-display');
  const volSlider = document.getElementById('volumeSlider');
  const speedSelect = document.getElementById('speedSelect');
  const versionDisplay = document.getElementById('currentVersion');

  function formatTime(sec) {{
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60).toString().padStart(2, '0');
    return m + ':' + s;
  }}

  function updateTime() {{
    const cur = ws.getCurrentTime();
    const total = ws.getDuration();
    timeDisplay.textContent = formatTime(cur) + ' / ' + formatTime(total);
  }}

  function setLabelActive(idx) {{
    labelEls.forEach((el,i)=> el.classList.toggle('active', i===idx));
    versionDisplay.textContent = 'Lyrics ' + labels[idx];
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
      ws.setVolume(parseFloat(volSlider.value));
      ws.setPlaybackRate(parseFloat(speedSelect.value));
      updateSliderGradient(volSlider.value);
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

  ws.on('ready', () => {{
    updateTime();
    ws.setVolume(parseFloat(volSlider.value));
    updateSliderGradient(volSlider.value);
  }});
  ws.on('audioprocess', updateTime);
  ws.on('finish', () => {{
    playBtn.textContent = '▶';
    playBtn.classList.remove('pause');
  }});

  // Play/pause
  playBtn.addEventListener('click', () => ws.playPause());
  ws.on('play', () => {{ 
    playBtn.textContent = '⏸'; 
    playBtn.classList.add('pause');
  }});
  ws.on('pause', () => {{ 
    playBtn.textContent = '▶'; 
    playBtn.classList.remove('pause');
  }});

  // Update slider gradient
  function updateSliderGradient(value) {{
    const percent = value * 100;
    volSlider.style.background = 'linear-gradient(to right, #5f6bff ' + percent + '%, #3a4150 ' + percent + '%)';
  }}

  // Volume slider
  volSlider.addEventListener('input', e => {{
    const val = parseFloat(e.target.value);
    ws.setVolume(val);
    updateSliderGradient(val);
  }});

  // Speed control
  speedSelect.addEventListener('change', e => {{
    ws.setPlaybackRate(parseFloat(e.target.value));
  }});

  // Click knob cycles A→B→C
  document.getElementById('knob').addEventListener('click', () => {{
    const next = (currentIdx + 1) % 3;
    loadVersion(next);
  }});

  // Click labels directly
  labelEls.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      const idx = parseInt(el.getAttribute('data-idx'));
      if (idx !== currentIdx) loadVersion(idx);
    }});
  }});

  // Keyboard shortcuts
  document.addEventListener('keydown', (e) => {{
    // Prevent if user is typing in an input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    
    switch(e.key) {{
      case ' ': // Space - play/pause
        e.preventDefault();
        ws.playPause();
        break;
      case '1': // Switch to version A
        e.preventDefault();
        if (currentIdx !== 0) loadVersion(0);
        break;
      case '2': // Switch to version B
        e.preventDefault();
        if (currentIdx !== 1) loadVersion(1);
        break;
      case '3': // Switch to version C
        e.preventDefault();
        if (currentIdx !== 2) loadVersion(2);
        break;
      case 'ArrowLeft': // Seek backward
        e.preventDefault();
        ws.skip(-5);
        break;
      case 'ArrowRight': // Seek forward
        e.preventDefault();
        ws.skip(5);
        break;
      case 'ArrowUp': // Volume up
        e.preventDefault();
        const newVolUp = Math.min(1, parseFloat(volSlider.value) + 0.1);
        volSlider.value = newVolUp;
        ws.setVolume(newVolUp);
        updateSliderGradient(newVolUp);
        break;
      case 'ArrowDown': // Volume down
        e.preventDefault();
        const newVolDown = Math.max(0, parseFloat(volSlider.value) - 0.1);
        volSlider.value = newVolDown;
        ws.setVolume(newVolDown);
        updateSliderGradient(newVolDown);
        break;
    }}
  }});

  // Click on waveform to seek
  document.getElementById('waveform').style.cursor = 'pointer';
</script>
"""

st.components.v1.html(html, height=1100)