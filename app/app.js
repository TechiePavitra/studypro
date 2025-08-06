function loadTab(tabPath) {
  const container = document.getElementById('tab-content');

  if (tabPath === 'home') {
    container.innerHTML = `
      <h2>📌 Welcome to StudyPro</h2>
      <p>Select a tab to begin…</p>
    `;
    return;
  }

  // Use absolute path including repo name to load from GitHub Pages
  fetch('/studypro/app/' + tabPath)
    .then(res => {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.text();
    })
    .then(html => {
      container.innerHTML = html;
    })
    .catch(err => {
      container.innerHTML = `<p style="color:red;">Error loading tab: ${err.message}</p>`;
    });
}
