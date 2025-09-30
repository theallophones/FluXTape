import streamlit as st
import base64

st.set_page_config(layout="wide")

# --- Custom CSS for the Gradient Background ---
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

/* Base colors for the application */
:root {
    --bg: #0f1115;
    --accent: #4CAF50; /* Play button green */
    --playing-color: #00bcd4; /* Playing button cyan */
    --text: #ffffff;
    --knob-active: #b71c1c; /* Label active red */
}
html, body, .stApp {
    height: 100%;
    margin: 0;
    background: linear-gradient(160deg, #0f1115 0%, #1a1d25 100%);
}

.play-btn {
    width: 82px;
    height: 82px;
    border-radius: 50%;
    border: none;
    font-size: 34px;
    cursor: pointer;
    color: #fff;
    background: var(--accent);
    transition: background 0.25s ease, transform 0.2s ease, box-shadow .3s ease;
    box-shadow: 0 6px 20px rgba(76,175,80,.4);
}
.play-btn:hover { transform: scale(1.1); }

/* Playing/Pause state for a cleaner look */
.play-btn.pause {
    background: var(--playing-color);
    box-shadow: 0 6px 20px rgba(0, 188, 212, 0.4);
    font-size: 26px; 
    padding-top: 2px;
}

.knob-wrap {
    position: relative;
    width: 260px;
    height: 260px;
    margin: 40px auto;
    display: flex;
    align-items: center;
    justify-content: center;
}

.knob {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #2b313c, #1b1f27 70%);
    position: relative;
    box-shadow: inset 0 6px 14px rgba(0,0,0,.5), 0 8px 24px rgba(0,0,0,.35);
    border: 1px solid #2e3440;
    cursor: pointer; /* make the whole knob area clickable */
}
.knob:active {
    /* Slight press effect on knob click */
    transform: scale(0.98);
}
.center-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #cfd8dc;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
}
.pointer {
    position: absolute;
    width: 4px;
    height: 55px;
    background: #ffffff;
    border-radius: 2px;
    transform-origin: bottom center;
    bottom: 50%;
    left: 50%;
    translate: -50% 0;
    box-shadow: 0 0 8px rgba(255,255,255,.35);
    transition: transform 0.4s ease;
}

.label {
    position: absolute;
    background: #2a2f3a;
    color: var(--text);
    padding: 7px 14px;
    border-radius: 14px;
    font-family: sans-serif;
    font-size: 14px;
    cursor: pointer;
    transition: background .25s ease, box-shadow .25s ease, transform .1s ease;
}
.label:hover { 
    background: #3a4150; 
    transform: scale(1.05); /* Slight hover scale */
}
.label.active {
    background: var(--knob-active);
    box-shadow: 0 0 14px rgba(183,28,28,0.9);
}

/* Volume slider styling */
.slider {
    -webkit-appearance: none;
    width: 260px;
    height: 6px;
    border-radius: 3px;
    /* Initial gradient set to 100% full volume */
    background: linear-gradient(to right, #5f6bff 100%, #c9cbd3 100%); 
    outline: none;
    cursor: pointer;
}
.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 0 6px rgba(200,200,200,.6);
    transition: transform 0.2s ease;
}
.slider::-webkit-slider-thumb:hover {
    transform: scale(1.2);
}
.slider::-moz-range-thumb {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #cfd8dc;
    box-shadow: 0 0 6px rgba(200,200,200,.6);
    cursor: pointer;
}

/* Positions: A=9pm, B=12, C=3pm */
.labelA { top: 50%; left: -40px; transform: translateY(-50%); }
.labelB { top: -20px; left: 50%; transform: translateX(-50%); }
.labelC { top: 50%; right: -40px; transform: translateY(-50%); }

/* Wavesurfer/Spectrogram container styles */
#spectrogram .wavesurfer-spectrogram {
    border-radius: 8px 8px 0 0; 
    overflow: hidden;
}
#waveform {
    margin-top: -1px !important; /* to align with spectrogram */
}
#waveform .wavesurfer-canvas {
    border-radius: 0 0 8px 8px; 
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
    """Converts a local file to a Base64 data URL for embedding in HTML."""
    try:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except FileNotFoundError:
        st.error(f"Audio file not found: {path}. Please ensure it is in the same directory.")
        return ""

audio_map = {k: file_to_data_url(v) for k, v in audio_files.items()}

# --- HTML/JS/CSS Block ---
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

<div id="spectrogram" style="margin:25px auto 0 auto; width:85%;"></div>
<div id="waveform" style="margin:0 auto; width:85%;"></div>

<div id="time-display" style="text-align:center; margin-top:14px; color:#ccc; font-family:sans-serif; font-size:14px;">
    0:00 / 0:00
</div>

<div style="text-align:center; margin:18px 0;">
    <div style="color:#c9cbd3; font-size:20px; margin-bottom:6px;">🔊</div>
    <input id="volumeSlider" type="range" min="0" max="1" step="0.01" value="1" class="slider">
</div>

<div class="knob-wrap">
    <div id="knob" class="knob" title="Click to switch Lyrics version">
        <div id="pointer" class="pointer"></div>
        <div class="center-dot"></div>
    </div>
    <div class="label labelA" data-idx="0">Lyrics A</div>
    <div class="label labelB" data-idx="1">Lyrics B</div>
    <div class="label labelC" data-idx="2">Lyrics C</div>
</div>


<script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>
<script src="https://unpkg.com/wavesurfer.js@7/dist/plugins/spectrogram.min.js"></script>

<script>
    const audioMap = {audio_map};
    const labels = ["A","B","C"];
    // Angles for the pointer: A=left (270 deg), B=top (0 deg), C=right (90 deg)
    const angles = [270, 0, 90]; 

    // --- WaveSurfer Initialization with Spectrogram Plugin ---
    const ws = WaveSurfer.create({
        container: '#waveform',
        waveColor: '#c9cbd3',
        progressColor: '#5f6bff',
        height: 100, // Reduced height for the waveform
        backend: 'WebAudio',
        cursorWidth: 2,
        // Add the Spectrogram Plugin
        plugins: [
            WaveSurfer.Spectrogram.create({
                container: '#spectrogram',
                labels: true, // Show frequency labels
                fftSize: 512, // Standard FFT size
                
                // Custom Color Map for a high-tech dark visualizer
                colorMap: [
                    { percent: 0, color: 'rgb(15, 17, 21)' },
                    { percent: 0.05, color: 'rgb(0, 0, 50)' },
                    { percent: 0.3, color: 'rgb(60, 0, 100)' },
                    { percent: 0.8, color: 'rgb(95, 200, 255)' }, 
                    { percent: 1, color: 'rgb(255, 255, 255)' },
                ]
            })
        ]
    });

    let currentIdx = 0;
    let current = labels[currentIdx];

    const playBtn = document.getElementById('playBtn');
    const pointer = document.getElementById('pointer');
    const labelEls = Array.from(document.querySelectorAll('.label'));
    const timeDisplay = document.getElementById('time-display');
    const volSlider = document.getElementById('volumeSlider');

    // Utility function to format seconds into M:SS
    function formatTime(sec) {
        const m = Math.floor(sec / 60);
        const s = Math.floor(sec % 60).toString().padStart(2, '0');
        return `${m}:${s}`;
    }

    // Updates the time display counter
    function updateTime() {
        const cur = ws.getCurrentTime();
        const total = ws.getDuration();
        timeDisplay.textContent = formatTime(cur) + ' / ' + formatTime(total);
    }

    // Visually sets the active label
    function setLabelActive(idx) {
        labelEls.forEach((el,i)=> el.classList.toggle('active', i===idx));
    }

    // Rotates the knob pointer
    function setPointer(idx) {
        pointer.style.transform = 'translate(-50%, 0) rotate(' + angles[idx] + 'deg)';
    }

    // Handles loading and switching the audio version
    function loadVersion(idx, keepTime=true) {
        const label = labels[idx];
        const t = ws.getCurrentTime();
        const playing = ws.isPlaying();
        
        // Stop playback before loading new track for cleaner transition
        if (playing) ws.pause();

        ws.load(audioMap[label]);

        // Once the new track is ready, restart playback and update state
        ws.once('ready', () => {
            if (keepTime) ws.setTime(Math.min(t, ws.getDuration()-0.01));
            if (playing) ws.play();
            updateTime();
            ws.setVolume(parseFloat(volSlider.value)); // sync volume
            updateSliderGradient(volSlider.value);
        });
        currentIdx = idx;
        current = label;
        setPointer(idx);
        setLabelActive(idx);
    }

    // Update slider gradient based on current volume value
    function updateSliderGradient(value) {
        const percent = value * 100;
        volSlider.style.background =
            `linear-gradient(to right, #5f6bff ${percent}%, #c9cbd3 ${percent}%)`;
    }


    // --- Init ---
    ws.load(audioMap[current]);
    setPointer(currentIdx);
    setLabelActive(currentIdx);

    // Initial setup when WaveSurfer is ready
    ws.on('ready', () => {
        updateTime();
        ws.setVolume(parseFloat(volSlider.value)); 
        updateSliderGradient(volSlider.value);
    });
    ws.on('audioprocess', updateTime);
    ws.on('finish', () => { 
        playBtn.textContent = '▶'; 
        playBtn.classList.remove('pause');
    });

    // --- Event Listeners ---
    
    // Play/pause button handler
    playBtn.addEventListener('click', () => ws.playPause());
    ws.on('play', () => { playBtn.textContent = '❚❚'; playBtn.classList.add('pause'); });
    ws.on('pause', () => { playBtn.textContent = '▶'; playBtn.classList.remove('pause'); });

    // Volume slider handler
    volSlider.addEventListener('input', e => {
        const val = parseFloat(e.target.value);
        ws.setVolume(val);
        updateSliderGradient(val);
    });

    // Click knob cycles A→B→C
    document.getElementById('knob').addEventListener('click', () => {
        const next = (currentIdx + 1) % 3;
        loadVersion(next);
    });

    // Click labels directly
    labelEls.forEach(el => {
        el.addEventListener('click', () => {
            const idx = parseInt(el.getAttribute('data-idx'));
            if (idx !== currentIdx) loadVersion(idx);
        });
    });
</script>
"""

# Render the custom HTML/JS/CSS component in Streamlit
st.components.v1.html(html, height=980)