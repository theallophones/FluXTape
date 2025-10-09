import streamlit as st
import base64
import os
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

# --- Audio files (must sit next to this script) ---
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

if len(audio_map) < 8:
    st.error("❌ Not all audio files could be loaded. Please ensure all 8 stem files are in the same directory as this script.")
    st.stop()

# ✅ Fix: safely inject JSON for JS
json_audio_map = json.dumps(audio_map)

html = f"""
<!-- =======================  HTML UI START  ======================= -->
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
  {"".join([f'<div class="vis-bar" style="animation-delay:{i*0.05}s;"></div>' for i in range(12)])}
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
      <div class="label-small labelA-small" data-idx="0">A</div>
      <div class="label-small labelB-small" data-idx="1">B</div>
      <div class="label-small labelC-small" data-idx="2">C</div>
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

<!-- =======================  JAVASCRIPT  ======================= -->
<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  const audioMap = {json_audio_map};
  const lyricsAngles = [270, 0, 90];
  let currentLyrics = 0, currentSolo = 'A', currentHarmony = 'narrow', isPlaying = false;
  let readyStems = {{ groove:false, lyrics:false, solo:false, harmony:false }};

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
    normalize: true
  }});

  function createHiddenWS() {{
    const c = document.createElement('div');
    c.style.display='none';
    document.body.appendChild(c);
    return WaveSurfer.create({{container:c, backend:'WebAudio'}});
  }}
  const lyricsWS=createHiddenWS(), soloWS=createHiddenWS(), harmonyWS=createHiddenWS();

  const playBtn=document.getElementById('playBtn');
  const lyricsPointer=document.getElementById('lyricsPointer');
  const lyricsLabels=Array.from(document.querySelectorAll('.label-small'));
  const timeDisplay=document.getElementById('time-display');
  const volSlider=document.getElementById('volumeSlider');
  const speedSelect=document.getElementById('speedSelect');
  const visualizer=document.querySelector('.visualizer-container');
  const lyricsDisplay=document.getElementById('lyricsDisplay');
  const soloDisplay=document.getElementById('soloDisplay');
  const harmonyDisplay=document.getElementById('harmonyDisplay');

  function formatTime(s) {{
    const m=Math.floor(s/60);const sec=Math.floor(s%60).toString().padStart(2,'0');return m+':'+sec;
  }}
  function updateTime() {{
    timeDisplay.textContent=formatTime(grooveWS.getCurrentTime())+' / '+formatTime(grooveWS.getDuration());
  }}
  function applySettings(ws) {{
    ws.setVolume(parseFloat(volSlider.value));ws.setPlaybackRate(parseFloat(speedSelect.value));
  }}
  function playAll() {{
    if(Object.values(readyStems).every(v=>v)){{isPlaying=true;grooveWS.play();lyricsWS.play();soloWS.play();harmonyWS.play();}}
  }}
  function pauseAll() {{
    isPlaying=false;grooveWS.pause();lyricsWS.pause();soloWS.pause();harmonyWS.pause();
  }}
  function syncTime(t) {{
    lyricsWS.setTime(t);soloWS.setTime(t);harmonyWS.setTime(t);
  }}
  function loadStem(ws,key,readyKey,cb) {{
    const t=grooveWS.getCurrentTime(), was=isPlaying;if(was)pauseAll();
    readyStems[readyKey]=false;ws.load(audioMap[key]);
    ws.once('ready',()=>{{readyStems[readyKey]=true;ws.setTime(t);applySettings(ws);if(cb)cb();if(was)setTimeout(playAll,50);}});
  }}

  grooveWS.load(audioMap.groove);lyricsWS.load(audioMap.lyricsA);soloWS.load(audioMap.soloA);harmonyWS.load(audioMap.harmony_narrow);
  grooveWS.on('ready',()=>{{readyStems.groove=true;updateTime();applySettings(grooveWS);}});
  lyricsWS.on('ready',()=>{{readyStems.lyrics=true;applySettings(lyricsWS);}});
  soloWS.on('ready',()=>{{readyStems.solo=true;applySettings(soloWS);}});
  harmonyWS.on('ready',()=>{{readyStems.harmony=true;applySettings(harmonyWS);}});
  grooveWS.on('audioprocess',updateTime);
  grooveWS.on('finish',()=>{{pauseAll();playBtn.textContent='▶';playBtn.classList.remove('pause');visualizer.classList.add('paused');}});

  playBtn.onclick=()=>{{if(isPlaying){{pauseAll();playBtn.textContent='▶';playBtn.classList.remove('pause');visualizer.classList.add('paused');}}else{{playAll();playBtn.textContent='⏸';playBtn.classList.add('pause');visualizer.classList.remove('paused');}}}};

  function setLyricsActive(i) {{
    lyricsLabels.forEach((el,idx)=>el.classList.toggle('active',idx===i));
    lyricsPointer.style.transform='translate(-50%,0) rotate('+lyricsAngles[i]+'deg)';
    lyricsDisplay.textContent='Lyrics '+['A','B','C'][i];
  }}
  function switchLyrics(i) {{
    loadStem(lyricsWS,'lyrics'+['A','B','C'][i],'lyrics',()=>{{currentLyrics=i;setLyricsActive(i);}});
  }}
  document.getElementById('lyricsKnob').onclick=()=>{{switchLyrics((currentLyrics+1)%3);}};
  lyricsLabels.forEach(el=>el.onclick=e=>{{e.stopPropagation();const i=parseInt(el.dataset.idx);if(i!==currentLyrics)switchLyrics(i);}});

  document.querySelectorAll('[data-solo]').forEach(btn=>btn.onclick=()=>{{const v=btn.dataset.solo;if(v===currentSolo)return;document.querySelectorAll('[data-solo]').forEach(b=>b.classList.remove('active'));btn.classList.add('active');loadStem(soloWS,'solo'+v,'solo',()=>{{currentSolo=v;soloDisplay.textContent='Solo '+v;}});}});
  document.querySelectorAll('[data-harmony]').forEach(btn=>btn.onclick=()=>{{const v=btn.dataset.harmony;if(v===currentHarmony)return;document.querySelectorAll('[data-harmony]').forEach(b=>b.classList.remove('active'));btn.classList.add('active');loadStem(harmonyWS,'harmony_'+v,'harmony',()=>{{currentHarmony=v;harmonyDisplay.textContent=v.charAt(0).toUpperCase()+v.slice(1);}});}});

  volSlider.oninput=e=>{{const v=parseFloat(e.target.value);[grooveWS,lyricsWS,soloWS,harmonyWS].forEach(ws=>ws.setVolume(v));}};
  speedSelect.onchange=e=>{{const r=parseFloat(e.target.value);[grooveWS,lyricsWS,soloWS,harmonyWS].forEach(ws=>ws.setPlaybackRate(r));}};
  grooveWS.on('seek',p=>syncTime(p*grooveWS.getDuration()));

  document.addEventListener('keydown',e=>{{if(['INPUT','TEXTAREA'].includes(e.target.tagName))return;
    switch(e.key){{case' ':e.preventDefault();playBtn.click();break;
      case'1':if(currentLyrics!==0)switchLyrics(0);break;
      case'2':if(currentLyrics!==1)switchLyrics(1);break;
      case'3':if(currentLyrics!==2)switchLyrics(2);break;
      case'ArrowLeft':[grooveWS,lyricsWS,soloWS,harmonyWS].forEach(ws=>ws.skip(-5));break;
      case'ArrowRight':[grooveWS,lyricsWS,soloWS,harmonyWS].forEach(ws=>ws.skip(5));break;}}
  }});
  setLyricsActive(0);
</script>
"""

st.components.v1.html(html, height=1200)