import os
def writetxt(name,content,mode="w"):
  """
  writetxt(name,content) , write in txt file something  
  """
  content=str(content)
  with open(name, mode) as file:
    file.write(content)
    file.close()

def readtxt(name):
  """
  readtxt(name) , return txt content as array ,element by line 
  """
  content = []
  with open(name, 'r') as file:
    for i in file.readlines():
      content.append(str(i).replace("\n",""))
  return content
def joinWebpage(direccions,webApp,actualapp,url=""):  
    for webroute in direccions:   
      @actualapp.route(url+webroute, endpoint=webroute , methods=['GET','POST'])
      def site():
        return webApp
    return site()
    
def genPreview(name,path):
    txt = f'\n\t@app.route("/{name}")\n\tdef {str(name[:-5]).replace("/","")}():\n\t\treturn render_template("{path}/{name}")'
    return txt

def initMap(dataDir:str)->None:
    """
    initMap(dataDir:str)->None
    create python file with code for add flask,like the code that generates genPreview 
    """
    newCode = """from flask import Flask, render_template
app = Flask(__name__)
class maps():"""
    writetxt(dataDir,newCode)
    #tryng to move to emacs is ... a disasters with tabs 
def validData(txt:str,dicts:list)-> bool:
  """
  validData(txt:str,dicts:list)-> bool
  check if data is valid, if character is in dicts is not valid
  """
  tmp=False
  for i in txt:
    if not i in dicts:
      tmp=False
      break
    else:
      tmp=True
  return tmp

def readRealtime(name:str,sep=";"):
  """
  readRealtime(name:str,sep=";":str)) , is a genteretor return row of csv at iteration 
  """
  with open(name, 'r') as file:
    for i in file.readlines():
      yield i.split(sep)
