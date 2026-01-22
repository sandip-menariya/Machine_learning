import streamlit as st
import google.generativeai as genai
import re

# 1. CONFIGURE THE AI
# Replace 'YOUR_API_KEY' with the actual key you got from Google AI Studio
genai.configure(api_key=".......YOUR_API_KEY.........")

# Set up the model with our specific "System Instruction"
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="""
    You are a Principal Software Architect. You value EFFICIENCY and LOGIC above all else.
    
    Rules for Review:
    1. **The "Pass" Condition:** If the code is logically sound, efficient (O(n) or better), and works, YOU MUST APPROVE IT.
       - Response format for success: "Approval Granted. [Insert a begrudging compliment, e.g. 'Finally, some code that doesn't make my eyes bleed.']"
    
    2. **The "Fail" Condition:** Only reject code for REAL issues:
       - Response format for failure: "Rejected. [Insert a sharp critique, e.g. 'This is a nightmare to maintain.']"
       - Bugs / Infinite loops.
       - Terrible Time Complexity (e.g., O(n^2) where O(n) is possible).
       - Security risks.
       - Truly unreadable "spaghetti" logic.
    
    3. **Anti-Nitpick Mode:** - Do NOT complain about variable names like 'n' or 'i' in math functions (context matters).
       - Do NOT demand comments for obvious code (e.g., 'i += 1'). 

    4. **The "Senior's Secret" (Crucial):** - If the code passes but could be cleaner, add a section called "**Refactoring Tip**". 
       - Show how to make it more Pythonic, readable, or faster. 
       - Frame it as: "It passes, but if you want to write code that impresses me, do this instead..."
    5. **Respnse: ** - Do not write any code in your response, you can hint at the solution.
    Tone:
    - Brief, professional, slightly cynical. 
    - Treat the user like they are smart but lazy. 
    """
)

# 2. BUILD THE UI (The Website)
st.set_page_config(page_title="CodeDrill", page_icon="💀")

st.title("🥷 CodeDrill")
st.subheader("The Uncompromising AI Mentor")

st.write("Paste or Write your code below. I will review it for technical debt and efficiency.")

# The Text Area for code input
user_code = st.text_area("Your Code Snippet:", height=200, placeholder="def my_function()...")

# 3. THE LOGIC
if st.button("Submit for Review"):
    if user_code:
        with st.spinner("Analyzing technical debt..."):
            # Send the user's code to the AI
            response = model.generate_content(f"Review this code:\n{user_code}")
            approval=re.search(r'((A|R)[A-Za-z]+) *([A-Za-z]+)*\.',response.text.strip(),re.IGNORECASE)
            # Display the result
            if approval and approval.group(0).lower()=="rejected.":
                st.error("Code Review Failed:") # Uses a red box for dramatic effect
            elif approval and approval.group(0).lower()=="approval granted.":
                st.success("Code Review Passed:") # Uses a green box for celebration
            st.write(response.text)
    else:
        st.warning("You submitted empty code. Are you testing my patience?")
