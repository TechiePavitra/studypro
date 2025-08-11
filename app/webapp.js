:root{
  --bg:#f6f7fb; --card:#fff; --muted:#6b7280; --accent:#0ea5a4;
}
*{box-sizing:border-box;font-family:Inter, system-ui, Arial, sans-serif}
body{margin:0;background:var(--bg);color:#111}
.topbar{display:flex;align-items:center;gap:12px;padding:12px 18px;background:linear-gradient(180deg,#fff,#f2f5f8);box-shadow:0 2px 8px rgba(0,0,0,0.06)}
.logo{width:36px;height:36px;border-radius:6px}
.spacer{flex:1}
.split{display:flex;gap:16px;padding:18px;max-width:1200px;margin:20px auto}
.left,.right{background:var(--card);padding:14px;border-radius:12px;box-shadow:0 6px 20px rgba(12,20,30,0.05)}
.left{flex:1;min-width:320px}
.right{flex:0.9;min-width:320px}
.controls{display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap}
textarea#questionText{width:100%;height:120px;border-radius:8px;padding:10px;border:1px solid #e7e9ee;font-size:16px;resize:vertical}
input, select{border-radius:6px;border:1px solid #e7e9ee;padding:8px;font-size:16px}
select{background:var(--card);cursor:pointer}
.mcq-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}
.buttons{display:flex;gap:8px;margin-top:10px}
button{background:var(--accent);border:none;color:#fff;padding:8px 12px;border-radius:10px;cursor:pointer;min-height:44px}
.preview-box{min-height:220px;border:1px dashed #e1e6f0;padding:10px;border-radius:8px}
.question-list{list-style:none;padding:0;margin:0;max-height:360px;overflow:auto}
.question-list li{padding:8px 10px;border-bottom:1px solid #f1f3f6;display:flex;gap:8px;align-items:center}
.question-list li .meta{font-size:12px;color:var(--muted);margin-left:auto}

/* Mobile responsiveness */
@media(max-width:900px){
  .split{flex-direction:column;padding:12px;gap:12px}
  .topbar{flex-wrap:wrap;gap:8px;padding:8px 12px}
  .topbar h1{font-size:18px;margin:0}
  .logo{width:28px;height:28px}
  .controls{flex-direction:column;gap:6px}
  .controls select{width:100%;padding:10px;font-size:16px}
  textarea#questionText{height:100px;font-size:16px}
  .mcq-grid{grid-template-columns:1fr;gap:6px}
  .mcq-grid input{padding:10px;font-size:16px}
  .buttons{flex-direction:column;gap:6px}
  .buttons button{width:100%;padding:12px;font-size:16px}
  button{padding:10px 16px;font-size:16px;min-height:44px}
  .question-list{max-height:250px}
  .question-list li{padding:12px 8px;flex-direction:column;align-items:flex-start;gap:4px}
  .question-list li .meta{margin-left:0;font-size:11px}
  .right label{display:block;margin-bottom:8px}
  .right label input, .right label select{width:100%;padding:10px;font-size:16px;margin-top:4px}
  .preview-box{min-height:120px;font-size:14px}
}

@media(max-width:600px){
  .topbar{padding:6px 8px}
  .topbar button{padding:6px 8px;font-size:14px}
  .split{padding:8px;gap:8px}
  .left,.right{padding:10px}
  .left h2,.right h2{font-size:16px;margin-bottom:12px}
  .left h3,.right h3{font-size:14px;margin:12px 0 8px 0}
  textarea#questionText{height:80px}
  .modal-content{width:95%;padding:8px;max-height:95vh}
  .pdf-viewer-container{height:50vh}
  .modal-footer{flex-direction:column;gap:6px}
  .modal-footer button, .modal-footer input{width:100%}
}

@media(max-width:400px){
  .topbar h1{display:none}
  .topbar{justify-content:space-between}
  .spacer{display:none}
  .controls select{font-size:14px}
  textarea#questionText{font-size:14px}
  .buttons button{font-size:14px;padding:10px}
}

/* modal PDF viewer */
.modal{position:fixed;inset:0;background:rgba(0,0,0,0.45);display:flex;align-items:center;justify-content:center;z-index:9999}
.modal-content{width:90%;max-width:1000px;background:var(--card);border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:8px;max-height:90vh;overflow:hidden}
@media(max-width:600px){
  .modal-content{width:95%;padding:8px;border-radius:8px}
}
.modal-header{display:flex;align-items:center;justify-content:space-between}
.pdf-viewer-container{overflow:auto;background:#fff;padding:8px;border-radius:8px;height:60vh;border:1px solid #e6eef5}
.pdf-page{margin-bottom:10px;position:relative;border:1px solid #f1f3f6;padding:6px}
.pdf-canvas{width:100%;height:auto;display:block}
.pdf-textLayer{position:absolute;left:6px;top:6px;right:6px;bottom:6px;pointer-events:auto}
.modal-footer{display:flex;gap:8px;align-items:center;justify-content:flex-end}
