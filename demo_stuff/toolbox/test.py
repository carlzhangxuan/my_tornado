from header import *

def print_neo_version():
	print neo4j_db.neo4j_version

def print_redis_version():
	print redis_db.info()


