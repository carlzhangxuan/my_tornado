"""
====================
Galaxy By Igraph /Graph
====================

"""
__author__ = """\n""".join(['Xuan Zhang'])

__version__ ="""2014-06-05.alpha"""

#!/usr/bin/env python
#coning:utf8

import igraph as ig



def get_graph(ndlist, edlist):
	GI = ig.Graph()
	GI.add_vertices(ndlist)
	GI.add_edges(edlist)
	return GI

def community_det(GI, c = 1):
	if c == 2:
		group = ig.Graph.community_spinglass(GI)
	elif c == 3:
		group = ig.Graph.community_leading_eigenvector(GI)
	elif c == 4:
		group = ig.Graph.community_infomap(GI)
	elif c == 5:
		group = ig.Graph.community_label_propagation(GI)
	else:
		group = ig.Graph.community_multilevel(GI)
	g = 0
	res_dic = {}
	for cls in group:
		for ele in cls:
			res_dic[ele] = g
		g += 1
	return res_dic
