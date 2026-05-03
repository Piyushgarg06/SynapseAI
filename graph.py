def add_relationship(graph, source, relation, target):
    graph.setdefault(source,[]).append((relation,target))

graph = {}

add_relationship(graph, "Python", "used_for", "AI")
add_relationship(graph, "Python", "used_for", "Web Dev")
add_relationship(graph, "TensorFlow", "used_for", "Deep Learning")

print(graph)