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

def generate_report(result):
    prompt = f"""
    -format the above json response in a nice format without the errors and dont change or interpret it in any way 
    -calculate the user score out of the total score
    - total score would  be marks alloated for part a times number of part a + same for the part b and the part c. accurately calculate dont overtake or undertake
    - part a has 2 marks
    - part b has 13 marks
    - part c has 14 marks
    - calculate the user score and the total score from the json response
    
    Json Data:
    {result}

    return the correct format and the user score out of the tatal max marks
    """
    # Generate evaluation using GenAI
    response = model.generate_content(prompt)

    return response.text 

