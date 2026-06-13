import json
from graph import add_relationship
from extractor import generate_prompt
from extractor import extractor

# user_text = "The CEO of Apple met Microsoft executives in Seattle."
# user_text = "Google acquired DeepMind after years of collaboration."
# user_text = "Researchers from MIT developed a framework inspired by TensorFlow."
user_text = "I really like Python because it is easy to learn and Python is used for AI."


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
print(knowledge_graph)