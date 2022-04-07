import pandas as pd
dataclear=""
SOURCEURL="https://raw.githubusercontent.com/mauriciotoro/ST0245-Eafit/master/proyecto/Datasets/calles_de_medellin_con_acoso.csv"
FILE="calles_de_medellin_con_acoso.csv"

data=pd.read_csv(FILE, on_bad_lines='skip',sep=";")#.head(100)
#print(data["harassmentRisk"])
#exit()
for i in range(len(data)): 
  origin=(data["origin"][i][1:-1].split(","))
  destination=(data["destination"][i][1:-1].split(","))
  try:
    dataclear+='{"name":"'+data["name"][i]+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+']],"node":['+origin[0]+","+origin[1]+'],"harassmentRisk":'+str(data["harassmentRisk"][i]).replace("nan","0")+',"length":'+str(data["length"][i])+'},'
  except:
    dataclear+='{"name":"'+str(i)+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+']],"node":['+origin[0]+","+origin[1]+'],"harassmentRisk":0,"length":'+str(data["length"][i])+'},'
def writetxt(name,content):
  """
  writetxt(name,content) , write in txt file something  
  """
  content =str(content)
  with open(name, 'w',encoding="utf8") as file:
    file.write(content)
    file.close()
writetxt("graph_medellin_no_private_data.json","["+dataclear[:-1]+"]")
#writetxt("graph_medellin_data.json","["+dataclear[:-1]+"]")