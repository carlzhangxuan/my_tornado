#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from py2neo import neo4j, node, rel, cypher
import redis

neo4j_db = neo4j.GraphDatabaseService()
redis_db = redis.Redis(host='localhost', port=6379, db=0)

