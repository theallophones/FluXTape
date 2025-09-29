import streamlit as st
import base64

st.set_page_config(layout="wide")

st.markdown("""
<style>
/* page gradient */
[data-testid="stAppViewContainer"] {
  background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%) fixed !important;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
[data-testid="stSidebar"] { background: rgba(0,0,0,0.15) !important; }

/* general */
html, body, .stApp {
  height: 100%;
  margin: 0;
  background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%);
}

/* play button */
.play-btn {
  width: 82px; height: 82px; border-radius: 50%;
  border: none; font-size: 34px; cursor: pointer; color: #fff;
  background: #4CAF50;
  transition: background .25s ease, transform .2s ease, box-shadow .3s ease;
  box-shadow: 0 6px 20px rgba(76,175,80,.4);
}
.play-btn:hover { transform: scale(1.1); }
.play-btn.pause { background: #FBC02D; box-shadow: 0 6px 20px rgba(251,192,45,.4); }

/* knob */
.knob-wrap {
  position: relative; width: 260px; height: 260px;
  margin: 50px auto; display: flex; align-items: center; justify-content: center;
}
.knob {
  width: 160px; height: 160px; border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, #2b313c, #1b1f27 70%);
  position: relative; box-shadow: inset 0 6px 14px rgba(0,0,0,.5), 0 8px 24px rgba(0,0,0,.35);
  border: 1px solid #2e3440;
}
.center-dot {
  width: 12px; height: 12px; border-radius: 50%; background: #cfd8dc;
  position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%);
}
.pointer {
  position: absolute; width: 4px; height: 55px; background: #ffffff; border-radius: 2px;
  transform-origin: bottom center; bottom: 50%; left: 50%; translate: -50% 0;
  box-shadow: 0 0 8px rgba(255,255,255,.35); transition: transform .4s ease;
}

/* labels */
.label {
  position: absolute; background: #2a2f3a; color: #ffffff; padding: 7px 14px;
  border-radius: 14px; font-family: sans-serif; font-size: 14px; cursor: pointer;
  transition: background .25s ease, box-shadow .25s ease;
}
.label:hover { background: #3a4150; }
.label.active { background: #b71c1c; box-shadow: 0 0 14px rgba(183,28,28,0.9); }
/* A=9pm, B=12, C=3pm */
.labelA { top: 50%; left: -40px; transform: translateY(-50%); }
.labelB { top: -20px; left: 50%; transform: translateX(-50%); }
.labelC { top: 50%; right: -40px; transform: translateY(-50%); }

/* volume slider (purple fill left, grey right; grey thumb) */
.slider {
  -webkit-appearance: none; width: 260px; height: 6px; border-radius: 3px;
  background: linear-gradient(to right, #5f6bff 100%, #c9cbd3 0%);
  outline: none; cursor: pointer;
}
.slider::-webkit-slider-thumb {
  -webkit-appearance: none; appearance: none; width: 18px; height: 18px;
  border-radius: 50%; background: #c9cbd3; box-shadow: 0 0 6px rgba(200,200,200,.6);
  transition: transform .2s ease;
}
.slider::-webkit-slider-thumb:hover { transform: scale(1.2); }
.slider::-moz-range-thumb {
  width: 18px; height: 18px; border-radius: 50%; background: #c9cbd3;
  box-shadow: 0 0 6px rgba(200,200,200,.6); cursor: pointer;
}

/* spectrum canvas */
#spectrum {
  display:block; margin:20px auto; background: transparent;
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

<!-- waveform -->
<div id="waveform" style="margin:25px auto; width:85%;"></div>

<!-- time counter -->
<div id="time-display" style="text-align:center; margin-top:6px; color:#ccc; font-family:sans-serif; font-size:14px;">
  0:00 / 0:00
</div>

<!-- spectrum analyzer (bouncing bars) -->
<canvas id="spectrum" width="600" height="120"></canvas>

<!-- knob + labels -->
<div class="knob-wrap">
  <div id="knob" class="knob" title="Click to switch Lyrics version">
    <div id="pointer" class="pointer"></div>
    <div class="center-dot"></div>
  </div>
  <div class="label labelA" data-idx="0">Lyrics A</div>
  <div class="label labelB" data-idx="1">Lyrics B</div>
  <div class="label labelC" data-idx="2">Lyrics C</div>
</div>

<!-- volume -->
<div style="text-align:center; margin-top:20px;">
  <input id="volumeSlider" type="range" min="0" max="1" step="0.01" value="1" class="slider">
</div>

<!-- wavesurfer -->
<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>

<script>
  const audioMap = {audio_map};
  const labels = ["A","B","C"];
  const angles = [270, 0, 90]; // A=left, B=top, C=right

  // Use MediaElement backend so we can grab the <audio> and build our own WebAudio chain
  const ws = WaveSurfer.create({{
    container: '#waveform',
    waveColor: '#c9cbd3',
    progressColor: '#5f6bff',
    height: 120,
    backend: 'MediaElement',
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

  function updateSliderGradient(value) {{
    const percent = value * 100;
    volSlider.style.background =
      `linear-gradient(to right, #5f6bff ${{percent}}%, #c9cbd3 ${{percent}}%)`;
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
      // keep gain and slider visuals in sync
      gainNode.gain.value = parseFloat(volSlider.value);
      updateSliderGradient(volSlider.value);
    }});
    currentIdx = idx;
    current = label;
    setPointer(idx);
    setLabelActive(idx);
  }}

  // init
  ws.load(audioMap[current]);
  setPointer(currentIdx);
  setLabelActive(currentIdx);

  ws.on('ready', () => {{
    updateTime();
    updateSliderGradient(volSlider.value);
  }});
  ws.on('audioprocess', updateTime);

  // --- Web Audio graph for analyzer (using the <audio> element) ---
  const audioEl = ws.getMediaElement(); // HTMLAudioElement
  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  const ac = new AudioCtx();

  // Route: audioEl (muted) -> MediaElementSource -> Analyser -> Gain -> destination
  const source = ac.createMediaElementSource(audioEl);
  const analyser = ac.createAnalyser();
  analyser.fftSize = 256;
  const bufferLength = analyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);

  const gainNode = ac.createGain();

  source.connect(analyser);
  analyser.connect(gainNode);
  gainNode.connect(ac.destination);

  // prevent double-audio (we output via our context)
  audioEl.muted = true;

  // Start/resume AudioContext on user gesture
  let acStarted = false;
  function ensureAC() {{
    if (!acStarted) {{
      ac.resume();
      acStarted = true;
    }}
  }}

  // play/pause
  playBtn.addEventListener('click', () => {{ ensureAC(); ws.playPause(); }});
  ws.on('play', () => {{ playBtn.textContent = '⏸'; playBtn.classList.add('pause'); }});
  ws.on('pause', () => {{ playBtn.textContent = '▶'; playBtn.classList.remove('pause'); }});

  // volume: control our gain node (and keep slider gradient)
  volSlider.addEventListener('input', e => {{
    const val = parseFloat(e.target.value);
    gainNode.gain.value = val;
    updateSliderGradient(val);
  }});
  // set initial gain
  gainNode.gain.value = parseFloat(volSlider.value);

  // knob cycle
  document.getElementById('knob').addEventListener('click', () => {{
    ensureAC();
    const next = (currentIdx + 1) % 3;
    loadVersion(next);
  }});

  // label click
  labelEls.forEach(el => {{
    el.addEventListener('click', () => {{
      ensureAC();
      const idx = parseInt(el.getAttribute('data-idx'));
      if (idx !== currentIdx) loadVersion(idx);
    }});
  }});

  // --- draw bouncing spectrum bars ---
  const spectrumCanvas = document.getElementById('spectrum');
  const ctx = spectrumCanvas.getContext('2d');

  function drawSpectrum() {{
    requestAnimationFrame(drawSpectrum);
    analyser.getByteFrequencyData(dataArray);

    ctx.clearRect(0, 0, spectrumCanvas.width, spectrumCanvas.height);

    const barWidth = (spectrumCanvas.width / bufferLength) * 2.5;
    let x = 0;

    for (let i = 0; i < bufferLength; i++) {{
      const barHeight = dataArray[i] / 2;

      // Purple → pinkish based on level
      const r = Math.min(255, 80 + barHeight);
      const g = 60;
      const b = 200;
      ctx.fillStyle = `rgb(${{r}}, ${{g}}, ${{b}})`;

      ctx.fillRect(x, spectrumCanvas.height - barHeight, barWidth, barHeight);
      x += barWidth + 1;
    }}
  }}
  drawSpectrum();
</script>
"""

# Give enough height to show everything (waveform, spectrum, knob, slider)
st.components.v1.html(html, height=900)