import streamlit as st
import base64
import os

st.set_page_config(layout="wide", page_title="FluXTape Complete", page_icon="🎵")

# Style override
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
  background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%) fixed !important;
}
[data-testid="stHeader"], [data-testid="stSidebar"], #MainMenu, footer {
  background: rgba(0,0,0,0) !important;
  visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# All audio stems
audio_files = {
    "groove": "groove.mp3",
    "lyricsA": "lyricsA.mp3",
    "lyricsB": "lyricsB.mp3",
    "lyricsC": "lyricsC.mp3",
    "adlibA": "adlibA.mp3",
    "adlibB": "adlibB.mp3",
    "adlibC": "adlibC.mp3",
    "soloA": "soloA.mp3",
    "soloB": "soloB.mp3",
    "harmony_narrow": "harmony_narrow.mp3",
    "harmony_wide": "harmony_wide.mp3",
}

# Encode audio to base64
def file_to_data_url(path, mime="audio/mpeg"):
    if not os.path.exists(path):
        st.error(f"❌ Audio file not found: {path}")
        return None
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

# Load audio into map
audio_map = {}
for k, v in audio_files.items():
    data_url = file_to_data_url(v)
    if data_url:
        audio_map[k] = data_url

if len(audio_map) < len(audio_files):
    st.error("❌ Some audio files are missing. Please check your folder.")
    st.stop()

# Inject HTML/JS
st.components.v1.html(f"""
<div style="text-align:center;">
  <h1 style="color:white; font-size: 48px;">FluXTape</h1>
  <h4 style="color:#aaa;">Songs as Probability Clouds</h4>
  <button id="playBtn" class="play-btn">▶</button>
</div>

<!-- Control Sections -->
<div style="margin: 30px auto; display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; max-width: 900px;">

  <!-- Lyrics -->
  <div style="text-align:center;">
    <div>Lyrics</div>
    <button onclick="cycleLyrics()" id="lyricsLabel" class="control-label">A</button>
  </div>

  <!-- Solo -->
  <div style="text-align:center;">
    <div>Solo</div>
    <button onclick="setSolo('A')" id="soloA" class="control-label selected">A</button>
    <button onclick="setSolo('B')" id="soloB" class="control-label">B</button>
  </div>

  <!-- Spatialize -->
  <div style="text-align:center;">
    <div>Spatialize</div>
    <button onclick="toggleSpatial()" id="spatialBtn" class="control-label">Narrow</button>
  </div>

  <!-- Back Vocals -->
  <div style="text-align:center;">
    <div>Back Vocals</div>
    <button onclick="toggleBackVocals()" id="backBtn" class="control-label">OFF</button>
  </div>

</div>

<script>
  const audioMap = {audio_map};

  const audio = {{
    groove: new Audio(audioMap["groove"]),
    lyricsA: new Audio(audioMap["lyricsA"]),
    lyricsB: new Audio(audioMap["lyricsB"]),
    lyricsC: new Audio(audioMap["lyricsC"]),
    adlibA: new Audio(audioMap["adlibA"]),
    adlibB: new Audio(audioMap["adlibB"]),
    adlibC: new Audio(audioMap["adlibC"]),
    soloA: new Audio(audioMap["soloA"]),
    soloB: new Audio(audioMap["soloB"]),
    harmony_narrow: new Audio(audioMap["harmony_narrow"]),
    harmony_wide: new Audio(audioMap["harmony_wide"]),
  }};

  let currentLyrics = "A";
  let currentSolo = "A";
  let spatial = false;
  let backVocals = false;

  Object.values(audio).forEach(a => {{
    a.preload = 'auto';
    a.volume = 0;
  }});
  audio["groove"].volume = 1;
  audio["lyricsA"].volume = 1;
  audio["adlibA"].volume = 0;

  function syncTime(toTime) {{
    Object.values(audio).forEach(a => {{
      a.currentTime = toTime;
    }});
  }}

  function updateVolumes() {{
    const vol = 1;
    audio["lyricsA"].volume = currentLyrics === "A" ? vol : 0;
    audio["lyricsB"].volume = currentLyrics === "B" ? vol : 0;
    audio["lyricsC"].volume = currentLyrics === "C" ? vol : 0;

    audio["adlibA"].volume = backVocals && currentLyrics === "A" ? vol : 0;
    audio["adlibB"].volume = backVocals && currentLyrics === "B" ? vol : 0;
    audio["adlibC"].volume = backVocals && currentLyrics === "C" ? vol : 0;

    audio["soloA"].volume = currentSolo === "A" ? vol : 0;
    audio["soloB"].volume = currentSolo === "B" ? vol : 0;

    audio["harmony_narrow"].volume = spatial ? 0 : vol;
    audio["harmony_wide"].volume = spatial ? vol : 0;
  }}

  function playAll() {{
    Object.values(audio).forEach(a => {{
      a.play();
    }});
  }}

  function pauseAll() {{
    Object.values(audio).forEach(a => {{
      a.pause();
    }});
  }}

  function togglePlay() {{
    if (audio["groove"].paused) {{
      syncTime(audio["groove"].currentTime);
      playAll();
      document.getElementById("playBtn").textContent = "⏸";
    }} else {{
      pauseAll();
      document.getElementById("playBtn").textContent = "▶";
    }}
  }}

  function cycleLyrics() {{
    const next = {{A: "B", B: "C", C: "A"}}[currentLyrics];
    currentLyrics = next;
    document.getElementById("lyricsLabel").textContent = next;
    updateVolumes();
  }}

  function setSolo(which) {{
    currentSolo = which;
    document.getElementById("soloA").classList.remove("selected");
    document.getElementById("soloB").classList.remove("selected");
    document.getElementById("solo" + which).classList.add("selected");
    updateVolumes();
  }}

  function toggleSpatial() {{
    spatial = !spatial;
    document.getElementById("spatialBtn").textContent = spatial ? "Wide" : "Narrow";
    updateVolumes();
  }}

  function toggleBackVocals() {{
    backVocals = !backVocals;
    document.getElementById("backBtn").textContent = backVocals ? "ON" : "OFF";
    updateVolumes();
  }}

  document.getElementById("playBtn").addEventListener("click", togglePlay);
</script>

<style>
  .control-label {{
    padding: 8px 14px;
    margin: 4px;
    background: #333;
    color: white;
    border: 2px solid #666;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
  }}
  .control-label.selected {{
    background: #4CAF50;
    border-color: #4CAF50;
    color: #fff;
  }}
  .play-btn {{
    background: #5f6bff;
    border: none;
    color: white;
    font-size: 28px;
    border-radius: 50%;
    width: 80px;
    height: 80px;
    cursor: pointer;
    margin-top: 20px;
  }}
</style>
"""

st.components.v1.html(html, height=1300)