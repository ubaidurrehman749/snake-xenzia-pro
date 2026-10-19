import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Snake Xenzia Pro",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }
.stApp { background: #050d14; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
iframe {
    border: 0 !important;
    width: 100% !important;
    height: 100vh !important;
    height: 100dvh !important;
}
</style>
""", unsafe_allow_html=True)

base = Path(__file__).parent
JS_FILES = ["game1.js", "game2.js", "game3.js"]
ENDS = {
    "style.css": "}",
    "body.html": "</div>",
    "game1.js": "}",
    "game2.js": "}",
    "game3.js": "requestAnimationFrame(loop);",
}

texts = {}
for name in ENDS:
    path = base / name
    if not path.exists():
        st.error("File missing in GitHub: " + name)
        st.stop()
    texts[name] = path.read_text(encoding="utf-8")

problems = []
for name, text in texts.items():
    if not text.rstrip().endswith(ENDS[name]):
        problems.append(name + " is incomplete (code is cut at the end)")
    if name.endswith((".js", ".css")) and text.count("{") != text.count("}"):
        problems.append(name + " has unmatched { } brackets")
if problems:
    st.warning("Fix these files in GitHub:\n\n" + "\n".join("- " + p for p in problems))

ERR = """<script>
var MAP = __MAP__;
window.addEventListener('error', function (e) {
  if (document.getElementById('errbox')) return;
  var ln = e.lineno, where = '';
  for (var i = 0; i < MAP.length; i++) {
    if (ln >= MAP[i][1] && ln < MAP[i][1] + MAP[i][2]) {
      where = MAP[i][0] + ' line ' + (ln - MAP[i][1] + 1);
    }
  }
  var d = document.createElement('div');
  d.id = 'errbox';
  d.style.cssText = 'position:fixed;left:6px;right:6px;bottom:6px;z-index:99999;background:#b91c1c;color:#fff;font:12px/1.4 Arial;padding:8px 10px;border-radius:10px;word-break:break-word';
  d.textContent = 'ERROR: ' + e.message + ' [' + (where || ('line ' + ln)) + ']';
  document.body.appendChild(d);
});
</script>
"""

page = (
    "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>"
    "<meta name='viewport' content='width=device-width, initial-scale=1, "
    "maximum-scale=1, user-scalable=no'>\n"
    "<style>\n" + texts["style.css"] + "\n</style></head><body>\n"
    + texts["body.html"] + "\n"
    + ERR
)

mapping = []
for name in JS_FILES:
    start = page.count("\n") + 2
    mapping.append([name, start, texts[name].count("\n") + 1])
    page += "<script>\n" + texts[name] + "\n</script>\n"
page += "</body></html>"
page = page.replace("__MAP__", json.dumps(mapping))

components.html(page, height=700, scrolling=False)
