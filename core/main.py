#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
alOtrolado - 2022 - por jero98772
alOtrolado - 2022 - by jero98772
"""
from flask import Flask, render_template, request, flash, redirect,json,render_template_string
import pandas as pd
import pydeck as pdk
import networkx as nx

import os
import json
import datetime

from core.tools.tools import *

TEMPLATEDIR="templates/"
MAPS="core/maps.py"
MAPWEBADRESS="/maps/"
MAPSDIR="core/templates"+MAPWEBADRESS
FILES = os.listdir(MAPSDIR)

DATACSVFILE="https://raw.githubusercontent.com/entifais/ST0245-Plantilla/master/proyecto/codigo/alOtroLado/data/calles_de_medellin_con_acoso.csv"
DATACSVFILE="data/calles_de_medellin_con_acoso.csv"
DATANODESJSON="core/data/nodes_data.json"
DATAJSON="core/data/medellin_data.json"
DATACOMPLETE="core/data/data_csv.csv"
app = Flask(__name__)
if os.path.isfile(MAPS):
    if readtxt(MAPS)=="":
        initMap(MAPS)
    try:
        from .maps import maps 
        from .maps import app as appmaps
        print(FILES)
        joinWebpage(FILES,appmaps,app,"/")
        print("not try error")
    except:
        print("error open file")
else:
    initMap(MAPS)
#https://github.com/jero98772/B-FeelLog/blob/main/core/main.py
class webpage():
    #web app 
    @app.route("/",methods=["GET","POST"])
    def index(): 
        msg=""
        data=configData(DATAJSON).getData()
        maps=configMap(data)

        if request.method=="POST":
            validateTxt="1234567890.,- []'"
            source=request.form["source"]
            target=request.form["target"]

            if target=="" or source=="" or  not (validData(target,validateTxt) and  validData(source,validateTxt)):
                msg="Datos invalidos"
            
            else:
                print
                data=configData(DATAJSON).getData()
                maps=configMap(data)
                print(source,target)
                newPath=pathsX(data,"["+str(source)+"]", "["+str(target)+"]",graphX)
                #newPath=pathsX(DATACOMPLETE,str(source),str(target),fastgraphX)
                newPath.dijkstra()
                nodesData=newPath.getData()                
                salt=str(datetime.datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".","")
                fileName="map"+str(salt)+".html"

                serveMapCode=genPreview(fileName,"maps")
                writetxt(MAPS,serveMapCode,"a")

                configMap.newPath(nodesData)
                layers=[maps.getPathMap(),maps.getnodesMap(),configMap.newPath(nodesData)]
                maps.genMapMultlayer(MAPSDIR+fileName,layers)
                funcs=[writetxt,maps.genMapMultlayer]
                args=[[MAPS,serveMapCode,"a"],[MAPSDIR+fileName,layers]]
                return redirect("/ineedtimetowork/"+fileName)
        return render_template("index.html",msg=msg)

    #information web page
    @app.route("/about.html")
    def about():
        return render_template("about.html")

    #geografic visualisations
    @app.route("/mapBase.html")
    def webMapBase():
        return render_template("mapBase.html")
    @app.route("/dotsdir.html")
    def dotsdir():
        return render_template("mapsplots/dotsdir.html")  
    @app.route("/heatmap.html")
    def heatmap():
        return render_template("mapsplots/heatmap.html")
    @app.route("/medellingraph.html")
    def medellingraph():
        return render_template("mapsplots/medellingraph.html")
    
    #tests 
    @app.route("/concord2tesoro.html")
    def concord2tesoro():
        return render_template("examples/concord2tesoro.html")
    @app.route("/eafit_santafe.html")
    def eafit_santafe():
        return render_template("examples/eafit_santafe.html")
    @app.route("/eafit2medellin.html")
    def eafit2medellin():
        return render_template("examples/eafit2medellin.html")
    @app.route("/antioquia2nacional.html")
    def antioquia2nacional():
        return render_template("examples/antioquia2nacional.html")
    @app.route("/nacional2luisamigo.html")
    def nacional2luisamigo():
        return render_template("examples/nacional2luisamigo.html")

        
    #data
    @app.route("/data.json")
    def webDataJson():
        data=json.dumps(readtxt(DATAJSON))
        response = app.response_class(response=data,mimetype='application/json')
        return response
    @app.route("/nodes.json")
    def webDataNodes():
        data=json.dumps(readtxt(DATANODESJSON))
        response = app.response_class(response=data,mimetype='application/json')
        return response

    #redirection to make time,for fix error 
    @app.route("/ineedtimetowork/<string:fileName>",methods=["GET","POST"])
    def redirected(fileName):
        return "<h1>please wait, my algoritm is very faster for this web</h1><script>setTimeout(function () {window.location.href = '/"+fileName+"';}, 1);</script>"
        return redirect(fileName)
  
 
class configData:
    def __init__(self,file,sep=";"):
        self._data=""
        if file[-4:]==".csv":
            self._data = pd.read_csv(file,sep=";")
        if file[-5:]==".json":
            self._data = pd.read_json(file)

    #if needed download, you can pass a url remote acces of data
    def downloadCsv(self):
        self._data.to_csv(index=False)

    def downloadJson(self):
        self._data.to_json(index=False)

    def getData(self):
        return self._data
    #code for clear data     
    def clearDataJsonRoutes(data,name="out.json"):
        dataclear = ""
        for i in range(len(data)): 
            origin = (data["origin"][i][1:-1].split(","))
            destination = (data["destination"][i][1:-1].split(","))
            try:
                dataclear+='{"name":"'+data["name"][i]+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+"]]},"
            except:
                dataclear+='{"name":"'+str(i)+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+"]]},"
        writetxt(name,"["+dataclear[:-1]+"]")
    
    def clearAllDataJson(data,name="out.json"):
        dataclear = ""
        for i in range(len(data)): 
            origin = (data["origin"][i][1:-1].split(","))
            destination = (data["destination"][i][1:-1].split(","))
            try:
                dataclear+='{"name":"'+data["name"][i]+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+']],"node":['+origin[0]+","+origin[1]+'],"harassmentRisk":'+str(data["harassmentRisk"][i]).replace("nan","0")+',"length":'+str(data["length"][i])+'},'
            except:
                dataclear+='{"name":"'+str(i)+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+']],"node":['+origin[0]+","+origin[1]+'],"harassmentRisk":0,"length":'+str(data["length"][i])+'},'
        writetxt(name,"["+dataclear[:-1]+"]")

    def createNodes(self,data,name="data/out.json"):
        data=self.data
        dataclear = ""
        for i in range(len(data)): 
            origin = (data["origin"][i][1:-1].split(","))
            destination = (data["destination"][i][1:-1].split(","))
            try:
                dataclear+='{"name":"'+data["name"][i]+'","node":['+origin[0]+','+origin[1]+']},'
            except:
                dataclear+='{"name":"'+str(i)+'","node":['+origin[0]+','+origin[1]+']},'
        writetxt(name,"["+dataclear[:-1]+"]")
    def cretejson(self,fileName="data/"):
        import numpy as np

        if fileName=="data/":
            salt=str(datetime.datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".","")
            fileName="data"+str(salt)
        mean=np.mean(self._data["harassmentRisk"])
        for i in range(len(self._data)):
            length=self._data["length"][i]
            origin = (self._data["origin"][i][1:-1].split(","))
            destination = (self._data["destination"][i][1:-1].split(","))
            node=[str(self._data["origin"][i][1:-1])]
            edges="["+str(node)+",["+str(self._data["destination"][i][1:-1])+"]]"
            weights=(self._data["harassmentRisk"][i]*length)/length

        if np.isnan(self._data["harassmentRisk"][i]) and  (self._data["name"][i]=="nan" or type(self._data["name"][i])==type(0.0)):
            weights=(mean*length)/length
            newdata+='{"name":"'+str(i)+'","origin":"'+str(self._data["origin"][i])+'","destination":"'+str(self._data["destination"][i])+'","length":"'+str(self._data["length"][i])+'","oneway":"'+str(self._data["oneway"][i])+'","harassmentRisk":"'+str(mean)+'","geometry":"'+str(self._data["geometry"][i])+'","weights":"'+str(weights)+'","edges":"'+str("[["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1])+']]","node":"['+origin[0]+","+origin[1]+']"},'
        
        elif self._data["name"][i]=="nan" or type(self._data["name"][i])==type(0.0) :
            newdata+='{"name":"'+str(i)+'","origin":"'+str(self._data["origin"][i])+'","destination":"'+str(self._data["destination"][i])+'","length":"'+str(self._data["length"][i])+'","oneway":"'+str(self._data["oneway"][i])+'","harassmentRisk":"'+str(self._data["harassmentRisk"][i])+'","geometry":"'+str(self._data["geometry"][i])+'","weights":"'+str(weights)+'","edges":"'+str("[["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1])+']]","node":"['+origin[0]+","+origin[1]+']"},'
        
        elif np.isnan(self._data["harassmentRisk"][i]):
            weights=(mean*length)/length
            newdata+='{"name":"'+self._data["name"][i]+'","origin":"'+str(self._data["origin"][i])+'","destination":"'+str(self._data["destination"][i])+'","length":"'+str(self._data["length"][i])+'","oneway":"'+str(self._data["oneway"][i])+'","harassmentRisk":"'+str(mean)+'","geometry":"'+str(self._data["geometry"][i])+'","weights":"'+str(weights)+'","edges":"'+str("[["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1])+']]","node":"['+origin[0]+","+origin[1]+']"},'

        else:
            newdata+='{"name":"'+self._data["name"][i]+'","origin":"'+str(self._data["origin"][i])+'","destination":"'+str(self._data["destination"][i])+'","length":"'+str(self._data["length"][i])+'","oneway":"'+str(self._data["oneway"][i])+'","harassmentRisk":"'+str(self._data["harassmentRisk"][i])+'","geometry":"'+str(self._data["geometry"][i])+'","weights":"'+str(weights)+'","edges":"'+str("[["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1])+']]","node":"['+origin[0]+","+origin[1]+']"},'
        writetxt(fileName+".json","["+newdata[:-1]+"]")

    def cretecsv(self,fileName="data/"):
        import numpy as np

        newdata="name;origin;destination;length;oneway;harassmentRisk;geometry;weights;edges;node\n"
        mean=np.mean(self._data["harassmentRisk"])

        if fileName=="data/":
            salt=str(datetime.datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".","")
            fileName="data"+str(salt)
        for i in range(len(self._data)):
            length=self._data["length"][i]
            node=[str(self._data["origin"][i][1:-1])]
            edges="["+str(node)+",["+str(self._data["destination"][i][1:-1])+"]]"
            weights=(self._data["harassmentRisk"][i]*length)/length

            if np.isnan(self._data["harassmentRisk"][i]) and  (self._data["name"][i]=="nan" or type(self._data["name"][i])==type(0.0)):
                weights=(mean*length)/length
                newdata+=str(i)+";"+str(self._data["origin"][i])+";"+str(self._data["destination"][i])+";"+str(self._data["length"][i])+";"+str(self._data["oneway"][i])+";"+str(mean)+";"+str(self._data["geometry"][i])+";"+str(weights)+";"+str(edges)+";"+";"+str(node)+"\n"
            
            elif self._data["name"][i]=="nan" or type(self._data["name"][i])==type(0.0) :
                newdata+=str(i)+";"+str(self._data["origin"][i])+";"+str(self._data["destination"][i])+";"+str(self._data["length"][i])+";"+str(data["oneway"][i])+";"+str(self._data["harassmentRisk"][i])+";"+str(self._data["geometry"][i])+";"+str(weights)+";"+str(edges)+";"+";"+str(node)+"\n"
            
            elif np.isnan(self._data["harassmentRisk"][i]):
                weights=(mean*length)/length
                newdata+=str(data["name"][i])+";"+str(data["origin"][i])+";"+str(data["destination"][i])+";"+str(data["length"][i])+";"+str(data["oneway"][i])+";"+str(mean)+";"+str(data["geometry"][i])+";"+str(weights)+";"+str(edges)+";"+";"+str(node)+"\n"
            
            else:
                newdata+=str(data["name"][i])+";"+str(data["origin"][i])+";"+str(data["destination"][i])+";"+str(data["length"][i])+";"+str(data["oneway"][i])+";"+str(data["harassmentRisk"][i])+";"+str(data["geometry"][i])+";"+str(weights)+";"+str(edges)+";"+";"+str(node)+"\n"
            writetxt(fileName+".csv",newdata)

class graphX():
    """
    create graph with pandas data
    """
    def __init__(self,data):
        self.graph=nx.Graph()
        for i in range(len(data)):
            node=data["node"][i]
            weight=(data["length"][i])
            self.graph.add_edge(str(data["edges"][i][0]),str(data["edges"][i][1]),weight=weight)
            self.graph.add_node(str(node))

class fastgraphX():
    """
    create graph while read file
    """
    def __init__(self,file):
        self.graph=nx.Graph()
        i=0
        for data in readRealtime(file,sep=";"): 
            if i==0:
                i+=1
            else:
                edge=data[-2][2:-2].split("],[")
                self.graph.add_edge(str(edge[0]),str(edge[1]),weight=float(data[-3]))
                self.graph.add_node(str(data[-1][:-1]))
            i+=1

class pathsX(graphX):
    def __init__(self,data,source,target,graphtype):
        """
        class for chose shorts path algoritms
        modes
        fast
        nofast
        """
        super().__init__(data)
        self._source=source
        self._target=target
    def dijkstra(self):
        self._nodes=nx.dijkstra_path(self.graph, self._source, self._target, weight='weight')

    def dijkstraNoW(self):
        self._nodes=nx.dijkstra_path(self.graph, self._source, self._target, weight=None)

    def bellmanford(self):
        self._nodes=nx.shortest_path(self.graph, self._source, self._target, weight='weight', method='bellman-ford')

    def getData(self):
        """
        return data from shorts path algoritms
        """
        pathdf=pd.DataFrame([{"name":"path","path":[eval(i) for i in self._nodes]}])
        return pathdf
    def printg(self):
        print(self.graph.to_string())

#debugs code no erase
#self._nodes=nx.dijkstra_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5572602, 6.2612576]", weight=None)
#self._nodes=nx.shortest_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight=None, method='bellman-ford')
#nodes=nx.shortest_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight='weight', method='dijkstra')
#nodes=nx.shortest_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight=None, method='dijkstra')
#self._nodes=nx.dijkstra_path(self.graph, "[-75.6909483, 6.338773]", "[-75.5572602, 6.2612576]", weight=None)

class configMap:
    """
    class for draw in map
    """
    def __init__(self,data):

        self.emptyMap = pdk.Layer(
            type="PathLayer",
            data="",
            pickable=True,
            get_color=(0,155,0),
            width_scale=1,
            width_min_pixels=1,
            get_path="edges",
            get_width=1,
        )

        self.pathMap = pdk.Layer(
            type="PathLayer",
            data=data,
            pickable=True,
            get_color=(0,155,0),
            width_scale=1,
            width_min_pixels=1,
            get_path="edges",
            get_width=2,
        )

        self.nodesMap = pdk.Layer(
            "ScatterplotLayer",
            data=data,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position="node",
            get_radius=1,
            get_fill_color=[137, 36, 250],
            get_line_color=[0, 0, 0],
        )

    def newPath(data,tag="path",color=(0,15,205)):
        newPath = pdk.Layer(
            type="PathLayer",
            data=data,
            pickable=False,
            get_color=color,
            width_scale=5,
            width_min_pixels=5,
            get_path=tag,
            get_width=5,
        )
        return newPath

    def genMapMultlayer(self,fileName,layers:list):
        view = pdk.ViewState(latitude=6.256405968932449, longitude= -75.59835591123756, pitch=40, zoom=12)
        mapCompleate = pdk.Deck(layers=layers, initial_view_state=view)
        mapCompleate.to_html(fileName)
    
    def getEmptyMap(self):return self.emptyMap
    def getPathMap(self):return self.pathMap
    def getnodesMap(self):return self.nodesMap


