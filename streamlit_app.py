import streamlit as st
import google.generativeai as genai
from datetime import datetime

# CONFIG API KEY AND MODEL

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

# SESSION STATE
if "history" not in st.session_state:
    st.session_state.history = []

if "total_words" not in st.session_state:
    st.session_state.total_words = 0

if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0

# PAGE
st.set_page_config(
    page_title="Prompt Engineering Playground",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Prompt Engineering Playground")

st.caption(
    "Built to demonstrate the impact of prompt engineering techniques on LLM outputs."
)


st.info(
    "🎯 Explore how different prompting techniques affect the same LLM output. Compare personas, transformations, summarization, and temperature-controlled generations."
)

# SIDEBAR
with st.sidebar:

    temperature = st.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.5,
    value=0.7,
    step=0.1
    )

    st.info(
"""
Temperature Controls Creativity

0.0 = Deterministic
0.3 = Focused
0.7 = Balanced
1.0 = Creative
1.5 = Highly Creative
"""
)
    
    st.header("Statistics")

    st.metric(
    "Total Generations",
    st.session_state.total_queries
    )

    st.metric(
    "Total Words Generated",
    st.session_state.total_words
    )

    st.metric(
    "History Size",
    len(st.session_state.history)
    )


    st.divider()

    st.subheader("📚 Implemented Features")

    st.markdown("""
✅ Persona Prompting

✅ Summarization

✅ Transformation

✅ Expansion

✅ Prompt Comparison

✅ Temperature Control
                 """)

    
# INPUTS

feature = st.selectbox(
    "Choose Prompt Technique",
    [
        "Explain Like I'm 5",
        "Teacher Mode",
        "Mentor Mode",
        "Professional Rewrite",
        "Summarizer",
        "Grammar Correction",
        "Format Converter",
        "Interview Question Generator",
        "Compare Prompt Styles",
        "Temperature Experiment"
    ]
)

if feature in [
    "Explain Like I'm 5",
    "Teacher Mode",
    "Mentor Mode"
]:
    st.badge("Persona Prompting")

elif feature in [
    "Professional Rewrite",
    "Grammar Correction",
    "Format Converter"
]:
    st.badge("Transformation")

elif feature == "Summarizer":
    st.badge("Summarization")

elif feature == "Interview Question Generator":
    st.badge("Expansion")

elif feature == "Compare Prompt Styles":
    st.badge("Prompt Comparison")

elif feature == "Temperature Experiment":
    st.badge("Temperature Control")

show_prompt = st.checkbox(
    "Show Prompt Template"
)

user_input = st.text_area(
    "Enter your text",
    height=200
)

# GENERATE BUTTON

if st.button("🚀 Generate Response"):


    if user_input.strip() == "":
        st.error("Please enter some text.")

    elif feature == "Compare Prompt Styles":

            eli5_prompt = f"""
You are a world-class educator specializing in translating complex concepts for young children. 
Explain the following topic to a 5-year-old child: "{user_input}"

Adhere strictly to these rules:
1. **The Playground Rule**: Do not use jargon, abstract concepts, or complex technical terms. If you must use a big word, immediately explain it using an analogy a child can touch, see, or feel on a playground.
2. **Relatable Analogy**: Center the explanation around a single, clear analogy (e.g., comparing the internet to a massive library with fast delivery trucks, or electricity to tiny running ants).
3. **Tone and Style**: Keep the tone enthusiastic, curious, and respectful. Do not use patronizing filler words like "Hey kiddo" or "Guess what?". 
4. **Formatting**: Break the explanation into 2-3 short paragraphs maximum. Use simple, active sentences.
"""

            teacher_prompt = f"""
You are an exceptionally engaging, highly experienced university professor known for making difficult subjects intuitive and crystal clear.
Explain the following topic: "{user_input}"

Structure your response using this pedagogical framework:

1. **The Intuitive Hook (The 'Why It Matters')**: Start with a 2-3 sentence high-level overview. Explain the core utility of this topic before dropping any heavy vocabulary. What problem does it solve?
2. **The Core Concept Breakdown**: Define the topic clearly, then break down the 2-3 absolute essential pillars. Use clear formatting (bolding or bullet points) to make it highly scannable.
3. **The Concrete Blueprint (Example)**: Provide one detailed, real-world example or practical use case. Walk through it step-by-step so the theory becomes visible in practice.
4. **The Common Pitfall**: Explicitly call out one major misconception, common student mistake, or tricky edge case associated with this topic, and clarify why it happens.
5. **Cheatsheet Summary (Revision Notes)**: A highly condensed, high-yield bulleted summary of the absolute non-negotiables a student must memorize for an exam.

Tone: Professional, encouraging, sharp, and authoritative. Avoid generic filler text or patronizing introductory remarks. Move straight into the teaching.
"""
            
            mentor_prompt = f"""
You are an experienced industry mentor and strategic advisor. Your goal is to help the user not just understand "{user_input}" academically, but master its real-world application, strategic value, and career relevance.

Structure your mentorship guidance into these distinct sections:

1. **The Strategic Perspective (Why it matters)**: Explain the high-level significance of this topic. Why is it worth their time right now? How does it fit into the bigger picture of the industry or modern problem-solving?
2. **Industry Blueprint (Applications)**: Provide concrete examples of how top professionals use this in production or industry right now. Move past basic examples and look at actual, high-value use cases.
3. **The Tactical Learning Path**: Lay out a clear, phased roadmap for moving from beginner to proficient. Explicitly state what they should learn first, what to practice building or doing next, and how to validate their skills.
4. **The Blindspots & Traps**: What are the costly mistakes, architectural flaws, or mental traps that juniors fall into when dealing with this? Share the "lessons learned the hard way" that save weeks of frustration.
5. **Next Actionable Step**: End with one specific, immediate challenge or project idea they can start on today to apply this knowledge.

Tone: Incisive, deeply reasoned, professional, and pragmatic. Do not use generic motivational fluff ("You've got this!"). Focus entirely on actionable, high-density strategic advice.

"""
            
            with st.spinner("Comparing prompt styles..."):

             eli5_response = model.generate_content(
             eli5_prompt,
             generation_config=genai.GenerationConfig(
                temperature=temperature
            )
        )

             teacher_response = model.generate_content(
             teacher_prompt,
             generation_config=genai.GenerationConfig(
                temperature=temperature
            )
        )

             mentor_response = model.generate_content(
             mentor_prompt,
             generation_config=genai.GenerationConfig(
                temperature=temperature
            )
        )

             tab1, tab2, tab3 = st.tabs(
             ["ELI5", "Teacher", "Mentor"]
    )

             with tab1:
              st.markdown(eli5_response.text)

             with tab2:
              st.markdown(teacher_response.text)

             with tab3:
              st.markdown(mentor_response.text)
             st.session_state.total_queries += 1

             comparison_words = (
             len(eli5_response.text.split()) +
             len(teacher_response.text.split()) +
             len(mentor_response.text.split())
                )

             st.session_state.total_words += comparison_words


             st.session_state.history.append(
              {
               "time": datetime.now(),
               "feature": feature,
               "input": user_input,
               "response": "ELI5 + Teacher + Mentor Comparison"
              }
             )

            if len(st.session_state.history) > 10:
               st.session_state.history.pop(0)

            st.stop()

    elif feature == "Temperature Experiment":

        if user_input.strip() == "":
         st.error("Please enter some text.")
         st.stop()

        prompt = f"""
You are a senior machine learning engineer and AI researcher known for absolute technical clarity. 
Explain the following topic with precision: "{user_input}"

Structure your response into these 4 technical layers:

1.  **The First Principles (The 'What')**: Define the topic using correct mathematical or engineering terminology. Avoid analogies here; focus on the literal mechanism or architecture.
2.  **The Structural Logic (The 'How')**: Break down the core components or the workflow. Use a step-by-step or modular breakdown of how the data or logic flows through this system.
3.  **The Engineering Trade-offs**: This is critical. Explain the "Cost vs. Benefit." What are the limitations (e.g., computational overhead, latency, gradient instability)? What are the alternatives?
4.  **Implementation Gist**: Provide a brief, high-level pseudocode snippet or a logical outline of how this would be implemented in a production environment (e.g., using PyTorch, JAX, or a standard systems design).

Rules:
- Maintain a blunt, no-nonsense tone. 
- Eliminate all conversational filler, "I hope this helps," or introductory fluff.
"""

        cold_response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.0
                )
            )

        balanced_response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.7
                )
            )

        creative_response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=1.5
                )
            )
        
        st.info(
        "Comparing the same prompt at temperatures 0.0, 0.7, and 1.5"
        )

        tab1, tab2, tab3 = st.tabs(
            [
                "0.0 Focused",
                "0.7 Balanced",
                "1.5 Creative"
            ]
        )

        with tab1:
            st.markdown(cold_response.text)

        with tab2:
            st.markdown(balanced_response.text)

        with tab3:
            st.markdown(creative_response.text)
        st.session_state.total_queries += 1


        temp_words = (
        len(cold_response.text.split()) +
        len(balanced_response.text.split()) +
        len(creative_response.text.split())
)

        st.session_state.total_words += temp_words

        current_time = datetime.now()

        st.session_state.history.append(
    {
        "time": current_time,
        "feature": feature,
        "input": user_input,
        "response": f"Generated 3 responses (0.0, 0.7, 1.5 temperature)"
    }
)
        if len(st.session_state.history) > 10:
         st.session_state.history.pop(0)
        
        st.stop()
     


    else:

    # PROMPTS

        if feature == "Explain Like I'm 5":

            prompt = f"""
You are a world-class educator specializing in translating complex concepts for young children. 
Explain the following topic to a 5-year-old child: "{user_input}"

Adhere strictly to these rules:
1. **The Playground Rule**: Do not use jargon, abstract concepts, or complex technical terms. If you must use a big word, immediately explain it using an analogy a child can touch, see, or feel on a playground.
2. **Relatable Analogy**: Center the explanation around a single, clear analogy (e.g., comparing the internet to a massive library with fast delivery trucks, or electricity to tiny running ants).
3. **Tone and Style**: Keep the tone enthusiastic, curious, and respectful. Do not use patronizing filler words like "Hey kiddo" or "Guess what?". 
4. **Formatting**: Break the explanation into 2-3 short paragraphs maximum. Use simple, active sentences.
"""

        elif feature == "Teacher Mode":

         prompt = f"""
You are an exceptionally engaging, highly experienced university professor known for making difficult subjects intuitive and crystal clear.
Explain the following topic: "{user_input}"

Structure your response using this pedagogical framework:

1. **The Intuitive Hook (The 'Why It Matters')**: Start with a 2-3 sentence high-level overview. Explain the core utility of this topic before dropping any heavy vocabulary. What problem does it solve?
2. **The Core Concept Breakdown**: Define the topic clearly, then break down the 2-3 absolute essential pillars. Use clear formatting (bolding or bullet points) to make it highly scannable.
3. **The Concrete Blueprint (Example)**: Provide one detailed, real-world example or practical use case. Walk through it step-by-step so the theory becomes visible in practice.
4. **The Common Pitfall**: Explicitly call out one major misconception, common student mistake, or tricky edge case associated with this topic, and clarify why it happens.
5. **Cheatsheet Summary (Revision Notes)**: A highly condensed, high-yield bulleted summary of the absolute non-negotiables a student must memorize for an exam.

Tone: Professional, encouraging, sharp, and authoritative. Avoid generic filler text or patronizing introductory remarks. Move straight into the teaching.
"""

        elif feature == "Mentor Mode":

         prompt = f"""
You are an experienced industry mentor and strategic advisor. Your goal is to help the user not just understand "{user_input}" academically, but master its real-world application, strategic value, and career relevance.

Structure your mentorship guidance into these distinct sections:

1. **The Strategic Perspective (Why it matters)**: Explain the high-level significance of this topic. Why is it worth their time right now? How does it fit into the bigger picture of the industry or modern problem-solving?
2. **Industry Blueprint (Applications)**: Provide concrete examples of how top professionals use this in production or industry right now. Move past basic examples and look at actual, high-value use cases.
3. **The Tactical Learning Path**: Lay out a clear, phased roadmap for moving from beginner to proficient. Explicitly state what they should learn first, what to practice building or doing next, and how to validate their skills.
4. **The Blindspots & Traps**: What are the costly mistakes, architectural flaws, or mental traps that juniors fall into when dealing with this? Share the "lessons learned the hard way" that save weeks of frustration.
5. **Next Actionable Step**: End with one specific, immediate challenge or project idea they can start on today to apply this knowledge.

Tone: Incisive, deeply reasoned, professional, and pragmatic. Do not use generic motivational fluff ("You've got this!"). Focus entirely on actionable, high-density strategic advice.

"""
         
        elif feature == "Professional Rewrite":

         prompt = f"""
You are an expert executive communications consultant. Your task is to transform the provided text into a polished, high-impact professional communication.

Input Text: "{user_input}"

Apply the following transformations:
1. **Diplomatic Precision**: Strip away emotional language, passive-aggression, or informal slang. Replace them with objective, results-oriented phrasing that maintains a firm but respectful tone.
2. **Structural Clarity**: Reorganize the thoughts into a logical flow. Use active voice to ensure accountability and clear ownership of actions.
3. **The "Bottom Line Up Front" (BLUF)**: Ensure the primary purpose or "ask" of the communication is immediately clear within the first two sentences.
4. **Brevity & Density**: Eliminate redundant words and filler phrases. Every sentence must provide unique value.
5. **Contextual Adaptation**: Provide two versions:
    - **Version A (The Email/Memo)**: A formal, structured version suitable for superiors or external clients.
    - **Version B (The Instant Message)**: A concise, direct, yet professional version for platforms like Slack or Teams.

Tone: Sharp, authoritative, and efficient. Do not add conversational filler to your response; provide the rewrites immediately.
"""
         

        elif feature == "Summarizer":

         prompt = f"""
You are an expert research analyst tasked with extracting the core value from dense information. 
Analyze the following text and provide a high-density summary: "{user_input}"

Structure your response into three distinct, scannable sections:

1. **The Bottom Line (TL;DR)**: A single, definitive sentence capturing the absolute core message or conclusion of the text.
2. **Key Takeaways**: A structured list of the most critical points (maximum 5). Each bullet point must begin with a bolded 2-4 word keyword anchor. Focus strictly on hard facts, decisions, or core concepts—eliminate background fluff.
3. **Action Items / Next Steps (If Applicable)**: If the text contains commitments, deadlines, tasks, or implications for future action, list them here explicitly. If none exist, omit this section entirely.

Rules:
- Do not repeat information across sections.
- Keep sentences short, punchy, and in the active voice.
- If the source text is short, do not force 5 bullets; prioritize substance over length.
"""
         
        elif feature == "Grammar Correction":

         prompt = f"""
You are an elite copyeditor and proofreader. Clean up the following text, correcting all grammatical, spelling, punctuation, and structural errors while preserving the user's original intent.

Input Text: "{user_input}"

Provide your output in these three clear sections:

1. **Corrected Version**: The fully polished, error-free text. Do not add introductory fluff; start immediately with the corrected text.
2. **Changelog (What Changed & Why)**: A concise, bulleted list detailing the specific corrections made (e.g., subject-verb agreement, tenses, punctuation, run-on sentences). For each change, provide a brief, logical explanation of the rule applied.
3. **Alternative Suggestions (Optional)**: If a sentence was grammatically correct but awkward, wordy, or structurally weak, offer 1-2 sharper stylistic alternatives.

Rules:
- Never change technical jargon, proper nouns, or formulas unless they are explicitly misspelled.
- If the original text is completely error-free, state: "The text is grammatically flawless." then provide 1-2 stylistic enhancements under Section 3.
"""
         
        elif feature == "Format Converter":

         prompt = f"""
You are an expert data analyst and Markdown formatting specialist. Your task is to extract unstructured or semi-structured data and convert it into a clean, perfectly aligned Markdown table.

Source Data: "{user_input}"

Apply the following data normalization rules:
1. **Header Identification**: Infer the most logical, concise column headers based on the data provided. Capitalize them properly.
2. **Data Consistency**: Ensure every row has the exact same number of columns. If a specific data point is missing for a row, populate that cell with "N/A" or "—" rather than leaving it blank or breaking the table structure.
3. **Sorting**: Sort the rows logically (e.g., alphabetically by the first column, chronologically, or numerically by a primary metric) to maximize readability.
4. **Data Cleanliness**: Strip out redundant text inside the cells (e.g., if a column header is "Price", do not repeat the word "dollars" or the symbol "$" in every single row—keep it in the header or use standard shorthand).
5. **Aesthetic Alignment**: Left-align text columns, center short codes or dates, and right-align numeric values using standard Markdown colon syntax (`| :--- | :---: | ---: |`).

Output only the resulting Markdown table. Do not include conversational filler or introductory text.
"""
         
        elif feature == "Interview Question Generator":

         prompt = f"""
You are an expert technical recruiter and senior engineering hiring manager. Generate a highly targeted, comprehensive interview question bank for the following topic: "{user_input}"

Structure your response into 3 distinct tiers of difficulty (Easy/Conceptual, Medium/Practical, Hard/Architectural). For each tier, provide a mix of core questions.

For each question, provide the output in this strict layout:
*   **Question**: The precise question to ask the candidate.
*   **Target Answer (The 'What')**: The ideal, accurate response expected from a proficient candidate.
*   **Evaluation Criteria (What to look for)**: Specific keywords, mental models, or concepts the candidate *must* mention to score highly.
*   **The Probing Follow-Up**: One deep-dive question to ask if the candidate gives a superficial or rehearsed first answer.

Rules:
- Generate a total of 6-8 exceptionally high-quality questions (2 per difficulty tier) rather than a high volume of generic ones.
- Focus on practical, real-world application and problem-solving over dry definition-matching.
- Include at least one scenario-based behavioral/debugging question where the candidate has to troubleshoot a failure related to the topic.
"""
         
         
    # SHOW PROMPT TEMPLATE

    if show_prompt:
     st.subheader("🔍 Prompt Template")
     st.code(prompt)

    with st.expander("📊 Prompt Analysis"):

     st.write(f"Prompt Length: {len(prompt.split())} words")

     st.write(f"Characters: {len(prompt)}")

     if len(prompt.split()) < 50:
        st.success("Simple Prompt")

     elif len(prompt.split()) < 150:
        st.info("Moderate Prompt")

     else:
        st.warning("Complex Prompt")
    # API CALL

    with st.spinner("Thinking..."):

        try:

            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature
                )
            )

            response_text = response.text

        except Exception as e:
         if "429" in str(e):
          st.error("Gemini rate limit exceeded. Please wait a minute and try again.")
        else:
          st.error(f"Error: {e}")
          st.stop()

    # STATS

    word_count = len(response_text.split())

    st.session_state.total_words += word_count
    st.session_state.total_queries += 1

    current_time = datetime.now()

    st.session_state.history.append(
        {
            "time": current_time,
            "feature": feature,
            "input": user_input,
            "response": response_text
        }
    )

    if len(st.session_state.history) > 10:
        st.session_state.history.pop(0)

    # DISPLAY RESPONSE

    st.success("Response Generated")

    st.markdown("### Response")

    st.markdown(response_text)

    col1, col2, col3 = st.columns(3)

    with col1:
     st.metric("Temperature", temperature)

    with col2:
     st.metric("Prompt Words", len(prompt.split()))

    with col3:
     st.metric("Response Words", word_count)


    st.download_button(
        label="📥 Download Response",
        data=response_text,
        file_name="response.md",
        mime="text/markdown"
    )

# HISTORY

st.divider()

st.subheader("🕒 Generation History")

if len(st.session_state.history) == 0:

    st.info("No history available.")

    

else:

    for item in reversed(st.session_state.history):

        with st.expander(
            f"{item['feature']} | {item['time'].strftime('%H:%M:%S')}"
        ):

            st.write(
                f"Input: {item['input']}"
            )

            st.write(
                item["response"]
            )

            st.divider()
st.divider()

st.markdown("""
### 👨‍💻 About the Developer

**Ashish Kumar**

Mechx | MIT Manipal

🔗 GitHub: https://github.com/ashishh0555

Built using:
- Streamlit
- Gemini API
- Prompt Engineering Techniques
- Temperature Control
""")