// StudyPro - webapp.js
// Structure kept: app/, assets/, data/, fonts/
// No emojis; inline SVG only. Dashboard last. Rasa font-ready.

const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/TechiePavitra/studypro/database';
const SUBJECTS = ['economics','gujarati','sanskrit','english','psychology','philosophy','computer'];

const els = {
  // nav
  navBtns: null, panels: null,
  // csv
  csvInput: null, btnImportCSV: null, btnExportCSV: null,
  // manager
  subjectSelect: null, typeSelect: null, raritySelect: null, sectionSelect: null,
  questionText: null, mcqOptions: null, optA:null,optB:null,optC:null,optD:null,
  addQuestionBtn: null, viewAllBtn: null, preview: null,
  // generator
  generateBtn: null, paperSubject:null, paperMarks:null, paperDuration:null, paperDate:null, includeRarity:null,
  // importer
  pdfFileInput:null, pdfViewerContainer:null, addSelectedTextBtn:null,
  // all modal
  allModal:null, closeAllModal:null, allList:null, searchAll:null,
  // dashboard
  papersCount:null, questionsCount:null, papersChart:null, questionsChart:null,
};

const state = {
  questions: [],
  stats: {
    papersGenerated: Number(localStorage.getItem('papersGenerated')||0),
    questionsAdded: Number(localStorage.getItem('questionsAdded')||0),
    papersTimeline: JSON.parse(localStorage.getItem('papersTimeline')||'[]'),
    questionsTimeline: JSON.parse(localStorage.getItem('questionsTimeline')||'[]'),
  },
  loadedFromGithub: false,
};

document.addEventListener('DOMContentLoaded', () => {
  bindEls();
  setupNav();
  setupManager();
  setupCSV();
  setupImporter();
  setupGenerator();
  setupModal();
  // initial panel = Manager for speed
  document.querySelector('.nav-btn[data-target="manager"]').classList.add('active');
  document.getElementById('manager').classList.add('active');
  // defer DB load so first paint is quick
  setTimeout(autoFetchDatabase, 50);
  // init charts after a tick
  setTimeout(initCharts, 200);
  renderPreview();
  updateCountsUI();
});

function bindEls(){
  els.navBtns = document.querySelectorAll('.nav-btn');
  els.panels = document.querySelectorAll('.panel');
  els.csvInput = document.getElementById('csvInput');
  els.btnImportCSV = document.getElementById('btnImportCSV');
  els.btnExportCSV = document.getElementById('btnExportCSV');

  els.subjectSelect = document.getElementById('subjectSelect');
  els.typeSelect = document.getElementById('typeSelect');
  els.raritySelect = document.getElementById('raritySelect');
  els.sectionSelect = document.getElementById('sectionSelect');
  els.questionText = document.getElementById('questionText');
  els.mcqOptions = document.getElementById('mcqOptions');
  els.optA = document.getElementById('optA');
  els.optB = document.getElementById('optB');
  els.optC = document.getElementById('optC');
  els.optD = document.getElementById('optD');
  els.addQuestionBtn = document.getElementById('addQuestionBtn');
  els.viewAllBtn = document.getElementById('viewAllBtn');
  els.preview = document.getElementById('preview');

  els.generateBtn = document.getElementById('generateBtn');
  els.paperSubject = document.getElementById('paperSubject');
  els.paperMarks = document.getElementById('paperMarks');
  els.paperDuration = document.getElementById('paperDuration');
  els.paperDate = document.getElementById('paperDate');
  els.includeRarity = document.getElementById('includeRarity');

  els.pdfFileInput = document.getElementById('pdfFileInput');
  els.pdfViewerContainer = document.getElementById('pdfViewerContainer');
  els.addSelectedTextBtn = document.getElementById('addSelectedTextBtn');

  els.allModal = document.getElementById('allModal');
  els.closeAllModal = document.getElementById('closeAllModal');
  els.allList = document.getElementById('allList');
  els.searchAll = document.getElementById('searchAll');

  els.papersCount = document.getElementById('papersCount');
  els.questionsCount = document.getElementById('questionsCount');
}

function setupNav(){
  els.navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      els.navBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const target = btn.dataset.target;
      els.panels.forEach(p => p.classList.remove('active'));
      document.getElementById(target).classList.add('active');
    });
  });
}

function setupManager(){
  els.typeSelect.addEventListener('change', () => {
    els.mcqOptions.style.display = els.typeSelect.value === 'mcq' ? '' : 'none';
  });
  document.querySelectorAll('.tbtn').forEach(tb => {
    tb.addEventListener('click', () => {
      const wrap = tb.dataset.wrap || '';
      const ta = els.questionText;
      const s = ta.selectionStart, e = ta.selectionEnd;
      const before = ta.value.slice(0,s);
      const sel = ta.value.slice(s,e);
      const after = ta.value.slice(e);
      ta.value = before + wrap + sel + wrap + after;
      ta.focus();
      ta.selectionStart = s + wrap.length; ta.selectionEnd = e + wrap.length;
    });
  });
  els.addQuestionBtn.addEventListener('click', () => {
    const qtxt = (els.questionText.value || '').trim();
    if(!qtxt) return alert('Write a question first');
    const type = els.typeSelect.value;
    const options = type==='mcq' ? [els.optA.value,els.optB.value,els.optC.value,els.optD.value].join(',') : '';
    const q = {
      question: qtxt,
      type, options,
      rarity: els.raritySelect.value,
      section: els.sectionSelect.value,
      subject: els.subjectSelect.value
    };
    state.questions.push(q);
    bumpQuestionsStat();
    els.questionText.value=''; els.optA.value=els.optB.value=els.optC.value=els.optD.value='';
    renderPreview();
    alert('Question added');
  });
  document.getElementById('viewAllBtn').addEventListener('click', openAllModal);
}

function setupCSV(){
  els.btnImportCSV.addEventListener('click', () => els.csvInput.click());
  els.csvInput.addEventListener('change', (e) => {
    const f = e.target.files[0]; if(!f) return;
    Papa.parse(f, {header:true, skipEmptyLines:true, complete: res => {
      let added=0;
      (res.data||[]).forEach(row => {
        if(row.question){
          state.questions.push(normalizeRow(row));
          added++;
        }
      });
      if(added){ bumpQuestionsStat(added); renderPreview(); }
      alert(`Imported ${added} questions`);
    }});
  });
  els.btnExportCSV.addEventListener('click', () => {
    if(!state.questions.length) return alert('No questions to export');
    const csv = Papa.unparse(state.questions, {quotes:true, quoteChar:'"', escapeChar:'"', newline:'\r\n'});
    const BOM = '\uFEFF';
    const blob = new Blob([BOM + csv], {type:'text/csv;charset=utf-8;'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href=url; a.download='questions.csv'; a.click();
    URL.revokeObjectURL(url);
  });
}

function normalizeRow(row){
  return {
    question: (row.question||'').toString(),
    type: (row.type||'paragraph').toString().toLowerCase(),
    options: (row.options||'').toString(),
    rarity: (row.rarity||'common').toString().toLowerCase(),
    section: (row.section||'A').toString().toUpperCase(),
    subject: (row.subject||'').toString() || guessSubjectFromContext()
  };
}
function guessSubjectFromContext(){ return els.subjectSelect ? els.subjectSelect.value : 'General'; }

function setupImporter(){
  els.pdfFileInput.addEventListener('change', async (e) => {
    const f = e.target.files[0]; if(!f) return;
    const buf = await f.arrayBuffer();
    renderPDF(buf, els.pdfViewerContainer);
  });
  els.addSelectedTextBtn.addEventListener('click', () => {
    const sel = window.getSelection().toString().trim();
    if(!sel) return alert('Select text in the PDF first');
    els.questionText.value = sel;
    els.typeSelect.value = 'paragraph';
    els.mcqOptions.style.display = 'none';
    alert('Selected text added to Question box');
  });
}

async function renderPDF(arrayBuffer, container){
  container.innerHTML = '';
  const pdf = await pdfjsLib.getDocument({data: arrayBuffer}).promise;
  for(let i=1;i<=pdf.numPages;i++){
    const page = await pdf.getPage(i);
    const viewport = page.getViewport({scale:1.2});
    const wrap = document.createElement('div');
    wrap.style.position='relative'; wrap.style.marginBottom='10px';
    const canvas = document.createElement('canvas');
    canvas.width = viewport.width; canvas.height = viewport.height; canvas.style.width='100%';
    const ctx = canvas.getContext('2d');
    await page.render({canvasContext:ctx, viewport}).promise;
    const textContent = await page.getTextContent();
    const textLayerDiv = document.createElement('div');
    Object.assign(textLayerDiv.style, {position:'absolute', left:0, top:0, right:0, bottom:0, pointerEvents:'auto'});
    wrap.appendChild(canvas); wrap.appendChild(textLayerDiv); container.appendChild(wrap);
    pdfjsLib.renderTextLayer({textContent, container:textLayerDiv, viewport, textDivs: []});
  }
  container.scrollTop = 0;
}

function setupModal(){
  els.closeAllModal.addEventListener('click', ()=> els.allModal.style.display='none');
  els.searchAll.addEventListener('input', listAll);
}
function openAllModal(){ els.allModal.style.display='flex'; listAll(); }
function listAll(){
  const term = (els.searchAll.value||'').toLowerCase();
  els.allList.innerHTML='';
  const items = state.questions.filter(q => !term || JSON.stringify(q).toLowerCase().includes(term));
  if(!items.length){ els.allList.innerHTML = '<div class="muted">No questions yet.</div>'; return; }
  items.forEach((q,i) => {
    const d = document.createElement('div');
    d.className='q-item';
    d.innerHTML = `<div>${i+1}. ${q.question}</div><div class="meta">${q.subject} • ${q.type.toUpperCase()} • Section ${q.section} • ${q.rarity}</div>`;
    els.allList.appendChild(d);
  });
}

function setupGenerator(){
  els.generateBtn.addEventListener('click', async () => {
    if(!state.questions.length) return alert('No questions available');
    const subject = (els.paperSubject.value||'').trim() || 'GSEB Class 12';
    const marks = els.paperMarks.value || '100';
    const duration = els.paperDuration.value || '3';
    const dateStr = els.paperDate.value || new Date().toISOString().slice(0,10);

    let qs = state.questions.slice();
    const rarity = els.includeRarity.value;
    if(rarity !== 'all') qs = qs.filter(q => (q.rarity||'').toLowerCase() === rarity);

    const isComputer = subject.toLowerCase() === 'computer';
    if(isComputer){
      qs = qs.filter(q => q.type === 'mcq');
      if(!qs.length) return alert('Computer paper requires MCQs – none available.');
    }

    const grouped = {};
    qs.forEach(q => { const s=(q.section||'A').toUpperCase(); (grouped[s] ||= []).push(q); });

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({unit:'pt', format:'a4'});
    const w = doc.internal.pageSize.getWidth();
    const h = doc.internal.pageSize.getHeight();

    // Always use Rasa font
    try{
    const base64 = arrayBufferToBase64(new Uint8Array(buf));
    doc.addFileToVFS('Rasa-Regular.ttf', base64);
    // Force Unicode (CID) encoding
    doc.addFont('Rasa-Regular.ttf', 'Rasa', 'normal', 'Identity-H');
    doc.setFont('Rasa');

    }catch{}

    let y = 64;
    doc.setFontSize(18);
    doc.text('Gujarat Secondary and Higher Secondary Education Board', w/2, y, {align:'center'});
    y += 22;
    doc.setFontSize(15);
    doc.text(subject.toUpperCase(), w/2, y, {align:'center'});
    y += 8;
    doc.setLineWidth(0.8); doc.line(40, y, w-40, y); y += 16;

    doc.setFontSize(11);
    doc.text(`Date: ${formatDate(dateStr)}`, 40, y);
    doc.text(`Time: ${duration} Hours`, w/2, y, {align:'center'});
    doc.text(`Total Marks: ${marks}`, w-40, y, {align:'right'});
    y += 22;

    doc.setFontSize(10);
    const inst = [
      '• Read all questions carefully.',
      isComputer ? '• This paper contains only MCQs.' : '• Answer all questions.'
    ];
    doc.text(inst, 48, y); y += inst.length*14 + 6;

    let qn = 1;
    for(const sec of Object.keys(grouped).sort()){
      doc.setFontSize(12);
      doc.text(`Section ${sec}`, w/2, y, {align:'center'});
      y += 14;
      doc.setFontSize(11);
      for(const q of grouped[sec]){
        const cleanQ = (q.question||'').replace(/\((?:most|common|rare)[^\)]*\)/ig,'').replace(/\b(most\s*imp)\b/ig,'').trim();
        const lines = doc.splitTextToSize(`${qn}. ${cleanQ}`, w-88);
        if (y + lines.length*14 > h - 64){ doc.addPage(); y = 64; }
        doc.text(lines, 48, y); y += lines.length*14;

        if(q.type==='mcq' && q.options){
          const opts = q.options.split(',').map(s=>s.trim()).filter(Boolean);
          for(let i=0;i<opts.length;i++){
            const line = doc.splitTextToSize(`(${String.fromCharCode(65+i)}) ${opts[i]}`, w-108);
            if (y + line.length*14 > h - 64){ doc.addPage(); y = 64; }
            doc.text(line, 68, y); y += line.length*14;
          }
        }else if(q.type==='diagram'){
          if (y + 18 > h - 64){ doc.addPage(); y = 64; }
          doc.text('(Draw a neat labelled diagram.)', 68, y); y += 18;
        }
        y += 8; qn++;
      }
      y += 6;
    }
    doc.save(`${subject.replace(/\s+/g,'_')}_paper.pdf`);
    bumpPapersStat();
    updateCountsUI();
  });
}

function arrayBufferToBase64(buf){
  let binary=''; for(let i=0;i<buf.length;i++) binary += String.fromCharCode(buf[i]); return btoa(binary);
}
function formatDate(s){ try{ const d=new Date(s); return d.toLocaleDateString(); }catch{ return s; }}

async function autoFetchDatabase(){
  if(state.loadedFromGithub) return; state.loadedFromGithub = true;
  let added = 0;
  for(const subj of SUBJECTS){
    const url = `${GITHUB_RAW_BASE}/${subj}/questions.csv`;
    try{
      const res = await fetch(url, {cache:'no-store'});
      if(!res.ok) continue;
      const txt = await res.text();
      const parsed = Papa.parse(txt, {header:true});
      (parsed.data||[]).forEach(row => {
        if(row.question){
          state.questions.push(normalizeRow({...row, subject: subj[0].toUpperCase()+subj.slice(1)}));
          added++;
        }
      });
    }catch(e){ console.warn('DB fetch error', e); }
  }
  if(added){ bumpQuestionsStat(added); renderPreview(); }
}

function renderPreview(){
  const byS = {};
  state.questions.forEach(q => byS[q.subject] = (byS[q.subject]||0)+1);
  const parts = Object.entries(byS).map(([s,c])=>`${s}: ${c}`);
  els.preview.textContent = `${state.questions.length} questions · ${parts.join(' · ')}`;
}

// ---------- Dashboard ----------
let papersChart, questionsChart;
function initCharts(){
  const pc = document.getElementById('papersChart');
  const qc = document.getElementById('questionsChart');
  if(!pc || !qc || !window.Chart) return;
  const t1 = state.stats.papersTimeline;
  const t2 = state.stats.questionsTimeline;
  papersChart = new Chart(pc, { type:'line',
    data:{ labels:t1.map(x=>x.d), datasets:[{label:'Papers', data:t1.map(x=>x.v)}] },
    options:{responsive:true, maintainAspectRatio:false}
  });
  questionsChart = new Chart(qc, { type:'bar',
    data:{ labels:t2.map(x=>x.d), datasets:[{label:'Questions', data:t2.map(x=>x.v)}] },
    options:{responsive:true, maintainAspectRatio:false}
  });
}
function updateCountsUI(){
  els.papersCount.textContent = state.stats.papersGenerated;
  els.questionsCount.textContent = state.stats.questionsAdded;
  if(papersChart) papersChart.update();
  if(questionsChart) questionsChart.update();
}
function bumpPapersStat(){
  state.stats.papersGenerated++;
  addTimelinePoint(state.stats.papersTimeline);
  saveStats();
}
function bumpQuestionsStat(n=1){
  state.stats.questionsAdded += n;
  addTimelinePoint(state.stats.questionsTimeline, n);
  saveStats();
}
function addTimelinePoint(arr, inc=1){
  const today = new Date().toISOString().slice(0,10);
  const last = arr[arr.length-1];
  if(last && last.d===today){ last.v += inc; } else { arr.push({d:today, v:inc}); }
}
function saveStats(){
  localStorage.setItem('papersGenerated', state.stats.papersGenerated);
  localStorage.setItem('questionsAdded', state.stats.questionsAdded);
  localStorage.setItem('papersTimeline', JSON.stringify(state.stats.papersTimeline));
  localStorage.setItem('questionsTimeline', JSON.stringify(state.stats.questionsTimeline));
}
