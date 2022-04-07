#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
alOtrolado - 2022 - por jero98772
alOtrolado - 2022 - by jero98772
"""
from core.main import webpage
from core.main import app
if __name__=='__main__':
    #data=configData(DATAJSON).getData()
    #data=configData(DATACSVFILE)
    #configData.clearAllDataJson(data.getData())

    #maps=configMap(data)
    #maps.genMapMultlayer(GENMAPFILE,[maps.getPathMap(),maps.getnodesMap()])
    #graphNetworX(data)
    app.run(debug=True,host="0.0.0.0",port=9600)