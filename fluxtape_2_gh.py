import streamlit as st
import base64
import os
import json  # ✅ Needed for safe JSON injection

st.set_page_config(layout="wide", page_title="FluXTape Complete", page_icon="🎵")

# ---------- THEME STYLING ----------
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
#MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- AUDIO FILE MAP ----------
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
    """Convert file to base64 data URL."""
    try:
        if not os.path.exists(path):
            st.error(f"❌ Missing audio file: {path}")
            return None
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        st.error(f"❌ Error loading {path}: {e}")
        return None

audio_map = {}
for key, filename in audio_files.items():
    data_url = file_to_data_url(filename)
    if data_url:
        audio_map[key] = data_url

if len(audio_map) < len(audio_files):
    st.error("❌ Not all audio files loaded — ensure all 8 are present.")
    st.stop()

# ✅ Convert to safe JSON string for frontend
json_audio_map = json.dumps(audio_map)

# ---------- FRONTEND HTML ----------
html = f"""
<!-- ====================== HTML BODY ====================== -->
<div style="text-align:center; margin-bottom:10px;">
  <h1 style="font-family:'Inter', sans-serif; font-weight:800; color:#ffffff; font-size:48px; margin-bottom:5px; letter-spacing:-1px;">
    FluX‑Tape
  </h1>
  <h3 style="font-family:'Inter', sans-serif; font-weight:400; color:#8b92a8; font-size:16px; margin-top:0; letter-spacing:0.5px;">
    Songs as Probability Clouds
  </h3>
  <div style="margin-top:15px;">
    <button id="playBtn" class="play-btn" title="Play/Pause (Space)">▶</button>
  </div>
</div>

<div id="waveform" style="margin:30px auto; width:90%; max-width:1200px;"></div>

<div class="visualizer-container paused">
  {''.join([f'<div class="vis-bar" style="animation-delay:{i*0.1}s;"></div>' for i in range(12)])}
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

<!-- Control panels -->
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
    <div class="control-header">SPATIALIZE</div>
    <div style="display:flex; justify-content:center;">
      <button id="spatializeBtn" class="spatialize-btn">OFF</button>
    </div>
    <div id="spatializeDisplay" class="version-badge">Narrow</div>
  </div>
</div>

<!-- ====================== JAVASCRIPT ====================== -->
<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  // ✅ JSON-safe injection
  const audioMap = {json_audio_map};
  const lyricsAngles = {{A: 270, B: 0, C: 90}};

  const audioElements = {{}};
  Object.keys(audioMap).forEach(k => {{
    const el = new Audio(audioMap[k]);
    el.preload = 'auto';
    audioElements[k] = el;
  }});

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
    normalize: true
  }});

  // STATE
  let currentLyrics = 'A';
  let currentSolo = 'A';
  let spatializeOn = false;
  let isPlaying = false;

  // ELEMENTS
  const playBtn = document.getElementById('playBtn');
  const volSlider = document.getElementById('volumeSlider');
  const speedSelect = document.getElementById('speedSelect');
  const lyricsLabels = Array.from(document.querySelectorAll('[data-lyrics]'));
  const lyricsPointer = document.getElementById('lyricsPointer');
  const lyricsDisplay = document.getElementById('lyricsDisplay');
  const soloDisplay = document.getElementById('soloDisplay');
  const spatializeBtn = document.getElementById('spatializeBtn');
  const spatializeDisplay = document.getElementById('spatializeDisplay');
  const visualizer = document.querySelector('.visualizer-container');
  const timeDisplay = document.getElementById('time-display');

  function formatTime(s) {{
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60).toString().padStart(2, '0');
    return m + ':' + sec;
  }}

  function updateTime() {{
    const a = audioElements.groove;
    timeDisplay.textContent = formatTime(a.currentTime) + ' / ' + formatTime(a.duration || 0);
  }}

  function updateVolumes() {{
    const vol = parseFloat(volSlider.value);
    audioElements.groove.volume = vol;
    ['A','B','C'].forEach(v => audioElements['lyrics'+v].volume = (v===currentLyrics)?vol:0);
    ['A','B'].forEach(v => audioElements['solo'+v].volume = (v===currentSolo)?vol:0);
    audioElements.harmony_narrow.volume = spatializeOn?0:vol;
    audioElements.harmony_wide.volume = spatializeOn?vol:0;
  }}

  function updateSpeed() {{
    const r = parseFloat(speedSelect.value);
    Object.values(audioElements).forEach(a => a.playbackRate = r);
  }}

  function syncAll() {{
    const t = audioElements.groove.currentTime;
    Object.entries(audioElements).forEach(([k,a]) => {{
      if (k!=='groove') a.currentTime = t;
    }});
  }}

  function playAll() {{
    syncAll();
    Object.values(audioElements).forEach(a => a.play());
    isPlaying = true;
    playBtn.textContent='⏸';
    playBtn.classList.add('pause');
    visualizer.classList.remove('paused');
  }}

  function pauseAll() {{
    Object.values(audioElements).forEach(a => a.pause());
    isPlaying=false;
    playBtn.textContent='▶';
    playBtn.classList.remove('pause');
    visualizer.classList.add('paused');
  }}

  grooveWS.load(audioMap.groove);
  grooveWS.on('seek', p => {{
    const t = p * audioElements.groove.duration;
    Object.values(audioElements).forEach(a => a.currentTime = t);
  }});
  audioElements.groove.addEventListener('timeupdate', updateTime);
  audioElements.groove.addEventListener('ended', pauseAll);

  // Play/Pause
  playBtn.onclick = ()=> isPlaying?pauseAll():playAll();

  // Lyrics
  function setLyricsActive(v) {{
    lyricsLabels.forEach(el=>el.classList.toggle('active', el.dataset.lyrics===v));
    lyricsPointer.style.transform='translate(-50%,0) rotate('+lyricsAngles[v]+'deg)';
    lyricsDisplay.textContent='Lyrics '+v;
  }}
  function switchLyrics(v) {{ currentLyrics=v; updateVolumes(); setLyricsActive(v); }}
  document.getElementById('lyricsKnob').onclick = ()=>switchLyrics({{A:'B',B:'C',C:'A'}}[currentLyrics]);
  lyricsLabels.forEach(el=>el.onclick=e=>switchLyrics(el.dataset.lyrics));

  // Solo
  document.querySelectorAll('[data-solo]').forEach(btn=>btn.onclick=()=>{
    const v=btn.dataset.solo;
    if(v!==currentSolo){{
      currentSolo=v;
      updateVolumes();
      document.querySelectorAll('[data-solo]').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      soloDisplay.textContent='Solo '+v;
    }}
  });

  // Spatialize
  spatializeBtn.onclick=()=>{
    spatializeOn=!spatializeOn;
    updateVolumes();
    spatializeBtn.classList.toggle('active', spatializeOn);
    spatializeBtn.textContent=spatializeOn?'ON':'OFF';
    spatializeDisplay.textContent=spatializeOn?'Wide':'Narrow';
  };

  // Volume + Speed
  volSlider.oninput=e=>updateVolumes();
  speedSelect.onchange=e=>updateSpeed();

  // Keyboard
  document.addEventListener('keydown',e=>{
    if(['INPUT','TEXTAREA'].includes(e.target.tagName)) return;
    switch(e.key){{
      case ' ': e.preventDefault(); playBtn.click(); break;
      case '1': switchLyrics('A'); break;
      case '2': switchLyrics('B'); break;
      case '3': switchLyrics('C'); break;
      case 'ArrowLeft': Object.values(audioElements).forEach(a=>a.currentTime=Math.max(0,a.currentTime-5)); break;
      case 'ArrowRight': Object.values(audioElements).forEach(a=>a.currentTime=Math.min(a.duration,a.currentTime+5)); break;
    }}
  });

  // Init
  setLyricsActive('A');
  updateVolumes();
  updateSpeed();
  console.log('✅ FluXTape Initialized');
</script>
"""

st.components.v1.html(html, height=1200)