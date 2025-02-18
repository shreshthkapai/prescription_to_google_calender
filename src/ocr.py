import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
from PIL import Image
import re

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4o"

openai = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def extract_text_from_image(image_path):
    response = openai.chat.completions.create(
        model = MODEL,
        max_tokens = 1000,
        messages=[
            {
                "role": "system", "content": """You are an OCR assistant that extracts text from medical
                                                prescription images. Extract all the text exactly as it 
                                                appears in the prescription image. Dont include images. Only 
                                                extract text."""
                                                },
                  {
                      "role": "user",
                      "content": [
                      {
                        "type": "text",
                        "text": "Extract text from this image: "
                       },
                       {
                         "type": "image_url",
                         "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(image_path)}"
                                }
                            }
                        ]
                    }
                ]
            )
    return response.choices[0].message.content

import re

def clean_text(text):
    text = re.sub(r'-', ' ', text)
    
    text = re.sub(r'[^\w\s.,()%/]', '', text)

    text = re.sub(r'\s+', ' ', text)

    text = re.sub(r'\n+', '\n', text)

    text = re.sub(r'([.,])([^\s])', r'\1 \2', text)

    return text.strip()



