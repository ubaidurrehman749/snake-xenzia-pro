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
function stopTimer() { if (timer !== null) { clearTimeout(timer); timer = null; } }

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
      if (p && !(Math.abs(p.x - 8) < 4 && Math.abs(p.y - 10) < 3)) obstacles.push(p);
    }
  }
}
function burst(x, y, color, n) {
  for (let i = 0; i < n; i++) {
    const a = Math.random() * Math.PI * 2;
    const s = 0.6 + Math.random() * 2.2;
    particles.push({
      x: x + 0.5, y: y + 0.5, z: 0.5,
      vx: Math.cos(a) * s, vy: Math.sin(a) * s, vz: 2 + Math.random() * 3,
      life: 0.7, color: color
    });
  }
}

function resetGame() {
  stopTimer();
  snake = [{x: 8, y: 10}, {x: 7, y: 10}, {x: 6, y: 10}];
  freezePrev();
  direction = {x: 1, y: 0};
  nextDirection = {x: 1, y: 0};
  score = 0; food = null; bonus = null; bonusTicks = 0; particles = [];
  running = false; started = false; gameOver = false;
  $("score").textContent = "0";
  $("level").textContent = "1";
  $("lvlbar").style.width = "0%";
  $("pauseBtn").textContent = "⏸ Pause";
  makeObstacles();
  spawnFood();
  $("overlayTitle").textContent = "READY?";
  $("overlayText").innerHTML =
    "Eat the food 🍎 to grow your snake.<br>" +
    "Avoid walls and your own tail.<br>" +
    "Collect golden bonus food for extra points!";
  $("startBtn").textContent = "▶ PLAY NOW";
  $("overlay").style.display = "flex";
}

function startGame() {
  if (gameOver) resetGame();
  playerName = ($("playerName").value || "Player").trim().slice(0, 16) || "Player";
  started = true;
  running = true;
  $("overlay").style.display = "none";
  $("pauseBtn").textContent = "⏸ Pause";
  freezePrev();
  schedule();
}

function pauseGame() {
  if (!started || gameOver) return;
  running = !running;
  if (running) {
    $("overlay").style.display = "none";
    $("pauseBtn").textContent = "⏸ Pause";
    freezePrev();
    schedule();
  } else {
    stopTimer();
    $("pauseBtn").textContent = "▶ Resume";
    $("overlayTitle").textContent = "PAUSED";
    $("overlayText").textContent = "Your game is paused.";
    $("startBtn").textContent = "▶ RESUME";
    $("overlay").style.display = "flex";
  }
}

function setDirection(name) {
  const dirs = {
    up: {x: 0, y: -1}, down: {x: 0, y: 1},
    left: {x: -1, y: 0}, right: {x: 1, y: 0}
  };
  const d = dirs[name];
  if (!d) return;
  if (d.x === -direction.x && d.y === -direction.y) return;
  if (d.x === -nextDirection.x && d.y === -nextDirection.y) return;
  nextDirection = d;
  if (!started && !gameOver) startGame();
}

function tick() {
  if (!running) return;
  direction = {...nextDirection};
  const head = {x: snake[0].x + direction.x, y: snake[0].y + direction.y};
  const eating = food && head.x === food.x && head.y === food.y;
  const eatingBonus = bonus && head.x === bonus.x && head.y === bonus.y;

  if (head.x < 0 || head.x >= CELLS || head.y < 0 || head.y >= CELLS) {
    endGame();
    return;
  }
  const bodyToCheck = (eating || eatingBonus) ? snake : snake.slice(0, -1);
  if (bodyToCheck.some(p => p.x === head.x && p.y === head.y) ||
      obstacles.some(p => p.x === head.x && p.y === head.y)) {
    endGame();
    return;
  }

  freezePrev();
  snake.unshift(head);

  if (eating) {
    score += 10;
    burst(head.x, head.y, T.food, 14);
    buzz(15);
    spawnFood();
    if (score % 50 === 0) {
      const p = randomFree();
      if (p) { bonus = p; bonusTicks = 35; }
    }
  } else if (eatingBonus) {
    score += 30;
    burst(head.x, head.y, T.bonus, 20);
    buzz(25);
    bonus = null;
    bonusTicks = 0;
  } else {
    snake.pop();
  }

  if (bonus) {
    bonusTicks--;
    if (bonusTicks <= 0) bonus = null;
  }

  $("score").textContent = score;
  $("level").textContent = Math.floor(score / 50) + 1;
  $("lvlbar").style.width = ((score % 50) / 50 * 100) + "%";

  if (score > best) {
    best = score;
    $("best").textContent = best;
    try { localStorage.setItem("sxpro_best", String(best)); } catch (e) {}
  }
  if (running) schedule();
}

function endGame() {
  running = false;
  gameOver = true;
  stopTimer();
  saveScores();
  burst(snake[0].x, snake[0].y, "#ff3355", 22);
  buzz(120);
  $("overlayTitle").textContent = "GAME OVER!";
  $("overlayText").innerHTML =
    (playerName || "Player") + ", your score: <b>" + score + "</b><br>" +
    "Best score: <b>" + best + "</b><br><br>Try again and beat your record!";
  $("startBtn").textContent = "↻ PLAY AGAIN";
  $("pauseBtn").textContent = "⏸ Pause";
  setTimeout(() => { if (gameOver) $("overlay").style.display = "flex"; }, 450);
}

function winGame() {
  running = false;
  gameOver = true;
  stopTimer();
  saveScores();
  $("overlayTitle").textContent = "🏆 BOARD CLEARED!";
  $("overlayText").textContent = "Amazing! You filled the board. Score: " + score;
  $("startBtn").textContent = "↻ PLAY AGAIN";
  $("overlay").style.display = "flex";
}

/* rendering */
let lastFrame = performance.now();

function drawEyes(x, y, z) {
  const hx = x + 0.5, hy = y + 0.5;
  const dx = direction.x, dy = direction.y;
  const px = -dy, py = dx;
  [-1, 1].forEach(s => {
    const p = proj(hx + dx * 0.2 + px * 0.2 * s, hy + dy * 0.2 + py * 0.2 * s, z);
    const r = 0.16 * p[2] * SC;
    g.fillStyle = "#ffffff";
    g.beginPath(); g.arc(p[0], p[1], r, 0, Math.PI * 2); g.fill();
    g.fillStyle = "#07110b";
    g.beginPath(); g.arc(p[0] + dx * r * 0.3, p[1] + dy * r * 0.2, r * 0.55, 0, Math.PI * 2); g.fill();
  });
}

function render(now) {
  const dt = Math.min(0.05, (now - lastFrame) / 1000);
  lastFrame = now;
  g = ctx;
  ctx.clearRect(0, 0, W, H);
  ctx.drawImage(bg, 0, 0, W, H);

  const t = running ? Math.min(1, (now - lastTick) / interval) : 1;
  const items = [];
  obstacles.forEach(o => items.push({k: "ob", x: o.x, y: o.y}));
  snake.forEach((s, i) => {
    const p = prev[i] || s;
    items.push({k: "sn", i: i, x: p.x + (s.x - p.x) * t, y: p.y + (s.y - p.y) * t});
  });
  if (food) items.push({k: "food", x: food.x, y: food.y});
  if (bonus) items.push({k: "bonus", x: bonus.x, y: bonus.y});
  items.sort((a, b) => (a.y - b.y) || (Math.abs(b.x + 0.5 - 10) - Math.abs(a.x + 0.5 - 10)));

  const len = snake.length;
  items.forEach(it => {
    if (it.k === "ob") {
      box(it.x, it.y, 0, 0.9, T.obstacle, 0.06);
    } else if (it.k === "sn") {
      quad([[it.x + 0.05, it.y + 0.05, 0], [it.x + 0.95, it.y + 0.05, 0],
            [it.x + 0.95, it.y + 0.95, 0], [it.x + 0.05, it.y + 0.95, 0]], "rgba(0,0,0,.28)");
      const col = it.i === 0 ? T.head : lerpHex(T.body, T.tail, len > 1 ? it.i / (len - 1) : 0);
      const top = it.i === 0 ? 0.85 : 0.7;
      if (it.i === 0 && T.glow) { g.shadowColor = "#2ee67f"; g.shadowBlur = 12; }
      box(it.x, it.y, 0, top, col, 0.07);
      g.shadowBlur = 0;
      if (it.i === 0) drawEyes(it.x, it.y, top);
    } else if (it.k === "food") {
      const z = 0.5 + 0.1 * Math.sin(now / 250);
      const s = sphere(it.x + 0.5, it.y + 0.5, z, 0.38, T.food, T.glow);
      g.strokeStyle = "#54e879";
      g.lineWidth = 2;
      g.beginPath();
      g.moveTo(s.x, s.y - s.R);
      g.lineTo(s.x + 3, s.y - s.R - 5);
      g.stroke();
    } else if (it.k === "bonus") {
      if (bonusTicks < 10 && Math.floor(now / 150) % 2) return;
      const z = 0.6 + 0.12 * Math.sin(now / 200);
      const s = sphere(it.x + 0.5, it.y + 0.5, z, 0.44, T.bonus, T.glow);
      g.fillStyle = "#513d00";
      g.font = "bold " + Math.round(s.R * 1.2) + "px Arial";
      g.textAlign = "center";
      g.fillText("★", s.x, s.y + s.R * 0.42);
    }
  });

  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];
    p.x += p.vx * dt; p.y += p.vy * dt; p.z += p.vz * dt;
    p.vz -= 14 * dt;
    if (p.z < 0) { p.z = 0; p.vz *= -0.3; }
    p.life -= dt;
    if (p.life <= 0) { particles.splice(i, 1); continue; }
    const q = proj(p.x, p.y, p.z);
    g.globalAlpha = Math.max(0, p.life / 0.7);
    g.fillStyle = p.color;
    g.beginPath();
    g.arc(q[0], q[1], 2.6 * q[2], 0, Math.PI * 2);
    g.fill();
  }
  g.globalAlpha = 1;

  for (let x = -1; x <= CELLS; x++) box(x, CELLS, 0, 0.55, T.wall, 0);
  requestAnimationFrame(render);
}

/* input */
document.querySelectorAll("[data-dir]").forEach(btn => {
  btn.addEventListener("pointerdown", e => {
    e.preventDefault();
    setDirection(btn.dataset.dir);
  });
});
$("startBtn").addEventListener("click", startGame);
$("pauseBtn").addEventListener("click", pauseGame);
$("restartBtn").addEventListener("click", resetGame);
$("themeBtn").addEventListener("click", () => {
  neon = !neon;
  T = neon ? THEMES.neon : THEMES.classic;
  document.body.classList.toggle("classic", !neon);
  buildBg();
});
$("mode").addEventListener("change", resetGame);
$("difficulty").addEventListener("change", () => {
  if (running) { freezePrev(); schedule(); }
});

let tx = 0, ty = 0;
canvas.addEventListener("touchstart", e => {
  const t = e.touches[0];
  tx = t.clientX; ty = t.clientY;
}, {passive: true});
canvas.addEventListener("touchend", e => {
  const t = e.changedTouches[0];
  const dx = t.clientX - tx, dy = t.clientY - ty;
  if (Math.max(Math.abs(dx), Math.abs(dy)) < 24) return;
  if (Math.abs(dx) > Math.abs(dy)) setDirection(dx > 0 ? "right" : "left");
  else setDirection(dy > 0 ? "down" : "up");
}, {passive: true});

document.addEventListener("keydown", e => {
  const keys = {
    ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right",
    w: "up", s: "down", a: "left", d: "right"
  };
  if (keys[e.key]) {
    e.preventDefault();
    setDirection(keys[e.key]);
  } else if (e.key === " " || e.key === "p") {
    e.preventDefault();
    if (!started || gameOver) startGame(); else pauseGame();
  }
});

/* start */
buildBg();
renderScores();
resetGame();
requestAnimationFrame(render);
