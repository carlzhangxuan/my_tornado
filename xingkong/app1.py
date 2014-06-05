#!/usr/bin/env python
#coding:utf-8

import tornado.httpserver 
import tornado.httpclient
import tornado.ioloop 
import tornado.options 
import tornado.web
import sys
import igraph as ig
from tornado.options import define, options
from function.box import *
from function.graph_tools import *
from function.community_det import *
from itertools import *
from multiprocessing.pool import ThreadPool

 
_workers = ThreadPool(100)

ports = sys.argv[1]
define('port', ports, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		title = 'GALAXY-X'
		self.render("index.html", title = str(title))

class Page_2_Editor(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		nid = self.get_argument('nid')
		title = 'GALAXY-Editor'
		self.render("editor.html", title = title, items = nid, port = ports)

class Page_3_viewer(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		import json, urllib
		graph = self.get_argument('graph')
		d_graph = json.JSONDecoder().decode(graph.encode('utf-8'))
		simple_graph = graph_to_ori(d_graph)
		ndlist = range(len(simple_graph['nodes']))
		edlist = []
		for link in simple_graph['links']:
			edlist.append((link['source'], link['target']))
		GI = get_graph(ndlist, edlist)
		Group = community_det(GI)
		n = 0
		for nd in simple_graph['nodes']:
			nd['commu'] = str(Group[n])
			n += 1
		graph_json_str = json.dumps(simple_graph)
		#self.render("third_file.html", graph_str = graph_json_str)
		self.write(graph_json_str)		
		
class Get_One(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		nid = self.get_argument('nid')
		one_sub = {'nodes':[]}
		res = get_one_step_by_nid(nid)
		for path in res:
			one_sub['nodes'].append(path)
		self.write(one_sub)

class Get_Two(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		nid = self.get_argument('nid')
		#res = get_two_steps_by_nid_cypher(nid)
		self.run_background(func=get_two_steps_by_nid_cypher, args=(nid,), callback=self.on_complete)
	
	def on_complete(self, res):
		res_json ={'nodes':[],'links':[]}
		node_td = {}
		node_list = []
		node_list_d = {}
		edge_list = []
		edge_list_d = []
		group_dict = {}
		#res = get_two_steps_by_nid_cypher(nid)
		for path in res:
			for i in xrange(3):
				group_dict[path[i]] = i
				if path[i] not in node_td:
					node_td[path[i]] = ''
					node_list.append(path[i])
			for i in xrange(2):
				edge_list.append((path[i], path[i+1]))
		for (n, v) in enumerate(node_list):
			node_list_d[v] = n
		for link in edge_list:
			d = {}	
			d["source"] = node_list_d[link[0]]
			d["target"] = node_list_d[link[1]]
			d["value"] = 1
			if d not in edge_list_d:
				res_json["links"].append(d)
				edge_list_d.append(d)
		for node in node_list:
			d = {}
			d["name"] = node
			d["group"] = group_dict[node]
			res_json["nodes"].append(d)	
		self.write(res_json)
		self.finish()
	
	def run_background(self, func, callback, args=(), kwds={}):
        	self.ioloop = tornado.ioloop.IOLoop.instance()
        	def _callback(result):
                	self.ioloop.add_callback(callback,result)
        	_workers.apply_async(func, args, kwds, _callback)

class Syn_Requst(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		import time
		time.sleep(10)
		self.write("10s")

class Asyn_Requst(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		import time
		print 'Asyn...B'
		self.run_background(func=time.sleep, args=(10,), callback=self.on_complete)
	
	def on_complete(self, res):
		self.add_header("Access-Control-Allow-Origin", "*")
		print 'Asyn...A'
		self.write("A10s")
		self.finish()

	def run_background(self, func, callback, args=(), kwds={}):
		self.add_header("Access-Control-Allow-Origin", "*")
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
(r"/", IndexHandler), \
(r"/Editor", Page_2_Editor), \
(r"/GetOne", Get_One), \
(r"/GetTwo", Get_Two), \
(r"/Viewer", Page_3_viewer), \
(r"/SynR", Syn_Requst), \
(r"/AsynR", Asyn_Requst)\
], **settings) 
	http_server = tornado.httpserver.HTTPServer(app) 
	http_server.listen(options.port) 
	tornado.ioloop.IOLoop.instance().start()
