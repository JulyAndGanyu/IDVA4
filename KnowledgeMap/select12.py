from py2neo import NodeMatcher,RelationshipMatcher
from py2neo import Graph, Node, Relationship
import pandas as pd
from tqdm import tqdm
graph = Graph("http://localhost:7474", username='neo4j', password='c224510.')


node_matcher = NodeMatcher(graph)
relationship_matcher =  RelationshipMatcher(graph)
node1 = list(node_matcher.match("DS").where("_.name =~'straight.*'"))
node2 = 
relationship = relationship_matcher.match((node1,node2)
