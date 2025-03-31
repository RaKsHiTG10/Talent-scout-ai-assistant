import streamlit as st
from chatbot import TalentScoutChatbot
import time
import os
import json
from datetime import datetime
from utils import save_candidate_data

# Set page config
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="💼",  # Suit emoji
    layout="centered"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main {
            background-color: #f5f7f9;
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            gap: 0.75rem;
        }
        .chat-message.user {
            background-color: #e6f3ff;
            border-left: 5px solid #2c88d9;
        }
        .chat-message.bot {
            background-color: #f0f2f5;
            border-left: 5px solid #6c757d;
        }
        .chat-message .avatar {
            min-width: 40px;
        }
        .chat-message .message {
            flex-grow: 1;
        }
        .stButton>button {
            border-radius: 20px;
            padding: 0.5rem 1rem;
            background-color: #2c88d9;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background-color: #1b5a8a;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize chatbot in session state if not already initialized
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = TalentScoutChatbot()

if 'messages' not in st.session_state:
    st.session_state.messages = []
    bot_message = st.session_state.chatbot.generate_response("Hi")
    st.session_state.messages.append({"role": "bot", "content": bot_message})

# Track if data has been saved
if 'data_saved' not in st.session_state:
    st.session_state.data_saved = False

# Function to save candidate data
def save_data():
    if not st.session_state.data_saved:
        candidate_info = st.session_state.chatbot.get_candidate_info()
        
        # Check if we have enough data to save
        if candidate_info['name'] and candidate_info['email']:
            try:
                # Create data directory if it doesn't exist
                if not os.path.exists('data'):
                    os.makedirs('data')
                
                # Generate a unique filename
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                name = candidate_info.get("name", "unknown").lower().replace(" ", "_")
                filename = f"data/candidate_{name}_{timestamp}.json"
                
                # Save to file
                with open(filename, 'w') as f:
                    json.dump(candidate_info, f, indent=4)
                
                st.session_state.data_saved = True
                st.session_state.saved_filename = filename
                return True
            except Exception as e:
                st.error(f"Error saving data: {e}")
                return False
    return False

# App header
st.title("TalentScout Hiring Assistant")
st.subheader("AI-powered candidate screening")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user">
                <div class="avatar">👤</div>  <!-- User icon -->
                <div class="message">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot">
                <div class="avatar">🤖</div>  <!-- Robot icon -->
                <div class="message">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

# Chat input with form
with st.form(key="message_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your message:", 
        key="user_input",
        placeholder="Type your message here..."
    )
    submit_button = st.form_submit_button("Send")
    
    if submit_button and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("Thinking..."):
            bot_response = st.session_state.chatbot.generate_response(user_input)
            time.sleep(0.5)  # Simulate typing delay
            st.session_state.messages.append({"role": "bot", "content": bot_response})
            
            # Check if conversation is concluding and save data
            current_state = st.session_state.chatbot.get_state()
            if current_state == "conclude":
                save_data()

# Display saved data notification
if st.session_state.get('data_saved', False):
    st.success(f"Candidate data has been saved to {st.session_state.saved_filename}")
    
    # Show download button for the saved data
    if os.path.exists(st.session_state.saved_filename):
        with open(st.session_state.saved_filename, 'r') as f:
            st.download_button(
                label="Download Candidate Data",
                data=f.read(),
                file_name=os.path.basename(st.session_state.saved_filename),
                mime="application/json"
            )

# Display debug info (optional)
current_state = st.session_state.chatbot.get_state()
if st.checkbox("Show debug info"):
    st.write(f"Current state: {current_state}")
    st.write("Candidate info:")
    st.write(st.session_state.chatbot.get_candidate_info())

    # Add a manual save button in debug mode
    if st.button("Save Data Now"):
        if save_data():
            st.success("Data saved successfully!")
        else:
            st.warning("Not enough data to save or data already saved.")

# Admin section (password protected)
with st.expander("Admin Access"):
    password = st.text_input("Admin Password", type="password")
    if password == "admin123":  # Very simple password, should be more secure in production
        st.success("Admin access granted")
        
        # List all saved candidate files
        if os.path.exists('data'):
            files = [f for f in os.listdir('data') if f.endswith('.json')]
            if files:
                selected_file = st.selectbox("Select candidate data file", files)
                
                if selected_file:
                    file_path = os.path.join('data', selected_file)
                    with open(file_path, 'r') as f:
                        candidate_data = json.load(f)
                        st.json(candidate_data)
                        
                        st.download_button(
                            label="Download Selected Data",
                            data=json.dumps(candidate_data, indent=4),
                            file_name=selected_file,
                            mime="application/json"
                        )
            else:
                st.info("No candidate data files found.")
    elif password and password != "":
        st.error("Incorrect password")

# Footer
st.markdown("---")
st.markdown("© 2025 TalentScout - AI Hiring Assistant")
