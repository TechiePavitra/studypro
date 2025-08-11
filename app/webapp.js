/* app/webapp.js - v0.1 features:
   - Horizontal line under subject title in generated PDF
   - Fix CSV export bug (explicit headers + BOM)
   - Auto-fetch CSVs from GitHub 'database' branch for configured subjects
   - PDF viewer with selectable text
   - Computer subject MCQ-only enforcement
   - Fix Generate Button
*/

const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/TechiePavitra/studypro/database'; // branch 'database'
const SUBJECTS = ['economics','gujarati','sanskrit','english','psychology','philosophy','computer'];

const state = { questions: [] };

const els = {
  subjectSelect: document.getElementById('subjectSelect'),
  typeSelect: document.getElementById('typeSelect'),
  raritySelect: document.getElementById('raritySelect'),
  sectionSelect: document.getElementById('sectionSelect'),
  questionText: document.getElementById('questionText'),
  mcqOptions: document.getElementById('mcqOptions'),
  optA: document.getElementById('optA'),
  optB: document.getElementById('optB'),
  optC: document.getElementById('optC'),
  optD: document.getElementById('optD'),
  addQuestionBtn: document.getElementById('addQuestionBtn'),
  questionList: document.getElementById('questionList'),
  qcount: document.getElementById('qcount'),
  openPdfViewerBtn: document.getElementById('openPdfViewerBtn'),
  pdfModal: document.getElementById('pdfModal'),
  pdfViewerContainer: document.getElementById('pdfViewerContainer'),
  closePdfModal: document.getElementById('closePdfModal'),
  addSelectedTextBtn: document.getElementById('addSelectedTextBtn'),
  pdfFileInput: document.getElementById('pdfFileInput'),
  csvInput: document.getElementById('csvInput'),
  topCsvInput: document.getElementById('topCsvInput'),
  generateBtn: document.getElementById('generateBtn'),
  paperSubject: document.getElementById('paperSubject'),
  paperMarks: document.getElementById('paperMarks'),
  includeRarity: document.getElementById('includeRarity'),
  preview: document.getElementById('preview')
};

// Other functions like refreshQuestionList, resetForm, addQuestionFromForm, etc.

els.generateBtn.addEventListener('click', async () => {
  console.log("Generate Paper button clicked!");

  if (!state.questions.length) {
    console.error("No questions available.");
    return alert('Add some questions first');
  }

  const filterRarity = els.includeRarity.value;
  const subjectInput = (els.paperSubject.value || '').trim();
  const subjectLower = subjectInput.toLowerCase();
  const selectedSubject = (els.subjectSelect.value || '').toLowerCase();
  const isComputerPaper = subjectLower === 'computer' || selectedSubject === 'computer';
  let questions = state.questions.slice();

  if (filterRarity !== 'all') {
    questions = questions.filter(q => q.rarity === filterRarity);
  }

  if (isComputerPaper) {
    questions = questions.filter(q => q.type === 'mcq');
    if (!questions.length) {
      console.error("No MCQ questions available for Computer subject.");
      return alert('No MCQ questions available for Computer subject.');
    }
  }

  const grouped = {};
  questions.forEach(q => {
    const s = q.section || 'A';
    if (!grouped[s]) grouped[s] = [];
    grouped[s].push(q);
  });

  // Attempt to fetch font and check for fontBuffer
  const fontUrl = '/fonts/NotoSansGujarati-Regular.ttf';
  let fontBuffer = null;
  try {
    fontBuffer = await fetch(fontUrl).then(r => {
      if (!r.ok) throw new Error("Font file not found");
      return r.arrayBuffer();
    });
  } catch (e) {
    console.error("Error fetching font:", e);
    fontBuffer = null;
  }

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: 'pt', format: 'a4' });

  if (fontBuffer) {
    const base64Font = arrayBufferToBase64(new Uint8Array(fontBuffer));
    doc.addFileToVFS('NotoGujarati.ttf', base64Font);
    doc.addFont('NotoGujarati.ttf', 'NotoGujarati', 'normal');
    doc.setFont('NotoGujarati');
  }

  doc.setFontSize(12);
  const pageWidth = doc.internal.pageSize.getWidth();
  let y = 60;
  doc.setFontSize(18);
  doc.text((subjectInput || 'CLASS12').toUpperCase(), pageWidth / 2, y, { align: 'center' });

  // Horizontal line under subject title
  const lineY = y + 6;
  doc.setLineWidth(0.7);
  doc.line(40, lineY, pageWidth - 40, lineY);
  y += 26;

  doc.setFontSize(10);
  const now = new Date().toLocaleString();
  doc.text(`Generated: ${now}`, 40, y);
  doc.text(`Total: ${els.paperMarks.value || '100'} Marks`, pageWidth - 40, y, { align: 'right' });
  y += 24;

  let qNo = 1;
  const sectionKeys = Object.keys(grouped).sort();
  for (const sec of sectionKeys) {
    doc.setFontSize(13);
    doc.text(`Section - ${sec}`, pageWidth / 2, y, { align: 'center' });
    y += 20;
    doc.setFontSize(11);

    for (const q of grouped[sec]) {
      const prefix = `${qNo}. `;
      const lines = doc.splitTextToSize(prefix + q.question + ` (${q.rarity})`, pageWidth - 80);
      doc.text(lines, 40, y);
      y += lines.length * 14;

      if (q.type === 'mcq' && q.options) {
        const opts = q.options.split(',');
        for (let i = 0; i < opts.length; i++) {
          const optLine = `(${String.fromCharCode(65 + i)}) ${opts[i].trim()}`;
          doc.text(optLine, 60, y);
          y += 14;
        }
      } else if (q.type === 'diagram') {
        doc.text('(Draw a diagram for this question)', 60, y);
        y += 16;
      }

      y += 8;
      qNo++;
      if (y > doc.internal.pageSize.getHeight() - 60) {
        doc.addPage();
        y = 60;
      }
    }
  }

  doc.save(`${(subjectInput || 'Class12').replace(/\s+/g, '_')}_paper.pdf`);
});

function arrayBufferToBase64(buffer) {
  let binary = '';
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) binary += String.fromCharCode(bytes[i]);
  return btoa(binary);
}

// Other functions remain unchanged
// Remember to update your other event listeners similarly as required
