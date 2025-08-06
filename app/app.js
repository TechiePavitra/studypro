function loadTab(tabName) {
  const tab = document.getElementById('tab-content');
  if (tabName === 'home') {
    tab.innerHTML = `
      <h2>📌 Welcome to StudyPro</h2>
      <p>Select a tab to begin...</p>
    `;
  } else {
    fetch(tabName)
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch");
        return res.text();
      })
      .then(html => tab.innerHTML = html)
      .catch(err => tab.innerHTML = `<p style="color:red">Error loading tab: ${err.message}</p>`);
  }
}
