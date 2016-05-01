from py2neo import Graph
graph = Graph()


qry = "MATCH (u :USER) RETURN u"

resp = graph.cypher.execute( qry )
data = {}
for itm in resp:
	print (itm[0].properties.keys())
	data[itm[0]['shortname']]={}
	for it in itm[0].properties.keys():
		data[itm[0]['shortname']][it]=itm[0][it]

print(data)		

print("*******************")

print (data['Riley_Rewington'])