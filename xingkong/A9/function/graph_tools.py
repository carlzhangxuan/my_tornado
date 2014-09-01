#!/usr/bin/env python
#coding:utf8

def graph_to_ori(d):
	[[stage1.pop(key) for key in ['x', 'y', 'px', 'py', 'index']] for stage1 in d['nodes']]
	for rec in d['links']:
		rec['source'], rec['target'] = rec['source']['index'], rec['target']['index']
	return d

def graph_to_edlist(d):
	for rec in d['links']:
		yield (rec['source']['index'], rec['target']['index'])

def graph_to_ndlist(d):
	for rec in d['nodes']:
		yield rec['index']

if __name__ == '__main__':
	td = {'nodes':[{'index':0,'name':1,'value':2, 'color':'r', 'x':11, 'y': 22, 'px': 333, 'py': 444},{'index':9,'source':3,'target':4,'x':11, 'y': 22, 'px':0, 'py':2}],'links':[{'l1':1,'l2':2, 'source':{'x':1,'y':2,'px':2,'py':3,'index':4},'target':{'x':1,'y':2,'px':2,'py':3,'index':5}},{'l1':1,'l2':2, 'source':{'index':5,'x':1,'y':2,'px':2,'py':3},'target':{'index':5,'x':1,'y':2,'px':2,'py':3}}]}
#	print graph_to_ori(td)
	for item in graph_to_edlist(td):
		print item
	for item in graph_to_ndlist(td):
		print item
