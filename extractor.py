from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
client = genai.Client()

prompt_template = """you are an information extractor system whose work is to extract information in 
the specified schema and return the output in the specified type only 
RETURN ONLY THE VALID JSON

Extract:-
    1. Concepts
    2. Relationships

RETURN OUTPUT USING THIS SCHEMA ONLY
{{
  "concepts": [],
  "relationships": [
    {{
      "source": "",
      "relation": "",
      "target": ""
    }}
  ]
}}
text: {input_text}

BELOW IS AN EXAMPLE ON HOW THE OUTPUT SHOULD LOOK LIKE


text: Python is used for AI and Tensorflow is used in AI
{{
  "concepts": [
    "Python",
    "TensorFlow",
    "AI"
  ],
  "relationships": [
    {{
      "source": "Python",
      "relation": "used_for",
      "target": "AI"
    }},
    {{
      "source": "TensorFlow",
      "relation": "used_in",
      "target": "AI"
    }}
  ]
}}
"""

def generate_prompt(user_text):
  prompt = prompt_template.format(input_text=user_text)
  return prompt

def extractor(prompt):
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=prompt,
  )
  return response

if __name__ == "__main__":
  user_text = "LangChain is used for LLM applications and OpenAI developed GPT models."
  print(type(extractor(generate_prompt(user_text)).text))