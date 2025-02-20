import fitz  # PyMuPDF for working with PDFs
import google.generativeai as genai

# Set your API key
API_KEY = "AIzaSyBO4ly06ph2u9Co1Ag1gYAprWcDNPmW6tc"
genai.configure(api_key=API_KEY)

def upload_file(path, mime_type=None):
    file = genai.upload_file(path=path, mime_type=mime_type)
    return file

def extract_images_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    image_paths = []
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_extension = base_image["ext"]
            image_path = f"page_{page_num+1}_img_{img_index+1}.{image_extension}"
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
            image_paths.append(image_path)
    return image_paths

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




def generate_ocr(path):
# Path to the PDF
    pdf_path = path

    # Extract images from the PDF
    image_paths = extract_images_from_pdf(pdf_path)

    # Upload each image and collect their file metadata
    uploaded_files = [upload_file(path=image_path, mime_type="image/*") for image_path in image_paths]

    response = model.generate_content([
        *uploaded_files,
        "Extract the text exactly as it appears in the images. Do not add, change, or interpret the words in any way."
    ])
    return response.text
