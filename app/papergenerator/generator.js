// app/papergenerator/generator.js
function generatePaper() {
  const subject = document.getElementById("subjectSelect").value;
  const checkedSections = Array.from(
    document.querySelectorAll("#sectionCheckboxes input:checked")
  ).map(el => el.value);

  if (!checkedSections.length) {
    alert("Please select at least one section.");
    return;
  }

  let output = `📘 Subject: ${subject.toUpperCase()}\n`;
  output += `📄 Sections: ${checkedSections.join(", ")}\n\n`;
  output += "🔍 Sample questions would appear here...\n";

  document.getElementById("previewArea").innerText = output;

  // TODO: Fetch CSV from data/{subject}/{section}.csv
  // TODO: Display questions grouped by section with marks
  // TODO: Add print to PDF support via Pyodide
}
