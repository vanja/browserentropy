function isCanvasSupported() {
    var c = document.createElement("canvas");
    return !!(c.getContext && c.getContext("2d"));
}

function drawOnCanvas() {
    var cEl = document.createElement("canvas");
    cEl.setAttribute("height", "50");
    cEl.setAttribute("width", "400");
    cEl.style.display = "inline";
    var cCtx = cEl.getContext("2d");
    cCtx.textBaseline = "alphabetic";
    cCtx.fillStyle = "#f60";
    cCtx.fillRect(230, 1, 62, 20);
    cCtx.fillStyle = "#069";
    cCtx.font = "12pt invalid-font-42";
    var txt = "Cwm fjord veg balks nth pyx quiz! ,$% \ud83d\ude03";
    cCtx.fillText(txt, 2, 15);
    cCtx.fillStyle = "rgba(102, 204, 0, 0.7)";
    cCtx.font = "14pt Arial";
    cCtx.fillText(txt, 4, 37);
    return cEl.toDataURL();
}

function runCanvasFingerprint() {
  return {"img": isCanvasSupported() ? drawOnCanvas() : "not supported"};
}
