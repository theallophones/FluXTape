import streamlit as st
import base64
import os

st.set_page_config(layout="wide", page_title="FluXTape Complete", page_icon="🎵")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
  background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%) fixed !important;
}
[data-testid="stHeader"] {
  background: rgba(0,0,0,0) !important;
}
[data-testid="stSidebar"] {
  background: rgba(0,0,0,0.15) !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

audio_files = {
    "groove": "groove.mp3",
    "lyricsA": "lyricsA.mp3",
    "lyricsB": "lyricsB.mp3",
    "lyricsC": "lyricsC.mp3",
    "soloA": "soloA.mp3",
    "soloB": "soloB.mp3",
    "harmony_narrow": "harmony_narrow.mp3",
    "harmony_wide": "harmony_wide.mp3",
}

def file_to_data_url(path, mime="audio/mpeg"):
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

audio_map = {}
for k, v in audio_files.items():
    data_url = file_to_data_url(v)
    if data_url:
        audio_map[k] = data_url

if len(audio_map) < 8:
    st.error("❌ Not all audio files could be loaded. Please ensure all 8 stem files are present.")
    st.stop()

html = f"""
<div style="text-align:center; margin-bottom:10px;">
  <h1 style="font-family:'Inter', sans-serif; font-weight:800; color:#ffffff; font-size:48px; margin-bottom:5px; letter-spacing:-1px;">
    FluX-Tape
  </h1>
  <h3 style="font-family:'Inter', sans-serif; font-weight:400; color:#8b92a8; font-size:16px; margin-top:0; letter-spacing:0.5px;">
    Complete Multi-Stem System
  </h3>
  <div style="margin-top:15px;">
    <button id="playBtn" class="play-btn" title="Play/Pause (Space)">▶</button>
  </div>
</div>

<div id="waveform" style="margin:30px auto; width:90%; max-width:1200px;"></div>

<div class="visualizer-container paused">
  <div class="vis-bar" style="animation-delay: 0s;"></div>
  <div class="vis-bar" style="animation-delay: 0.1s;"></div>
  <div class="vis-bar" style="animation-delay: 0.2s;"></div>
  <div class="vis-bar" style="animation-delay: 0.15s;"></div>
  <div class="vis-bar" style="animation-delay: 0.05s;"></div>
  <div class="vis-bar" style="animation-delay: 0.25s;"></div>
  <div class="vis-bar" style="animation-delay: 0.3s;"></div>
  <div class="vis-bar" style="animation-delay: 0.12s;"></div>
  <div class="vis-bar" style="animation-delay: 0.18s;"></div>
  <div class="vis-bar" style="animation-delay: 0.08s;"></div>
  <div class="vis-bar" style="animation-delay: 0.22s;"></div>
  <div class="vis-bar" style="animation-delay: 0.28s;"></div>
</div>

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

<div style="text-align:center; margin:25px 0;">
  <div style="color:#8b92a8; font-size:22px; margin-bottom:8px;">🔊</div>
  <input id="volumeSlider" type="range" min="0" max="1" step="0.01" value="1" class="slider" title="Volume Control">
</div>

<div class="controls-grid">
  <div class="control-section">
    <div class="control-header">LYRICS</div>
    <div class="knob-wrap-small">
      <div id="lyricsKnob" class="knob-small" title="Click to cycle lyrics">
        <div id="lyricsPointer" class="pointer-small"></div>
        <div class="center-dot-small"></div>
      </div>
      <div class="label-small labelA-small" data-lyrics="A">A</div>
      <div class="label-small labelB-small" data-lyrics="B">B</div>
      <div class="label-small labelC-small" data-lyrics="C">C</div>
    </div>
    <div id="lyricsDisplay" class="version-badge">Lyrics A</div>
  </div>

  <div class="control-section">
    <div class="control-header">SOLO</div>
    <div class="toggle-container">
      <button class="toggle-btn active" data-solo="A">Take A</button>
      <button class="toggle-btn" data-solo="B">Take B</button>
    </div>
    <div id="soloDisplay" class="version-badge">Solo A</div>
  </div>

  <div class="control-section">
    <div class="control-header">HARMONY</div>
    <div class="toggle-container">
      <button class="toggle-btn active" data-harmony="narrow">Narrow</button>
      <button class="toggle-btn" data-harmony="wide">Wide</button>
    </div>
    <div id="harmonyDisplay" class="version-badge">Narrow</div>
  </div>
</div>

<div style="text-align:center; margin-top:30px; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px; max-width:600px; margin-left:auto; margin-right:auto;">
  <div style="color:#8b92a8; font-size:13px; font-family:'Inter', sans-serif; margin-bottom:10px; font-weight:600;">
    ⌨️ KEYBOARD SHORTCUTS
  </div>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; color:#6b7280; font-size:12px; font-family:'Inter', sans-serif;">
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">Space</kbd> Play/Pause</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">←→</kbd> Seek ±5s</div>
    <div><kbd style="background:#2a2f3a; padding:2px 8px; border-radius:4px; color:#fff;">1/2/3</kbd> Lyrics A/B/C</div>
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
  
  * {{ font-family: 'Inter', sans-serif; }}

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
  .play-btn:active {{ transform: scale(0.98); }}
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

  .controls-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 30px;
    max-width: 900px;
    margin: 40px auto;
    padding: 0 20px;
  }}

  .control-section {{
    background: rgba(255,255,255,0.03);
    border-radius: 16px;
    padding: 25px 20px;
    text-align: center;
  }}

  .control-header {{
    color: #8b92a8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 20px;
  }}

  .version-badge {{
    margin-top: 15px;
    display: inline-block;
    background: rgba(95,107,255,0.2);
    border: 1px solid #5f6bff;
    border-radius: 12px;
    padding: 6px 14px;
    color: #8b9dff;
    font-size: 13px;
    font-weight: 600;
  }}

  .knob-wrap-small {{
    position: relative;
    width: 140px;
    height: 140px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .knob-small {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #2b313c, #1b1f27 70%);
    position: relative;
    box-shadow: inset 0 4px 10px rgba(0,0,0,.6), 0 6px 18px rgba(0,0,0,.4);
    border: 2px solid #2e3440;
    cursor: pointer;
    transition: transform 0.2s ease;
  }}
  .knob-small:hover {{ transform: scale(1.05); }}
  .knob-small:active {{ transform: scale(0.98); }}

  .center-dot-small {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #cfd8dc;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    box-shadow: 0 1px 4px rgba(0,0,0,0.4);
  }}

  .pointer-small {{
    position: absolute;
    width: 3px;
    height: 30px;
    background: linear-gradient(to top, #ffffff, #e0e0e0);
    border-radius: 2px;
    transform-origin: bottom center;
    bottom: 50%;
    left: 50%;
    translate: -50% 0;
    box-shadow: 0 0 8px rgba(255,255,255,.5);
    transition: transform 0.5s cubic-bezier(0.4, 0.0, 0.2, 1);
  }}

  .label-small {{
    position: absolute;
    background: #2a2f3a;
    color: var(--text);
    padding: 6px 12px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid transparent;
    user-select: none;
  }}
  .label-small:hover {{
    background: #3a4150;
    border-color: #4a5160;
  }}
  .label-small.active {{
    background: #b71c1c;
    box-shadow: 0 0 12px rgba(183,28,28,0.9);
    border-color: #d32f2f;
  }}

  .labelA-small {{ top: 50%; left: -20px; transform: translateY(-50%); }}
  .labelB-small {{ top: -15px; left: 50%; transform: translateX(-50%); }}
  .labelC-small {{ top: 50%; right: -20px; transform: translateY(-50%); }}

  .toggle-container {{
    display: flex;
    gap: 10px;
    justify-content: center;
  }}

  .toggle-btn {{
    flex: 1;
    max-width: 120px;
    background: #2a2f3a;
    color: #8b92a8;
    border: 2px solid #3a4150;
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }}
  .toggle-btn:hover {{
    background: #3a4150;
    border-color: #4a5160;
  }}
  .toggle-btn.active {{
    background: #4CAF50;
    color: #fff;
    border-color: #66BB6A;
    box-shadow: 0 4px 12px rgba(76,175,80,0.4);
  }}

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
  .slider:hover {{ height: 9px; }}
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
  .slider::-webkit-slider-thumb:hover {{ transform: scale(1.3); }}
  .slider::-webkit-slider-thumb:active {{ cursor: grabbing; }}
  .slider::-moz-range-thumb {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 2px 8px rgba(200,200,200,.7);
    cursor: pointer;
    border: none;
  }}

  .visualizer-container {{
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 6px;
    height: 100px;
    margin: 25px auto;
    max-width: 400px;
    padding: 0 20px;
  }}
  
  .vis-bar {{
    width: 14px;
    background: linear-gradient(to top, #5f6bff, #8b9dff);
    border-radius: 8px 8px 0 0;
    height: 20%;
    box-shadow: 0 0 15px rgba(95, 107, 255, 0.5);
    animation: pulse 0.8s ease-in-out infinite alternate;
    transition: opacity 0.3s ease;
  }}
  
  @keyframes pulse {{
    0% {{ height: 15%; opacity: 0.6; }}
    50% {{ height: 75%; opacity: 1; }}
    100% {{ height: 30%; opacity: 0.7; }}
  }}
  
  .visualizer-container.paused .vis-bar {{
    animation: none;
    height: 20%;
    opacity: 0.3;
  }}
</style>

<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  const audioMap = {audio_map};
  const lyricsAngles = {{A: 270, B: 0, C: 90}};

  // Create visible groove waveform
  const grooveWS = WaveSurfer.create({{
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

  // Create hidden WaveSurfer instances for all other stems
  function createHiddenWS() {{
    const div = document.createElement('div');
    div.style.display = 'none';
    document.body.appendChild(div);
    return WaveSurfer.create({{ container: div, backend: 'WebAudio' }});
  }}

  const stems = {{
    lyricsA: createHiddenWS(),
    lyricsB: createHiddenWS(),
    lyricsC: createHiddenWS(),
    soloA: createHiddenWS(),
    soloB: createHiddenWS(),
    harmony_narrow: createHiddenWS(),
    harmony_wide: createHiddenWS()
  }};

  // State
  let currentLyrics = 'A';
  let currentSolo = 'A';
  let currentHarmony = 'narrow';
  let isPlaying = false;
  let allReady = false;
  let readyCount = 0;

  // UI Elements
  const playBtn = document.getElementById('playBtn');
  const lyricsPointer = document.getElementById('lyricsPointer');
  const lyricsLabels = Array.from(document.querySelectorAll('[data-lyrics]'));
  const timeDisplay = document.getElementById('time-display');
  const volSlider = document.getElementById('volumeSlider');
  const speedSelect = document.getElementById('speedSelect');
  const visualizer = document.querySelector('.visualizer-container');
  const lyricsDisplay = document.getElementById('lyricsDisplay');
  const soloDisplay = document.getElementById('soloDisplay');
  const harmonyDisplay = document.getElementById('harmonyDisplay');

  // Helper Functions
  function formatTime(sec) {{
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60).toString().padStart(2, '0');
    return m + ':' + s;
  }}

  function updateTime() {{
    const cur = grooveWS.getCurrentTime();
    const total = grooveWS.getDuration();
    timeDisplay.textContent = formatTime(cur) + ' / ' + formatTime(total);
  }}

  function checkReady() {{
    readyCount++;
    console.log('Stem ready:', readyCount + '/8');
    if (readyCount === 8) {{
      allReady = true;
      console.log('✅ All stems loaded!');
      
      // CRITICAL: Set initial volumes immediately
      const vol = parseFloat(volSlider.value);
      const rate = parseFloat(speedSelect.value);
      
      grooveWS.setVolume(vol);
      grooveWS.setPlaybackRate(rate);
      
      // Set active stems to full volume, inactive to 0
      stems.lyricsA.setVolume(vol);
      stems.lyricsB.setVolume(0);
      stems.lyricsC.setVolume(0);
      stems.soloA.setVolume(vol);
      stems.soloB.setVolume(0);
      stems.harmony_narrow.setVolume(vol);
      stems.harmony_wide.setVolume(0);
      
      // Set playback rate for all
      Object.values(stems).forEach(ws => ws.setPlaybackRate(rate));
      
      console.log('✅ Initial volumes set - ready to play!');
    }}
  }}

  function updateActiveStemVolumes() {{
    const vol = parseFloat(volSlider.value);
    const rate = parseFloat(speedSelect.value);
    
    // Groove always plays
    grooveWS.setVolume(vol);
    grooveWS.setPlaybackRate(rate);
    
    // Update all stems
    Object.keys(stems).forEach(key => {{
      const ws = stems[key];
      ws.setPlaybackRate(rate);
      
      // Only unmute active stems
      if (key === 'lyrics' + currentLyrics || 
          key === 'solo' + currentSolo || 
          key === 'harmony_' + currentHarmony) {{
        ws.setVolume(vol);
      }} else {{
        ws.setVolume(0); // Mute inactive
      }}
    }});
  }}

  function playAll() {{
    if (!allReady) {{
      console.warn('Not all stems ready yet');
      return;
    }}
    isPlaying = true;
    grooveWS.play();
    Object.values(stems).forEach(ws => ws.play());
  }}

  function pauseAll() {{
    isPlaying = false;
    grooveWS.pause();
    Object.values(stems).forEach(ws => ws.pause());
  }}

  // Load all 8 stems at startup
  console.log('Loading groove...');
  grooveWS.load(audioMap.groove);
  grooveWS.on('ready', () => {{
    console.log('✓ Groove ready');
    updateTime();
    checkReady();
  }});

  Object.keys(stems).forEach(key => {{
    console.log('Loading ' + key + '...');
    stems[key].load(audioMap[key]);
    stems[key].on('ready', () => {{
      console.log('✓ ' + key + ' ready');
      checkReady();
    }});
  }});

  // Event Handlers
  grooveWS.on('audioprocess', updateTime);
  grooveWS.on('finish', () => {{
    pauseAll();
    playBtn.textContent = '▶';
    playBtn.classList.remove('pause');
    visualizer.classList.add('paused');
  }});

  // Play/Pause Button
  playBtn.addEventListener('click', () => {{
    if (isPlaying) {{
      pauseAll();
      playBtn.textContent = '▶';
      playBtn.classList.remove('pause');
      visualizer.classList.add('paused');
    }} else {{
      playAll();
      playBtn.textContent = '⏸';
      playBtn.classList.add('pause');
      visualizer.classList.remove('paused');
    }}
  }});

  // Lyrics Controls
  function setLyricsActive(version) {{
    lyricsLabels.forEach(el => {{
      el.classList.toggle('active', el.getAttribute('data-lyrics') === version);
    }});
    lyricsPointer.style.transform = 'translate(-50%, 0) rotate(' + lyricsAngles[version] + 'deg)';
    lyricsDisplay.textContent = 'Lyrics ' + version;
  }}

  function switchLyrics(version) {{
    if (version === currentLyrics) return;
    
    // Mute old, unmute new
    stems['lyrics' + currentLyrics].setVolume(0);
    stems['lyrics' + version].setVolume(parseFloat(volSlider.value));
    
    currentLyrics = version;
    setLyricsActive(version);
  }}

  document.getElementById('lyricsKnob').addEventListener('click', () => {{
    const next = {{A: 'B', B: 'C', C: 'A'}}[currentLyrics];
    switchLyrics(next);
  }});

  lyricsLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      const version = el.getAttribute('data-lyrics');
      switchLyrics(version);
    }});
  }});

  // Solo Controls
  document.querySelectorAll('[data-solo]').forEach(btn => {{
    btn.addEventListener('click', () => {{
      const version = btn.getAttribute('data-solo');
      if (version === currentSolo) return;
      
      // Mute old, unmute new
      stems['solo' + currentSolo].setVolume(0);
      stems['solo' + version].setVolume(parseFloat(volSlider.value));
      
      document.querySelectorAll('[data-solo]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      currentSolo = version;
      soloDisplay.textContent = 'Solo ' + version;
    }});
  }});

  // Harmony Controls
  document.querySelectorAll('[data-harmony]').forEach(btn => {{
    btn.addEventListener('click', () => {{
      const version = btn.getAttribute('data-harmony');
      if (version === currentHarmony) return;
      
      // Mute old, unmute new
      stems['harmony_' + currentHarmony].setVolume(0);
      stems['harmony_' + version].setVolume(parseFloat(volSlider.value));
      
      document.querySelectorAll('[data-harmony]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      currentHarmony = version;
      harmonyDisplay.textContent = version.charAt(0).toUpperCase() + version.slice(1);
    }});
  }});

  // Volume Control
  function updateSliderGradient(value) {{
    const percent = value * 100;
    volSlider.style.background = 'linear-gradient(to right, #5f6bff ' + percent + '%, #3a4150 ' + percent + '%)';
  }}

  volSlider.addEventListener('input', e => {{
    const val = parseFloat(e.target.value);
    updateSliderGradient(val);
    updateActiveStemVolumes();
  }});

  // Speed Control
  speedSelect.addEventListener('change', e => {{
    const rate = parseFloat(e.target.value);
    grooveWS.setPlaybackRate(rate);
    Object.values(stems).forEach(ws => ws.setPlaybackRate(rate));
  }});

  // Seek Sync - when groove seeks, all stems follow
  grooveWS.on('seek', (progress) => {{
    const time = progress * grooveWS.getDuration();
    Object.values(stems).forEach(ws => {{
      const targetTime = Math.min(time, ws.getDuration() - 0.01);
      ws.setTime(targetTime);
    }});
  }});

  // Keyboard Shortcuts
  document.addEventListener('keydown', (e) => {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    
    switch(e.key) {{
      case ' ':
        e.preventDefault();
        playBtn.click();
        break;
      case '1':
        e.preventDefault();
        switchLyrics('A');
        break;
      case '2':
        e.preventDefault();
        switchLyrics('B');
        break;
      case '3':
        e.preventDefault();
        switchLyrics('C');
        break;
      case 'ArrowLeft':
        e.preventDefault();
        grooveWS.skip(-5);
        Object.values(stems).forEach(ws => ws.skip(-5));
        break;
      case 'ArrowRight':
        e.preventDefault();
        grooveWS.skip(5);
        Object.values(stems).forEach(ws => ws.skip(5));
        break;
      case 'ArrowUp':
        e.preventDefault();
        const newVolUp = Math.min(1, parseFloat(volSlider.value) + 0.1);
        volSlider.value = newVolUp;
        updateSliderGradient(newVolUp);
        updateActiveStemVolumes();
        break;
      case 'ArrowDown':
        e.preventDefault();
        const newVolDown = Math.max(0, parseFloat(volSlider.value) - 0.1);
        volSlider.value = newVolDown;
        updateSliderGradient(newVolDown);
        updateActiveStemVolumes();
        break;
    }}
  }});

  // Initialize
  document.getElementById('waveform').style.cursor = 'pointer';
  setLyricsActive('A');
  updateSliderGradient(1);
</script>
"""

st.components.v1.html(html, height=1200)