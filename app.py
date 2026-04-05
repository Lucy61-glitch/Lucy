import streamlit as st
import json
from datetime import datetime, date

# 1. EXTERNAL DATA LOADING (Criterion: 10 pts)
def load_questions():
    try:
        with open("questions.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Error: questions.json not found! Please ensure it is uploaded to your GitHub repository.")
        return []

# 2. PSYCHOLOGICAL ASSESSMENT LOGIC (7 States)
def interpret_psych_state(score):
    if score <= 15:
        return "Level 1: Master of Efficiency. Perfect digital control; zero planning anxiety."
    elif score <= 30:
        return "Level 2: High Productivity. Stable psychological state; high confidence."
    elif score <= 45:
        return "Level 3: Functional User. Organized, but minor gaps cause occasional worry."
    elif score <= 60:
        return "Level 4: Moderate Risk. Prone to procrastination; missed alerts cause stress."
    elif score <= 75:
        return "Level 5: Low Effectiveness. High technostress; the system is a burden."
    elif score <= 85:
        return "Level 6: High Anxiety. Disorganization is leading to academic distress."
    else:
        return "Level 7: Critical Disarray. System failure. Immediate stress intervention recommended."

def main():
    # Page Configuration
    st.set_page_config(page_title="Digital Stress Lab", page_icon="📅", layout="centered")

    # Header Section
    st.title("🌐 Digital Calendar & Psychological Stress Lab")
    st.image("https://images.unsplash.com/photo-1506784983877-45594efa4cbe?auto=format&fit=crop&q=80&w=1000", 
             caption="Academic Time Management & Stress Assessment")
    
    st.write("""
    ### About this Survey
    This psychometric tool evaluates how your digital planning habits affect your 
    mental well-being and academic stress levels.
    """)

    # 3. USER REGISTRATION (Sidebar)
    st.sidebar.header("📋 User Registration")
    first_name = st.sidebar.text_input("First Name")
    last_name = st.sidebar.text_input("Surname")
    student_id = st.sidebar.text_input("Student ID Number")
    
    # Fixed: min_value now uses the 'date' object correctly
    dob = st.sidebar.date_input("Date of Birth", min_value=date(1950, 1, 1))

    # Load Questions
    questions = load_questions()
    user_responses = []

    if questions:
        st.divider()
        st.info("Please answer the following 20 questions based on your current habits.")
        
        # 4. SURVEY LOOP
        for i, item in enumerate(questions):
            st.markdown(f"#### Question {i+1}")
            st.write(item['q'])
            
            # Display Options
            options_labels = [opt[0] for opt in item['o']]
            choice = st.radio(
                f"Select option for Q{i+1}:", 
                options_labels, 
                key=f"q{i}", 
                label_visibility="collapsed"
            )
            
            # Record points for the selected answer
            for opt in item['o']:
                if opt[0] == choice:
                    user_responses.append(opt[1])
        
        st.divider()

        # 5. SUBMISSION & ANALYSIS
        if st.button("🚀 Submit and Analyze My Results"):
            if not first_name or not last_name or not student_id:
                st.warning("⚠️ Please complete the Registration form in the sidebar.")
            else:
                final_score = sum(user_responses)
                psych_result = interpret_psych_state(final_score)
                
                # Success Visuals
                st.balloons()
                st.header(f"Results for {first_name} {last_name}")
                
                col1, col2 = st.columns(2)
                col1.metric("Stress Score", f"{final_score} pts")
                
                # Efficiency Calculation (Assuming 80 is max points)
                efficiency = round(((80 - final_score) / 80) * 100)
                col2.metric("Efficiency Level", f"{max(0, efficiency)}%")

                st.subheader("Psychological Analysis:")
                st.success(psych_result)
                
                st.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()