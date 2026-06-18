import json
from .extractor import generate_prompt

def process_text(user_text:str,extractor):

    """
    Extract structured relationships from text using an LLM.
    """

    prompt = generate_prompt(user_text)
    raw_response = extractor(prompt)
    cleaned_text = (
        raw_response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )
    try:
        parsed_response = json.loads(cleaned_text)
        return parsed_response
    except json.JSONDecodeError:
        return {
            "concepts":[],
            "relationships":[]
        }