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

/* 3D camera */
const PITCH = 55 * Math.PI / 180;
const SP = Math.sin(PITCH), CP = Math.cos(PITCH);
const CAMD = 34, SC = 15.5, CX = W / 2, CY = 162;

function proj(x, y, z) {
  const X = x - 10, Y = y - 10;
  const dc = Y * CP + z * SP;
  const f = CAMD / (CAMD - dc);
  return [CX + X * f * SC, CY + (Y * SP - z * CP) * f * SC, f];
}

const THEMES = {
  neon: {
    bgA: "#123a31", bgB: "#050d14", floorA: "#0f3027", floorB: "#0b2620",
    wall: "#1a9a70", obstacle: "#6b7b99", head: "#d4ffe6", body: "#2ee67f",
    tail: "#0f8f4c", food: "#ff4b5c", bonus: "#ffd84d", glow: true
  },
  classic: {
    bgA: "#dbe8c7", bgB: "#9fb48a", floorA: "#c6d8ae", floorB: "#bacf9f",
    wall: "#6b8a5a", obstacle: "#5a6b50", head: "#1b4223", body: "#3a7437",
    tail: "#27552b", food: "#d93a49", bonus: "#e8b923", glow: false
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
