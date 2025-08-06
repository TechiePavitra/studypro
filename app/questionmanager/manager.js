 appquestionmanagermanager.js

const subjectDropdown = document.getElementById(subject);
const sectionDropdown = document.getElementById(section);
const questionList = document.getElementById(questionList);

const subjects = [
  Gujarati, English, Psychology, Philosophy,
  Sanskrit, Computer, Economics
];

 Dynamically populate subject and section dropdowns
window.onload = () = {
  subjects.forEach(sub = {
    const option = document.createElement(option);
    option.value = sub;
    option.text = sub;
    subjectDropdown.appendChild(option);
  });

  for (let i = 0; i  5; i++) {
    const section = String.fromCharCode(65 + i);  A, B, C...
    const option = document.createElement(option);
    option.value = `section_${section.toLowerCase()}`;
    option.text = `Section ${section}`;
    sectionDropdown.appendChild(option);
  }
};

 Load questions from CSV (placeholder - will need Pyodide for actual CSV ops)
function loadQuestions() {
  questionList.innerHTML = `p🔄 CSV loading not yet implemented. Pyodide support needed.p`;
}

 Add a question to the current section
function addQuestion() {
  const text = document.getElementById(questionText).value;
  const type = document.getElementById(questionType).value;
  const rarity = document.getElementById(rarity).value;
  const marks = document.getElementById(marks).value;

  if (!text  !marks) {
    alert(Question text and marks are required.);
    return;
  }

  const item = document.createElement(div);
  item.className = question-item neumorphic;
  item.innerHTML = `
    pstrong${text}strong [${marks}]p
    pType ${type}  Rarity ${rarity}p
    button onclick=this.parentElement.remove() class=neumorphic-button small❌ Removebutton
  `;

  questionList.appendChild(item);

   Clear input
  document.getElementById(questionText).value = ;
  document.getElementById(marks).value = ;
}
