import google.generativeai as genai
import json

# Configure Google Generative AI
API_KEY = "AIzaSyBO4ly06ph2u9Co1Ag1gYAprWcDNPmW6tc"
genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)


def evaluate_exam_with_ocr_to_json(ocr_content, answer_key):
    """
    Use GenAI to evaluate OCR content directly for an exam and return results in JSON format.

    Args:
        ocr_content (str): The entire OCR preprocessed content containing the question paper and student's answers.
        answer_key (list): List of correct answers for each question.

    Returns:
        dict: Evaluation results in JSON format.
    """
    # Create the evaluation prompt
    prompt = f"""
    You are evaluating an exam paper where the questions and answers have been extracted from an OCR system. Your task is to:

    1. **Identify and separate** each question and its corresponding student answer from the provided OCR content.
    2. **Match** each question with the correct answer from the provided answer key.
    3. **Assign marks** based on the following rules:
    - **Part A questions (Short Answers) → 2 Marks**
    - **Part B questions (Long Answers) → 13 Marks**
    - **Part C questions (Detailed Explanations) → 14 Marks**
    - Award **full marks** if the student's answer is highly similar to the correct answer and provides sufficient depth (measured by the number of lines).
    - Award **partial marks** if the answer is somewhat correct but lacks key details.
    - Award **zero marks** if the answer is incorrect, irrelevant, or missing.

    4. **Ensure accuracy**: Do not introduce extra questions or duplicate any.

    ### **Evaluation Criteria**  
    For each question, return a **JSON object** with:
    - `"question_number"`: The number of the question.
    - `"question"`: The extracted question text.
    - `"student_answer"`: The student's response.
    - `"correct_answer"`: The expected answer from the answer key.
    - `"marks_awarded"`: The marks assigned based on evaluation.
    - `"max_marks"`: The appropriate maximum marks (2, 13, or 14 based on the section).
    - `"reason"`: Justification for the marks awarded.

    ### **Input Variables:**
    - **OCR Content:** `{ocr_content}`
    - **Answer Key:** `{answer_key}`
    """



    # Generate evaluation using GenAI
    response = model.generate_content(prompt)

    return response.text


