from .utils import normalize
def add_relationship(
    graph:dict,
    source:str,
    relation:str, 
    target:str
    ):

    """
    Add a relationship to the graph.

    Prevents duplicate relationships and normalizes text.
    """
    
    source = normalize(source)
    relation = normalize(relation)
    target = normalize(target)
    tup = (relation,target)

    graph.setdefault(source,[])
    if tup in graph[source]:
        return graph
    else:
        graph[source].append(tup)
    return graph
    