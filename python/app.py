import streamlit as st
import pandas as pd
import os
from utils.gujarati_text import GujaratiText
from utils.csv_handler import CSVHandler

# Page configuration
st.set_page_config(
    page_title="StudyPro - GSEB 12th Study Material Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Gujarati text helper
gt = GujaratiText()

# Initialize session state
if 'questions_df' not in st.session_state:
    st.session_state.questions_df = pd.DataFrame()
if 'subjects' not in st.session_state:
    st.session_state.subjects = []
if 'csv_handler' not in st.session_state:
    st.session_state.csv_handler = CSVHandler()

def load_subjects():
    """Load subjects from subjects.txt file"""
    try:
        if os.path.exists('subjects.txt'):
            with open('subjects.txt', 'r', encoding='utf-8') as f:
                subjects = [line.strip() for line in f.readlines() if line.strip()]
                st.session_state.subjects = subjects
        else:
            # Create default subjects file
            default_subjects = [
                "ગુજરાતી (Gujarati)",
                "અંગ્રેજી (English)", 
                "ગણિત (Mathematics)",
                "ભૌતિકશાસ્ત્ર (Physics)",
                "રસાયણશાસ્ત્ર (Chemistry)",
                "જીવવિજ્ઞાન (Biology)",
                "ઇતિહાસ (History)",
                "ભૂગોળ (Geography)",
                "અર્થશાસ્ત્ર (Economics)",
                "રાજકારણ (Political Science)"
            ]
            with open('subjects.txt', 'w', encoding='utf-8') as f:
                for subject in default_subjects:
                    f.write(f"{subject}\n")
            st.session_state.subjects = default_subjects
    except Exception as e:
        st.error(f"Error loading subjects: {str(e)}")

def main():
    # Load subjects on startup
    load_subjects()
    
    # Header
    st.title("📚 StudyPro - GSEB 12th Study Material Generator")
    st.markdown("### ગુજરાત માધ્યમિક અને ઉચ્ચતર માધ્યમિક શિક્ષણ બોર્ડ માટે અભ્યાસ સામગ્રી જનરેટર")
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation / નેવિગેશન")
    
    page = st.sidebar.selectbox(
        "Select Page / પેજ પસંદ કરો:",
        [
            "🏠 Home / હોમ",
            "📝 Question Management / પ્રશ્ન વ્યવસ્થાપન", 
            "📄 Paper Generator / પેપર જનરેટર",
            "🔍 Question Scanner / પ્રશ્ન સ્કેનર"
        ]
    )
    
    # Main content based on selected page
    if page == "🏠 Home / હોમ":
        show_home()
    elif page == "📝 Question Management / પ્રશ્ન વ્યવસ્થાપન":
        import pages.question_management as qm
        qm.show_question_management()
    elif page == "📄 Paper Generator / પેપર જનરેટર":
        import pages.paper_generator as pg
        pg.show_paper_generator()
    elif page == "🔍 Question Scanner / પ્રશ્ન સ્કેનર":
        import pages.question_scanner as qs
        qs.show_question_scanner()

def show_home():
    """Display home page with overview and quick stats"""
    
    # Welcome section
    st.header("🎓 Welcome to StudyPro / StudyPro માં આપનું સ્વાગત છે")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌟 Features / લક્ષણો:
        - **Question Management** / પ્રશ્ન વ્યવસ્થાપન
        - **Automated Paper Generation** / સ્વચાલિત પેપર જનરેશન
        - **PDF Export** / PDF નિકાસ
        - **Gujarati Language Support** / ગુજરાતી ભાષા સપોર્ટ
        - **Question Importance Levels** / પ્રશ્ન મહત્વના સ્તરો
        - **Subject-wise Organization** / વિષય પ્રમાણે સંગઠન
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Quick Stats / ઝડપી આંકડા:
        """)
        
        # Load and display stats
        try:
            if os.path.exists('sample_questions.csv'):
                df = pd.read_csv('sample_questions.csv')
                st.metric("Total Questions / કુલ પ્રશ્નો", len(df))
                st.metric("Available Subjects / ઉપલબ્ધ વિષયો", len(st.session_state.subjects))
                
                if 'importance' in df.columns:
                    important_count = len(df[df['importance'] == 'Most Important'])
                    st.metric("Most Important Questions / સૌથી મહત્વપૂર્ણ પ્રશ્નો", important_count)
            else:
                st.info("No questions database found. Please upload or create questions.")
        except Exception as e:
            st.error(f"Error loading statistics: {str(e)}")
    
    # Quick actions
    st.header("⚡ Quick Actions / ઝડપી ક્રિયાઓ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Add Questions / પ્રશ્નો ઉમેરો", use_container_width=True):
            st.switch_page("pages/question_management.py")
    
    with col2:
        if st.button("📄 Generate Paper / પેપર બનાવો", use_container_width=True):
            st.switch_page("pages/paper_generator.py")
    
    with col3:
        if st.button("🔍 Scan Questions / પ્રશ્નો સ્કેન કરો", use_container_width=True):
            st.switch_page("pages/question_scanner.py")
    
    # CSV Upload section
    st.header("📤 Upload Question Database / પ્રશ્ન ડેટાબેસ અપલોડ કરો")
    
    uploaded_file = st.file_uploader(
        "Choose CSV file / CSV ફાઇલ પસંદ કરો:",
        type=['csv'],
        help="Upload a CSV file containing questions with columns: subject, question_type, question, options, correct_answer, importance, diagram_required"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validate required columns
            required_columns = ['subject', 'question_type', 'question', 'importance']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
            else:
                # Save the uploaded file
                df.to_csv('sample_questions.csv', index=False)
                st.session_state.questions_df = df
                st.success(f"Successfully uploaded {len(df)} questions! / સફળતાપૂર્વક {len(df)} પ્રશ્નો અપલોડ કર્યા!")
                st.rerun()
        except Exception as e:
            st.error(f"Error uploading file: {str(e)}")
    
    # Instructions
    st.header("📖 How to Use / કેવી રીતે ઉપયોગ કરવો")
    
    with st.expander("📋 CSV Format Instructions / CSV ફોર્મેટ સૂચનાઓ"):
        st.markdown("""
        Your CSV file should contain the following columns:
        
        | Column | Description | Example |
        |--------|-------------|---------|
        | subject | Subject name | ગણિત |
        | question_type | MCQ, Paragraph, or Diagram | MCQ |
        | question | The question text | What is 2+2? |
        | options | For MCQ (comma-separated) | A) 3, B) 4, C) 5, D) 6 |
        | correct_answer | Correct answer | B) 4 |
        | importance | Most Important, Important, Normal | Most Important |
        | diagram_required | Yes/No | No |
        """)

if __name__ == "__main__":
    main()
