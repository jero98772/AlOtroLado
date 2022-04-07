import pandas as pd
dataclear=""
SOURCEURL="https://raw.githubusercontent.com/mauriciotoro/ST0245-Eafit/master/proyecto/Datasets/calles_de_medellin_con_acoso.csv"
FILE="calles_de_medellin_con_acoso.csv"
data=pd.read_csv(FILE, on_bad_lines='skip',sep=";")
mean=(sum(pd.read_csv[])/len(a))
print()
for i in range(len(data)): 
  origin=(data["origin"][i][1:-1].split(","))
  destination=(data["destination"][i][1:-1].split(","))
  try:
    dataclear+='{"name":"'+data["name"][i]+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+"]]},"
  except:
    dataclear+='{"name":"'+str(i)+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+"]]},"
def writetxt(name,content):
  """
  writetxt(name,content) , write in txt file something  
  """
  content =str(content)
  with open(name, 'w') as file:
    file.write(content)
    file.close()
writetxt("out.json","["+dataclear[:-1]+"]")
def createNodes(data,name="out.json"):
    dataclear = ""
    for i in range(len(data)): 
        origin = (data["origin"][i][1:-1].split(","))
        destination = (data["destination"][i][1:-1].split(","))
        try:
            dataclear+='{"name":"'+data["name"][i]+'","node":['+origin[0]+","+origin[1]+'],"name2":"'+origin[0]+","+origin[1]+'"},'
        except:
            dataclear+='{"name":"'+str(i)+'","node":['+origin[0]+","+origin[1]+'],"name2":"'+origin[0]+","+origin[1]+'"},'
    writetxt(name,"["+dataclear[:-1]+"]")
#createNodes(data,"nodes_data.json")