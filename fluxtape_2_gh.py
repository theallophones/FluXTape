import streamlit as st
import base64
import os

st.set_page_config(layout="wide", page_title="FluXTape", page_icon="🎵")

# Hide branding and headers
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
  background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%) fixed !important;
}
[data-testid="stHeader"], #MainMenu, footer {
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Audio stems
audio_files = {
    "A": "lyricsA.mp3",
    "B": "lyricsB.mp3",
    "C": "lyricsC.mp3",
    "groove": "groove.mp3"
}

def file_to_data_url(path, mime="audio/mpeg"):
    try:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        st.error(f"Error loading {path}: {e}")
        return None

# Convert to base64
audio_map = {}
for k, v in audio_files.items():
    if os.path.exists(v):
        audio_map[k] = file_to_data_url(v)
    else:
        st.error(f"File not found: {v}")
        st.stop()

# Send to frontend
st.components.v1.html(f"""
<script src="https://unpkg.com/wavesurfer.js@7"></script>

<div style="text-align:center; margin-top:30px;">
  <h1 style="color:white; font-family:Inter, sans-serif;">FluXTape REF3</h1>
  <p style="color:#ccc;">Lyrics A/B/C + Groove (always on)</p>
  
  <div style="margin:10px 0;">
    <button id="playBtn" style="font-size:26px;">▶</button>
    <select id="versionSelect" style="font-size:16px; padding:6px 12px;">
      <option value="A">Lyrics A</option>
      <option value="B">Lyrics B</option>
      <option value="C">Lyrics C</option>
    </select>
  </div>

  <div id="waveform" style="margin:30px auto; width:90%; max-width:1000px;"></div>
</div>

<script>
const audioMap = {{
  A: "{audio_map['A']}",
  B: "{audio_map['B']}",
  C: "{audio_map['C']}",
  groove: "{audio_map['groove']}"
}};

let current = 'A';

const wsLyrics = WaveSurfer.create({{
  container: '#waveform',
  waveColor: '#555',
  progressColor: '#5f6bff',
  height: 120,
  backend: 'WebAudio',
  cursorColor: '#fff',
  normalize: true
}});

const wsGroove = WaveSurfer.create({{
  backend: 'WebAudio',
  normalize: true
}});

const playBtn = document.getElementById('playBtn');
const select = document.getElementById('versionSelect');

function syncPlayPause(play) {{
  if (play) {{
    wsGroove.play();
    wsLyrics.play();
    playBtn.textContent = '⏸';
  }} else {{
    wsGroove.pause();
    wsLyrics.pause();
    playBtn.textContent = '▶';
  }}
}}

function loadBoth(label) {{
  const wasPlaying = wsLyrics.isPlaying();
  const time = wsLyrics.getCurrentTime();
  wsLyrics.load(audioMap[label]);
  wsGroove.load(audioMap["groove"]);
  current = label;

  wsLyrics.once('ready', () => {{
    wsGroove.setTime(time);
    wsLyrics.setTime(time);
    if (wasPlaying) {{
      wsGroove.play();
      wsLyrics.play();
    }}
  }});
}}

select.addEventListener('change', e => {{
  const next = e.target.value;
  if (next !== current) loadBoth(next);
}});

playBtn.addEventListener('click', () => {{
  const isPlaying = wsLyrics.isPlaying();
  syncPlayPause(!isPlaying);
}});

loadBoth(current);
</script>
""", height=600)