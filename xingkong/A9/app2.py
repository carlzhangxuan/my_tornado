"""
====================
Galaxy By Tornado /APP
====================

"""
__author__ = """\n""".join(['Xuan Zhang'])

__version__ ="""2014-06-05.alpha"""

__all__ = ['']

#!/usr/bin/env python
#coding:utf-8

import tornado.httpserver 
import tornado.httpclient
import tornado.ioloop 
import tornado.options 
import tornado.web
import sys, math
import igraph as ig
from tornado.options import define, options
from function.graph_db import *
from function.graph_tools import *
from function.community_det import *
from itertools import *
from multiprocessing.pool import ThreadPool

_workers = ThreadPool(100)

define('port', 8888, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		title = 'GALAXY-X'
		self.render("new_file.html", title = str(title))

class Page_2_Editor(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		nid = self.get_argument('nid')
		db_flag = self.get_argument('dbf')
		title = 'GALAXY-Editor'
		self.render("sec_file.html", title = title, items = nid, dbf = db_flag)

class Page_3_viewer(tornado.web.RequestHandler):
	def post(self):
		import json
		self.add_header("Access-Control-Allow-Origin", "*")
		graph = self.get_argument('graph')
		Node_size = float(self.get_argument('Node_size'))
		Link_length = int(self.get_argument('Link_length'))
		Graph_group = int(self.get_argument('Graph_group'))
		items = self.get_argument('items')
		print Node_size, Link_length, Graph_group
		d_graph = json.JSONDecoder().decode(graph.encode('utf-8'))
		simple_graph = graph_to_ori(d_graph)
		ndlist = range(len(simple_graph['nodes']))
		edlist = []
		for link in simple_graph['links']:
			edlist.append((link['source'], link['target']))
		GI = get_graph(ndlist, edlist)
		Group = community_det(GI, Graph_group)
		n = 0
		for nd in simple_graph['nodes']:
			nd['commu'] = str(Group[n])
			nd['size'] = str(Node_size*float(nd['size']))
			n += 1
			print nd
		for lk in simple_graph['links']:
			lk['commu'] = str(Group[lk['target']])
			print lk
		graph_json_str = json.dumps(simple_graph)
		self.render("third_file.html", graph_str = graph_json_str, Link_length = Link_length, items = items)

class Get_Group(tornado.web.RequestHandler):
	def post(self):
		import json
		self.add_header("Access-Control-Allow-Origin", "*")
		graph = self.get_argument('graph')
		#Node_size = float(self.get_argument('Node_size'))
		#Link_length = int(self.get_argument('Link_length'))
		Graph_group = int(self.get_argument('Graph_group'))
		#items = self.get_argument('items')
		d_graph = json.JSONDecoder().decode(graph.encode('utf-8'))
		#print d_graph
		#simple_graph = graph_to_ori(d_graph)
		simple_graph = d_graph
		#print simple_graph
		ndlist = range(len(simple_graph['nodes']))
		edlist = []
		for link in simple_graph['links']:
			edlist.append((link['source'], link['target']))
		GI = get_graph(ndlist, edlist)
		Group = community_det(GI, Graph_group)
		n = 0
		for nd in simple_graph['nodes']:
			nd['commu'] = str(Group[n])
			#nd['size'] = str(Node_size*float(nd['size']))
			n += 1
			#print nd
		for lk in simple_graph['links']:
			lk['commu'] = str(Group[lk['target']])
			#print lk
		graph_json_str = json.dumps(simple_graph)
		#self.render("third_file.html", graph_str = graph_json_str, Link_length = Link_length, items = items)
		self.write(graph_json_str)
		#self.write(Link_length)
		#self.write(items)

class Get_Aj(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		import json, urllib
		graph = self.get_argument('graph')
		d_graph = json.JSONDecoder().decode(graph.encode('utf-8'))
		self.write(d_graph)
		
class Get_One(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		nid = self.get_argument('nid')
		o_db_flag = int(self.get_argument('dbf'))
		#o_db_flag = 1
		one_sub = {'nodes':[]}
		#res = get_one_step_by_nid(nid)
		res = Word.get_one_step(nid, o_db_flag)
		for path in res:
			one_sub['nodes'].append(path)
		self.write(one_sub)

class Get_Two(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		nid = self.get_argument('nid')
		nid = nid.encode('utf-8')
		t_db_flag = int(self.get_argument('dbf'))
		#print t_db_flag
		#self.get_data_asyn(func=get_two_steps_by_nid_cypher, args=(nid,), callback=self.on_complete)
		self.get_data_asyn(func=Word.get_two_steps, args=(nid, t_db_flag), callback=self.on_complete)
		
	def on_complete(self, res):
		res_json ={'nodes':[],'links':[]}
		node_td = {}
		node_list = []
		node_list_d = {}
		node_size = {}
		edge_list = []
		edge_list_d = []
		group_dict = {}
		weight_dict = res[1]
		res = res[0]
		for path in res:
			for i in xrange(3):
				if path[i] not in group_dict or int(group_dict[path[i]]) > i:
					group_dict[path[i]] = str(i)
				if path[i] not in node_td:
					#node_size[path[i]] = 1
					node_td[path[i]] = ''
					node_list.append(path[i])
				else:
					#node_size[path[i]] += 1
					pass
			for i in xrange(2):
				edge_list.append((path[i], path[i+1]))
		for (n, v) in enumerate(node_list):
			node_list_d[v] = n
		for link in edge_list:
			d = {}	
			d["source"] = node_list_d[link[0]]
			d["target"] = node_list_d[link[1]]
			d["value"] = 10
			if d not in edge_list_d:
				res_json["links"].append(d)
				edge_list_d.append(d)
		for node in node_list:
			d = {}
			d["name"] = node
			d["group"] = group_dict[node]
			#s = math.log(node_size[node] + 1, 10)*10 + 5
			s = math.log(weight_dict[node]['weight'] + 1, 2)/2
			d["size"] = str(s)
			res_json["nodes"].append(d)	
		self.write(res_json)
		self.finish()
	
	def get_data_asyn(self, func, callback, args=(), kwds={}):
        	self.ioloop = tornado.ioloop.IOLoop.instance()
        	def _callback(result):
                	self.ioloop.add_callback(callback,result)
        	_workers.apply_async(func, args, kwds, _callback)

if __name__ == "__main__":
	import os
	settings = {
    		"static_path" : os.path.join(os.path.dirname(__file__), "static"),
    		"template_path" : os.path.join(os.path.dirname(__file__), "template"
			)} 
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[\
(r"/index", IndexHandler), \
(r"/sec", Page_2_Editor), \
(r"/GetOne", Get_One), \
(r"/GetTwo", Get_Two), \
(r"/GetA", Get_Aj), \
(r"/third", Page_3_viewer),\
(r"/GetGroup", Get_Group)\
], **settings) 
	http_server = tornado.httpserver.HTTPServer(app) 
	http_server.listen(options.port) 
	tornado.ioloop.IOLoop.instance().start()
