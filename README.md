# Talent-scout-ai-assistant
# An AI-powered technical screening chatbot for initial candidate interviews using Python, Streamlit, and OpenAI.
TalentScout AI Hiring Assistant
An interactive AI-powered screening system for technical candidates that automates the initial interview process. Built with Python, Streamlit, and OpenAI, this application guides candidates through a structured conversation to collect their information and assess their technical skills.
Features

Conversational AI interface for candidate screening
Systematic collection of candidate information
Dynamic technical question generation based on candidate's tech stack
User-friendly interface with modern styling
Admin dashboard for reviewing candidate submissions
Data export functionality for further processing

Project Structure
The project consists of several core modules:

prompts.py: Contains all conversation templates and system prompts
chatbot.py: Main conversation management and state flow logic
utils.py: Helper functions for data validation and processing
app.py: Streamlit-based web interface

Technical Stack

Python: Core programming language
Streamlit: Web application framework
OpenAI API: AI conversation engine
Ngrok: Secure tunneling for deployment

Getting Started
demo link: https://12e2-34-91-130-93.ngrok-free.app
Screenshots
![image](https://github.com/user-attachments/assets/f423d13c-ece8-4ac4-af48-c3007d828950)


Detailed Description for README
How It Works
TalentScout guides candidates through a structured conversation flow to gather essential information and assess technical skills. The system:

Initializes the Conversation: Greets the candidate professionally and explains the purpose of the interaction.
Information Collection: Systematically collects:

Full name
Email address
Phone number
Years of experience
Desired position
Current location
Technical skill set


Technical Assessment: Analyzes the candidate's tech stack and generates relevant technical questions tailored to their experience level and the position they're applying for.
Data Storage: Saves candidate profiles to JSON files for easy access and integration with other HR systems.
Administrative Review: Provides an admin interface for reviewing candidate submissions and downloading data.

# Code Architecture
The application follows a modular architecture:
prompts.py
Contains all conversation templates, system prompts, and message structures that guide the conversation flow. This separation allows easy modification of conversation content without changing the core logic.

Key Components
SYSTEM_PROMPT = "..."  
INFORMATION_COLLECTION_PROMPTS = {...}  
TECH_QUESTION_GENERATION_PROMPT = "..." 

chatbot.py
The core conversation engine that manages:

Conversation state transitions
Candidate information storage
Response generation based on current state
Technical question generation and processing

Key Components:
class TalentScoutChatbot:
    # Manages conversation state
    # Processes user input
    # Stores candidate information
    # Generates appropriate responses
    
utils.py
Helper functions for:

Email and phone validation
Data storage and retrieval
Technology extraction and categorization

app.py
Streamlit-based web interface providing:

Real-time chat interface
Message history display
Form handling
Data export
Administrative functionality

# Deployment
The application can be deployed locally or on a server using Streamlit's built-in server or containerized using Docker. For temporary deployments, the code includes Ngrok integration for secure tunneling.

# Future Improvements

Integration with ATS (Applicant Tracking Systems)
Enhanced technical question generation
Video interview capabilities
Resume parsing functionality
Candidate skill assessment visualization
