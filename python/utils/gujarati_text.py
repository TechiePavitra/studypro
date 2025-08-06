class GujaratiText:
    """Handle Gujarati text and translations for the application"""
    
    def __init__(self):
        self.translations = {
            # Navigation
            "home": "હોમ",
            "question_management": "પ્રશ્ન વ્યવસ્થાપન",
            "paper_generator": "પેપર જનરેટર",
            "question_scanner": "પ્રશ્ન સ્કેનર",
            
            # Common UI elements
            "subject": "વિષય",
            "question": "પ્રશ્ન",
            "answer": "જવાબ",
            "marks": "ગુણ",
            "type": "પ્રકાર",
            "importance": "મહત્વ",
            "options": "વિકલ્પો",
            "add": "ઉમેરો",
            "edit": "સંપાદિત કરો",
            "delete": "દૂર કરો",
            "save": "સેવ કરો",
            "cancel": "રદ કરો",
            "submit": "સબમિટ કરો",
            "upload": "અપલોડ કરો",
            "download": "ડાઉનલોડ કરો",
            "generate": "બનાવો",
            "select": "પસંદ કરો",
            "filter": "ફિલ્ટર",
            "search": "શોધો",
            
            # Question types
            "mcq": "બહુવિકલ્પીય",
            "paragraph": "ફકરો",
            "diagram": "આકૃતિ",
            
            # Importance levels
            "most_important": "સૌથી મહત્વપૂર્ણ",
            "important": "મહત્વપૂર્ણ",
            "normal": "સામાન્ય",
            
            # Messages
            "success": "સફળતા",
            "error": "ભૂલ",
            "warning": "ચેતવણી",
            "info": "માહિતી",
            "loading": "લોડ થઈ રહ્યું છે",
            "processing": "પ્રોસેસ થઈ રહ્યું છે",
            "completed": "પૂર્ણ",
            
            # File operations
            "file_uploaded": "ફાઇલ અપલોડ થઈ",
            "file_saved": "ફાઇલ સેવ થઈ",
            "file_not_found": "ફાઇલ મળી નથી",
            "invalid_file": "અયોગ્ય ફાઇલ",
            
            # Question management
            "add_question": "પ્રશ્ન ઉમેરો",
            "edit_question": "પ્રશ્ન સંપાદિત કરો",
            "delete_question": "પ્રશ્ન દૂર કરો",
            "question_added": "પ્રશ્ન ઉમેર્યો",
            "question_updated": "પ્રશ્ન અપડેટ કર્યો",
            "question_deleted": "પ્રશ્ન દૂર કર્યો",
            "no_questions": "કોઈ પ્રશ્નો નથી",
            "question_text": "પ્રશ્ન ટેક્સ્ટ",
            "correct_answer": "સાચો જવાબ",
            "diagram_required": "આકૃતિ જરૂરી",
            
            # Paper generation
            "paper_title": "પેપર શીર્ષક",
            "exam_duration": "પરીક્ષા અવધિ",
            "total_marks": "કુલ ગુણ",
            "exam_date": "પરીક્ષા તારીખ",
            "school_name": "શાળાનું નામ",
            "paper_generated": "પેપર બન્યો",
            "generate_paper": "પેપર બનાવો",
            "automatic_selection": "સ્વચાલિત પસંદગી",
            "manual_selection": "મેન્યુઅલ પસંદગી",
            "question_distribution": "પ્રશ્ન વિતરણ",
            "answer_key": "જવાબ કી",
            
            # Statistics
            "total_questions": "કુલ પ્રશ્નો",
            "available_subjects": "ઉપલબ્ધ વિષયો",
            "statistics": "આંકડાઓ",
            "quick_stats": "ઝડપી આંકડા",
            
            # Scanner
            "scan_questions": "પ્રશ્નો સ્કેન કરો",
            "upload_file": "ફાઇલ અપલોડ કરો",
            "scan_document": "દસ્તાવેજ સ્કેન કરો",
            "extraction_results": "એક્સટ્રેક્શન પરિણામો",
            "detected_questions": "શોધાયેલા પ્રશ્નો",
            "confidence": "વિશ્વાસ",
            "add_to_database": "ડેટાબેસમાં ઉમેરો",
            
            # Sections
            "section_a": "વિભાગ અ",
            "section_b": "વિભાગ બ", 
            "section_c": "વિભાગ સ",
            "multiple_choice": "બહુવિકલ્પીય પ્રશ્નો",
            "short_answer": "ટૂંકા જવાબના પ્રશ્નો",
            "diagram_questions": "આકૃતિના પ્રશ્નો",
            
            # Instructions
            "general_instructions": "સામાન્ય સૂચનાઓ",
            "read_carefully": "કાળજીપૂર્વક વાંચો",
            "all_questions_compulsory": "બધા પ્રશ્નો ફરજિયાત",
            "write_clearly": "સ્પષ્ટ લખો",
            
            # Time units
            "hours": "કલાક",
            "minutes": "મિનિટ",
            "seconds": "સેકંડ",
            
            # Common phrases
            "welcome": "સ્વાગત",
            "thank_you": "આભાર",
            "please_wait": "કૃપા કરીને રાહ જુઓ",
            "try_again": "ફરીથી પ્રયાસ કરો",
            "back": "પાછળ",
            "next": "આગળ",
            "previous": "પહેલાં",
            "finish": "સમાપ્ત",
            "start": "શરૂ કરો",
            "stop": "બંધ કરો",
            "continue": "ચાલુ રાખો",
            "help": "મદદ",
            "about": "વિશે",
            "contact": "સંપર્ક",
            "settings": "સેટિંગ્સ",
            "logout": "લોગઆઉટ",
            "login": "લોગઇન",
        }
        
        # Subject translations
        self.subject_translations = {
            "gujarati": "ગુજરાતી",
            "english": "અંગ્રેજી",
            "mathematics": "ગણિત",
            "physics": "ભૌતિકશાસ્ત્ર",
            "chemistry": "રસાયણશાસ્ત્ર",
            "biology": "જીવવિજ્ઞાન",
            "history": "ઇતિહાસ",
            "geography": "ભૂગોળ",
            "economics": "અર્થશાસ્ત્ર",
            "political_science": "રાજકારણ",
            "computer_science": "કમ્પ્યુટર સાયન્સ",
            "business_studies": "વ્યવસાય અભ્યાસ",
            "accountancy": "હિસાબશાસ્ત્ર",
            "psychology": "મનોવિજ્ઞાન",
            "sociology": "સમાજશાસ્ત્ર",
            "philosophy": "ફિલસૂફી"
        }
    
    def translate(self, key: str) -> str:
        """Get Gujarati translation for a given key"""
        return self.translations.get(key.lower(), key)
    
    def get_subject_gujarati(self, subject_english: str) -> str:
        """Get Gujarati name for a subject"""
        key = subject_english.lower().replace(" ", "_")
        return self.subject_translations.get(key, subject_english)
    
    def get_bilingual_text(self, english_text: str, gujarati_key: str = None) -> str:
        """Get bilingual text (English / Gujarati)"""
        if gujarati_key:
            gujarati_text = self.translate(gujarati_key)
            return f"{english_text} / {gujarati_text}"
        return english_text
    
    def get_question_type_gujarati(self, question_type: str) -> str:
        """Get Gujarati translation for question types"""
        type_map = {
            "MCQ": "બહુવિકલ્પીય",
            "Paragraph": "ફકરો", 
            "Diagram": "આકૃતિ"
        }
        return type_map.get(question_type, question_type)
    
    def get_importance_gujarati(self, importance: str) -> str:
        """Get Gujarati translation for importance levels"""
        importance_map = {
            "Most Important": "સૌથી મહત્વપૂર્ણ",
            "Important": "મહત્વપૂર્ણ",
            "Normal": "સામાન્ય"
        }
        return importance_map.get(importance, importance)
    
    def format_number_gujarati(self, number: int) -> str:
        """Format numbers in Gujarati"""
        gujarati_digits = {
            '0': '૦', '1': '૧', '2': '૨', '3': '૩', '4': '૪',
            '5': '૫', '6': '૬', '7': '૭', '8': '૮', '9': '૯'
        }
        
        number_str = str(number)
        gujarati_number = ''
        
        for digit in number_str:
            gujarati_number += gujarati_digits.get(digit, digit)
        
        return gujarati_number
    
    def get_instruction_text(self, instruction_type: str) -> str:
        """Get instruction text in Gujarati"""
        instructions = {
            "read_all_questions": "બધા પ્રશ્નો કાળજીપૂર્વક વાંચો",
            "all_compulsory": "બધા પ્રશ્નો ફરજિયાત છે",
            "write_clearly": "સ્પષ્ટ અને વાંચી શકાય તેવું લખો",
            "use_separate_sheets": "જરૂરિયાત મુજબ અલગ કાગળનો ઉપયોગ કરો",
            "check_answers": "જવાબો આપતા પહેલા ચકાસો",
            "time_management": "સમયનું યોગ્ય નિયોજન કરો"
        }
        return instructions.get(instruction_type, instruction_type)
    
    def get_section_header(self, section_letter: str, section_type: str) -> str:
        """Get section header in Gujarati"""
        gujarati_letters = {'A': 'અ', 'B': 'બ', 'C': 'સ', 'D': 'દ'}
        gujarati_letter = gujarati_letters.get(section_letter, section_letter)
        
        section_types = {
            "multiple_choice": "બહુવિકલ્પીય પ્રશ્નો",
            "short_answer": "ટૂંકા જવાબના પ્રશ્નો",
            "long_answer": "લાંબા જવાબના પ્રશ્નો",
            "diagram": "આકૃતિના પ્રશ્નો"
        }
        
        gujarati_type = section_types.get(section_type, section_type)
        return f"વિભાગ {gujarati_letter}: {gujarati_type}"
    
    def validate_gujarati_text(self, text: str) -> bool:
        """Validate if text contains Gujarati characters"""
        gujarati_range = range(0x0A80, 0x0B00)  # Gujarati Unicode range
        
        for char in text:
            if ord(char) in gujarati_range:
                return True
        return False
    
    def get_error_message(self, error_type: str) -> str:
        """Get error messages in Gujarati"""
        error_messages = {
            "file_not_found": "ફાઇલ મળી નથી",
            "invalid_format": "અયોગ્ય ફોર્મેટ",
            "empty_field": "ખાલી ફીલ્ડ",
            "duplicate_entry": "ડુપ્લિકેટ એન્ટ્રી",
            "save_failed": "સેવ કરવામાં નિષ્ફળ",
            "load_failed": "લોડ કરવામાં નિષ્ફળ",
            "connection_error": "કનેક્શન એરર",
            "permission_denied": "પરવાનગી નકારવામાં આવી"
        }
        return error_messages.get(error_type, "અજાણી ભૂલ")
    
    def get_success_message(self, action_type: str) -> str:
        """Get success messages in Gujarati"""
        success_messages = {
            "file_uploaded": "ફાઇલ સફળતાપૂર્વક અપલોડ થઈ",
            "question_added": "પ્રશ્ન સફળતાપૂર્વક ઉમેર્યો",
            "question_updated": "પ્રશ્ન સફળતાપૂર્વક અપડેટ કર્યો",
            "question_deleted": "પ્રશ્ન સફળતાપૂર્વક દૂર કર્યો",
            "paper_generated": "પેપર સફળતાપૂર્વક બન્યો",
            "data_saved": "ડેટા સફળતાપૂર્વક સેવ થયો",
            "export_completed": "એક્સપોર્ટ પૂર્ણ થયું"
        }
        return success_messages.get(action_type, "કામ સફળતાપૂર્વક પૂર્ણ થયું")
