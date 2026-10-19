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
[data-testid="stStatusWidget"] {
    display: none !important;
}
.stApp { background: #050d14; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
iframe { border: 0 !important; }
</style>
""", unsafe_allow_html=True)

game_html = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<style>
* { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

:root {
    --panel: rgba(255,255,255,.06);
    --line: rgba(255,255,255,.13);
    --green: #39ff88;
    --cyan: #22d3ee;
    --muted: #9eb5c9;
    --text: #f5fff9;
    --btn: rgba(255,255,255,.08);
    --ovl: rgba(4,12,18,.82);
}
body.classic {
    --panel: rgba(255,255,255,.45);
    --line: rgba(40,70,35,.28);
    --green: #214b2b;
    --cyan: #3a7437;
    --muted: #4b6143;
    --text: #152719;
    --btn: rgba(255,255,255,.55);
    --ovl: rgba(214,228,196,.88);
}

body {
    margin: 0;
    padding: 14px 12px 24px;
    background:
        radial-gradient(circle at 20% 0%, #14403a 0%, transparent 45%),
        radial-gradient(circle at 90% 30%, #1b2a5e 0%, transparent 40%),
        #060e16;
    color: var(--text);
    font-family: "Segoe UI", Roboto, Arial, sans-serif;
    text-align: center;
    user-select: none;
    -webkit-user-select: none;
}
body.classic {
    background: radial-gradient(circle at top, #e1edd0, #a9bd94);
}

.wrap { max-width: 480px; margin: 0 auto; }

.glass {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(0,0,0,.25);
}

.header { display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 4px; }
.logo {
    width: 46px; height: 46px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center; font-size: 26px;
    background: linear-gradient(135deg, var(--green), var(--cyan));
    box-shadow: 0 0 22px rgba(57,255,136,.45);
}
h1 {
    margin: 0; font-size: clamp(22px, 6.4vw, 32px); font-weight: 800; letter-spacing: 1px;
    background: linear-gradient(90deg, var(--green), var(--cyan));
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.subtitle { color: var(--muted); font-size: 11px; letter-spacing: 4px; margin: 4px 0 14px; font-weight: 600; }

.setup { display: flex; gap: 8px; padding: 10px; margin-bottom: 12px; }
.setup input { flex: 1.3; min-width: 0; }
.setup select { flex: 1; min-width: 0; }

button, select, input {
    border: 1px solid var(--line);
    background: var(--btn);
    color: var(--text);
    border-radius: 12px;
    font-size: 14px; font-weight: 700;
    padding: 11px 12px; min-height: 44px;
    touch-action: manipulation;
    font-family: inherit;
}
select option { color: #111; }
input::placeholder { color: var(--muted); font-weight: 500; }
button { cursor: pointer; transition: transform .1s, filter .1s; }
button:active { transform: scale(.95); filter: brightness(1.25); }

.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 12px; }
.stat { padding: 10px 4px 8px; }
.label { font-size: 10px; color: var(--muted); letter-spacing: 1.5px; font-weight: 700; }
.value { font-size: 26px; font-weight: 800; color: var(--green); margin-top: 2px; }
.bar { height: 4px; border-radius: 4px; background: var(--line); margin: 6px 14px 0; overflow: hidden; }
.bar i { display: block; height: 100%; width: 0; background: linear-gradient(90deg, var(--green), var(--cyan)); transition: width .25s; }

.gamebox {
    position: relative; overflow: hidden; border-radius: 20px;
    border: 2px solid var(--green);
    box-shadow: 0 0 30px rgba(57,255,136,.28), 0 18px 40px rgba(0,0,0,.45);
    background: #06101a;
}
body.classic .gamebox { box-shadow: 0 14px 30px rgba(0,0,0,.3); background: #b6c9a0; }
canvas { display: block; width: 100%; height: auto; touch-action: none; }

.overlay {
    position: absolute; inset: 0;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    background: var(--ovl);
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    padding: 20px;
}
.overlay h2 {
    margin: 0 0 8px; font-size: 30px; font-weight: 800; letter-spacing: 1px;
    background: linear-gradient(90deg, var(--green), var(--cyan));
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.overlay p { line-height: 1.6; color: var(--text); font-size: 13px; margin: 6px 0 18px; opacity: .9; }

.primary {
    background: linear-gradient(135deg, #39ff88, #22d3ee);
    color: #04150c; border: 0; min-width: 170px; font-size: 15px;
    box-shadow: 0 8px 22px rgba(34,211,238,.4);
}
body.classic .primary { background: linear-gradient(135deg, #3a7437, #214b2b); color: #fff; box-shadow: none; }

.toolbar { display: grid; grid-template-columns: 1.1fr 1fr 1fr 1fr; gap: 7px; margin: 14px 0 6px; }
.toolbar button, .toolbar select { padding: 10px 4px; font-size: 12.5px; }

.controls {
    display: grid; grid-template-columns: repeat(3, 70px); grid-template-rows: repeat(2, 56px);
    justify-content: center; gap: 8px; margin: 14px auto 6px;
}
.controls button {
    font-size: 24px; padding: 4px; border-radius: 16px;
    background: linear-gradient(180deg, rgba(255,255,255,.14), rgba(255,255,255,.04));
    box-shadow: 0 4px 0 rgba(0,0,0,.35);
}
.up { grid-column: 2; grid-row: 1; }
.left { grid-column: 1; grid-row: 2; }
.down { grid-column: 2; grid-row: 2; }
.right { grid-column: 3; grid-row: 2; }

.hint { font-size: 10px; color: var(--muted); margin: 12px 0 8px; letter-spacing: 1.2px; font-weight: 600; }

.panels { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 12px 0; text-align: left; }
.panel { padding: 13px; }
.panel h3 { font-size: 12.5px; margin: 0 0 9px; color: var(--green); letter-spacing: .5px; }
.panel p { font-size: 11.5px; color: var(--muted); margin: 6px 0; }
#leaderboard { font-size: 12.5px; line-height: 1.9; color: var(--text); white-space: pre-line; overflow-wrap: anywhere; }
.badge {
    display: inline-block; border: 1px solid var(--line); border-radius: 20px;
    padding: 5px 10px; color: var(--muted); font-size: 10px; margin-top: 6px;
}
.foot { font-size: 11px; color: var(--muted); margin-top: 10px; letter-spacing: 1px; }

@media (max-width: 380px) {
    body { padding: 8px 6px 18px; }
    .controls { grid-template-columns: repeat(3, 60px); grid-template-rows: repeat(2, 50px); }
    .panels { grid-template-columns: 1fr; }
    .toolbar button, .toolbar select { font-size: 11px; }
}
</style>
</head>

<body>
<div class="wrap">

<div class="header">
    <div class="logo">🐍</div>
    <h1>SNAKE XENZIA PRO</h1>
</div>
<div class="subtitle">3D ARCADE EDITION</div>

<div class="setup glass">
    <input id="playerName" maxlength="16" placeholder="Your player name" aria-label="Player name">
    <select id="mode" aria-label="Game mode">
        <option value="classic">Classic Mode</option>
        <option value="obstacles">Obstacle Mode</option>
        <option value="rush">Speed Rush</option>
    </select>
</div>

<div class="stats">
    <div class="stat glass">
        <div class="label">⭐ SCORE</div>
        <div class="value" id="score">0</div>
    </div>
    <div class="stat glass">
        <div class="label">🏆 BEST</div>
        <div class="value" id="best">0</div>
    </div>
    <div class="stat glass">
        <div class="label">⚡ LEVEL</div>
        <div class="value" id="level">1</div>
        <div class="bar"><i id="lvlbar"></i></div>
    </div>
</div>

<div class="gamebox">
    <canvas id="game"></canvas>
    <div class="overlay" id="overlay">
        <h2 id="overlayTitle">READY?</h2>
        <p id="overlayText">
            Eat the food 🍎 to grow your snake.<br>
            Avoid walls and your own tail.<br>
            Collect golden bonus food for extra points!
        </p>
        <button class="primary" id="startBtn">▶ PLAY NOW</button>
    </div>
</div>

<div class="toolbar">
    <select id="difficulty" aria-label="Difficulty">
        <option value="175">Easy</option>
        <option value="135" selected>Medium</option>
        <option value="100">Hard</option>
    </select>
    <button id="pauseBtn">⏸ Pause</button>
    <button id="restartBtn">↻ Restart</button>
    <button id="themeBtn">🎨 Theme</button>
</div>

<div class="controls">
    <button class="up" data-dir="up">▲</button>
    <button class="left" data-dir="left">◀</button>
    <button class="down" data-dir="down">▼</button>
    <button class="right" data-dir="right">▶</button>
</div>

<div class="hint">ARROW BUTTONS • SWIPE ON THE BOARD • KEYBOARD ARROWS</div>

<div class="panels">
    <div class="panel glass">
        <h3>🏆 TOP SCORES ON THIS DEVICE</h3>
        <div id="leaderboard">No scores yet. Play a round!</div>
    </div>
    <div class="panel glass">
        <h3>🎯 HOW TO PLAY</h3>
        <p>🍎 Red food: +10 points</p>
        <p>⭐ Golden bonus: +30 points</p>
        <p>🚧 Obstacle mode: avoid blocks</p>
        <p>⚡ Speed Rush: faster as you score</p>
        <span class="badge">Best score saves in this browser</span>
    </div>
</div>

<div class="foot">SNAKE XENZIA PRO • 3D EDITION</div>

</div>

<script>
(() => {

const $ = id => document.getElementById(id);
const canvas = $("game");
const ctx = canvas.getContext("2d");

const W = 440, H = 370, CELLS = 20;
const DPR = Math.min(window.devicePixelRatio || 1, 2);
canvas.width = W * DPR;
canvas.height = H * DPR;
ctx.setTransform(DPR, 0, 0, DPR, 0, 0);

const bg = document.createElement("canvas");
bg.width = W * DPR;
bg.height = H * DPR;
const bgx = bg.getContext("2d");
bgx.setTransform(DPR, 0, 0, DPR, 0, 0);

let g = ctx;

/* ---------- 3D camera ---------- */
const PITCH = 55 * Math.PI / 180;
const SP = Math.sin(PITCH), CP = Math.cos(PITCH);
const CAMD = 34, SC = 15.5, CX = W / 2, CY = 162;

function proj(x, y, z) {
    const X = x - 10, Y = y - 10;
    const dc = Y * CP + z * SP;
    const f = CAMD / (CAMD - dc);
    return [CX + X * f * SC, CY + (Y * SP - z * CP) * f * SC, f];
}

/* ---------- colors ---------- */
const THEMES = {
    neon: {
        bgA: "#123a31", bgB: "#050d14",
        floorA: "#0f3027", floorB: "#0b2620",
        wall: "#1a9a70", obstacle: "#6b7b99",
        head: "#d4ffe6", body: "#2ee67f", tail: "#0f8f4c",
        food: "#ff4b5c", bonus: "#ffd84d", glow: true
    },
    classic: {
        bgA: "#dbe8c7", bgB: "#9fb48a",
        floorA: "#c6d8ae", floorB: "#bacf9f",
        wall: "#6b8a5a", obstacle: "#5a6b50",
        head: "#1b4223", body: "#3a7437", tail: "#27552b",
        food: "#d93a49", bonus: "#e8b923", glow: false
    }
};
let neon = true;
let T = THEMES.neon;

function hexToRgb(h) {
    const n = parseInt(h.slice(1), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}
function shade(h, f) {
    const c = hexToRgb(h);
    return "rgb(" + c.map(v => Math.min(255, Math.round(v * f))).join(",") + ")";
}
function lerpHex(a, b, t) {
    const A = hexToRgb(a), B = hexToRgb(b);
    return "#" + A.map((v, i) =>
        Math.round(v + (B[i] - v) * t).toString(16).padStart(2, "0")).join("");
}

/* ---------- 3D drawing helpers ---------- */
function quad(pts, color) {
    const p = pts.map(q => proj(q[0], q[1], q[2]));
    g.beginPath();
    g.moveTo(p[0][0], p[0][1]);
    for (let i = 1; i < p.length; i++) g.lineTo(p[i][0], p[i][1]);
    g.closePath();
    g.fillStyle = color;
    g.fill();
    g.strokeStyle = color;
    g.lineWidth = 0.6;
    g.stroke();
}

function box(x, y, z0, z1, color, inset) {
    const x0 = x + inset, x1 = x + 1 - inset;
    const y0 = y + inset, y1 = y + 1 - inset;
    const cxm = x + 0.5 - 10;
    quad([[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]], shade(color, 0.72));
    if (cxm < 0) {
        quad([[x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [x1, y0, z1]], shade(color, 0.52));
    } else {
        quad([[x0, y0, z0], [x0, y1, z0], [x0, y1, z1], [x0, y0, z1]], shade(color, 0.52));
    }
    quad([[x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], shade(color, 1.12));
}

function sphere(cx, cy, z, r, color, glow) {
    const p = proj(cx, cy, z);
    const R = r * p[2] * SC;
    const s = proj(cx, cy, 0);
    g.fillStyle = "rgba(0,0,0,.35)";
    g.beginPath();
    g.ellipse(s[0], s[1], R, R * SP * 0.8, 0, 0, Math.PI * 2);
    g.fill();
    const gr = g.createRadialGradient(p[0] - R * 0.35, p[1] - R * 0.35, R * 0.1, p[0], p[1], R);
    gr.addColorStop(0, shade(color, 1.55));
    gr.addColorStop(0.55, color);
    gr.addColorStop(1, shade(color, 0.5));
    g.shadowColor = color;
    g.shadowBlur = glow ? 14 : 0;
    g.fillStyle = gr;
    g.beginPath();
    g.arc(p[0], p[1], R, 0, Math.PI * 2);
    g.fill();
    g.shadowBlur = 0;
    return {x: p[0], y: p[1], R: R};
}

function buildBg() {
    g = bgx;
    g.clearRect(0, 0, W, H);
    const grd = g.createRadialGradient(W / 2, H / 2, 20, W / 2, H / 2, W * 0.75);
    grd.addColorStop(0, T.bgA);
    grd.addColorStop(1, T.bgB);
    g.fillStyle = grd;
    g.fillRect(0, 0, W, H);

    for (let y = 0; y < CELLS; y++) {
        for (let x = 0; x < CELLS; x++) {
            quad([[x, y, 0], [x + 1, y, 0], [x + 1, y + 1, 0], [x, y + 1, 0]],
                 (x + y) % 2 ? T.floorA : T.floorB);
        }
    }
    for (let x = -1; x <= CELLS; x++) box(x, -1, 0, 0.55, T.wall, 0);
    for (let y = 0; y < CELLS; y++) {
        box(-1, y, 0, 0.55, T.wall, 0);
        box(CELLS, y, 0, 0.55, T.wall, 0);
    }
    g = ctx;
}

/* ---------- game state ---------- */
let snake = [], prev = [];
let direction = {x: 1, y: 0};
let nextDirection = {x: 1, y: 0};
let food = null, bonus = null, obstacles = [];
let score = 0, best = 0;
let running = false, started = false, gameOver = false;
let timer = null, bonusTicks = 0, playerName = "Player";
let lastTick = 0, interval = 135;
let particles = [];

try { best = Number(localStorage.getItem("sxpro_best")) || 0; } catch (e) {}
$("best").textContent = best;

function safeGetScores() {
    try { return JSON.parse(localStorage.getItem("sxpro_scores") || "[]"); }
    catch (e) { return []; }
}
function renderScores() {
    const list = safeGetScores();
    $("leaderboard").textContent = list.length
        ? list.map((x, i) => (i + 1) + ". " + x.name + " - " + x.score).join("\n")
        : "No scores yet. Play a round!";
}
function saveScores() {
    if (score <= 0) return;
    let list = safeGetScores();
    list.push({name: playerName || "Player", score: score, date: new Date().toLocaleDateString()});
    list.sort((a, b) => b.score - a.score);
    list = list.slice(0, 5);
    try { localStorage.setItem("sxpro_scores", JSON.stringify(list)); } catch (e) {}
    renderScores();
}

function buzz(ms) { try { if (navigator.vibrate) navigator.vibrate(ms); } catch (e) {} }

function stopTimer() {
    if (timer !== null) { clearTimeout(timer); timer = null; }
}

function delay() {
    let base = Number($("difficulty").value);
    if ($("mode").value === "rush") {
        base = Math.max(60, base - Math.floor(score / 30) * 4);
    } else {
        base = Math.max(75, base - Math.floor(score / 100) * 4);
    }
    return base;
}

function freezePrev() { prev = snake.map(p => ({x: p.x, y: p.y})); }

function schedule() {
    stopTimer();
    interval = delay();
    lastTick = performance.now();
    timer = setTimeout(tick, interval);
}

function occupied(x, y) {
    return snake.some(p => p.x === x && p.y === y) ||
           obstacles.some(p => p.x === x && p.y === y);
}

function randomFree() {
    const free = [];
    for (let y = 0; y < CELLS; y++) {
        for (let x = 0; x < CELLS; x++) {
            if (!occupied(x, y) &&
                (!food || food.x !== x || food.y !== y) &&
                (!bonus || bonus.x !== x || bonus.y !== y)) {
                free.push({x, y});
            }
        }
    }
    if (!free.length) return null;
    return free[Math.floor(Math.random() * free.length)];
}

function spawnFood() {
    food = randomFree();
    if (!food) winGame();
}

function makeObstacles() {
    obstacles = [];
    if ($("mode").value === "obstacles") {
        for (let i = 0; i < 14; i++) {
            const p = randomFree();
            if (p && !(Math.abs(p.x - 8) < 4 && Math.abs(p.y - 10) < 3)) {
                obstacles.push(p);
            }
        }
    }
}

function burst(x, y, color, n) {
    for (let i = 0; i < n; i++) {
        const a = Math.random() * Math.PI * 2;
        const s = 0.6 + Math.random() * 2.2;
        particles.push({
