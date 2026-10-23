import os

# HTML template containing the WMP9 UI, tracklist reader, and 60FPS canvas visualizer
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Beats</title>
  <style>
    /* Windows Media Player 9 / XP Silver-Blue Theme */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      background-color: #ECE9D8;
      font-family: Tahoma, Arial, sans-serif;
      color: #000;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 10px;
    }
    .wmp-container {
      width: 100%;
      max-width: 600px;
      background: linear-gradient(to bottom, #d6dfef 0%, #b0c4de 100%);
      border: 3px solid;
      border-color: #ffffff #7190b9 #7190b9 #ffffff;
      box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
      border-radius: 4px;
      overflow: hidden;
    }
    .wmp-titlebar {
      background: linear-gradient(to right, #0055ea 0%, #3d8bff 50%, #0055ea 100%);
      color: white;
      padding: 6px 10px;
      font-weight: bold;
      font-size: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      text-shadow: 1px 1px #002366;
    }
    .wmp-content {
      padding: 12px;
    }
    .visualizer-box {
      width: 100%;
      height: 160px;
      background-color: #000000;
      border: 2px solid;
      border-color: #405060 #ffffff #ffffff #405060;
      box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.8);
      position: relative;
      overflow: hidden;
      margin-bottom: 12px;
    }
    #wmpVisualizer {
      width: 100%;
      height: 100%;
      display: block;
    }
    .now-playing {
      font-size: 13px;
      font-weight: bold;
      margin-bottom: 8px;
      color: #002366;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .controls-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 12px;
      background: #c5d4ef;
      padding: 6px;
      border: 1px solid #7190b9;
    }
    button.wmp-btn {
      background: linear-gradient(to bottom, #f9f9f9 0%, #dcdcdc 100%);
      border: 1px solid #707070;
      padding: 4px 10px;
      font-size: 11px;
      cursor: pointer;
      font-weight: bold;
      border-radius: 2px;
    }
    button.wmp-btn:active {
      background: linear-gradient(to bottom, #dcdcdc 0%, #f9f9f9 100%);
    }
    .tracklist {
      max-height: 220px;
      overflow-y: auto;
      background: #fff;
      border: 2px inset #7190b9;
      padding: 4px;
    }
    .track-item {
      padding: 6px 8px;
      font-size: 12px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      border-bottom: 1px solid #f0f0f0;
    }
    .track-item:hover {
      background-color: #3d8bff;
      color: white;
    }
    .track-item.active {
      background-color: #0055ea;
      color: white;
      font-weight: bold;
    }
    @media (max-width: 480px) {
      .wmp-container {
        border-width: 1px;
      }
      .visualizer-box {
        height: 130px;
      }
    }
  </style>
</head>
<body>

  <div class="wmp-container">
    <div class="wmp-titlebar">
      <span>Windows Media Player - Outtamnd Beats</span>
      <span>[_][O][X]</span>
    </div>
    <div class="wmp-content">
      
      <!-- Visualizer Box -->
      <div class="visualizer-box">
        <canvas id="wmpVisualizer"></canvas>
      </div>

      <div class="now-playing" id="nowPlayingText">Select a beat to play</div>

      <!-- Audio Element -->
      <audio id="audioPlayer"></audio>

      <!-- Controls -->
      <div class="controls-bar">
        <button class="wmp-btn" id="playPauseBtn">Play</button>
        <span id="currentTime" style="font-size: 11px;">0:00</span>
        <input type="range" id="progressBar" value="0" max="100" style="flex-grow: 1;">
        <span id="duration" style="font-size: 11px;">0:00</span>
      </div>

      <!-- Playlist -->
      <div class="tracklist" id="trackList"></div>

    </div>
  </div>

  <script>
    const audio = document.getElementById('audioPlayer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const progressBar = document.getElementById('progressBar');
    const currentTimeEl = document.getElementById('currentTime');
    const durationEl = document.getElementById('duration');
    const nowPlayingText = document.getElementById('nowPlayingText');
    const trackListEl = document.getElementById('trackList');

    let tracks = [
      { title: "Sample Beat 1", file: "beat1.mp3" },
      { title: "Sample Beat 2", file: "beat2.mp3" }
    ];

    let currentTrackIndex = 0;
    let isInitialized = false;
    let audioCtx, analyser, dataArray, sourceNode;

    fetch('beats.json')
      .then(res => res.json())
      .then(data => {
        if (data && data.length > 0) {
          tracks = data;
          renderTracklist();
          loadTrack(0);
        }
      })
      .catch(() => {
        renderTracklist();
        loadTrack(0);
      });

    function renderTracklist() {
      trackListEl.innerHTML = '';
      tracks.forEach((track, index) => {
        const div = document.createElement('div');
        div.className = 'track-item' + (index === currentTrackIndex ? ' active' : '');
        div.innerHTML = `<span>${track.title || track.name}</span>`;
        div.addEventListener('click', () => {
          currentTrackIndex = index;
          loadTrack(currentTrackIndex);
          audio.play();
          updateActiveTrackUI();
        });
        trackListEl.appendChild(div);
      });
    }

    function loadTrack(index) {
      const track = tracks[index];
      audio.src = track.file || track.url;
      nowPlayingText.innerText = "Now Playing: " + (track.title || track.name);
      updateActiveTrackUI();
    }

    function updateActiveTrackUI() {
      const items = trackListEl.querySelectorAll('.track-item');
      items.forEach((item, index) => {
        if (index === currentTrackIndex) {
          item.classList.add('active');
        } else {
          item.classList.remove('active');
        }
      });
    }

    playPauseBtn.addEventListener('click', () => {
      if (!isInitialized) initAudio();
      if (audio.paused) {
        audio.play();
        playPauseBtn.innerText = "Pause";
      } else {
        audio.pause();
        playPauseBtn.innerText = "Play";
      }
    });

    audio.addEventListener('play', () => {
      playPauseBtn.innerText = "Pause";
      if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
    });

    audio.addEventListener('pause', () => {
      playPauseBtn.innerText = "Play";
    });

    audio.addEventListener('timeupdate', () => {
      if (audio.duration) {
        progressBar.value = (audio.currentTime / audio.duration) * 100;
        currentTimeEl.innerText = formatTime(audio.currentTime);
        durationEl.innerText = formatTime(audio.duration);
      }
    });

    progressBar.addEventListener('input', () => {
      if (audio.duration) {
        audio.currentTime = (progressBar.value / 100) * audio.duration;
      }
    });

    function formatTime(seconds) {
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }

    // --- 60 FPS WMP9 Canvas Visualizer ---
    const canvas = document.getElementById('wmpVisualizer');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
      canvas.width = canvas.clientWidth * window.devicePixelRatio;
      canvas.height = canvas.clientHeight * window.devicePixelRatio;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function initAudio() {
      if (isInitialized) return;
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 64;
      dataArray = new Uint8Array(analyser.frequencyBinCount);

      sourceNode = audioCtx.createMediaElementSource(audio);
      sourceNode.connect(analyser);
      analyser.connect(audioCtx.destination);
      isInitialized = true;
    }

    let phase = 0;

    function drawVisualizer() {
      requestAnimationFrame(drawVisualizer);

      ctx.fillStyle = 'rgba(0, 4, 12, 0.25)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      if (!analyser) return;
      analyser.getByteFrequencyData(dataArray);

      let bassSum = 0;
      for (let i = 0; i < 6; i++) bassSum += dataArray[i];
      let bassEnergy = bassSum / 6;

      phase += 0.03 + (bassEnergy / 5000);

      const width = canvas.width;
      const height = canvas.height;
      const centerY = height / 2;

      const ribbons = [
        { color: 'rgba(0, 162, 255, 0.8)', speed: 1.0, freq: 0.008, amp: 0.35 },
        { color: 'rgba(0, 230, 255, 0.6)', speed: 1.3, freq: 0.012, amp: 0.25 },
        { color: 'rgba(100, 80, 255, 0.5)', speed: 0.7, freq: 0.005, amp: 0.45 }
      ];

      ribbons.forEach((r) => {
        ctx.beginPath();
        ctx.lineWidth = 3 * window.devicePixelRatio;
        ctx.strokeStyle = r.color;

        for (let x = 0; x <= width; x += 4 * window.devicePixelRatio) {
          let binIndex = Math.floor((x / width) * dataArray.length);
          let freqValue = dataArray[binIndex] || 0;

          let wave1 = Math.sin(x * r.freq + phase * r.speed);
          let wave2 = Math.cos(x * (r.freq * 0.5) - phase * 0.5);
          
          let displacement = (wave1 + wave2) * (height * r.amp) * (0.2 + (freqValue / 255) * 0.8);
          let y = centerY + displacement;

          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      });
    }

    drawVisualizer();
  </script>
</body>
</html>
"""

def build():
    print("Building index.html...")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    print("Build complete! index.html generated successfully.")

if __name__ == "__main__":
    build()