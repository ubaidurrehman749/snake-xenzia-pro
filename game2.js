let snake = [], prev = [];
let direction = {x: 1, y: 0};
let dirQueue = [];
let food = null, bonus = null, obstacles = [];
let score = 0, best = 0, newBest = false;
let running = false, started = false, gameOver = false, counting = false;
let bonusTicks = 0, playerName = "Player";
let acc = 0, interval = 150;
let particles = [], pops = [];
let soundOn = true, cdTimer = null, actx = null;

try { best = Number(localStorage.getItem("sxpro_best")) || 0; } catch (e) {}
$("best").textContent = best;

function beep(f, d, type, vol) {
  if (!soundOn) return;
  try {
    actx = actx || new (window.AudioContext || window.webkitAudioContext)();
    if (actx.state === "suspended") actx.resume();
    const o = actx.createOscillator(), gn = actx.createGain(), t = actx.currentTime;
    o.type = type || "sine";
    o.frequency.value = f;
    gn.gain.setValueAtTime(vol || 0.07, t);
    gn.gain.exponentialRampToValueAtTime(0.001, t + d);
    o.connect(gn);
    gn.connect(actx.destination);
    o.start(t);
    o.stop(t + d);
  } catch (e) {}
}

function buzz(ms) { try { if (navigator.vibrate) navigator.vibrate(ms); } catch (e) {} }

function safeGetScores() {
  try { return JSON.parse(localStorage.getItem("sxpro_scores") || "[]"); }
  catch (e) { return []; }
}
function renderScores() {
  const list = safeGetScores().slice(0, 3);
  $("leaderboard").textContent = list.length
    ? "🏆 TOP SCORES\n" + list.map((x, i) => (i + 1) + ". " + x.name + " - " + x.score).join("\n")
    : "🏆 No scores yet. Be the first!";
}
function saveScores() {
  if (score <= 0) return;
  let list = safeGetScores();
  list.push({name: playerName || "Player", score: score});
  list.sort((a, b) => b.score - a.score);
  list = list.slice(0, 5);
  try { localStorage.setItem("sxpro_scores", JSON.stringify(list)); } catch (e) {}
  renderScores();
}

function showMenu() {
  $("overlay").style.display = "flex";
  $("menuScreen").style.display = "flex";
  $("msgScreen").style.display = "none";
}
function showMsg(title, html, btn) {
  $("overlayTitle").textContent = title;
  $("overlayText").innerHTML = html;
  $("resumeBtn").textContent = btn;
  $("overlay").style.display = "flex";
  $("menuScreen").style.display = "none";
  $("msgScreen").style.display = "flex";
}
function hideOverlay() { $("overlay").style.display = "none"; }

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
function pop(x, y, text, color) {
  pops.push({x: x + 0.5, y: y + 0.5, z: 0.9, text: text, life: 0.9, color: color});
}

function resetGame() {
  if (cdTimer) { clearInterval(cdTimer); cdTimer = null; }
  $("count").style.display = "none";
  snake = [{x: 8, y: 10}, {x: 7, y: 10}, {x: 6, y: 10}];
  freezePrev();
  direction = {x: 1, y: 0};
  dirQueue = [];
  score = 0; newBest = false;
  food = null; bonus = null; bonusTicks = 0;
  particles = []; pops = [];
  running = false; started = false; gameOver = false; counting = false;
  acc = 0;
  $("score").textContent = "0";
  $("level").textContent = "1";
  $("lvlbar").style.width = "0%";
  $("pauseBtn").textContent = "⏸";
  makeObstacles();
  spawnFood();
  interval = delay();
}

function showCount(n) {
  const c = $("count");
  c.style.display = "flex";
  c.textContent = n;
  c.classList.remove("beat");
  void c.offsetWidth;
  c.classList.add("beat");
  beep(440, 0.08, "triangle", 0.06);
}

function startGame() {
  resetGame();
  playerName = ($("playerName").value || "Player").trim().slice(0, 16) || "Player";
  hideOverlay();
  counting = true;
  let n = 3;
  showCount(n);
  cdTimer = setInterval(() => {
    n--;
    if (n > 0) {
      showCount(n);
    } else {
      clearInterval(cdTimer);
      cdTimer = null;
      $("count").style.display = "none";
      counting = false;
      started = true;
      running = true;
      acc = 0;
      freezePrev();
      beep(700, 0.15, "triangle", 0.07);
    }
  }, 650);
}

function pauseGame() {
  if (!started || gameOver || counting) return;
  if (running) {
    running = false;
    $("pauseBtn").textContent = "▶";
    showMsg("PAUSED", "Take a breath, then jump back in!", "▶ Resume");
  } else {
    running = true;
    $("pauseBtn").textContent = "⏸";
    hideOverlay();
  }
}

function setDirection(name) {
  const dirs = {
    up: {x: 0, y: -1}, down: {x: 0, y: 1},
    left: {x: -1, y: 0}, right: {x: 1, y: 0}
  };
  const d = dirs[name];
  if (!d || !(running || counting)) return;
  const last = dirQueue.length ? dirQueue[dirQueue.length - 1] : direction;
  if (d.x === -last.x && d.y === -last.y) return;
  if (d.x === last.x && d.y === last.y) return;
  if (dirQueue.length < 2) dirQueue.push(d);
}

function step() {
  if (dirQueue.length) direction = dirQueue.shift();
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
    pop(head.x, head.y, "+10", "#ffffff");
    beep(620, 0.07, "square", 0.05);
    buzz(15);
    spawnFood();
    if (score % 50 === 0) {
      const p = randomFree();
      if (p) { bonus = p; bonusTicks = 35; }
    }
  } else if (eatingBonus) {
    score += 30;
    burst(head.x, head.y, T.bonus, 20);
    pop(head.x, head.y, "+30", "#ffd84d");
    beep(880, 0.12, "square", 0.06);
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
    newBest = true;
    $("best").textContent = best;
    try { localStorage.setItem("sxpro_best", String(best)); } catch (e) {}
  }
  interval = delay();
}

function endGame() {
  running = false;
  gameOver = true;
  saveScores();
  burst(snake[0].x, snake[0].y, "#ff3355", 22);
  buzz(120);
  beep(200, 0.25, "sawtooth", 0.08);
  setTimeout(() => beep(120, 0.35, "sawtooth", 0.08), 150);
  canvas.classList.remove("shake");
  void canvas.offsetWidth;
  canvas.classList.add("shake");
  setTimeout(() => {
    if (!gameOver) return;
    showMsg(
      newBest ? "🏆 NEW BEST!" : "GAME OVER",
      playerName + ", your score: <b>" + score + "</b><br>Best score: <b>" + best + "</b>",
      "↻ Play Again"
    );
  }, 650);
}

function winGame() {
  running = false;
  gameOver = true;
  saveScores();
  showMsg("🏆 BOARD CLEARED!", "Amazing! You filled the board.<br>Score: <b>" + score + "</b>", "↻ Play Again");
                          }
