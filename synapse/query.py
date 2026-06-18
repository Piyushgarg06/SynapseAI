from .utils import normalize
def get_relations(
    graph:dict, 
    concept:str,
    relation:str | None=None
    ):

    """
    Return all relations for a concept.

    Optionally filter by relation type.
    """

    if not concept.strip() or not concept:
        return []
    concept = normalize(concept)
    relations = graph.get(concept, [])
    if relation is None:
        return relations
    return [
        (relation_name,target)
        for relation_name,target in relations
        if relation_name.lower() == relation.lower()
    ]

def get_indirect_relations(
    graph:dict, 
    source:str
    ):
    if not source.strip() or not source:
        return []
    source = normalize(source)
    res=[]
    relations = get_relations(graph, source)
    for relation, target in relations:
        if target in graph:
            secondary_relations = get_relations(graph, target)
            for secondary_relation, secondary_target in secondary_relations:
                res.append((relation, target, secondary_relation, secondary_target))
    return res
