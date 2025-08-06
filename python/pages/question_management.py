import streamlit as st
import pandas as pd
import os
from utils.csv_handler import CSVHandler
from utils.gujarati_text import GujaratiText

def show_question_management():
    """Display question management interface"""
    
    gt = GujaratiText()
    csv_handler = CSVHandler()
    
    st.title("📝 Question Management / પ્રશ્ન વ્યવસ્થાપન")
    
    # Load existing questions
    if os.path.exists('sample_questions.csv'):
        df = pd.read_csv('sample_questions.csv')
    else:
        columns = ['subject', 'question_type', 'question', 'options', 'correct_answer', 'importance', 'diagram_required']
        df = pd.DataFrame(columns=columns)
    
    # Tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Add Question / પ્રશ્ન ઉમેરો",
        "📋 View Questions / પ્રશ્નો જુઓ", 
        "✏️ Edit Questions / પ્રશ્નો સંપાદિત કરો",
        "🗑️ Delete Questions / પ્રશ્નો દૂર કરો"
    ])
    
    with tab1:
        add_question_form(df, csv_handler)
    
    with tab2:
        view_questions(df)
    
    with tab3:
        edit_questions(df, csv_handler)
    
    with tab4:
        delete_questions(df, csv_handler)

def add_question_form(df, csv_handler):
    """Form to add new questions"""
    
    st.header("➕ Add New Question / નવો પ્રશ્ન ઉમેરો")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.selectbox(
            "Subject / વિષય:",
            options=st.session_state.subjects,
            help="Select the subject for this question"
        )
        
        question_type = st.selectbox(
            "Question Type / પ્રશ્ન પ્રકાર:",
            options=["MCQ", "Paragraph", "Diagram"],
            help="Select the type of question"
        )
        
        importance = st.selectbox(
            "Importance Level / મહત્વનું સ્તર:",
            options=["Most Important", "Important", "Normal"],
            help="Select the importance level of this question"
        )
    
    with col2:
        diagram_required = st.selectbox(
            "Diagram Required / આકૃતિ જરૂરી:",
            options=["No", "Yes"],
            help="Does this question require a diagram?"
        )
        
        num_options = 4
        if question_type == "MCQ":
            num_options = st.number_input(
                "Number of Options / વિકલ્પોની સંખ્યા:",
                min_value=2,
                max_value=6,
                value=4
            )
    
    # Question input
    question_text = st.text_area(
        "Question Text / પ્રશ્ન ટેક્સટ:",
        height=100,
        help="Enter the question in Gujarati or English"
    )
    
    # Options for MCQ
    options_text = ""
    correct_answer = ""
    
    if question_type == "MCQ":
        st.subheader("Options / વિકલ્પો:")
        options = []
        for i in range(int(num_options)):
            option = st.text_input(f"Option {chr(65+i)} / વિકલ્પ {chr(65+i)}:")
            if option:
                options.append(f"{chr(65+i)}) {option}")
        
        options_text = ", ".join(options)
        
        if options:
            correct_answer = st.selectbox(
                "Correct Answer / સાચો જવાબ:",
                options=options
            )
    
    elif question_type == "Paragraph":
        correct_answer = st.text_area(
            "Expected Answer / અપેક્ષિત જવાબ:",
            height=100,
            help="Provide the expected answer or key points"
        )
    
    elif question_type == "Diagram":
        diagram_description = st.text_area(
            "Diagram Description / આકૃતિનું વર્ણન:",
            height=60,
            help="Describe what diagram should be drawn"
        )
        correct_answer = st.text_area(
            "Expected Answer / અપેક્ષિત જવાબ:",
            height=100,
            help="Provide the expected answer along with diagram requirements"
        )
    
    # Submit button
    if st.button("Add Question / પ્રશ્ન ઉમેરો", type="primary"):
        if question_text and subject:
            new_question = {
                'subject': subject,
                'question_type': question_type,
                'question': question_text,
                'options': options_text,
                'correct_answer': correct_answer,
                'importance': importance,
                'diagram_required': diagram_required
            }
            
            # Add to dataframe
            new_df = pd.concat([df, pd.DataFrame([new_question])], ignore_index=True)
            
            # Save to CSV
            new_df.to_csv('sample_questions.csv', index=False)
            
            st.success("Question added successfully! / પ્રશ્ન સફળતાપૂર્વક ઉમેર્યો!")
            st.rerun()
        else:
            st.error("Please fill in all required fields / કૃપા કરીને બધા જરૂરી ફીલ્ડ્સ ભરો")

def view_questions(df):
    """Display all questions in a table"""
    
    st.header("📋 All Questions / બધા પ્રશ્નો")
    
    if df.empty:
        st.info("No questions available. Add some questions first. / કોઈ પ્રશ્નો ઉપલબ્ધ નથી. પહેલા કેટલાક પ્રશ્નો ઉમેરો.")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        subject_filter = st.selectbox(
            "Filter by Subject / વિષય દ્વારા ફિલ્ટર:",
            options=["All"] + list(df['subject'].unique())
        )
    
    with col2:
        type_filter = st.selectbox(
            "Filter by Type / પ્રકાર દ્વારા ફિલ્ટર:",
            options=["All"] + list(df['question_type'].unique())
        )
    
    with col3:
        importance_filter = st.selectbox(
            "Filter by Importance / મહત્વ દ્વારા ફિલ્ટર:",
            options=["All"] + list(df['importance'].unique())
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if subject_filter != "All":
        filtered_df = filtered_df[filtered_df['subject'] == subject_filter]
    
    if type_filter != "All":
        filtered_df = filtered_df[filtered_df['question_type'] == type_filter]
    
    if importance_filter != "All":
        filtered_df = filtered_df[filtered_df['importance'] == importance_filter]
    
    # Display statistics
    st.metric("Total Questions / કુલ પ્રશ્નો", len(filtered_df))
    
    # Display questions
    if not filtered_df.empty:
        # Create a display dataframe with limited columns
        display_df = filtered_df[['subject', 'question_type', 'question', 'importance']].copy()
        display_df['question'] = display_df['question'].str[:100] + "..."  # Truncate long questions
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Download filtered questions as CSV
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Questions / ફિલ્ટર્ડ પ્રશ્નો ડાઉનલોડ કરો",
            data=csv_data,
            file_name=f"filtered_questions_{subject_filter}_{type_filter}.csv",
            mime="text/csv"
        )
    else:
        st.info("No questions match the current filters / વર્તમાન ફિલ્ટર્સ સાથે કોઈ પ્રશ્નો મેળ ખાતા નથી")

def edit_questions(df, csv_handler):
    """Interface to edit existing questions"""
    
    st.header("✏️ Edit Questions / પ્રશ્નો સંપાદિત કરો")
    
    if df.empty:
        st.info("No questions available to edit. / સંપાદિત કરવા માટે કોઈ પ્રશ્નો ઉપલબ્ધ નથી.")
        return
    
    # Select question to edit
    question_options = []
    for idx, row in df.iterrows():
        preview = f"{row['subject']} - {row['question'][:50]}..."
        question_options.append((idx, preview))
    
    selected_idx = st.selectbox(
        "Select Question to Edit / સંપાદિત કરવા માટે પ્રશ્ન પસંદ કરો:",
        options=[idx for idx, _ in question_options],
        format_func=lambda x: next(preview for idx, preview in question_options if idx == x)
    )
    
    if selected_idx is not None:
        question_data = df.iloc[selected_idx]
        
        # Edit form
        with st.form("edit_question_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_subject = st.selectbox(
                    "Subject / વિષય:",
                    options=st.session_state.subjects,
                    index=st.session_state.subjects.index(question_data['subject']) if question_data['subject'] in st.session_state.subjects else 0
                )
                
                new_question_type = st.selectbox(
                    "Question Type / પ્રશ્ન પ્રકાર:",
                    options=["MCQ", "Paragraph", "Diagram"],
                    index=["MCQ", "Paragraph", "Diagram"].index(question_data['question_type'])
                )
                
                new_importance = st.selectbox(
                    "Importance Level / મહત્વનું સ્તર:",
                    options=["Most Important", "Important", "Normal"],
                    index=["Most Important", "Important", "Normal"].index(question_data['importance'])
                )
            
            with col2:
                new_diagram_required = st.selectbox(
                    "Diagram Required / આકૃતિ જરૂરી:",
                    options=["No", "Yes"],
                    index=["No", "Yes"].index(question_data['diagram_required'])
                )
            
            new_question_text = st.text_area(
                "Question Text / પ્રશ્ન ટેક્સટ:",
                value=question_data['question'],
                height=100
            )
            
            new_options = st.text_input(
                "Options (for MCQ) / વિકલ્પો (MCQ માટે):",
                value=question_data['options'] if pd.notna(question_data['options']) else ""
            )
            
            new_correct_answer = st.text_area(
                "Correct Answer / સાચો જવાબ:",
                value=question_data['correct_answer'] if pd.notna(question_data['correct_answer']) else "",
                height=100
            )
            
            if st.form_submit_button("Update Question / પ્રશ્ન અપડેટ કરો"):
                # Update the question
                df.loc[selected_idx, 'subject'] = new_subject
                df.loc[selected_idx, 'question_type'] = new_question_type
                df.loc[selected_idx, 'question'] = new_question_text
                df.loc[selected_idx, 'options'] = new_options
                df.loc[selected_idx, 'correct_answer'] = new_correct_answer
                df.loc[selected_idx, 'importance'] = new_importance
                df.loc[selected_idx, 'diagram_required'] = new_diagram_required
                
                # Save to CSV
                df.to_csv('sample_questions.csv', index=False)
                
                st.success("Question updated successfully! / પ્રશ્ન સફળતાપૂર્વક અપડેટ કર્યો!")
                st.rerun()

def delete_questions(df, csv_handler):
    """Interface to delete questions"""
    
    st.header("🗑️ Delete Questions / પ્રશ્નો દૂર કરો")
    
    if df.empty:
        st.info("No questions available to delete. / દૂર કરવા માટે કોઈ પ્રશ્નો ઉપલબ્ધ નથી.")
        return
    
    # Bulk delete options
    st.subheader("Bulk Delete / બલ્ક ડિલીટ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        delete_subject = st.selectbox(
            "Delete all questions from subject / વિષયમાંથી બધા પ્રશ્નો દૂર કરો:",
            options=["None"] + list(df['subject'].unique())
        )
    
    with col2:
        delete_importance = st.selectbox(
            "Delete all questions with importance / મહત્વ સાથેના બધા પ્રશ્નો દૂર કરો:",
            options=["None"] + list(df['importance'].unique())
        )
    
    if delete_subject != "None":
        count = len(df[df['subject'] == delete_subject])
        if st.button(f"Delete {count} questions from {delete_subject} / {delete_subject} માંથી {count} પ્રશ્નો દૂર કરો"):
            df_filtered = df[df['subject'] != delete_subject]
            df_filtered.to_csv('sample_questions.csv', index=False)
            st.success(f"Deleted {count} questions from {delete_subject}!")
            st.rerun()
    
    if delete_importance != "None":
        count = len(df[df['importance'] == delete_importance])
        if st.button(f"Delete {count} {delete_importance} questions / {count} {delete_importance} પ્રશ્નો દૂર કરો"):
            df_filtered = df[df['importance'] != delete_importance]
            df_filtered.to_csv('sample_questions.csv', index=False)
            st.success(f"Deleted {count} {delete_importance} questions!")
            st.rerun()
    
    # Individual delete
    st.subheader("Delete Individual Questions / વ્યક્તિગત પ્રશ્નો દૂર કરો")
    
    # Multi-select for individual questions
    question_options = []
    for idx, row in df.iterrows():
        preview = f"{row['subject']} - {row['question'][:50]}..."
        question_options.append((idx, preview))
    
    selected_indices = st.multiselect(
        "Select Questions to Delete / દૂર કરવા માટે પ્રશ્નો પસંદ કરો:",
        options=[idx for idx, _ in question_options],
        format_func=lambda x: next(preview for idx, preview in question_options if idx == x)
    )
    
    if selected_indices:
        if st.button(f"Delete {len(selected_indices)} Selected Questions / પસંદ કરેલા {len(selected_indices)} પ્રશ્નો દૂર કરો"):
            df_filtered = df.drop(selected_indices)
            df_filtered.to_csv('sample_questions.csv', index=False)
            st.success(f"Deleted {len(selected_indices)} questions!")
            st.rerun()
