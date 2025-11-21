import os
import streamlit as st
import PIL.Image
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(
    page_title="RoadSide AI", 
    page_icon="🔧", 
    layout="centered"
)

# Custom CSS to make the UI look like a native app
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    /* Chat bubble styling */
    .stChatMessage {
        background-color: #262730;
        border-radius: 15px;
    }
    /* Hide the camera popover arrow for a cleaner look */
    [data-testid="stPopover"] {
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("🔧 Settings")
    api_key = st.text_input("Google API Key", type="password")
    vehicle_type = st.text_input("Vehicle Model", value="General Vehicle")
    
    st.divider()
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Block execution if key is missing
if not api_key:
    st.info("Please enter your Google API Key in the sidebar to start.")
    st.stop()

genai.configure(api_key=api_key)

# --- AGENT FUNCTIONS ---

def mechanic_agent(history, user_input, img=None):
    """
    Primary agent: Diagnoses the issue based on text and optional image.
    """
    system_prompt = f"""
    You are 'Mac', an expert vehicle mechanic for a {vehicle_type}.
    
    YOUR PERSONALITY:
    - You love engines, grease, and gears.
    - If the user asks about a non-vehicle (like a laptop or toaster), joke about it: 
      "I usually stick to pistons and spark plugs, but let's take a look..." 
      Then apply your diagnostic logic anyway.

    PROTOCOL:
    1. Start with the simplest check (power, fuel, switches).
    2. Give instructions one step at a time.
    3. ALWAYS ask "Did that fix it?" before moving on.
    """
    
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=system_prompt
    )
    
    # Prepare chat history for the API
    api_history = []
    for msg in history:
        # We only send text history to keep context lightweight
        if isinstance(msg["content"], str):
            role = "user" if msg["role"] == "user" else "model"
            api_history.append({"role": role, "parts": [msg["content"]]})

    # Prepare current message
    content_parts = [user_input]
    if img:
        content_parts.append(PIL.Image.open(img))

    chat = model.start_chat(history=api_history)
    
    try:
        response = chat.send_message(content_parts)
        return response.text
    except Exception as e:
        return f"⚠️ Error communicating with mechanic: {str(e)}"

def safety_agent(mechanic_response):
    """
    Secondary agent: Reviews the mechanic's advice for safety risks.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    You are a Safety Supervisor. Review this advice given to a vehicle owner:
    "{mechanic_response}"
    
    If there is a safety risk (hot engine, electric shock, traffic, fire), 
    add a bold WARNING at the start. Otherwise, return the text exactly as is.
    """
    
    try:
        return model.generate_content(prompt).text
    except:
        return mechanic_response

# --- MAIN APP INTERFACE ---

st.title("RoadSide AI 🔧")
st.caption(f"Connected to: {vehicle_type}")

# Initialize chat session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "I'm ready to help. What's the problem?"}
    ]

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # If the message had an image, show it first
        if "image" in msg and msg["image"]:
            st.image(msg["image"], width=200)
        st.write(msg["content"])

st.markdown("---") # Divider

# --- INPUT AREA ---

# 1. The Camera Button (Hidden inside a Popover)
# This solves your issue: Camera is off until user clicks "Take Photo"
with st.popover("📸 Take Photo", use_container_width=True):
    camera_file = st.camera_input("Snap a picture", label_visibility="collapsed")

# 2. Text Input
user_text = st.chat_input("Type your problem here...")

# --- LOGIC HANDLER ---

if user_text or camera_file:
    # Create a container for the user's input logic
    input_content = user_text if user_text else "Check this image."
    
    # 1. Display User Message
    with st.chat_message("user"):
        if camera_file:
            st.image(camera_file, width=200)
        if user_text:
            st.write(user_text)
            
    # Add to history
    st.session_state.messages.append({
        "role": "user",
        "content": input_content,
        "image": camera_file
    })
    
    # 2. Generate Response
    with st.chat_message("assistant"):
        status_box = st.empty()
        status_box.markdown("*Mechanic is thinking...*")
        
        # Call Agent 1 (Mechanic)
        raw_advice = mechanic_agent(
            st.session_state.messages[:-1], 
            input_content, 
            camera_file
        )
        
        status_box.markdown("*Checking safety protocols...*")
        
        # Call Agent 2 (Safety Supervisor)
        final_advice = safety_agent(raw_advice)
        
        status_box.write(final_advice)
        
    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_advice
    })