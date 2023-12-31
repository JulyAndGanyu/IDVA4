# coding=utf-8 
import py2neo 
from py2neo import Graph,Node,Relationship,NodeMatcher,Subgraph
import pandas as pd
from tqdm import tqdm
import csv
graph = Graph("http://localhost:7474", username='neo4j', password='c224510.', run="sub")
graph.delete_all()

zstp = Node('复杂场景下的驾驶员注视区域认知图谱',name='复杂场景下的驾驶员注视区域认知图谱')
#graph.create(zstp)
scence_1 = Node('场景',name='城市道路')
scence_2 = Node('场景',name='高速公路')
scence_3 = Node('场景',name='乡间道路')
relation_1 = Relationship(zstp,'驾驶环境',scence_1)
relation_2 = Relationship(zstp,'驾驶环境',scence_2)
relation_3 = Relationship(zstp,'驾驶环境',scence_3)

position_1 = Node('位置',name='有红绿灯的路口')
position_2 = Node('位置',name='无红绿灯的路口')
position_3 = Node('位置',name='非路口路段')

relation_4 = Relationship(scence_1,'所处位置',position_1)
relation_5 = Relationship(scence_1,'所处位置',position_2)
relation_6 = Relationship(scence_1,'所处位置',position_3)


behavier_1 = Node('驾驶行为',name='左转')
behavier_2 = Node('驾驶行为',name='快速直行')
behavier_3 = Node('驾驶行为',name='慢速直行')
behavier_4 = Node('驾驶行为',name='右转')

relation_7 = Relationship(position_1,'驾驶意图',behavier_1)
relation_8 = Relationship(position_1,'驾驶意图',behavier_2)
relation_9 = Relationship(position_1,'驾驶意图',behavier_3)
relation_10 = Relationship(position_1,'驾驶意图',behavier_4)

#Car Person Bike Traffic light Traffic signs  
class_light_left = Node('关注目标的类别',name='关注目标的类别',class_name="Car,Person,Bike,Traffic Light,Traffic Sign",score=[0.3,0.2,0.2,0.3,0])
class_light_right = Node('关注目标的类别',name='关注目标的类别',class_name="Car,Person,Bike,Traffic Light,Traffic Sign",score=[0.3,0.2,0.2,0.3,0])
class_light_straight_fast = Node('关注目标的类别',name='关注目标的类别',class_name="Car,Person,Bike,Traffic Light,Traffic Sign",score=[0.3,0.2,0.2,0.3,0])
class_light_straight_slow = Node('关注目标的类别',name='关注目标的类别',class_name="Car,Person,Bike,Traffic Light,Traffic Sign",score=[0.3,0.2,0.2,0.3,0])

region_light_left = Node('关注区域',name='关注区域',region_name="left,mid,right",score=[0.6,0.3,0.1])
region_light_right = Node('关注区域',name='关注区域',region_name="left,mid,right",score=[0.1,0.3,0.6])
region_light_straight_fast = Node('关注区域',name='关注区域',region_name="left,mid,right",score=[0.1,0.8,0.1])
region_light_straight_slow = Node('关注区域',name='关注区域',region_name="left,mid,right",score=[0.2,0.6,0.2])

relation_11 = Relationship(behavier_1,'注视类别',class_light_left)
relation_12 = Relationship(behavier_1,'注视区域',region_light_left)
relation_13 = Relationship(behavier_4,'注视类别',class_light_right)
relation_14 = Relationship(behavier_4,'注视区域',region_light_right)
relation_15 = Relationship(behavier_2,'注视类别',class_light_straight_fast)
relation_16 = Relationship(behavier_2,'注视区域',region_light_straight_fast)
relation_17 = Relationship(behavier_3,'注视类别',class_light_straight_slow)
relation_18 = Relationship(behavier_3,'注视区域',region_light_straight_slow)

node_ls = [zstp,scence_1,scence_2,scence_3,position_1,position_2,position_3,behavier_1,behavier_2,behavier_3,behavier_4,class_light_left,class_light_right,class_light_straight_fast,class_light_straight_slow,region_light_left,region_light_right,region_light_straight_fast,region_light_straight_slow]
relation_ls =[relation_1,relation_2,relation_3,relation_4,relation_5,relation_6,relation_7,relation_8,relation_9,relation_10,relation_11,relation_12,relation_13,relation_14,relation_15,relation_16,relation_17,relation_18]
subgraph = Subgraph(node_ls,relation_ls)

tx = graph.begin()
tx.create(subgraph)
tx.commit()
