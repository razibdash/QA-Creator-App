prompt_template="""
  You are a question generation assistant for coding education and technical exam preparation.
Your task is to carefully read through the following technical material and generate a comprehensive list of exam-style questions.
------------
{text}
------------
🔹 Generate questions that:
Cover all key concepts, logic, and syntax

Include theoretical, practical, and application-based questions

Represent realistic questions a programmer might face in interviews, coding tests, or technical exams

🔹 Include a variety of question types:

❓ Conceptual (e.g., What is...? Why is...?)

🧠 Analytical (e.g., Explain how... Describe the behavior of...)

🧮 Predictive (e.g., What is the output of...? What will happen if...?)

🧑‍💻 Code Completion (e.g., Fill in the missing code...)

✅ Multiple Choice (if relevant)

🔹 Do not include answers, explanations, or summaries.
🔹 Do not leave out any important part of the original content.

QUESTIONS:
 1.
 2.
 3.
 4.

"""

refine_template = ("""
You are an expert at creating practice questions based on coding material and documentation.
Your goal is to help a coder or programmer prepare for a coding test.
We have received some practice questions to a certain extent: {existing_answer}.
We have the option to refine the existing questions or add new ones.
(only if necessary) with some more context below.
------------
{text}
------------

Given the new context, refine the original questions in English.
If the context is not helpful, please provide the original questions.
QUESTIONS:
"""
)