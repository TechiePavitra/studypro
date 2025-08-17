# StudyPro

Lightweight, modern, mobile-ready question paper generator for GSEB 12th (Gujarati Medium).  
- Minimal rounded UI + animations
- Question Manager with **bold/italic/underline** (Markdown-compatible)
- PDF Importer with selectable text (PDF.js)
- Auto-load questions from GitHub `database` branch for subjects
- Exam-style PDF with horizontal line and Rasa font support (swap `/fonts/NotoSansGujarati-Regular.ttf` with your Rasa font)
- Dashboard (last tab) with charts
- Computer subject => MCQ-only paper

## File structure
```
app/
  styles.css
  webapp.js
assets/
  icon.png
  IconLicence.txt
data/
  sample_economics.csv
fonts/
  NotoSansGujarati-Regular.ttf   # replace this with Rasa font file
index.html
README.md
```

## Notes
- CSV header: `question,type,options,rarity,section,subject`
- Export uses UTF‑8 BOM for Gujarati compatibility.
- GitHub DB loads async (after first paint) for fast initial UI.
