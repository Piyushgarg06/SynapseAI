import json
from graph import add_relationship
from extractor import generate_prompt
from extractor import extractor

user_text = "Python is used for AI applications, TensorFlow is used for Deep Learning and FastAPI is used for backend APIs."

prompt = generate_prompt(user_text)
raw_response = extractor(prompt)
cleaned_text = (
    raw_response.text
    .replace("```json", "")
    .replace("```", "")
    .strip()
)
parsed_response = json.loads(cleaned_text)

relationships = parsed_response['relationships']
def process_extraction(graph, relationships):
    for rel in relationships:
        add_relationship(graph, rel['source'], rel['relation'], rel['target'])

    return graph

graph = {}

knowledge_graph = process_extraction(graph, relationships)