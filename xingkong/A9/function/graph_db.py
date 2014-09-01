"""
====================
Galaxy By Neo4J /DB
====================

"""
__author__ = """\n""".join(['Xuan Zhang'])

__version__ ="""2014-06-05.alpha"""

#!/usr/bin/env python

import sys
from itertools import *
from py2neo import neo4j, node, rel, cypher

dbpath_0 = "http://cp01-rdtest-crm-int04.cp01.baidu.com:8890/db/data/"
dbpath_1 = "http://cp01-rdtest-crm-int04.cp01.baidu.com:8892/db/data/"
#neo4j_db = neo4j.GraphDatabaseService(dbpath)

class Word(object):
	
	def __init__(self, node):
		self._node = node

	@classmethod
	def get_names(cls, id_list):
		for ids in id_list:
			name = neo4j_db.node(ids)['name']
			yield name.encode('utf-8')

	@classmethod
	def get_nodes(cls, name_list):
		name_2_id_index = neo4j_db.get_or_create_index(neo4j.Node, "node_auto_index")
		for ids in name_list:
			ids = name_2_id_index.get("name", ids)
			yield ids[0]

	@classmethod
	def get_one_step(cls, name, db_flag = 1):
		if db_flag == 0:
			dbpath = dbpath_0
		elif db_flag == 1:
			dbpath = dbpath_1
		else:
			pass
		neo4j_db = neo4j.GraphDatabaseService(dbpath)
		import math
		name_2_id_index = neo4j_db.get_or_create_index(neo4j.Node, "name")
		target_node = name_2_id_index.get("name", name)[0]
		for rela in target_node.match_outgoing():
			#ans = {rela.end_node['name'].encode('utf-8'):{"weight":rela.end_node['weight']}}
			ans = {"name":rela.end_node['name'].encode('utf-8'),"weight":math.log(rela.end_node['weight']+1,10)*2}
			yield ans

	@classmethod
	def get_two_steps(cls, name, db_flag):
		if db_flag == 0:
			dbpath = dbpath_0
		elif db_flag == 1:
			dbpath = dbpath_1
		else:
			pass
		neo4j_db = neo4j.GraphDatabaseService(dbpath)
		query = "start n = node:name(name ='"+str(name)+"') \
			match n-[]->x-[]->y\
			return n, x, y;"
		#print query
		data, metadata = cypher.execute(neo4j_db, query)
		node_dict = {}
		link_list = [(str(da[0]['name'].encode('utf-8')),str(da[1]['name'].encode('utf-8')),str(da[2]['name'].encode('utf-8'))) for da in data]
		for path in data:
			for i in xrange(3):
				#print path[i]['name'].encode('utf-8')
				if path[i]['name'].encode('utf-8') not in node_dict:
					node_dict[path[i]['name'].encode('utf-8')] = {}
					node_dict[path[i]['name'].encode('utf-8')]['weight'] = path[i]['weight']
		return (link_list, node_dict)
	########return [({\
	########	str(da[0]['name'].encode('utf-8')):{"weight":da[0]['weight']},\
	########	str(da[1]['name'].encode('utf-8')):{"weight":da[1]['weight']},\
	########	str(da[2]['name'].encode('utf-8')):{"weight":da[2]['weight']}\
	########	}) for da in data]
	
	@classmethod
	def get_three_steps(cls, name):
		query = "start n = node:name(name ='"+str(name)+"') \
			match n-[]->x-[]->y-[]->a\
			return n, x, y, a;"
		data, metadata = cypher.execute(neo4j_db, query)
		return [(str(da[0]['name'].encode('utf-8')),str(da[1]['name'].encode('utf-8')),str(da[2]['name'].encode('utf-8')),str(da[3]['name'].encode('utf-8'))) for da in data]

	@classmethod
	def get_one_step_by_nid(cls, nid):
		target_node = neo4j_db.node(int(nid))
		for rela in target_node.match_outgoing():
			yield str(rela.end_node['id'])
	

	@classmethod
	def get_two_steps_by_nid(cls, nid):
		target_node = neo4j_db.node(int(nid))
		for rela in target_node.match_outgoing():
			print rela,
			for relas in rela.end_node.match_outgoing():
				print relas,

	@classmethod
	def get_two_steps_by_nid_cypher(cls, nid):
		query = 'start n = node('+str(nid)+') \
			match n-[]->x-[]->y\
			return n, x, y;'
		data, metadata = cypher.execute(neo4j_db, query)
		return [(str(da[0]['id']),str(da[1]['id']),str(da[2]['id'])) for da in data]
	
		
	@classmethod
	def point_2_point(cls, sp, ep, steps = 1, relat = 'REL'):
		"""5steps -> >20s"""
		query = "start sn = node:name(name ='"+str(sp)+"'), \
			en = node:name(name='"+str(ep)+"')\
			match p = sn-[:"+relat+"*2.."+str(steps)+"]->en\
			return p;"
		print query
		data, metadata = cypher.execute(neo4j_db, query)
		return data
		
	

if __name__ == "__main__":


	name = sys.argv[1]	
#	for rela in Word.get_one_step_by_nid(nid):
#		print rela
#	for rela in Word.get_two_steps_by_nid_cypher(nid):
#		print rela
	for rela in Word.get_one_step(name):
		print rela
#	for rela in Word.get_two_steps(name):
#		print rela
#	for rela in Word.get_three_steps(name):
#		print rela
#	for ids in Word.get_names([1000,2000]):
#		print ids
#	for item in Word.point_2_point('agin', 'and'):
#		print item

