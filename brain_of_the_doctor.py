# Step 1: Setup GROQ API key from .env file
import os
import base64
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing! Please set it in a .env file.")

# Step 2: Convert image to required format
def encode_image(image_path): 
    #image_path = "acne.jpg"  
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
  
# Step 3: Setup Multimodal LLM
query = """Please describe any visible skin features in this 
image in detail for educational purposes.
Do not provide a medical diagnosis — only describe observations.
.and plese suggest what measures should i take for avoiding the 
condition,and please mention what kind of doctor should i
 appointfor further examination."""
model = "meta-llama/llama-4-scout-17b-16e-instruct"
# Other model options:
# model = "meta-llama/llama-4-maverick-17b-128e-instruct"
# model = "llama-3.2-90b-vision-preview" # Deprecated

def analyze_image_with_query(query, model, encoded_image):
    client = Groq(api_key=GROQ_API_KEY)  # Pass API key here
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }
    ]
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content

