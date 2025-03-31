# chatbot.py
import os
import openai
from dotenv import load_dotenv
import random
from prompts import (
    SYSTEM_PROMPT, 
    INITIAL_GREETING, 
    INFORMATION_COLLECTION_PROMPTS,
    TECH_QUESTION_GENERATION_PROMPT,
    CONVERSATION_END_PROMPT,
    FALLBACK_RESPONSES
)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class TalentScoutChatbot:
    def __init__(self):
        self.conversation_history = []
        self.candidate_info = {
            "name": None,
            "email": None,
            "phone": None,
            "experience": None,
            "position": None,
            "location": None,
            "tech_stack": None,
            "technical_questions": [],
            "question_index": 0
        }
        self.current_state = "greeting"
        self.states = [
            "greeting", "get_name", "get_email", "get_phone", 
            "get_experience", "get_position", "get_location", 
            "get_tech_stack", "generate_questions", "ask_questions", 
            "conclude"
        ]
        
        # Initialize with system prompt
        self.add_to_history({"role": "system", "content": SYSTEM_PROMPT})
    
    def add_to_history(self, message):
        """Add a message to the conversation history."""
        self.conversation_history.append(message)
    
    def generate_response(self, user_input):
        """Generate a response based on the current state and user input."""
        # Check for exit keywords
        if self._is_exit_request(user_input):
            return self._generate_exit_message()
        
        # Process user input based on current state
        self.add_to_history({"role": "user", "content": user_input})
        
        # Update candidate info based on current state
        self._update_candidate_info(user_input)
        
        # Determine next state and generate appropriate response
        response = self._get_next_response()
        
        self.add_to_history({"role": "assistant", "content": response})
        return response
    
    def _is_exit_request(self, text):
        """Check if the user wants to exit the conversation."""
        exit_keywords = ["goodbye", "exit", "quit", "bye", "end", "stop"]
        return any(keyword in text.lower() for keyword in exit_keywords)
    
    def _generate_exit_message(self):
        """Generate a goodbye message."""
        name = self.candidate_info["name"] or "there"
        email = self.candidate_info["email"] or "your provided contact information"
        return CONVERSATION_END_PROMPT.format(name=name, email=email)
    
    def _update_candidate_info(self, user_input):
        """Update candidate information based on current state and user input."""
        if self.current_state == "get_name":
            self.candidate_info["name"] = user_input
        elif self.current_state == "get_email":
            self.candidate_info["email"] = user_input
        elif self.current_state == "get_phone":
            self.candidate_info["phone"] = user_input
        elif self.current_state == "get_experience":
            self.candidate_info["experience"] = user_input
        elif self.current_state == "get_position":
            self.candidate_info["position"] = user_input
        elif self.current_state == "get_location":
            self.candidate_info["location"] = user_input
        elif self.current_state == "get_tech_stack":
            self.candidate_info["tech_stack"] = user_input
    
    def _get_next_state(self):
        """Determine the next state in the conversation flow."""
        current_index = self.states.index(self.current_state)
        next_index = min(current_index + 1, len(self.states) - 1)
        return self.states[next_index]
    
    def _get_next_response(self):
        """Generate the next response based on the current state."""
        # Move to the next state
        next_state = self._get_next_state()
        
        if self.current_state == "greeting":
            self.current_state = "get_name"
            return INITIAL_GREETING
        
        elif self.current_state == "get_name":
            self.current_state = "get_email"
            return INFORMATION_COLLECTION_PROMPTS["email"].format(name=self.candidate_info["name"])
        
        elif self.current_state == "get_email":
            self.current_state = "get_phone"
            return INFORMATION_COLLECTION_PROMPTS["phone"]
        
        elif self.current_state == "get_phone":
            self.current_state = "get_experience"
            return INFORMATION_COLLECTION_PROMPTS["experience"]
        
        elif self.current_state == "get_experience":
            self.current_state = "get_position"
            return INFORMATION_COLLECTION_PROMPTS["position"]
        
        elif self.current_state == "get_position":
            self.current_state = "get_location"
            return INFORMATION_COLLECTION_PROMPTS["location"]
        
        elif self.current_state == "get_location":
            self.current_state = "get_tech_stack"
            return INFORMATION_COLLECTION_PROMPTS["tech_stack"]
        
        elif self.current_state == "get_tech_stack":
            self.current_state = "generate_questions"
            # Generate technical questions
            return self._generate_technical_questions()
        
        elif self.current_state == "generate_questions":
            self.current_state = "ask_questions"
            # Start asking the first question
            return self._ask_next_question()
        
        elif self.current_state == "ask_questions":
            self.candidate_info["question_index"] += 1
            # Check if we've asked all questions
            if self.candidate_info["question_index"] >= len(self.candidate_info["technical_questions"]):
                self.current_state = "conclude"
                return self._generate_conclusion()
            else:
                return self._ask_next_question()
        
        elif self.current_state == "conclude":
            return self._generate_exit_message()
        
        else:
            # Fallback
            return random.choice(FALLBACK_RESPONSES)
    
    def _generate_technical_questions(self):
        """Generate technical questions based on the candidate's tech stack."""
        prompt = TECH_QUESTION_GENERATION_PROMPT.format(
            tech_stack=self.candidate_info["tech_stack"],
            position=self.candidate_info["position"]
        )
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Or another appropriate model
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            questions = response.choices[0].message.content.strip().split('\n')
            # Filter out empty lines and numbering
            questions = [q.strip() for q in questions if q.strip()]
            # Remove numbering if present (e.g., "1. ", "- ", etc.)
            questions = [q.split('. ', 1)[-1] if '. ' in q[:4] else q for q in questions]
            questions = [q[2:] if q.startswith('- ') else q for q in questions]
            
            self.candidate_info["technical_questions"] = questions
            
            return f"Thank you for sharing your tech stack. I'd like to ask you a few technical questions to better understand your expertise.\n\nFirst question: {questions[0]}"
        
        except Exception as e:
            print(f"Error generating questions: {e}")
            return "I'd like to ask you some technical questions about your skills. Let's start with: What are some challenging projects you've worked on using your primary technical skills?"
    
    def _ask_next_question(self):
        """Ask the next technical question."""
        index = self.candidate_info["question_index"]
        questions = self.candidate_info["technical_questions"]
        
        if index < len(questions):
            return f"Question {index + 1}: {questions[index]}"
        else:
            self.current_state = "conclude"
            return self._generate_conclusion()
    
    def _generate_conclusion(self):
        """Generate a conclusion for the conversation."""
        name = self.candidate_info["name"] or "there"
        email = self.candidate_info["email"] or "your provided contact information"
        
        conclusion = f"""
Thank you, {name}, for taking the time to chat with me today! 

I've collected the following information:
- Name: {self.candidate_info['name']}
- Email: {self.candidate_info['email']}
- Phone: {self.candidate_info['phone']}
- Experience: {self.candidate_info['experience']}
- Desired Position: {self.candidate_info['position']}
- Location: {self.candidate_info['location']}
- Tech Stack: {self.candidate_info['tech_stack']}

Our recruitment team will review your information and technical responses. If there's a good match with our current openings, someone will reach out to you at {email} soon.

Is there anything else you'd like to add before we conclude this conversation?
"""
        return conclusion
    
    def get_state(self):
        """Get the current state of the conversation."""
        return self.current_state
    
    def get_candidate_info(self):
        """Get the collected candidate information."""
        return self.candidate_info
