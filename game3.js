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

function render(now, dt) {
  g = ctx;
  ctx.clearRect(0, 0, W, H);
  ctx.drawImage(bg, 0, 0, W, H);

  const t = (started && !gameOver) ? Math.min(1, acc / interval) : 1;
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
      box(it.x, it.y, 0, top, col, 0.07);
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

  for (let i = pops.length - 1; i >= 0; i--) {
    const p = pops[i];
    p.z += 1.6 * dt;
    p.life -= dt;
    if (p.life <= 0) { pops.splice(i, 1); continue; }
    const q = proj(p.x, p.y, p.z);
    g.globalAlpha = Math.min(1, p.life / 0.5);
    g.font = "bold " + Math.round(17 * q[2]) + "px Arial";
    g.textAlign = "center";
    g.lineWidth = 3;
    g.strokeStyle = "rgba(0,0,0,.6)";
    g.strokeText(p.text, q[0], q[1]);
    g.fillStyle = p.color;
    g.fillText(p.text, q[0], q[1]);
  }
  g.globalAlpha = 1;

  for (let x = -1; x <= CELLS; x++) box(x, CELLS, 0, 0.55, T.wall, 0);
}

function loop(now) {
  const ms = Math.min(100, now - lastFrame);
  lastFrame = now;
  if (running) {
    acc += ms;
    let guard = 0;
    while (acc >= interval && running && guard++ < 3) {
      acc -= interval;
      step();
    }
    if (acc > interval) acc = interval;
  }
  render(now, ms / 1000);
  requestAnimationFrame(loop);
}

/* ---------- input ---------- */
document.querySelectorAll("[data-dir]").forEach(btn => {
  btn.addEventListener("pointerdown", e => {
    e.preventDefault();
    setDirection(btn.dataset.dir);
  });
});

let tx = 0, ty = 0;
canvas.addEventListener("touchstart", e => {
  const t = e.touches[0];
  tx = t.clientX; ty = t.clientY;
}, {passive: true});
canvas.addEventListener("touchmove", e => {
  const t = e.touches[0];
  const dx = t.clientX - tx, dy = t.clientY - ty;
  if (Math.max(Math.abs(dx), Math.abs(dy)) < 18) return;
  if (Math.abs(dx) > Math.abs(dy)) setDirection(dx > 0 ? "right" : "left");
  else setDirection(dy > 0 ? "down" : "up");
  tx = t.clientX; ty = t.clientY;
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
    if (gameOver) startGame(); else pauseGame();
  }
});

/* ---------- buttons ---------- */
$("startBtn").addEventListener("click", startGame);
$("restartBtn").addEventListener("click", startGame);
$("pauseBtn").addEventListener("click", pauseGame);
$("resumeBtn").addEventListener("click", () => {
  if (gameOver) startGame(); else pauseGame();
});
$("menuBtn").addEventListener("click", () => {
  resetGame();
  renderScores();
  showMenu();
});
$("themeBtn").addEventListener("click", () => {
  neon = !neon;
  T = neon ? THEMES.neon : THEMES.classic;
  document.body.classList.toggle("classic", !neon);
  $("themeBtn").textContent = neon ? "🎨 Neon" : "🎨 Classic";
  buildBg();
});
$("soundBtn").addEventListener("click", () => {
  soundOn = !soundOn;
  $("soundBtn").textContent = soundOn ? "🔊 Sound On" : "🔇 Sound Off";
  beep(520, 0.08, "sine", 0.06);
});
$("mode").addEventListener("change", resetGame);
$("difficulty").addEventListener("change", () => { interval = delay(); });
document.addEventListener("visibilitychange", () => {
  if (document.hidden && running) pauseGame();
});

/* ---------- start ---------- */
buildBg();
renderScores();
resetGame();
showMenu();
requestAnimationFrame(loop);
