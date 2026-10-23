import os

print("Adding mobile responsive styles to styles.css...")

mobile_css = """
/* --- MOBILE RESPONSIVE OPTIMIZATIONS --- */
@media (max-width: 768px) {
  body {
    overflow: hidden;
    background-size: cover;
  }
  
  /* Make the WMP window take up the full screen on mobile */
  .window, .wmp-container, #player-window {
    width: 100vw !important;
    height: 100vh !important;
    max-width: 100% !important;
    max-height: 100% !important;
    top: 0 !important;
    left: 0 !important;
    transform: none !important;
    border-radius: 0 !important;
    position: fixed !important;
  }

  /* Stack main panels vertically */
  .content-area, .main-body, .catalog-container {
    flex-direction: column !important;
  }

  /* Optimize sidebars and panels for mobile viewports */
  .now-playing-panel, .right-sidebar {
    width: 100% !important;
    height: auto !important;
  }

  /* Make interactive buttons touch-friendly */
  button, .btn, .instant-buy-btn {
    padding: 10px 14px !important;
    font-size: 14px !important;
    cursor: pointer;
  }
}
"""

if os.path.exists("styles.css"):
  with open("styles.css", "r", encoding="utf-8") as f:
    css_content = f.read()

  if "MOBILE RESPONSIVE OPTIMIZATIONS" not in css_content:
    with open("styles.css", "a", encoding="utf-8") as f:
      f.write(mobile_css)
    print("✓ Mobile styles appended to styles.css.")
  else:
    print("✓ Mobile styles already present in styles.css.")
else:
  print("Error: styles.css not found!")

print("--- DONE ---")