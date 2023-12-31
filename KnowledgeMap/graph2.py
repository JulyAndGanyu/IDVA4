# coding=utf-8 
import py2neo 
from py2neo import Graph,Node,Relationship,NodeMatcher,Subgraph
import pandas as pd
from tqdm import tqdm
import csv
graph = Graph("http://localhost:7474", username='neo4j', password='c224510.', run="sub")
graph.delete_all()

zstp = Node('Driving intent-driven connitive mapping',name='Driving intent-driven connitive mapping')
#graph.create(zstp)
scence_1 = Node('Road Category',name='City Roads')
scence_2 = Node('Road Category',name='Expressway')
scence_3 = Node('Road Category',name='Country Road')
relation_1 = Relationship(zstp,'Driving Environment',scence_1)
relation_2 = Relationship(zstp,'Driving Environment',scence_2)
relation_3 = Relationship(zstp,'Driving Environment',scence_3)

position_1 = Node('Position',name='Intersections with traffic Light')
position_2 = Node('Position',name='Intersections with traffic Light')
position_3 = Node('Position',name='General Road')
position_4 = Node('Position',name='Curves')
position_5 = Node('Position',name='Forks')
position_6 = Node('Position',name='Traffic_circle')

relation_4 = Relationship(scence_1,'Location',position_1)
relation_5 = Relationship(scence_1,'Location',position_2)
relation_6 = Relationship(scence_1,'Location',position_3)
relation_7 = Relationship(scence_1,'Location',position_4)
relation_8 = Relationship(scence_1,'Location',position_5)
relation_9 = Relationship(scence_1,'Location',position_6)
relation_10 = Relationship(scence_1,'Location',position_3)
relation_11 = Relationship(scence_2,'Location',position_5)
relation_12 = Relationship(scence_3,'Location',position_2)
relation_13 = Relationship(scence_3,'Location',position_3)
relation_14 = Relationship(scence_3,'Location',position_4)

behavier_1 = Node('Driving Intention',name='Turn_left')
behavier_2 = Node('Driving Intention',name='Straight')
behavier_3 = Node('Driving Intention',name='Turnaround')
behavier_4 = Node('Driving Intention',name='Turn_right')
behavier_5 = Node('Driving Intention',name='Follow')
behavier_6 = Node('Driving Intention',name='Pull_over')
behavier_7 = Node('Driving Intention',name='Overtaking')

relation_15 = Relationship(position_1,'Intentions',behavier_1)
relation_16 = Relationship(position_1,'Intentions',behavier_2)
relation_17 = Relationship(position_1,'Intentions',behavier_3)
relation_18 = Relationship(position_1,'Intentions',behavier_4)

relation_19 = Relationship(position_2,'Intentions',behavier_1)
relation_20 = Relationship(position_2,'Intentions',behavier_2)
relation_21 = Relationship(position_2,'Intentions',behavier_3)
relation_22 = Relationship(position_2,'Intentions',behavier_4)
relation_23 = Relationship(position_3,'Intentions',behavier_5)
relation_24 = Relationship(position_3,'Intentions',behavier_6)
relation_25 = Relationship(position_3,'Intentions',behavier_7)
relation_26 = Relationship(position_4,'Intentions',behavier_1)
relation_27 = Relationship(position_4,'Intentions',behavier_4)
relation_28 = Relationship(position_5,'Intentions',behavier_2)

object_1 = Node('Object',name='Person')
object_2 = Node('Object',name='Cyclist')
object_3 = Node('Object',name='Car')
object_4 = Node('Object',name='Bus')
object_5 = Node('Object',name='Truck')
object_6 = Node('Object',name='Traffic_Light')
object_7 = Node('Object',name='Traffic_Sign')
object_8 = Node('Object',name='Dog')
object_9 = Node('Object',name='Cow')

area_1  = Node('Area',name='left_area_1')
area_2  = Node('Area',name='left_area_2')
area_3  = Node('Area',name='straight_area_1')
area_4  = Node('Area',name='straight_area_2')
area_5  = Node('Area',name='rigth_area_1')
area_5  = Node('Area',name='rigth_area_2')

node_ls = [zstp,scence_1,scence_2,scence_3,position_1,position_2,position_3,position_4,position_5,position_6,behavier_1,behavier_2,behavier_3,behavier_4,behavier_5,behavier_6,behavier_7]
relation_ls =[relation_1,relation_2,relation_3,relation_4,relation_5,relation_6,relation_7,relation_8,relation_9,relation_10,relation_11,relation_12,relation_13,relation_14,relation_15,relation_16,relation_17,relation_18,relation_19,relation_20,relation_21,relation_22,relation_23,relation_24,relation_25,relation_26,relation_27,relation_28]
subgraph = Subgraph(node_ls,relation_ls)

tx = graph.begin()
tx.create(subgraph)
tx.commit()
