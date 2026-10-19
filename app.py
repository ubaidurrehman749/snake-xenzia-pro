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


def read(name):
    return (base / name).read_text(encoding="utf-8")


page = (
    "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>"
    "<meta name='viewport' content='width=device-width, initial-scale=1, "
    "maximum-scale=1, user-scalable=no'>"
    "<style>" + read("style.css") + "</style></head><body>"
    + read("body.html")
    + "<script>"
    + read("game1.js") + "\n"
    + read("game2.js") + "\n"
    + read("game3.js")
    + "</script></body></html>"
)

components.html(page, height=700, scrolling=False)
