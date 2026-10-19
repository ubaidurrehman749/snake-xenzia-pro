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
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
iframe {
    border: 0 !important;
}
</style>
""", unsafe_allow_html=True)

game_html = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">

<style>
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

:root {
    --bg: #07111b;
    --panel: #0d201f;
    --line: #21443b;
    --green: #39ff88;
    --muted: #9eb5c9;
    --text: #f5fff9;
}

body {
    margin: 0;
    padding: 12px;
    background: radial-gradient(circle at top, #112a25, #07111b 58%);
    color: var(--text);
    font-family: Arial, sans-serif;
    text-align: center;
    user-select: none;
}

body.classic {
    --bg: #b8cba4;
    --panel: #d4e3bd;
    --line: #91a67d;
    --green: #214b2b;
    --muted: #52684a;
    --text: #152719;
}

.wrap {
    max-width: 480px;
    margin: auto;
}

h1 {
    margin: 5px 0;
    font-size: clamp(25px, 7vw, 39px);
    color: var(--green);
    text-shadow: 0 0 15px #00ff7740;
}

.subtitle {
    color: var(--muted);
    font-size: 11px;
    letter-spacing: 3px;
    margin-bottom: 12px;
}

.stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 7px;
    margin: 12px 0;
}

.stat {
    padding: 9px 4px;
    border: 1px solid var(--line);
    background: var(--panel);
    border-radius: 12px;
}

.label {
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 1px;
}

.value {
    font-size: 23px;
    font-weight: bold;
    color: var(--green);
    margin-top: 4px;
}

.gamebox {
    position: relative;
    border: 2px solid var(--green);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 22px #18ff7725;
    background: var(--bg);
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    touch-action: none;
}

.overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: #06120ee9;
    padding: 20px;
}

.overlay h2 {
    color: #39ff88;
    font-size: 28px;
    margin: 0 0 10px;
}

.overlay p {
    line-height: 1.55;
    color: #e1eee6;
    font-size: 13px;
    margin: 7px 0 16px;
}

button, select, input {
    border: 1px solid var(--green);
    background: var(--panel);
    color: var(--text);
    border-radius: 10px;
    font-size: 14px;
    font-weight: bold;
    padding: 11px 12px;
    touch-action: manipulation;
    min-height: 42px;
}

button {
    cursor: pointer;
}

button:active {
    transform: scale(.96);
    filter: brightness(1.25);
}

.primary {
    background: #39ff88;
    color: #06150c;
    border: 0;
    min-width: 150px;
}

.options {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 7px;
    margin: 12px auto;
}

select {
    max-width: 145px;
}

input {
    width: 100%;
    max-width: 220px;
    margin: 6px 0;
    background: #10221c;
}

.controls {
    display: grid;
    grid-template-columns: repeat(3, 66px);
    grid-template-rows: repeat(2, 52px);
    justify-content: center;
    gap: 7px;
    margin: 14px auto 8px;
}

.controls button {
    font-size: 23px;
    padding: 4px;
    background: #142b25;
    box-shadow: 0 3px 0 #07110d;
}

.up {
    grid-column: 2;
    grid-row: 1;
}

.left {
    grid-column: 1;
    grid-row: 2;
}

.down {
    grid-column: 2;
    grid-row: 2;
}

.right {
    grid-column: 3;
    grid-row: 2;
}

.hint {
    font-size: 10px;
    color: var(--muted);
    margin: 11px 0 6px;
}

.panels {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 9px;
    margin: 12px 0;
    text-align: left;
}

.panel {
    border: 1px solid var(--line);
    background: var(--panel);
    border-radius: 12px;
    padding: 11px;
}

.panel h3 {
    font-size: 13px;
    margin: 0 0 8px;
    color: var(--green);
}

.panel p {
    font-size: 11px;
    color: var(--muted);
    margin: 5px 0;
}

#leaderboard {
    font-size: 12px;
    line-height: 1.8;
    color: var(--text);
    white-space: pre-line;
    overflow-wrap: anywhere;
}

.badge {
    display: inline-block;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 5px 9px;
    color: var(--muted);
    font-size: 10px;
    margin: 3px;
}

@media (max-width: 360px) {
    body {
        padding: 7px;
    }

    .controls {
        grid-template-columns: repeat(3, 58px);
    }

    button, select {
        font-size: 12px;
        padding: 9px;
    }

    .panels {
        grid-template-columns: 1fr;
    }
}
</style>
</head>

<body>

<div class="wrap">

<h1>🐍 SNAKE XENZIA PRO</h1>

<div class="subtitle">
CLASSIC ARCADE • MOBILE EDITION
</div>

<div class="options">

<input id="playerName"
       maxlength="16"
       placeholder="Your player name"
       aria-label="Player name">

<select id="mode" aria-label="Game mode">
    <option value="classic">Classic Mode</option>
    <option value="obstacles">Obstacle Mode</option>
    <option value="rush">Speed Rush</option>
</select>

</div>

<div class="stats">

    <div class="stat">
        <div class="label">SCORE</div>
        <div class="value" id="score">0</div>
    </div>

    <div class="stat">
        <div class="label">BEST</div>
        <div class="value" id="best">0</div>
    </div>

    <div class="stat">
        <div class="label">LEVEL</div>
        <div class="value" id="level">1</div>
    </div>

</div>

<div class="gamebox">

    <canvas id="game" width="400" height="400"></canvas>

    <div class="overlay" id="overlay">

        <h2 id="overlayTitle">READY?</h2>

        <p id="overlayText">
            Eat the food 🍎 to grow your snake.<br>
            Avoid walls and your own tail.<br>
            Collect golden bonus food for extra points!
        </p>

        <button class="primary" id="startBtn">
            ▶ PLAY NOW
        </button>

    </div>

</div>

<div class="options">

    <select id="difficulty" aria-label="Difficulty">
        <option value="155">Easy</option>
        <option value="112" selected>Medium</option>
        <option value="76">Hard</option>
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

<div class="hint">
ARROW BUTTONS • SWIPE ON THE BOARD • KEYBOARD ARROWS
</div>

<div class="panels">

    <div class="panel">

        <h3>🏆 TOP SCORES ON THIS DEVICE</h3>

        <div id="leaderboard">
            No scores yet — play a round!
        </div>

    </div>

    <div class="panel">

        <h3>🎯 HOW TO PLAY</h3>

        <p>🍎 Red food: +10 points</p>
        <p>⭐ Golden bonus: +30 points</p>
        <p>🚧 Obstacle mode: avoid blocks</p>
        <p>⚡ Speed Rush: faster as you score</p>

        <p class="badge">
            Best score saves in this browser
        </p>

    </div>

</div>

</div>

<script>
(() => {

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const $ = id => document.getElementById(id);

const SIZE = 20;
const CELLS = 20;

let snake = [];
let direction = {x: 1, y: 0};
let nextDirection = {x: 1, y: 0};

let food = null;
let bonus = null;
let obstacles = [];

let score = 0;
let best = 0;

let running = false;
let started = false;
let gameOver = false;
let neon = true;

let timer = null;
let bonusTicks = 0;
let playerName = "Player";

try {
    best = Number(localStorage.getItem("sxpro_best")) || 0;
} catch (e) {}

$("best").textContent = best;


function safeGetScores() {
    try {
        return JSON.parse(
            localStorage.getItem("sxpro_scores") || "[]"
        );
    } catch (e) {
        return [];
    }
}


function renderScores() {

    const list = safeGetScores();

    $("leaderboard").textContent = list.length
        ? list.map((x, i) =>
            `${i + 1}. ${x.name} — ${x.score}`
          ).join("\n")
        : "No scores yet — play a round!";
}


function saveScores() {

    let list = safeGetScores();

    list.push({
        name: playerName || "Player",
        score: score,
        date: new Date().toLocaleDateString()
    });

    list.sort((a, b) => b.score - a.score);

    list = list.slice(0, 5);

    try {
        localStorage.setItem(
            "sxpro_scores",
            JSON.stringify(list)
        );
    } catch (e) {}

    renderScores();
}


function stopTimer() {

    if (timer !== null) {
        clearTimeout(timer);
        timer = null;
    }

}


function occupied(x, y) {

    return snake.some(
        p => p.x === x && p.y === y
    ) || obstacles.some(
        p => p.x === x && p.y === y
    );

}


function randomFree() {

    const free = [];

    for (let y = 0; y < CELLS; y++) {

        for (let x = 0; x < CELLS; x++) {

            if (
                !occupied(x, y) &&
                (!food || food.x !== x || food.y !== y) &&
                (!bonus || bonus.x !== x || bonus.y !== y)
            ) {
                free.push({x, y});
            }

        }

    }

    if (!free.length) {
        return null;
    }

    return free[
        Math.floor(Math.random() * free.length)
    ];

}


function spawnFood() {

    food = randomFree();

    if (!food) {
        winGame();
    }

}


function makeObstacles() {

    obstacles = [];

    if ($("mode").value === "obstacles") {

        for (let i = 0; i < 14; i++) {

            const p = randomFree();

            if (
                p &&
                !(Math.abs(p.x - 8) < 4 &&
                  Math.abs(p.y - 10) < 3)
            ) {
                obstacles.push(p);
            }

        }

    }

}


function resetGame() {

    stopTimer();

    snake = [
        {x: 8, y: 10},
        {x: 7, y: 10},
        {x: 6, y: 10}
    ];

    direction = {x: 1, y: 0};
    nextDirection = {x: 1, y: 0};

    score = 0;
    bonus = null;
    bonusTicks = 0;

    running = false;
    started = false;
    gameOver = false;

    $("score").textContent = "0";
    $("level").textContent = "1";
    $("pauseBtn").textContent = "⏸ Pause";

    makeObstacles();
    spawnFood();
    draw();

    $("overlayTitle").textContent = "READY?";

    $("overlayText").innerHTML =
        "Eat the food 🍎 to grow your snake.<br>" +
        "Avoid walls and your own tail.<br>" +
        "Collect golden bonus food for extra points!";

    $("startBtn").textContent = "▶ PLAY NOW";
    $("overlay").style.display = "flex";

}


function startGame() {

    if (gameOver) {
        resetGame();
    }

    playerName = (
        $("playerName").value || "Player"
    ).trim().slice(0, 16) || "Player";

    started = true;
    running = true;

    $("overlay").style.display = "none";
    $("pauseBtn").textContent = "⏸ Pause";

    stopTimer();
    tick();

}


function pauseGame() {

    if (!started || gameOver) {
        return;
    }

    running = !running;

    if (running) {

        $("overlay").style.display = "none";
        $("pauseBtn").textContent = "⏸ Pause";

        stopTimer();
        tick();

    } else {

        stopTimer();

        $("pauseBtn").textContent = "▶ Resume";
        $("overlayTitle").textContent = "PAUSED";
        $("overlayText").textContent =
            "Your game is paused.";

        $("startBtn").textContent = "▶ RESUME";
        $("overlay").style.display = "flex";

    }

}


function setDirection(name) {

    const dirs = {
        up:    {x: 0, y: -1},
        down:  {x: 0, y: 1},
        left:  {x: -1, y: 0},
        right: {x: 1, y: 0}
    };

    const d = dirs[name];

    if (!d) {
        return;
    }

    if (
        d.x === -direction.x &&
        d.y === -direction.y
    ) {
        return;
    }

    if (
        d.x === -nextDirection.x &&
        d.y === -nextDirection.y
    ) {
        return;
    }

    nextDirection = d;

    if (!started && !gameOver) {
        startGame();
    }

}


function tick() {

    if (!running) {
        return;
    }

    direction = {...nextDirection};

    const head = {
        x: snake[0].x + direction.x,
        y: snake[0].y + direction.y
    };

    const eating = food &&
        head.x === food.x &&
        head.y === food.y;

    const eatingBonus = bonus &&
        head.x === bonus.x &&
        head.y === bonus.y;

    if (
        head.x < 0 || head.x >= CELLS ||
        head.y < 0 || head.y >= CELLS
    ) {
        endGame();
        return;
    }

    const bodyToCheck =
        (eating || eatingBonus)
        ? snake
        : snake.slice(0, -1);

    if (
        bodyToCheck.some(
            p => p.x === head.x && p.y === head.y
        ) ||
        obstacles.some(
            p => p.x === head.x && p.y === head.y
        )
    ) {
        endGame();
        return;
    }

    snake.unshift(head);

    if (eating) {

        score += 10;

        spawnFood();

        if (score % 50 === 0) {

            const p = randomFree();

            if (p) {
                bonus = p;
                bonusTicks = 35;
            }

        }

    } else if (eatingBonus) {

        score += 30;
        bonus = null;
        bonusTicks = 0;

    } else {

        snake.pop();

    }

    if (bonus) {

        bonusTicks--;

        if (bonusTicks <= 0) {
            bonus = null;
        }

    }

    $("score").textContent = score;

    $("level").textContent =
        Math.floor(score / 50) + 1;

    if (score > best) {

        best = score;

        $("best").textContent = best;

        try {
            localStorage.setItem(
                "sxpro_best",
                String(best)
            );
        } catch (e) {}

    }

    draw();

    if (running) {

        let base = Number($("difficulty").value);

        if ($("mode").value === "rush") {

            base = Math.max(
                48,
                base - Math.floor(score / 20) * 5
            );

        } else {

            base = Math.max(
                55,
                base - Math.floor(score / 100) * 4
            );

        }

        timer = setTimeout(tick, base);

    }

}


function endGame() {

    running = false;
    gameOver = true;

    stopTimer();
    saveScores();

    $("overlayTitle").textContent = "GAME OVER!";

    $("overlayText").innerHTML =
        `${playerName || "Player"}, your score: <b>${score}</b><br>` +
        `Best score: <b>${best}</b><br><br>` +
        "Try again and beat your record!";

    $("startBtn").textContent = "↻ PLAY AGAIN";
    $("overlay").style.display = "flex";
    $("pauseBtn").textContent = "⏸ Pause";

}


function winGame() {

    running = false;
    gameOver = true;

    stopTimer();
    saveScores();

    $("overlayTitle").textContent = "🏆 BOARD CLEARED!";

    $("overlayText").textContent =
        "Amazing! You filled the board. Score: " + score;

    $("startBtn").textContent = "↻ PLAY AGAIN";
    $("overlay").style.display = "flex";

}


function draw() {

    const bg = neon ? "#081713" : "#b8cba4";
    const grid = neon ? "#163126" : "#9eb18b";

    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, 400, 400);

    ctx.strokeStyle = grid;
    ctx.lineWidth = 0.5;

    for (let i = 0; i <= CELLS; i++) {

        ctx.beginPath();
        ctx.moveTo(i * SIZE, 0);
        ctx.lineTo(i * SIZE, 400);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, i * SIZE);
        ctx.lineTo(400, i * SIZE);
        ctx.stroke();

    }

    obstacles.forEach(p => {

        ctx.fillStyle =
            neon ? "#7b8794" : "#65765c";

        ctx.fillRect(
            p.x * SIZE + 2,
            p.y * SIZE + 2,
            SIZE - 4,
            SIZE - 4
        );

    });

    if (food) {

        ctx.fillStyle = "#ff4b5c";
        ctx.shadowColor = "#ff334f";
        ctx.shadowBlur = neon ? 12 : 0;

        ctx.beginPath();

        ctx.arc(
            food.x * SIZE + 10,
            food.y * SIZE + 10,
            7,
            0,
            Math.PI * 2
        );

        ctx.fill();
        ctx.shadowBlur = 0;

        ctx.fillStyle = "#54e879";

        ctx.fillRect(
            food.x * SIZE + 11,
            food.y * SIZE + 1,
            3,
            5
        );

    }

    if (bonus) {

        ctx.fillStyle = "#ffd84d";
        ctx.shadowColor = "#ffcf33";
        ctx.shadowBlur = neon ? 14 : 0;

        ctx.beginPath();

        ctx.arc(
            bonus.x * SIZE + 10,
            bonus.y * SIZE + 10,
            8,
            0,
            Math.PI * 2
        );

        ctx.fill();
        ctx.shadowBlur = 0;

        ctx.fillStyle = "#513d00";
        ctx.font = "bold 12px Arial";
        ctx.textAlign = "center";

        ctx.fillText(
            "★",
            bonus.x * SIZE + 10,
            bonus.y * SIZE + 14
        );

    }

    snake.forEach((p, i) => {

        const pad = 1.5;

        ctx.fillStyle = neon
            ? (i === 0 ? "#c5ffda" : "#28e878")
            : (i === 0 ? "#183c20" : "#356b32");

        ctx.shadowColor = "#28e878";
        ctx.shadowBlur = neon && i === 0 ? 8 : 0;

        ctx.beginPath();

        ctx.roundRect(
            p.x * SIZE + pad,
            p.y * SIZE + pad,
            SIZE - pad * 2,
            SIZE - pad * 2,
            5
        );

        ctx.fill();

    });

    ctx.shadowBlur = 0;

    if (snake.length) {

        const h = snake[0];

        const cx = h.x * SIZE + 10;
        const cy = h.y * SIZE + 10;

        ctx.fillStyle = "#07110b";

        if (direction.x !== 0) {

            ctx.beginPath();

            ctx.arc(
                cx + direction.x * 4,
                cy - 4,
                2,
                0,
                Math.PI * 2
            );

            ctx.fill();

            ctx.beginPath();

            ctx.arc(
                cx + direction.x * 4,
                cy + 4,
                2,
                0,
                Math.PI * 2
            );

            ctx.fill();

        } else {

            ctx.beginPath();

            ctx.arc(
                cx - 4,
                cy + direction.y * 4,
                2,
                0,
                Math.PI * 2
            );

            ctx.fill();

            ctx.beginPath();

            ctx.arc(
                cx + 4,
                cy + direction.y * 4,
                2,
                0,
                Math.PI * 2
            );

            ctx.fill();

        }

    }

}


document.querySelectorAll("[data-dir]").forEach(btn => {

    btn.addEventListener("click", () => {
        setDirection(btn.dataset.dir);
    });

});


$("startBtn").addEventListener("click", startGame);

$("pauseBtn").addEventListener("click", pauseGame);

$("restartBtn").addEventListener("click", resetGame);


$("themeBtn").addEventListener("click", () => {

    neon = !neon;

    document.body.classList.toggle(
        "classic",
        !neon
    );

    draw();

});


$("mode").addEventListener("change", resetGame);


$("difficulty").addEventListener("change", () => {

    if (running) {
        stopTimer();
        tick();
    }

});


document.addEventListener("keydown", e => {

    const keys = {
        ArrowUp: "up",
        ArrowDown: "down",
        ArrowLeft: "left",
        ArrowRight: "right",
        w: "up",
        s: "down",
        a: "left",
        d: "right"
    };

    if (keys[e.key]) {
        e.preventDefault();
        setDirection(keys[e.key]);
    }

    if (e.code === "Space") {

        e.preventDefault();

        if (!started || gameOver) {
            startGame();
        } else {
            pauseGame();
        }

    }

});


let touchX = 0;
let touchY = 0;

canvas.addEventListener("touchstart", e => {

    const t = e.changedTouches[0];

    touchX = t.clientX;
    touchY = t.clientY;

}, {passive: true});


canvas.addEventListener("touchend", e => {

    const t = e.changedTouches[0];

    const dx = t.clientX - touchX;
    const dy = t.clientY - touchY;

    if (Math.max(Math.abs(dx), Math.abs(dy)) < 18) {
        return;
    }

    if (Math.abs(dx) > Math.abs(dy)) {

        setDirection(dx > 0 ? "right" : "left");

    } else {

        setDirection(dy > 0 ? "down" : "up");

    }

}, {passive: true});


renderScores();
resetGame();

})();
</script>

</body>
</html>
"""

components.html(
    game_html,
    height=1120,
    scrolling=False
)
