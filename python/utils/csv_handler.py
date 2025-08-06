import pandas as pd
import os
from typing import Dict, List, Optional

class CSVHandler:
    """Handle CSV operations for question management"""
    
    def __init__(self, csv_file: str = 'sample_questions.csv'):
        self.csv_file = csv_file
        self.required_columns = [
            'subject', 'question_type', 'question', 'options', 
            'correct_answer', 'importance', 'diagram_required'
        ]
    
    def load_questions(self) -> pd.DataFrame:
        """Load questions from CSV file"""
        try:
            if os.path.exists(self.csv_file):
                df = pd.read_csv(self.csv_file)
                
                # Ensure all required columns exist
                for col in self.required_columns:
                    if col not in df.columns:
                        df[col] = ''
                
                return df
            else:
                # Create empty dataframe with required columns
                return pd.DataFrame(columns=self.required_columns)
        except Exception as e:
            print(f"Error loading CSV: {str(e)}")
            return pd.DataFrame(columns=self.required_columns)
    
    def save_questions(self, df: pd.DataFrame) -> bool:
        """Save questions to CSV file"""
        try:
            # Ensure all required columns exist
            for col in self.required_columns:
                if col not in df.columns:
                    df[col] = ''
            
            # Reorder columns to match required order
            df = df[self.required_columns]
            
            # Save to CSV
            df.to_csv(self.csv_file, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error saving CSV: {str(e)}")
            return False
    
    def add_question(self, question_data: Dict) -> bool:
        """Add a single question to the CSV"""
        try:
            df = self.load_questions()
            
            # Validate question data
            if not self.validate_question_data(question_data):
                return False
            
            # Add new question
            new_df = pd.concat([df, pd.DataFrame([question_data])], ignore_index=True)
            
            return self.save_questions(new_df)
        except Exception as e:
            print(f"Error adding question: {str(e)}")
            return False
    
    def update_question(self, index: int, question_data: Dict) -> bool:
        """Update a question at specific index"""
        try:
            df = self.load_questions()
            
            if index < 0 or index >= len(df):
                return False
            
            # Validate question data
            if not self.validate_question_data(question_data):
                return False
            
            # Update question
            for key, value in question_data.items():
                if key in self.required_columns:
                    df.loc[index, key] = value
            
            return self.save_questions(df)
        except Exception as e:
            print(f"Error updating question: {str(e)}")
            return False
    
    def delete_question(self, index: int) -> bool:
        """Delete a question at specific index"""
        try:
            df = self.load_questions()
            
            if index < 0 or index >= len(df):
                return False
            
            # Delete question
            df = df.drop(index).reset_index(drop=True)
            
            return self.save_questions(df)
        except Exception as e:
            print(f"Error deleting question: {str(e)}")
            return False
    
    def delete_questions_by_criteria(self, criteria: Dict) -> int:
        """Delete questions matching specific criteria"""
        try:
            df = self.load_questions()
            initial_count = len(df)
            
            # Apply filters
            for key, value in criteria.items():
                if key in df.columns:
                    df = df[df[key] != value]
            
            deleted_count = initial_count - len(df)
            
            if deleted_count > 0:
                self.save_questions(df)
            
            return deleted_count
        except Exception as e:
            print(f"Error deleting questions by criteria: {str(e)}")
            return 0
    
    def get_questions_by_subject(self, subject: str) -> pd.DataFrame:
        """Get all questions for a specific subject"""
        df = self.load_questions()
        return df[df['subject'] == subject]
    
    def get_questions_by_type(self, question_type: str) -> pd.DataFrame:
        """Get all questions of a specific type"""
        df = self.load_questions()
        return df[df['question_type'] == question_type]
    
    def get_questions_by_importance(self, importance: str) -> pd.DataFrame:
        """Get all questions of a specific importance level"""
        df = self.load_questions()
        return df[df['importance'] == importance]
    
    def get_statistics(self) -> Dict:
        """Get statistics about the question database"""
        df = self.load_questions()
        
        if df.empty:
            return {
                'total_questions': 0,
                'subjects': [],
                'question_types': {},
                'importance_levels': {},
                'diagram_questions': 0
            }
        
        stats = {
            'total_questions': len(df),
            'subjects': list(df['subject'].unique()),
            'question_types': df['question_type'].value_counts().to_dict(),
            'importance_levels': df['importance'].value_counts().to_dict(),
            'diagram_questions': len(df[df['diagram_required'] == 'Yes'])
        }
        
        return stats
    
    def validate_question_data(self, question_data: Dict) -> bool:
        """Validate question data before saving"""
        # Check required fields
        required_fields = ['subject', 'question_type', 'question', 'importance']
        
        for field in required_fields:
            if field not in question_data or not question_data[field]:
                return False
        
        # Validate question type
        valid_types = ['MCQ', 'Paragraph', 'Diagram']
        if question_data['question_type'] not in valid_types:
            return False
        
        # Validate importance level
        valid_importance = ['Most Important', 'Important', 'Normal']
        if question_data['importance'] not in valid_importance:
            return False
        
        # Validate diagram required
        valid_diagram = ['Yes', 'No']
        if 'diagram_required' in question_data:
            if question_data['diagram_required'] not in valid_diagram:
                return False
        
        return True
    
    def export_questions(self, filters: Dict = None, filename: str = None) -> str:
        """Export questions to CSV with optional filters"""
        try:
            df = self.load_questions()
            
            # Apply filters if provided
            if filters:
                for key, value in filters.items():
                    if key in df.columns and value != "All":
                        df = df[df[key] == value]
            
            # Generate filename if not provided
            if not filename:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"questions_export_{timestamp}.csv"
            
            # Save filtered data
            df.to_csv(filename, index=False, encoding='utf-8')
            
            return filename
        except Exception as e:
            print(f"Error exporting questions: {str(e)}")
            return None
    
    def import_questions(self, file_path: str, merge: bool = True) -> bool:
        """Import questions from another CSV file"""
        try:
            # Load new questions
            new_df = pd.read_csv(file_path)
            
            # Validate columns
            missing_columns = [col for col in self.required_columns if col not in new_df.columns]
            if missing_columns:
                print(f"Missing required columns: {missing_columns}")
                return False
            
            if merge:
                # Merge with existing questions
                existing_df = self.load_questions()
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                # Replace existing questions
                combined_df = new_df
            
            return self.save_questions(combined_df)
        except Exception as e:
            print(f"Error importing questions: {str(e)}")
            return False
