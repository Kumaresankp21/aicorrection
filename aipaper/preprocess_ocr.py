import google.generativeai as genai

# Set up GenAI API
API_KEY = "AIzaSyBO4ly06ph2u9Co1Ag1gYAprWcDNPmW6tc"  # Replace with your API key
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


def preprocess_ocr_question_wise(ocr_text, question_paper_text):
    # print(ocr_text)
    """
    Preprocess OCR content to structure it question-wise and integrate it into the question paper.

    Args:
        ocr_text (str): Raw OCR content.
        question_paper_text (str): Original question paper content.

    Returns:
        str: Question paper with integrated answers in a structured manner.
    """
    try:
        # Define the prompt to organize content question-wise and handle continuation
        prompt = f"""
        The following OCR text is extracted from an answer sheet spread across multiple images. 
        Your task is to match the OCR content to the corresponding question numbers in the question paper 
        and structure it. If an answer is missing for a specific question number, state 
        "(No answer found in the provided text)".

        Original Question Paper:
        {question_paper_text}

        OCR Extracted Text (from multiple images):
        {ocr_text}

        Task:
        1. Match the OCR content to the corresponding question numbers in the question paper.
        2. If a question or its answer spans across multiple images, combine the text for that question.
        3. Do not change, add, or interpret the OCR text in any way. Use it exactly as extracted.
        4. If no content is found for a particular question number, output "(No answer found in the provided text)".
        5. Format the output as follows:

        Output Format:
        Q1: Question from the question paper
        Answer: Extracted answer from OCR or "(No answer found in the provided text)"

        Q2: Question from the question paper
        Answer: Extracted answer from OCR or "(No answer found in the provided text)"
        """

        # Call the Generative AI model
        response = model.generate_content(prompt)

        # Return structured content
        return response.text

    except Exception as e:
        print(f"Error occurred while preprocessing OCR content: {e}")
        return ""


