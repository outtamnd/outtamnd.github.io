import os

CSS_CONTENT = """/* Windows Media Player 9 / XP Silver-Blue Theme */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
body {
  background: url('bliss.jpg') no-repeat center center fixed;
  background-size: cover;
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
"""

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Outtamnd Beats</title>
  <link rel="stylesheet" href="styles.css">
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

    let tracks = [];
    let currentTrackIndex = 0;

    fetch('beats.json')
      .then(res => res.json())
      .then(data => {
        if (data && data.length > 0) {
          tracks = data;
          renderTracklist();
          loadTrack(0);
        }
      })
      .catch(err => console.error("Error loading beats.json:", err));

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
      if (audio.paused) {
        audio.play();
      } else {
        audio.pause();
      }
    });

    audio.addEventListener('play', () => {
      playPauseBtn.innerText = "Pause";
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
  </script>
</body>
</html>
"""

def build():
    print("Generating styles.css and index.html...")
    with open("styles.css", "w", encoding="utf-8") as f:
        f.write(CSS_CONTENT.strip())
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT.strip())
    print("Build complete! Files generated successfully.")

if __name__ == "__main__":
    build()