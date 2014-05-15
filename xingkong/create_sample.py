#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from py2neo import neo4j, node, rel, cypher

dbpath = "http://localhost:7474/db/data/"

graph_db = neo4j.GraphDatabaseService(dbpath)

n_node = graph_db.find({"name": "Alice"})

print n_node