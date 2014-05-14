from itertools import *
from header import *

def one_related(name):
	re_list = []
	n_id = redis_db.hget('neo_name2nid', name)
	n_node = neo4j_db.node(n_id)
	for n_n in list(n_node.match(bidirectional=True)):
		print n_n
		re_list.append(n_n.start_node._id) if n_n.start_node._id != n_node._id \
		else re_list.append(n_n.end_node._id)
		#print n_n.start_node._id, n_n.end_node._id
		#if n_n.start_node._id != n_node._id:
		#	re_list.append(n_n.start_node._id)
		#else:
		#	re_list.append(n_n.end_node._id)
	for item in re_list:
		yield redis_db.hget('neo_nid2name', str(item))


def one_x_extend(name,f = 1, t = 3):
	n_id = redis_db.hget('neo_name2nid', name)
	query = 'start n = node('+str(n_id)+') \
		match p = n-[:links*'+str(f)+'..'+str(t)+']->k\
		return p;'
	data, metadata = cypher.execute(neo4j_db, query)
	for i in range(len(data)):
		tmp = []
		for item in data[i][0].nodes:
			tmp.append(redis_db.hget('neo_nid2name', item._id))
		yield tmp

def one_x2_another(name1,name2,f = 3,t = 3):
#def one_x2_another(name1,name2,f = 1,t = 7):
	n_id1 = redis_db.hget('neo_name2nid', name1)
	n_id2 = redis_db.hget('neo_name2nid', name2)
	query = 'start n = node('+str(n_id1)+'),k = node('+str(n_id2)+') \
		match p = n-[*'+str(f)+'..'+str(t)+']->k\
		return p;'
	data, metadata = cypher.execute(neo4j_db, query)
	for i in range(len(data)):
		tmp = []
		for item in data[i][0].nodes:
			tmp.append(redis_db.hget('neo_nid2name', item._id))
		yield tmp

def cast_path_2_node(l):
	nl = set([])
	for recl in list(l):
		for nid in recl:
			nl.add(nid)
	return list(nl)

def cast_path_2_link(l):
	nl = set([])
	for recl in list(l):
		print recl
		for i in range(len(recl)-1):
			nl.add((recl[i],recl[i+1]))
			print recl[i],recl[i+1]
	return list(nl)

def cast_dict_2_gexf(di,pos):
	print pos
	textcon=[]
	header = \
"""<?xml version="1.0" encoding="utf-8"?><gexf version="1.1" xmlns="http://www.gexf.net/1.1draft" xmlns:viz="http://www.gexf.net/1.1draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance">
  <graph defaultedgetype="undirected" mode="static">
  <nodes>
"""
	footer = \
"""    </edges>
  </graph>
</gexf>
"""
	mid = \
"""    </nodes>
    <edges>
"""	
	#print header
	textcon.append(header)
	for node in di['nodes']:
		vx = pos[node['name']][0]*1000
		vy = pos[node['name']][1]*1000
		line ='       <node id="'+node['name']+'" label="'+node['name']+'">\n'
		posi = '	<viz:color b="0" g="0" r="0"/>\n	<viz:position x="'+str(vx-500)+'" y="'+str(vy-500)+'" z="0.0"/>\n	</node>\n'
		print posi
		textcon.append(line+posi)
	#print mid
	textcon.append(mid)
	n = 0
	for link in di['links']:
		line ='       <edge id="'+str(n)+'" source="'+str(link['source'])+'" target="'+str(link['target'])+'" />\n'
		n += 1
		textcon.append(line)
	#print footer
	textcon.append(footer)
	return textcon
