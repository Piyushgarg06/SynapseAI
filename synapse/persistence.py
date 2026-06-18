import json
GRAPH_FILE = 'graph.json'

def save(graph:dict):
    json_graph = {source: [list(item) for item in relation]
                   for source,relation in graph.items()
    }
    with open(GRAPH_FILE,'w') as f:
        json.dump(json_graph,f)

def load_graph():
    try:
        with open(GRAPH_FILE,'r') as f:
            json_graph = json.load(f)
    except FileNotFoundError:
        return {}

    loaded_graph = {
        source: [tuple(item) for item in relation]
        for source,relation in json_graph.items()
    }
    return loaded_graph
