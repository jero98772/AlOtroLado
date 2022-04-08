#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
alOtrolado - 2022 - por jero98772
alOtrolado - 2022 - by jero98772
"""
from flask import Flask, render_template, request, flash, redirect,json
import pandas as pd
import pydeck as pdk
import networkx as nx

import os
import json
import datetime
import time

from core.tools.tools import *

TEMPLATEDIR="templates/"
MAPS="core/maps.py"
MAPWEBADRESS="/maps/"
MAPSDIR="core/templates"+MAPWEBADRESS
FILES = os.listdir(MAPSDIR)

DATACSVFILE="https://raw.githubusercontent.com/entifais/ST0245-Plantilla/master/proyecto/codigo/alOtroLado/data/calles_de_medellin_con_acoso.csv"
DATACSVFILE="data/calles_de_medellin_con_acoso.csv"
DATAJSON="core/data/graph_medellin_all_data.json"

app = Flask(__name__)
if os.path.isfile(MAPS):
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
    @app.route("/",methods=["GET","POST"])
    def index(): 
        msg=""
        if request.method=="POST":
            validateTxt="1234567890.,- "
            source=request.form["source"]
            target=request.form["target"]
            if target=="" or source=="" or  not (validData(target,validateTxt) and  validData(source,validateTxt)):
                msg="Datos invalidos"
            else:
                data=configData(DATAJSON).getData()
                maps=configMap(data)
                newPath=pathsX(data,"["+str(source)+"]", "["+str(target)+"]")
                newPath.dijkstraNoW()
                nodesData=newPath.getData()
                
                salt=str(datetime.datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".","")
                fileName="map"+str(salt)+".html"

                configMap.newPath(nodesData)
                layers=[maps.getPathMap(),maps.getnodesMap(),configMap.newPath(nodesData)]
                maps.genMapMultlayer(MAPSDIR+fileName,layers)
                serveMapCode=genPreview(fileName,"maps")
                print(serveMapCode)
                writetxt(MAPS,serveMapCode,"a")
                return redirect(fileName)  
        return render_template("index.html",msg=msg)

    @app.route("/about")
    def about():
        return render_template("about.html")
    @app.route("/mapBase")
    def webMapBase():
        return render_template("mapBase.html")
    @app.route("/dotsdir.html")
    def dotsdir():
        return render_template("dotsdir.html")  
    @app.route("/data.json")
    def webData():
        data=json.dumps(readtxt(DATAJSON))
        response = app.response_class(response=data,mimetype='application/json')
        return response

class configData:
    def __init__(self,file,sep=";"):
        self._data=""
        if file[-4:]==".csv":
            self._data = pd.read_csv(file,sep=";")
        if file[-5:]==".json":
            self._data = pd.read_json(file)

    def downloadCsv(self):
        self._data.to_csv(index=False)

    def downloadJson(self):
        self._data.to_json(index=False)

    def getData(self):
        return self._data
        
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

    def createNodes(self,data,name="out.json"):
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

class graphX():
    def __init__(self,data):
        self.graph=nx.Graph()
        for i in range(len(data)):
            node=data["node"][i]
            weight=(data["length"][i])
            self.graph.add_edge(str(data["path"][i][0]),str(data["path"][i][1]),weight=weight)
            self.graph.add_node(str(node))


class pathsX(graphX):
    def __init__(self,data,source,target):
        graphX.__init__(self,data)
        self._source=source
        self._target=target
    def dijkstra(self):
        self._nodes=nx.dijkstra_path(self.graph, self._source, self._target, weight='weight')

    def dijkstraNoW(self):
        self._nodes=nx.dijkstra_path(self.graph, self._source, self._target, weight=None)

    def bellmanford(self):
        self._nodes=nx.shortest_path(self.graph, self._source, self._target, weight='weight', method='bellman-ford')

    def getData(self):
        pathdf=pd.DataFrame([{"name":"path","path":[eval(i) for i in self._nodes]}])
        return pathdf
        
class configMap:
    def __init__(self,data):

        self.emptyMap = pdk.Layer(
            type="PathLayer",
            data="",
            pickable=True,
            get_color=(0,155,0),
            width_scale=1,
            width_min_pixels=1,
            get_path="path",
            get_width=1,
        )

        self.pathMap = pdk.Layer(
            type="PathLayer",
            data=data,
            pickable=True,
            get_color=(0,155,0),
            width_scale=1,
            width_min_pixels=1,
            get_path="path",
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
        print("map"*50)
        view = pdk.ViewState(latitude=6.256405968932449, longitude= -75.59835591123756, pitch=40, zoom=12)
        mapCompleate = pdk.Deck(layers=layers, initial_view_state=view)
        mapCompleate.to_html(fileName)
    
    def getEmptyMap(self):return self.emptyMap
    def getPathMap(self):return self.pathMap
    def getnodesMap(self):return self.nodesMap


