import streamlit as st
import base64
import os

st.set_page_config(layout="wide", page_title="FluXTape", page_icon="🎵")

# Hide header and branding
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

# --- Audio files (must sit next to this script) ---
audio_files = {
    "A": "lyricsA.mp3",
    "B": "lyricsB.mp3",
    "C": "lyricsC.mp3",
    "groove": "groove.mp3"
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

# Load files
audio_map = {}
for k, v in audio_files.items():
    data_url = file_to_data_url(v)
    if data_url:
        audio_map[k] = data_url

if len(audio_map) < 4:
    st.error("❌ Missing one or more required audio files.")
    st.stop()

# JS Injection
st.components.v1.html(f'''
<script src="https://unpkg.com/wavesurfer.js@7"></script>
<div style="text-align:center; margin-top:30px;">
  <h1 style="color:white; font-family:Inter, sans-serif;">FluXTape REF3</h1>
  <p style="color:#ccc;">Lyrics knob + Groove always on</p>
  <button id="playBtn" style="font-size:28px;">▶</button>
  <div id="waveform" style="margin:20px auto; width:90%; max-width:1000px;"></div>
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

// Load initial stems
wsLyrics.load(audioMap[current]);
wsGroove.load(audioMap['groove']);

// Sync start times
wsLyrics.on('ready', () => {{
  wsGroove.setTime(0);
}});

// Playback toggle
const btn = document.getElementById('playBtn');
btn.onclick = () => {{
  if (wsLyrics.isPlaying()) {{
    wsLyrics.pause(); wsGroove.pause();
    btn.textContent = '▶';
  }} else {{
    wsLyrics.play(); wsGroove.play();
    btn.textContent = '⏸';
  }}
}};
</script>
''', height=600)