(function() {
  const OUT_PATH = "out.txt";
  const POLL_MS = 500;

  const outEl = document.getElementById("out");
  const stampEl = document.getElementById("stamp");
  const copyBtn = document.getElementById("copy");

  let last = "";

  function updateContent(text) {
    if (text === last) return;

    last = text;
    outEl.textContent = text || "[empty]";
    outEl.classList.toggle("empty", !text || text.trim().length === 0);
    stampEl.textContent = new Date().toLocaleTimeString();
    outEl.scrollTop = outEl.scrollHeight;
  }

  function fetchOutFile() {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", OUT_PATH + "?t=" + Date.now(), true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState !== 4) return;
      if (xhr.status === 200 || xhr.status === 0) {
        updateContent(xhr.responseText);
      } else {
        if (!last) {
          updateContent("Waiting for server / out.txt to appear...");
        }
      }
    };
    xhr.send();
  }

  (function loop() {
    try {
      fetchOutFile();
    } catch (e) { }
    setTimeout(loop, POLL_MS);
  })();

  copyBtn.addEventListener("click", function() {
    const text = last || outEl.textContent || "";
    if (!text) return;
    navigator.clipboard
      .writeText(text)
      .then(() => {
        copyBtn.textContent = "Copied";
        setTimeout(() => (copyBtn.textContent = "Copy"), 1200);
      })
      .catch(() => fallbackCopy(text));
  });
})();
