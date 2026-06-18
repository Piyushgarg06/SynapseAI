from .persistence import save,load_graph
from .query import get_relations, get_indirect_relations
from .processor import process_text
from .graph import add_relationship
from .extractor import extractor
class Synapse:
    def __init__(self):
        self.graph={}
        self.extractor=extractor


    def save(self):
        save(self.graph)


    def load_graph(self):
        self.graph = load_graph()


    def get_relations(
        self,
        concept:str,
        relation:str | None=None
        ):
        return get_relations(self.graph,concept)


    def get_indirect_relations(self,source:str):
        return get_indirect_relations(self.graph,source)


    def add(self,text:str):
        if not text.strip():
            return
        parsed_response=process_text(
            text,
            self.extractor
            )
        relationships = parsed_response['relationships']
        for rel in relationships:
            add_relationship(self.graph, rel['source'], rel['relation'], rel['target'])