// script.js (side-by-side private UI with history, 3s interval)

const video = document.getElementById("video");
const canvas = document.getElementById("captureCanvas");
const intervalInput = document.getElementById("intervalInput");
const autoToggle = document.getElementById("autoToggle");
const snapBtn = document.getElementById("snapBtn");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const serverUrlInput = document.getElementById("serverUrl");
const lastResult = document.getElementById("lastResult");
const lastConfidence = document.getElementById("lastConfidence");
const historyEl = document.getElementById("history");

let timerId = null;
let running = false;

async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    video.srcObject = stream;
    await video.play();
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
  } catch (e) {
    alert("Camera error: " + e);
  }
}

function captureFrameBlob(quality = 0.8) {
  const ctx = canvas.getContext("2d");
  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  return new Promise(resolve => {
    canvas.toBlob(blob => resolve(blob), "image/jpeg", quality);
  });
}

async function sendFrameToServer(blob) {
  const url = serverUrlInput.value || "/predict-file";
  const fd = new FormData();
  fd.append("file", blob, "frame.jpg");
  try {
    const resp = await fetch(url, { method: "POST", body: fd });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    return await resp.json();
  } catch (err) {
    console.error("Upload error", err);
    return { error: err.message || String(err) };
  }
}

function addHistoryItem(imgUrl, label, confidence, saved) {
  const node = document.createElement("div");
  node.className = "item";
  node.innerHTML = `
    <img class="thumb" src="${imgUrl}" />
    <div class="meta">
      <div class="label">${label} <span class="small">(${(confidence*100).toFixed(1)}%)</span></div>
      <div class="small">${new Date().toLocaleString()}</div>
    </div>
    <div>
      ${saved ? `<div class="badge warn">Saved</div>` : `<div class="badge ok">No Save</div>`}
    </div>
  `;
  historyEl.prepend(node);
  while (historyEl.children.length > 50) historyEl.removeChild(historyEl.lastChild);
}

async function doCaptureAndSend() {
  if (!video || video.paused || video.ended) return;
  const blob = await captureFrameBlob(0.8);
  const imgUrl = URL.createObjectURL(blob);
  const res = await sendFrameToServer(blob);

  if (res.error) {
    lastResult.textContent = "Error";
    lastConfidence.textContent = res.error;
    addHistoryItem(imgUrl, "Error", 0, false);
    return;
  }

  lastResult.textContent = res.label;
  lastConfidence.textContent = (res.confidence || 0).toFixed(3);
  addHistoryItem(imgUrl, res.label, res.confidence || 0, !!res.saved_filename);
}

function startAuto() {
  if (running) return;
  running = true;
  doCaptureAndSend();
  const interval = Math.max(200, parseFloat(intervalInput.value || 3) * 1000);
  timerId = setInterval(doCaptureAndSend, interval);
}

function stopAuto() {
  running = false;
  if (timerId) clearInterval(timerId);
  timerId = null;
}

snapBtn.addEventListener("click", () => doCaptureAndSend());
startBtn.addEventListener("click", () => {
  autoToggle.checked = true;
  startAuto();
});
stopBtn.addEventListener("click", () => {
  autoToggle.checked = false;
  stopAuto();
});
autoToggle.addEventListener("change", () => {
  if (autoToggle.checked) startAuto();
  else stopAuto();
});

// Start camera + auto
startCamera().then(() => {
  if (autoToggle.checked) startAuto();
});
