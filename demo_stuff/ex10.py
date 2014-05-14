#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.httpserver 
import tornado.ioloop 
import tornado.options 
import tornado.web
import networkx as nx
from tornado.options import define, options
from toolbox.one_related import *
from itertools import *
from random import choice

define("port", default=8889, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		n_name = self.get_argument('cnode')
		lt = one_related(n_name)
		rtid = {'da':[]}
		for item in lt:
			rtid['da'].append({'n_name':str(item),'label':str(item)})	
		self.write(rtid)

class Multilayer(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		n_name = self.get_argument('cnode')
		print n_name
		lt = list(one_x_extend(n_name))
		rtid = {"nodes":[],"links":[]}
		for item in cast_path_2_node(lt):
			tmp = {"name":str(item)}
			rtid["nodes"].append(tmp)
		cdict = {}
		for item in enumerate(cast_path_2_node(lt)):
			cdict[str(item[1])] = item[0]
		for item in cast_path_2_link(lt):
			tmp = {"source":cdict[item[0]],"target":cdict[item[1]]}
			rtid["links"].append(tmp)
		
		self.write(rtid)
		print rtid, cdict

class Point_2_point(tornado.web.RequestHandler):
	def get(self):
		self.add_header("Access-Control-Allow-Origin", "*")
		s = self.get_argument('s')
		t = self.get_argument('t')
		lt = list(one_x2_another(s, t))
		rtid = {"nodes":[],"links":[]}
		for item in cast_path_2_node(lt):
			tmp = {"name":str(item)}
			rtid["nodes"].append(tmp)
		cdict = {}
		for item in enumerate(cast_path_2_node(lt)):
			cdict[str(item[1])] = item[0]
		for item in cast_path_2_link(lt):
			tmp = {"source":cdict[item[0]],"target":cdict[item[1]]}
			rtid["links"].append(tmp)
		self.write(rtid)
		print rtid, cdict

class Gexf_gen(tornado.web.RequestHandler):
	def get(self):
		G = nx.Graph()
		self.add_header("Access-Control-Allow-Origin", "*")
		n_name = self.get_argument('cnode')
		lt = list(one_x_extend(n_name))
		rtid = {"nodes":[],"links":[]}
		for item in cast_path_2_node(lt):
			tmp = {"name":str(item)}
			rtid["nodes"].append(tmp)
		cdict = {}
		for item in enumerate(cast_path_2_node(lt)):
			cdict[str(item[1])] = item[0]
		for item in cast_path_2_link(lt):
			G.add_edge(item[0],item[1])
			tmp = {"source":item[0],"target":item[1]}
			rtid["links"].append(tmp)
		co = choice('01')
		#pos = nx.spring_layout(G, scale=1.0)
		if co == '0':
			pos = nx.circular_layout(G)
		elif co == '1':
			pos = nx.spring_layout(G)
		else:
			pos = nx.shell_layout(G)
		text = ''.join(cast_dict_2_gexf(rtid,pos))
		print text
		self.write(text)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r"/", IndexHandler),(r"/Multilayer",Multilayer),(r"/Point_2_point",Point_2_point),(r"/Gexf_gen",Gexf_gen)]) 
	http_server = tornado.httpserver.HTTPServer(app) 
	http_server.listen(options.port) 
	tornado.ioloop.IOLoop.instance().start()
