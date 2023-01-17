"""
========================
OpenStreetMap with OSMnx
========================

This example shows how to use OSMnx to download and model a street network
from OpenStreetMap, visualize centrality, and save the graph as a shapefile,
a GeoPackage, or GraphML.

OSMnx is a Python package to retrieve, model, analyze, and visualize
OpenStreetMap street networks as NetworkX MultiDiGraph objects. It can also
retrieve any other spatial data from OSM as geopandas GeoDataFrames. See
https://osmnx.readthedocs.io/ for OSMnx documentation and usage.
"""

import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from PIL import Image
import time
import threading
ox.settings.all_oneway = True
ox.settings.log_console = True
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
from threading import Event



st.write("# 城市时空数据挖掘与可视化 \n City specific spatio-temporal data mining and visualization")
cityName = st.text_input(' Please input the name of the city you want to mine data in English or Chinese pinyin，such as  \'macau\', \'zhuhai\'', 'macau')
opt=st.selectbox("选择你想要的时空数据类型", ["drive","walk","all","bike"])

def progressBar(event_1):
    with st.spinner('Wait for it...'):
        for i in range(1000):
            time.sleep(1)
            if event_1.is_set():
                
                
                break
        
    
    # my_bar = st.progress(0)
    # for percent_complete in range(100):
    #     time.sleep(0.2)
    #     my_bar.progress(percent_complete + 1)

event_1 = Event()

dataStorage = st.checkbox('存储时空数据')
Visualization = st.checkbox('Data Visualization')
if st.button('Start') and (dataStorage or Visualization):
    t=threading.Thread(target=progressBar,args=(event_1,))
    ctx = get_script_run_ctx()
    print('=== CTX ===\n', ctx)
    add_script_run_ctx(t)
    t.start()
    G = ox.graph_from_place(cityName, network_type=opt)
    ox.save_graph_xml(G, filepath=cityName+"_RoadNetwork.xml")
    
    
    if Visualization:
        img,ax=ox.plot_graph(G, save=True,filepath="City_RoadNetwork.jpg")
        image = Image.open("City_RoadNetwork.jpg")
        st.image(image, caption=cityName)
    event_1.set()
    t.join()    
    st.success('Done!')


