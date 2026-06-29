import ollama
def get_ollama_model():
    response = ollama.list()
    model_names=[]
    for model in response.models:
        model_names.append(model.model)
    return model_names
print(get_ollama_model())