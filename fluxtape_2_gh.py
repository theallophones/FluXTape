import streamlit as st
import json

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

audio_map = {
    "groove": "https://www.peymansalimi.com/wp-content/uploads/fluxtape/groove.mp3",
    "lyricsA": "https://www.peymansalimi.com/wp-content/uploads/fluxtape/lyricsA.mp3",
    "lyricsB": "https://www.peymansalimi.com/wp-content/uploads/fluxtape/lyricsB.mp3",
    "lyricsC": "https://www.peymansalimi.com/wp-content/uploads/fluxtape/lyricsC.mp3",
    "soloA": "https://www.peymansalimi.com/wp-content/uploads/fluxtape/soloA.mp3",
    "soloB": "https://www.peymansalimi.com/wp-content/uploads/fluxtape/soloB.mp3",
    "harmony_narrow": "https://www.peymansalimi.com/wp-content/uploads/fluxtape/harmony_narrow.mp3",
    "harmony_wide": "https://www.peymansalimi.com/wp-content/uploads/fluxtape/harmony_wide.mp3",
    "adlibA": "https://www.peymansalimi.com/wp-content/uploads/fluxtape/adlibA.mp3",
    "adlibB": "https://www.peymansalimi.com/wp-content/uploads/fluxtape/adlibB.mp3",
    "adlibC": "https://www.peymansalimi.com/wp-content/uploads/fluxtape/adlibC.mp3",
}

audio_map_json = json.dumps(audio_map)

html = f"""
<div style="text-align:center; margin-bottom:10px;">
  <h1 style="font-family:'Inter', sans-serif; font-weight:800; color:#ffffff; font-size:48px; margin-bottom:5px; letter-spacing:-1px;">
    FluX-Tape
  </h1>
  <h3 style="font-family:'Inter', sans-serif; font-weight:400; color:#8b92a8; font-size:16px; margin-top:0; letter-spacing:0.5px;">
    Songs as Probability Clouds
  </h3>
  <div id="loadingStatus" style="color:#8b92a8; margin:10px 0; font-size:14px;">Loading audio files...</div>
  <div style="margin-top:15px;">
    <button id="playBtn" class="play-btn" title="Play/Pause (Space)" disabled style="opacity:0.5;">▶</button>
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

<div style="display:flex; justify-content:center; align-items:center; margin-top:20px;">
  <div id="time-display" style="color:#ffffff; font-family:'JetBrains Mono', 'Courier New', monospace; font-size:24px; font-weight:600; letter-spacing:2px;">
    0:00 / 0:00
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
      <div class="label-small labelA-small active" data-lyrics="A">A</div>
      <div class="label-small labelB-small" data-lyrics="B">B</div>
      <div class="label-small labelC-small" data-lyrics="C">C</div>
    </div>
    <div id="lyricsDisplay" class="version-badge">Lyrics A</div>
  </div>

  <div class="control-section">
    <div class="control-header">SOLO <span style="font-size:10px; font-weight:400; opacity:0.7;">(from 1:03)</span></div>
    <div class="knob-wrap-small">
      <div id="soloKnob" class="knob-small" title="Click to switch solo">
        <div id="soloPointer" class="pointer-small"></div>
        <div class="center-dot-small"></div>
      </div>
      <div class="label-small labelLeft-small active" data-solo="A">A</div>
      <div class="label-small labelRight-small" data-solo="B">B</div>
    </div>
    <div id="soloDisplay" class="version-badge">Take A</div>
  </div>

  <div class="control-section">
    <div class="control-header">SPATIALIZE</div>
    <div class="knob-wrap-small">
      <div id="spatializeKnob" class="knob-small" title="Click to toggle spatialize">
        <div id="spatializePointer" class="pointer-small"></div>
        <div class="center-dot-small"></div>
      </div>
      <div class="label-small labelLeft-small active" data-spatialize="narrow">N</div>
      <div class="label-small labelRight-small" data-spatialize="wide">W</div>
    </div>
    <div id="spatializeDisplay" class="version-badge">Narrow</div>
  </div>

  <div class="control-section">
    <div class="control-header">BACK VOCALS</div>
    <div class="knob-wrap-small">
      <div id="backVocalsKnob" class="knob-small" title="Click to toggle back vocals">
        <div id="backVocalsPointer" class="pointer-small"></div>
        <div class="center-dot-small"></div>
      </div>
      <div class="label-small labelLeft-small active" data-backvocals="off">OFF</div>
      <div class="label-small labelRight-small" data-backvocals="on">ON</div>
    </div>
    <div id="backVocalsDisplay" class="version-badge">Off</div>
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
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
  
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
  .play-btn:disabled {{
    cursor: not-allowed;
    opacity: 0.5;
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
  
  .labelLeft-small {{ top: 50%; left: -25px; transform: translateY(-50%); }}
  .labelRight-small {{ top: 50%; right: -25px; transform: translateY(-50%); }}

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
  const audioMap = {audio_map_json};
  const lyricsAngles = {{"A": 270, "B": 0, "C": 90}};

  const AudioContext = window.AudioContext || window.webkitAudioContext;
  const audioContext = new AudioContext();
  
  const masterGain = audioContext.createGain();
  masterGain.gain.value = 1.0;
  masterGain.connect(audioContext.destination);
  
  const masterAnalyser = audioContext.createAnalyser();
  masterAnalyser.fftSize = 2048;
  masterGain.connect(masterAnalyser);

  const grooveWS = WaveSurfer.create({{
    container: '#waveform',
    waveColor: '#4a5568',
    progressColor: '#5f6bff',
    height: 140,
    backend: 'WebAudio',
    audioContext: audioContext,
    cursorWidth: 2,
    cursorColor: '#fff',
    barWidth: 3,
    barGap: 2,
    barRadius: 3,
    responsive: true,
    normalize: true
  }});

  function createHiddenWS() {{
    const div = document.createElement('div');
    div.style.display = 'none';
    document.body.appendChild(div);
    return WaveSurfer.create({{
      container: div,
      backend: 'MediaElement'
    }});
  }}

  const stems = {{
    lyricsA: createHiddenWS(),
    lyricsB: createHiddenWS(),
    lyricsC: createHiddenWS(),
    soloA: createHiddenWS(),
    soloB: createHiddenWS(),
    harmony_narrow: createHiddenWS(),
    harmony_wide: createHiddenWS(),
    adlibA: createHiddenWS(),
    adlibB: createHiddenWS(),
    adlibC: createHiddenWS()
  }};

  let currentLyrics = 'A';
  let currentSolo = 'A';
  let spatializeOn = false;
  let backVocalsOn = false;
  let isPlaying = false;
  let allReady = false;
  let readyCount = 0;

  const playBtn = document.getElementById('playBtn');
  const loadingStatus = document.getElementById('loadingStatus');
  const lyricsPointer = document.getElementById('lyricsPointer');
  const lyricsLabels = Array.from(document.querySelectorAll('[data-lyrics]'));
  const soloPointer = document.getElementById('soloPointer');
  const soloLabels = Array.from(document.querySelectorAll('[data-solo]'));
  const spatializePointer = document.getElementById('spatializePointer');
  const spatializeLabels = Array.from(document.querySelectorAll('[data-spatialize]'));
  const backVocalsPointer = document.getElementById('backVocalsPointer');
  const backVocalsLabels = Array.from(document.querySelectorAll('[data-backvocals]'));
  const timeDisplay = document.getElementById('time-display');
  const volSlider = document.getElementById('volumeSlider');
  const visualizer = document.querySelector('.visualizer-container');
  const lyricsDisplay = document.getElementById('lyricsDisplay');
  const soloDisplay = document.getElementById('soloDisplay');
  const spatializeDisplay = document.getElementById('spatializeDisplay');
  const backVocalsDisplay = document.getElementById('backVocalsDisplay');

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
    console.log('Ready:', readyCount + '/11');
    loadingStatus.textContent = 'Loading... (' + readyCount + '/11)';
    
    if (readyCount === 11) {{
      allReady = true;
      console.log('✅ All stems ready!');
      loadingStatus.textContent = '✅ Ready to play!';
      loadingStatus.style.color = '#4CAF50';
      
      playBtn.disabled = false;
      playBtn.style.opacity = '1';
      
      const vol = parseFloat(volSlider.value);
      
      grooveWS.setVolume(vol);
      stems.lyricsA.setVolume(vol);
      stems.lyricsB.setVolume(0);
      stems.lyricsC.setVolume(0);
      stems.soloA.setVolume(vol);
      stems.soloB.setVolume(0);
      stems.harmony_narrow.setVolume(vol);
      stems.harmony_wide.setVolume(0);
      stems.adlibA.setVolume(0);
      stems.adlibB.setVolume(0);
      stems.adlibC.setVolume(0);
      
      console.log('✅ Ready to play with sound!');
    }}
  }}

  function updateVolumes() {{
    const vol = parseFloat(volSlider.value);
    
    grooveWS.setVolume(vol);
    stems.lyricsA.setVolume(currentLyrics === 'A' ? vol : 0);
    stems.lyricsB.setVolume(currentLyrics === 'B' ? vol : 0);
    stems.lyricsC.setVolume(currentLyrics === 'C' ? vol : 0);
    stems.soloA.setVolume(currentSolo === 'A' ? vol : 0);
    stems.soloB.setVolume(currentSolo === 'B' ? vol : 0);
    stems.harmony_narrow.setVolume(!spatializeOn ? vol : 0);
    stems.harmony_wide.setVolume(spatializeOn ? vol : 0);
    stems.adlibA.setVolume(backVocalsOn && currentLyrics === 'A' ? vol : 0);
    stems.adlibB.setVolume(backVocalsOn && currentLyrics === 'B' ? vol : 0);
    stems.adlibC.setVolume(backVocalsOn && currentLyrics === 'C' ? vol : 0);
  }}

  function playAll() {{
    if (!allReady) return;
    
    isPlaying = true;
    const currentTime = grooveWS.getCurrentTime();
    grooveWS.play(currentTime);
    Object.values(stems).forEach(ws => ws.play(currentTime));
  }}

  function pauseAll() {{
    isPlaying = false;
    grooveWS.pause();
    Object.values(stems).forEach(ws => ws.pause());
  }}

  grooveWS.load(audioMap.groove);
  
  grooveWS.on('error', (err) => {{
    console.error('Groove load error:', err);
    loadingStatus.textContent = '❌ Error loading audio. Check console.';
    loadingStatus.style.color = '#f44336';
  }});
  
  grooveWS.on('ready', () => {{
    console.log('✓ Groove');
    updateTime();
    checkReady();
  }});

  Object.keys(stems).forEach(key => {{
    stems[key].load(audioMap[key]);
    
    stems[key].on('error', (err) => {{
      console.error(key + ' load error:', err);
      loadingStatus.textContent = '❌ Error loading ' + key;
      loadingStatus.style.color = '#f44336';
    }});
    
    stems[key].on('ready', () => {{
      console.log('✓', key);
      checkReady();
    }});
  }});

  grooveWS.on('audioprocess', updateTime);
  grooveWS.on('finish', () => {{
    pauseAll();
    playBtn.textContent = '▶';
    playBtn.classList.remove('pause');
    visualizer.classList.add('paused');
  }});

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

  function setLyricsActive(version) {{
    lyricsLabels.forEach(el => {{
      el.classList.toggle('active', el.getAttribute('data-lyrics') === version);
    }});
    lyricsPointer.style.transform = 'translate(-50%, 0) rotate(' + lyricsAngles[version] + 'deg)';
    lyricsDisplay.textContent = 'Lyrics ' + version;
  }}

  function switchLyrics(version) {{
    if (version === currentLyrics) return;
    currentLyrics = version;
    updateVolumes();
    setLyricsActive(version);
  }}

  document.getElementById('lyricsKnob').addEventListener('click', () => {{
    const next = {{"A": "B", "B": "C", "C": "A"}}[currentLyrics];
    switchLyrics(next);
  }});

  lyricsLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      switchLyrics(el.getAttribute('data-lyrics'));
    }});
  }});

  document.getElementById('soloKnob').addEventListener('click', () => {{
    const next = currentSolo === 'A' ? 'B' : 'A';
    switchSolo(next);
  }});

  soloLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      switchSolo(el.getAttribute('data-solo'));
    }});
  }});

  function switchSolo(version) {{
    if (version === currentSolo) return;
    currentSolo = version;
    updateVolumes();
    soloLabels.forEach(el => {{
      el.classList.toggle('active', el.getAttribute('data-solo') === version);
    }});
    const angle = version === 'A' ? 270 : 90;
    soloPointer.style.transform = 'translate(-50%, 0) rotate(' + angle + 'deg)';
    soloDisplay.textContent = 'Take ' + version;
  }}

  document.getElementById('spatializeKnob').addEventListener('click', () => {{
    toggleSpatialize();
  }});

  spatializeLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      const isWide = el.getAttribute('data-spatialize') === 'wide';
      if (isWide !== spatializeOn) {{
        toggleSpatialize();
      }}
    }});
  }});

  function toggleSpatialize() {{
    spatializeOn = !spatializeOn;
    updateVolumes();
    spatializeLabels.forEach(el => {{
      const isWide = el.getAttribute('data-spatialize') === 'wide';
      el.classList.toggle('active', isWide === spatializeOn);
    }});
    const angle = spatializeOn ? 90 : 270;
    spatializePointer.style.transform = 'translate(-50%, 0) rotate(' + angle + 'deg)';
    spatializeDisplay.textContent = spatializeOn ? 'Wide' : 'Narrow';
  }}

  document.getElementById('backVocalsKnob').addEventListener('click', () => {{
    toggleBackVocals();
  }});

  backVocalsLabels.forEach(el => {{
    el.addEventListener('click', (e) => {{
      e.stopPropagation();
      const isOn = el.getAttribute('data-backvocals') === 'on';
      if (isOn !== backVocalsOn) {{
        toggleBackVocals();
      }}
    }});
  }});

  function toggleBackVocals() {{
    backVocalsOn = !backVocalsOn;
    updateVolumes();
    backVocalsLabels.forEach(el => {{
      const isOn = el.getAttribute('data-backvocals') === 'on';
      el.classList.toggle('active', isOn === backVocalsOn);
    }});
    const angle = backVocalsOn ? 90 : 270;
    backVocalsPointer.style.transform = 'translate(-50%, 0) rotate(' + angle + 'deg)';
    backVocalsDisplay.textContent = backVocalsOn ? 'On' : 'Off';
  }}

  function updateSliderGradient(value) {{
    const percent = value * 100;
    volSlider.style.background = 'linear-gradient(to right, #5f6bff ' + percent + '%, #3a4150 ' + percent + '%)';
  }}

  volSlider.addEventListener('input', e => {{
    updateSliderGradient(e.target.value);
    updateVolumes();
  }});

  let isSeeking = false;
  let wasPlayingBeforeSeek = false;

  grooveWS.on('interaction', () => {{
    if (isPlaying && !isSeeking) {{
      console.log('Seeking started - pausing playback');
      isSeeking = true;
      wasPlayingBeforeSeek = true;
      grooveWS.pause();
      Object.values(stems).forEach(ws => ws.pause());
      isPlaying = false;
    }}
  }});

  grooveWS.on('seek', (progress) => {{
    const targetTime = progress * grooveWS.getDuration();
    console.log('Seek to:', targetTime);
    Object.values(stems).forEach(ws => {{
      ws.setTime(Math.min(targetTime, ws.getDuration() - 0.01));
    }});
    if (wasPlayingBeforeSeek) {{
      setTimeout(() => {{
        if (isSeeking) {{
          console.log('Seek ended - restarting playback');
          isSeeking = false;
          wasPlayingBeforeSeek = false;
          const exactTime = grooveWS.getCurrentTime();
          console.log('Restarting all at exact time:', exactTime);
          isPlaying = true;
          grooveWS.play(exactTime);
          Object.values(stems).forEach(ws => ws.play(exactTime));
        }}
      }}, 100);
    }}
  }});

  document.addEventListener('keydown', (e) => {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
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
        updateVolumes();
        break;
      case 'ArrowDown':
        e.preventDefault();
        const newVolDown = Math.max(0, parseFloat(volSlider.value) - 0.1);
        volSlider.value = newVolDown;
        updateSliderGradient(newVolDown);
        updateVolumes();
        break;
    }}
  }});

  document.getElementById('waveform').style.cursor = 'pointer';
  updateSliderGradient(1);
</script>
"""

st.components.v1.html(html, height=1300)