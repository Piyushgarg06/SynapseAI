def add_relationship(graph, source, relation, target):
    graph.setdefault(source,[]).append((relation,target))

def get_relations(graph, concept):
    return graph.get(concept, [])

def get_indirect_relations(graph, source):
    res=[]
    relations = get_relations(graph, source)
    for relation, target in relations:
        if target in graph:
            secondary_relations = get_relations(graph, target)
            for secondary_relation, secondary_target in secondary_relations:
                res.append((relation, target, secondary_relation, secondary_target))
    return res

if __name__ == "__main__":
    graph = {}

    add_relationship(graph, "Python", "used_for", "AI")
    add_relationship(graph, "Python", "used_for", "Web Dev")
    add_relationship(graph, "AI", "uses", "Tensorflow")

    # print(graph)

    relations = get_relations(graph, 'Python')
    if not relations:
        print("No relations were found")
    for relation, target in relations:
        print(f"python --> {relation} --> {target}")

    print(get_indirect_relations(graph, 'Python'))

    

    