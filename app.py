import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Snake Xenzia Pro",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, footer, header,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    iframe {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport"
 content="width=device-width, initial-scale=1, maximum-scale=1,
 user-scalable=no">

<style>
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

body {
    margin: 0;
    padding: 12px;
    background: #07111b;
    color: white;
    font-family: Arial, sans-serif;
    text-align: center;
    user-select: none;
}

h1 {
    margin: 6px 0;
    font-size: clamp(25px, 7vw, 38px);
    color: #39ff88;
    text-shadow: 0 0 15px #00ff7780;
}

.subtitle {
    color: #9eb5c9;
    margin-bottom: 14px;
    font-size: 12px;
    letter-spacing: 3px;
}

.stats {
    display: flex;
    justify-content: space-around;
    gap: 8px;
    margin: 12px auto;
    max-width: 440px;
}

.stat {
    flex: 1;
    padding: 10px 5px;
    border: 1px solid #21443b;
    background: #0d201f;
    border-radius: 12px;
}

.label {
    color: #8daea1;
    font-size: 11px;
}

.value {
    font-size: 23px;
    font-weight: bold;
    color: #39ff88;
    margin-top: 4px;
}

.gamebox {
    width: 100%;
    max-width: 440px;
    margin: 0 auto;
    position: relative;
    border: 2px solid #35ed86;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 0 20px #18ff7730;
    background: #0b1715;
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
    background: #06120ee8;
    padding: 20px;
}

.overlay h2 {
    color: #39ff88;
    font-size: 29px;
    margin: 0 0 10px;
}

.overlay p {
    line-height: 1.6;
    color: #d4e4dc;
    font-size: 14px;
}

button, select {
    border: 1px solid #39ff88;
    background: #102a21;
    color: white;
    border-radius: 10px;
    font-size: 15px;
    font-weight: bold;
    padding: 12px 15px;
    cursor: pointer;
    touch-action: manipulation;
}

button:active {
    background: #246a49;
    transform: scale(.96);
}

.primary {
    background: #39ff88;
    color: #06150c;
    border: none;
    min-width: 150px;
}

.options {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 9px;
    margin: 13px auto;
}

select {
    max-width: 150px;
}

.controls {
    display: grid;
    grid-template-columns: repeat(3, 66px);
    grid-template-rows: repeat(2, 54px);
    justify-content: center;
    gap: 7px;
    margin: 16px auto 10px;
}

.controls button {
    font-size: 23px;
    padding: 5px;
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
    font-size: 11px;
    color: #8da5a0;
    margin: 12px 0 5px;
}
</style>
</head>

<body>

<h1>🐍 SNAKE XENZIA PRO</h1>
<div class="subtitle">CLASSIC ARCADE • MOBILE EDITION</div>

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
            Eat the food 🍎<br>
            Grow your snake and beat your record!<br><br>
            Don't hit the walls or yourself.
        </p>
        <button class="primary" id="startBtn">▶ PLAY NOW</button>
    </div>
</div>

<div class="options">
    <select id="difficulty" aria-label="Difficulty">
        <option value="160">Easy</option>
        <option value="115" selected>Medium</option>
        <option value="75">Hard</option>
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
    USE THE ARROWS • SWIPE ON THE BOARD • KEYBOARD ALSO SUPPORTED
</div>

<script>
(() => {
    const canvas = document.getElementById("game");
    const ctx = canvas.getContext("2d");

    const scoreEl = document.getElementById("score");
    const bestEl = document.getElementById("best");
    const levelEl = document.getElementById("level");
    const overlay = document.getElementById("overlay");
    const overlayTitle = document.getElementById("overlayTitle");
    const overlayText = document.getElementById("overlayText");
    const startBtn = document.getElementById("startBtn");
    const pauseBtn = document.getElementById("pauseBtn");
    const difficulty = document.getElementById("difficulty");
    const restartBtn = document.getElementById("restartBtn");
    const themeBtn = document.getElementById("themeBtn");

    const SIZE = 20;
    const CELLS = 20;

    let snake, direction, nextDirection, food;
    let score = 0;
    let best = 0;
    let running = false;
    let started = false;
    let gameOver = false;
    let timer = null;
    let neon = true;

    try {
        best = Number(localStorage.getItem("snakeXenziaBest")) || 0;
    } catch (e) {}

    bestEl.textContent = best;

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
        running = false;
        started = false;
        gameOver = false;

        scoreEl.textContent = "0";
        levelEl.textContent = "1";
        pauseBtn.textContent = "⏸ Pause";

        spawnFood();
        draw();

        overlayTitle.textContent = "READY?";
        overlayText.innerHTML =
            "Eat the food 🍎<br>" +
            "Grow your snake and beat your record!<br><br>" +
            "Don't hit the walls or yourself.";

        startBtn.textContent = "▶ PLAY NOW";
        overlay.style.display = "flex";
    }

    function stopTimer() {
        if (timer !== null) {
            clearTimeout(timer);
            timer = null;
        }
    }

    function spawnFood() {
        const free = [];

        for (let y = 0; y < CELLS; y++) {
            for (let x = 0; x < CELLS; x++) {
                if (!snake.some(p => p.x === x && p.y === y)) {
                    free.push({x, y});
                }
            }
        }

        if (!free.length) {
            winGame();
            return;
        }

        food = free[Math.floor(Math.random() * free.length)];
    }

    function startGame() {
        if (gameOver) {
            resetGame();
        }

        started = true;
        running = true;
        overlay.style.display = "none";
        pauseBtn.textContent = "⏸ Pause";
        stopTimer();
        tick();
    }

    function pauseGame() {
        if (!started || gameOver) return;

        running = !running;

        if (running) {
            overlay.style.display = "none";
            pauseBtn.textContent = "⏸ Pause";
            stopTimer();
            tick();
        } else {
            stopTimer();
            pauseBtn.textContent = "▶ Resume";
            overlayTitle.textContent = "PAUSED";
            overlayText.textContent = "Take a break. Your snake is waiting!";
            startBtn.textContent = "▶ RESUME";
            overlay.style.display = "flex";
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
        if (!d) return;

        if (d.x === -direction.x && d.y === -direction.y) {
            return;
        }

        if (d.x === -nextDirection.x &&
            d.y === -nextDirection.y) {
            return;
        }

        nextDirection = d;

        if (!started && !gameOver) {
            startGame();
        }
    }

    function tick() {
        if (!running) return;

        direction = {...nextDirection};

        const head = {
            x: snake[0].x + direction.x,
            y: snake[0].y + direction.y
        };

        if (
            head.x < 0 || head.x >= CELLS ||
            head.y < 0 || head.y >= CELLS
        ) {
            endGame();
            return;
        }

        const eating = head.x === food.x && head.y === food.y;

        const bodyToCheck = eating ? snake : snake.slice(0, -1);

        if (bodyToCheck.some(p => p.x === head.x && p.y === head.y)) {
            endGame();
            return;
        }

        snake.unshift(head);

        if (eating) {
            score += 10;
            scoreEl.textContent = score;
            levelEl.textContent = Math.floor(score / 50) + 1;

            if (score > best) {
                best = score;
                bestEl.textContent = best;

                try {
                    localStorage.setItem("snakeXenziaBest", best);
                } catch (e) {}
            }

            spawnFood();
        } else {
            snake.pop();
        }

        draw();

        if (running) {
            const base = Number(difficulty.value);
            const speed = Math.max(48, base - Math.floor(score / 50) * 8);
            timer = setTimeout(tick, speed);
        }
    }

    function endGame() {
        running = false;
        gameOver = true;
        stopTimer();

        overlayTitle.textContent = "GAME OVER!";
        overlayText.innerHTML =
            "Your score: <b>" + score + "</b><br>" +
            "Best score: <b>" + best + "</b><br><br>" +
            "Can you beat your record?";

        startBtn.textContent = "↻ PLAY AGAIN";
        overlay.style.display = "flex";
        pauseBtn.textContent = "⏸ Pause";
    }

    function winGame() {
        running = false;
        gameOver = true;
        stopTimer();

        overlayTitle.textContent = "🏆 YOU WIN!";
        overlayText.textContent =
            "Amazing! You filled the entire board. Score: " + score;

        startBtn.textContent = "↻ PLAY AGAIN";
        overlay.style.display = "flex";
    }

    function draw() {
        ctx.fillStyle = neon ? "#081713" : "#b8cba4";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.strokeStyle = neon ? "#163126" : "#9eb18b";
        ctx.lineWidth = 0.5;

        for (let i = 0; i <= CELLS; i++) {
            ctx.beginPath();
            ctx.moveTo(i * SIZE, 0);
            ctx.lineTo(i * SIZE, canvas.height);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(0, i * SIZE);
            ctx.lineTo(canvas.width, i * SIZE);
            ctx.stroke();
        }

        // Food
        const fx = food.x * SIZE + SIZE / 2;
        const fy = food.y * SIZE + SIZE / 2;

        ctx.fillStyle = "#ff4b5c";
        ctx.shadowColor = "#ff334f";
        ctx.shadowBlur = neon ? 12 : 0;

        ctx.beginPath();
        ctx.arc(fx, fy, SIZE * 0.37, 0, Math.PI * 2);
        ctx.fill();

        ctx.shadowBlur = 0;

        ctx.fillStyle = "#54e879";
        ctx.fillRect(fx + 2, fy - 10, 3, 6);

        // Snake
        snake.forEach((p, i) => {
            const pad = 1.5;
            const x = p.x * SIZE + pad;
            const y = p.y * SIZE + pad;
            const s = SIZE - pad * 2;

            ctx.fillStyle = neon
                ? (i === 0 ? "#b8ffcf" : "#28e878")
                : (i === 0 ? "#183c20" : "#356b32");

            ctx.shadowColor = "#28e878";
            ctx.shadowBlur = neon && i === 0 ? 8 : 0;

            ctx.beginPath();
            ctx.roundRect(x, y, s, s, 5);
            ctx.fill();
        });

        ctx.shadowBlur = 0;

        // Eyes
        if (snake.length) {
            const h = snake[0];
            const cx = h.x * SIZE + SIZE / 2;
            const cy = h.y * SIZE + SIZE / 2;

            ctx.fillStyle = "#07110b";

            if (direction.x !== 0) {
                ctx.beginPath();
                ctx.arc(cx + direction.x * 4,
                        cy - 4, 2, 0, Math.PI * 2);
                ctx.fill();

                ctx.beginPath();
                ctx.arc(cx + direction.x * 4,
                        cy + 4, 2, 0, Math.PI * 2);
                ctx.fill();
            } else {
                ctx.beginPath();
                ctx.arc(cx - 4,
                        cy + direction.y * 4, 2, 0, Math.PI * 2);
                ctx.fill();

                ctx.beginPath();
                ctx.arc(cx + 4,
                        cy + direction.y * 4, 2, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    }

    document.querySelectorAll("[data-dir]").forEach(btn => {
        btn.addEventListener("click", () => {
            setDirection(btn.dataset.dir);
        });
    });

    startBtn.addEventListener("click", () => {
        if (started && !running && !gameOver) {
            startGame();
        } else {
            startGame();
        }
    });

    pauseBtn.addEventListener("click", pauseGame);

    restartBtn.addEventListener("click", resetGame);

    themeBtn.addEventListener("click", () => {
        neon = !neon;
        draw();
    });

    difficulty.addEventListener("change", () => {
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
            if (!started || gameOver) startGame();
            else pauseGame();
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

        if (Math.max(Math.abs(dx), Math.abs(dy)) < 18) return;

        if (Math.abs(dx) > Math.abs(dy)) {
            setDirection(dx > 0 ? "right" : "left");
        } else {
            setDirection(dy > 0 ? "down" : "up");
        }
    }, {passive: true});

    resetGame();
})();
</script>

</body>
</html>
"""

components.html(
    game_html,
    height=850,
    scrolling=False
)
