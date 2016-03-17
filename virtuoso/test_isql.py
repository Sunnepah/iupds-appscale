from isqlwrapper import ISQLWrapper

isql = ISQLWrapper('33.33.33.13', 'dba', 'dba')
username = 'ade'
result = isql.execute_cmd("select count(*) from sys_users;")
# result = isql.execute_cmd("GRANT SPARQL_SELECT TO %s;" % username)
# result = isql.execute_cmd("SPARQL CLEAR GRAPH <%s>" % 'http://mygraph.com')

print result
