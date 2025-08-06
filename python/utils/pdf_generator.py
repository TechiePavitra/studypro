from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import pandas as pd
from datetime import datetime

class PDFGenerator:
    """Generate PDF documents for question papers and answer keys"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_styles()
    
    def setup_styles(self):
        """Setup custom styles for the PDF"""
        
        # Custom styles for different elements
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkgreen,
            fontName='Helvetica-Bold'
        )
        
        self.question_style = ParagraphStyle(
            'QuestionStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leftIndent=20,
            fontName='Helvetica'
        )
        
        self.instruction_style = ParagraphStyle(
            'InstructionStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.darkred,
            fontName='Helvetica-Oblique'
        )
    
    def generate_paper_pdf(self, questions, total_marks, paper_info=None):
        """Generate question paper PDF"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
        
        # Content container
        content = []
        
        # Header
        self.add_header(content, total_marks, paper_info)
        
        # Instructions
        self.add_instructions(content)
        
        # Questions by sections
        self.add_questions_by_sections(content, questions)
        
        # Build PDF
        doc.build(content)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def add_header(self, content, total_marks, paper_info=None):
        """Add header section to the PDF"""
        
        # School/Board name
        board_name = "Gujarat Secondary and Higher Secondary Education Board (GSEB)"
        if paper_info and 'school_name' in paper_info:
            board_name = paper_info['school_name']
        
        content.append(Paragraph(board_name, self.title_style))
        content.append(Spacer(1, 12))
        
        # Paper title
        paper_title = "Question Paper"
        if paper_info and 'paper_title' in paper_info:
            paper_title = paper_info['paper_title']
        
        content.append(Paragraph(paper_title, self.title_style))
        content.append(Spacer(1, 20))
        
        # Paper details table
        paper_details = [
            ['Time Allowed:', paper_info.get('exam_duration', '3 hours') if paper_info else '3 hours',
             'Maximum Marks:', str(total_marks)],
            ['Date:', paper_info.get('exam_date', datetime.now().strftime('%d/%m/%Y')) if paper_info else datetime.now().strftime('%d/%m/%Y'),
             'Subject:', paper_info.get('subject', 'General') if paper_info else 'General']
        ]
        
        table = Table(paper_details, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        content.append(table)
        content.append(Spacer(1, 20))
    
    def add_instructions(self, content):
        """Add general instructions to the PDF"""
        
        content.append(Paragraph("GENERAL INSTRUCTIONS:", self.heading_style))
        
        instructions = [
            "1. Read all questions carefully before attempting.",
            "2. All questions are compulsory.",
            "3. Write your answers clearly and legibly.",
            "4. Use separate answer sheets if required.",
            "5. Check your answers before submitting.",
            "6. સામાન્ય સૂચનાઓ: બધા પ્રશ્નો ફરજિયાત છે અને સ્પષ્ટ લખાણ જરૂરી છે."
        ]
        
        for instruction in instructions:
            content.append(Paragraph(instruction, self.instruction_style))
        
        content.append(Spacer(1, 20))
    
    def add_questions_by_sections(self, content, questions):
        """Add questions organized by sections"""
        
        # Group questions by type
        mcq_questions = [q for q in questions if q['question_type'] == 'MCQ']
        para_questions = [q for q in questions if q['question_type'] == 'Paragraph']
        diagram_questions = [q for q in questions if q['question_type'] == 'Diagram']
        
        # Section A: MCQ Questions
        if mcq_questions:
            content.append(Paragraph("SECTION A: MULTIPLE CHOICE QUESTIONS", self.heading_style))
            content.append(Paragraph("વિભાગ અ: બહુવિકલ્પીય પ્રશ્નો", self.instruction_style))
            content.append(Spacer(1, 10))
            
            total_mcq_marks = sum(q['marks'] for q in mcq_questions)
            content.append(Paragraph(f"[Total Marks: {total_mcq_marks}]", self.instruction_style))
            content.append(Spacer(1, 10))
            
            for i, question in enumerate(mcq_questions, 1):
                self.add_mcq_question(content, i, question)
            
            content.append(Spacer(1, 20))
        
        # Section B: Short Answer Questions
        if para_questions:
            content.append(Paragraph("SECTION B: SHORT ANSWER QUESTIONS", self.heading_style))
            content.append(Paragraph("વિભાગ બ: ટૂંકા જવાબના પ્રશ્નો", self.instruction_style))
            content.append(Spacer(1, 10))
            
            total_para_marks = sum(q['marks'] for q in para_questions)
            content.append(Paragraph(f"[Total Marks: {total_para_marks}]", self.instruction_style))
            content.append(Spacer(1, 10))
            
            for i, question in enumerate(para_questions, 1):
                self.add_paragraph_question(content, i, question)
            
            content.append(Spacer(1, 20))
        
        # Section C: Diagram Questions
        if diagram_questions:
            content.append(Paragraph("SECTION C: DIAGRAM QUESTIONS", self.heading_style))
            content.append(Paragraph("વિભાગ સ: આકૃતિના પ્રશ્નો", self.instruction_style))
            content.append(Spacer(1, 10))
            
            total_diagram_marks = sum(q['marks'] for q in diagram_questions)
            content.append(Paragraph(f"[Total Marks: {total_diagram_marks}]", self.instruction_style))
            content.append(Spacer(1, 10))
            
            for i, question in enumerate(diagram_questions, 1):
                self.add_diagram_question(content, i, question)
    
    def add_mcq_question(self, content, question_num, question):
        """Add an MCQ question to the content"""
        
        question_text = f"{question_num}. {question['question']}"
        content.append(Paragraph(question_text, self.question_style))
        
        if pd.notna(question.get('options')) and question['options']:
            options_text = f"   {question['options']}"
            content.append(Paragraph(options_text, self.question_style))
        
        marks_text = f"[{question['marks']} Mark{'s' if question['marks'] > 1 else ''}]"
        content.append(Paragraph(marks_text, self.instruction_style))
        content.append(Spacer(1, 8))
    
    def add_paragraph_question(self, content, question_num, question):
        """Add a paragraph question to the content"""
        
        question_text = f"{question_num}. {question['question']}"
        content.append(Paragraph(question_text, self.question_style))
        
        marks_text = f"[{question['marks']} Mark{'s' if question['marks'] > 1 else ''}]"
        content.append(Paragraph(marks_text, self.instruction_style))
        content.append(Spacer(1, 12))
    
    def add_diagram_question(self, content, question_num, question):
        """Add a diagram question to the content"""
        
        question_text = f"{question_num}. {question['question']}"
        content.append(Paragraph(question_text, self.question_style))
        
        if question.get('diagram_required') == 'Yes':
            content.append(Paragraph("   (Draw appropriate diagram)", self.instruction_style))
        
        marks_text = f"[{question['marks']} Mark{'s' if question['marks'] > 1 else ''}]"
        content.append(Paragraph(marks_text, self.instruction_style))
        content.append(Spacer(1, 12))
    
    def generate_answer_key_pdf(self, questions):
        """Generate answer key PDF"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
        
        content = []
        
        # Header
        content.append(Paragraph("ANSWER KEY", self.title_style))
        content.append(Paragraph("જવાબ કી", self.instruction_style))
        content.append(Spacer(1, 20))
        
        # Group questions by type
        mcq_questions = [q for q in questions if q['question_type'] == 'MCQ']
        para_questions = [q for q in questions if q['question_type'] == 'Paragraph']
        diagram_questions = [q for q in questions if q['question_type'] == 'Diagram']
        
        # MCQ Answers
        if mcq_questions:
            content.append(Paragraph("SECTION A ANSWERS:", self.heading_style))
            for i, question in enumerate(mcq_questions, 1):
                if pd.notna(question.get('correct_answer')) and question['correct_answer']:
                    answer_text = f"{i}. {question['correct_answer']}"
                    content.append(Paragraph(answer_text, self.question_style))
            content.append(Spacer(1, 15))
        
        # Paragraph Answers
        if para_questions:
            content.append(Paragraph("SECTION B ANSWERS:", self.heading_style))
            for i, question in enumerate(para_questions, 1):
                question_text = f"{i}. {question['question']}"
                content.append(Paragraph(question_text, self.question_style))
                
                if pd.notna(question.get('correct_answer')) and question['correct_answer']:
                    answer_text = f"Answer: {question['correct_answer']}"
                    content.append(Paragraph(answer_text, self.instruction_style))
                content.append(Spacer(1, 10))
        
        # Diagram Answers
        if diagram_questions:
            content.append(Paragraph("SECTION C ANSWERS:", self.heading_style))
            for i, question in enumerate(diagram_questions, 1):
                question_text = f"{i}. {question['question']}"
                content.append(Paragraph(question_text, self.question_style))
                
                if pd.notna(question.get('correct_answer')) and question['correct_answer']:
                    answer_text = f"Answer: {question['correct_answer']}"
                    content.append(Paragraph(answer_text, self.instruction_style))
                content.append(Spacer(1, 10))
        
        # Build PDF
        doc.build(content)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_statistics_pdf(self, stats):
        """Generate statistics report PDF"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
        
        content = []
        
        # Header
        content.append(Paragraph("QUESTION BANK STATISTICS", self.title_style))
        content.append(Paragraph(f"Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.instruction_style))
        content.append(Spacer(1, 20))
        
        # Overall Statistics
        content.append(Paragraph("OVERALL STATISTICS:", self.heading_style))
        content.append(Paragraph(f"Total Questions: {stats['total_questions']}", self.question_style))
        content.append(Paragraph(f"Total Subjects: {len(stats['subjects'])}", self.question_style))
        content.append(Paragraph(f"Questions with Diagrams: {stats['diagram_questions']}", self.question_style))
        content.append(Spacer(1, 15))
        
        # Subject wise breakdown
        if stats['subjects']:
            content.append(Paragraph("SUBJECTS:", self.heading_style))
            for subject in stats['subjects']:
                content.append(Paragraph(f"• {subject}", self.question_style))
            content.append(Spacer(1, 15))
        
        # Question types
        if stats['question_types']:
            content.append(Paragraph("QUESTION TYPES:", self.heading_style))
            for qtype, count in stats['question_types'].items():
                content.append(Paragraph(f"• {qtype}: {count}", self.question_style))
            content.append(Spacer(1, 15))
        
        # Importance levels
        if stats['importance_levels']:
            content.append(Paragraph("IMPORTANCE LEVELS:", self.heading_style))
            for importance, count in stats['importance_levels'].items():
                content.append(Paragraph(f"• {importance}: {count}", self.question_style))
        
        # Build PDF
        doc.build(content)
        
        buffer.seek(0)
        return buffer.getvalue()
