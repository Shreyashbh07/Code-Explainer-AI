import streamlit as st
import time
from google import genai

# Page configuration
st.set_page_config(
    page_title="Code Explainer AI",
    page_icon="💻",
    layout="centered"
)

# Application title
st.title("💻 Code Explainer AI")
st.write("Understand programming code with AI in simple words.")

st.divider()

# Select programming language
language = st.selectbox(
    "Select Programming Language",
    ["Python", "Java", "C", "C++", "JavaScript", "HTML/CSS", "SQL", "Other"]
)

# Code input
code = st.text_area(
    "Paste your code here:",
    height=250,
    placeholder="Paste your programming code here..."
)

# API key input
api_key = st.text_input(
    "Enter your Gemini API Key:",
    type="password"
)

# Explain button
if st.button("🚀 Explain Code", use_container_width=True):

    if not code.strip():
        st.warning("Please paste your code first.")

    elif not api_key.strip():
        st.warning("Please enter your Gemini API key.")

    else:
        try:
            # Create Gemini client
            client = genai.Client(api_key=api_key)

            # Create prompt
            prompt = f"""
You are a beginner-friendly programming teacher.

Programming Language: {language}

Explain the following code in simple language.

Provide the explanation in these sections:

1. Code Overview:
Explain what the complete program does.

2. Line-by-Line Explanation:
Explain each line of the code in simple words.

3. Important Concepts:
Explain important functions, variables, loops,
conditions or concepts used in the code.

4. Expected Output:
Show the expected output if possible.

Keep the explanation clear and beginner-friendly.

Code:
{code}
"""

            # Generate AI explanation with retries
            with st.spinner("AI is explaining your code... Please wait."):

                interaction = None

                for attempt in range(3):
                    try:
                        interaction = client.interactions.create(
                            model="gemini-3.8-flash",
                            input=prompt
                        )
                        break

                    except Exception as e:
                        if "503" in str(e) and attempt < 2:
                            time.sleep(3)
                        else:
                            raise e

            # Display explanation
            if interaction:
                st.success("Explanation generated successfully!")

                st.subheader("📖 Code Overview & Explanation")
                st.markdown(interaction.output_text)

                st.divider()

                st.subheader("🧾 Original Code")
                st.code(code, language=language.lower())

        except Exception as e:
            st.error(f"Error: {e}")

            if "503" in str(e):
                st.info(
                    "The AI server is currently busy. "
                    "Please try again after a few minutes."
                )
