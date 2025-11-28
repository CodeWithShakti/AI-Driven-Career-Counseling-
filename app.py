import streamlit as st
import os
import requests  # for backend only
import pandas as pd

# Placeholder function to simulate LLM responses
def placeholder_llm(prompt):
    if "Generate 5 questions" in prompt:
        return """
1. What are your favorite subjects or areas of study?
2. What career goals do you have for the next 5 years?
3. Are there specific industries you are interested in?
4. What skills do you enjoy using the most?
5. What kind of work environment do you prefer?
        """
    elif "Assume you are a career counsellor" in prompt:
        return "Creative and analytical personality, suited for dynamic and problem-solving roles."
    elif "suggest the top 5 career options" in prompt:
        return """
- Software Developer: Designs and builds computer programs and applications.
- Data Analyst: Interprets data to provide actionable business insights.
- Graphic Designer: Creates visual content for media and branding.
- Marketing Specialist: Develops strategies to promote products or services.
- Project Manager: Oversees projects to ensure timely and successful completion.
        """
    return "Response generated."

# For conversation history and login state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "questions" not in st.session_state:
    st.session_state.questions = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Main prompt template
main_prompt_template = """You are a career counsellor for an EdTech company. Use the conversation history to provide personalized advice to the student and try to make it short and in bullet points.

Conversation History:
{history}

Student: {user_input}
Counsellor:"""

def generate_prompt(conversation, user_input):
    history = "\n".join(conversation)
    return main_prompt_template.format(history=history, user_input=user_input)

def generate_questions(edu_prompt):
    question_prompt = f"Generate 5 questions to ask a student in {edu_prompt} about their interests, goals, and preferences."
    questions = placeholder_llm(question_prompt)
    return questions.strip().split('\n')

# Login page
def login_page():
    st.title("Login to AI Career-Counsellor")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Simple mock authentication (replace with actual authentication logic if needed)
        if username == "user" and password == "pass123":
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password. Please try again.")

# Main app
def main_app():
    st.title("Hello 👋 Welcome to AI Career-Counsellor!")

    name = st.text_input("Enter your name")
    if name:
        st.write(f"Hello {name}! Let's clarify your doubts.")
        st.subheader("Enter Your Current Education Level")
        edu_prompt = st.radio(
            "Please select one:",
            ["High-School Junior", "College", "Professional"],
            index=None
        )
        st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        if edu_prompt:
            problem_description = st.text_input("Describe the problem you are facing")
            if problem_description:
                hobby = st.text_input("Enter your favourite pastime hobby")
                if hobby:
                    # Generate questions only if they haven't been generated in this session
                    if st.session_state.questions is None:
                        st.session_state.questions = generate_questions(edu_prompt)

                    questions = st.session_state.questions

                    responses = []
                    for i, question in enumerate(questions, 1):
                        st.subheader(f"{question}")
                        response = st.text_input(f"Answer for Question {i}")
                        responses.append(response)

                    if all(responses):
                        # Prompt for personality analysis
                        answer_stmt = (
                            f"Assume you are a career counsellor for {name}, a {edu_prompt} student. "
                            f"The student's problem description is: {problem_description}. Their hobby is {hobby}. "
                            f"Here are their responses to the questions: "
                        )
                        for i, response in enumerate(responses, 1):
                            answer_stmt += f"Question {i}: {questions[i-1]}, Answer: {response}. "

                        # Generate the full prompt
                        prompt = generate_prompt(st.session_state.conversation, answer_stmt)

                        # Run the personality analysis prompt
                        personality_type = placeholder_llm(prompt)

                        st.session_state.conversation.append(f"Student: {answer_stmt}")
                        st.session_state.conversation.append(f"Counsellor: {personality_type}")

                        # Display personality type
                        st.write(f"The personality type is: {personality_type}")

                        # Generate prompt for career advice based on personality type
                        goals = (
                            f"Based on the personality type '{personality_type}', suggest the top 5 career options for {name}. "
                            f"Provide the name of the profession and a short description (max 15 words) for each."
                        )

                        career_options = placeholder_llm(goals)
                        st.subheader("Some great career options for you could be:")
                        st.write(career_options)

                        # Parse career options for display
                        careers = []
                        descriptions = []
                        for line in career_options.strip().split('\n'):
                            if line.strip():
                                career, desc = line.split(':', 1)
                                careers.append(career.strip().replace('- ', ''))
                                descriptions.append(desc.strip())

                        # Allow user to select a career
                        st.subheader("Choose a Career to Explore")
                        selected_career = st.selectbox("Select a career:", careers)
                        if selected_career:
                            selected_desc = descriptions[careers.index(selected_career)]
                            st.write(f"**{selected_career}**: {selected_desc}")

                        # Append career advice to the conversation history
                        st.session_state.conversation.append(f"Student: {goals}")
                        st.session_state.conversation.append(f"Counsellor: {career_options}")

                else:
                    st.subheader("Please enter your favourite pastime hobby to continue.")
            else:
                st.subheader("Please describe the problem you are facing to continue.")
        else:
            st.subheader("Please select your current education level to continue.")

    # Display conversation history
    st.header("Conversation History")
    for message in st.session_state.conversation:
        st.markdown(f"**{message}**")

    # Button to clear the conversation history
    if st.button("Clear Conversation"):
        st.session_state.conversation = []
        st.session_state.questions = None
        st.rerun()

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.conversation = []
        st.session_state.questions = None
        st.rerun()

# Render login page or main app based on login state
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
