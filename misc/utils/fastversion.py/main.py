import networkx as nx
import pydeck as pdk

def readRealtime(name:str,sep=";":str):
  """
  readRealtime(name:str,sep=";":str)) , is a genteretor return row of csv at iteration 
  """
  with open(name, 'r') as file:
    for i in file.readlines():
      yield i.split(sep)

def main():
	Grafo = nx.Graph()
	#...weigths,edges,node
	ii=0
	for i in readRealtime("data_csv.csv",sep=";"): 
		if ii==0:
			pass
		else:
			edge=eval(i[-2])#.split("],[")
			Grafo.add_edge(str(edge[0]),str(edge[1]),weight=i[-3])
			Grafo.add_node(str(i[-1][:-2]))
		ii+=1
	print(nx.to_dict_of_dicts(Grafo))

main()