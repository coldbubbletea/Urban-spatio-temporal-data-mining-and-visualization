"""
========================
城市时空数据挖掘与可视化系统
City Spatio-temporal Data Mining and Visualization System
========================
author: Xiubo ZHANG
State Key Laboratory of Internet of Things for Smart City (University of Macau) 
https://skliotsc.um.edu.mo/
macau

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

import pandas as pd
import numpy as np
import networkx as nx
import osmnx as ox
import time
import threading
import streamlit as st
import matplotlib.pyplot as plt
ox.settings.all_oneway = True
ox.settings.log_console = True
from PIL import Image
from streamlit.runtime.scriptrunner import add_script_run_ctx
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
from threading import Event

import plotly.express as px
px.set_mapbox_access_token("pk.eyJ1IjoiYnJva2VuY3VwaCIsImEiOiJjbGRhYjh1dDAwaDhzM29ubjJ1MGVkN2ljIn0.-i-1xBsthviFlt6UXBh-jg")











st.title("城市时空数据挖掘与可视化")
st.title("City Spatio-temporal Data Mining and Visualization")
cityName = st.text_input('在文本框中输入想挖掘的地区/城市，如“横琴”，“纽约” Please input the name of the city you want to mine data in English or Chinese pinyin，such as  \'macau\', \'zhuhai\'', 'macau')

opt=st.selectbox("选择你想要的时空数据类型 Select the type of temporal data you want", ["drive","walk","all","bike"])




#'''
#An animation that encourages the user to wait
#event_1: Trigger for start the animation when click
#no returns.
#'''

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




#dataStorage = st.checkbox('存储时空数据')
scatter = st.checkbox('在地图上绘制散点图                            Plot scatter on map')
if scatter:
    user_colour = st.color_picker('选择散点的颜色 Choose a colour for your plot',"#F1E706")
roadNetwork = st.checkbox('路网图抽象建模                           Abstract road network map')

if st.button('Start'):
    t=threading.Thread(target=progressBar,args=(event_1,))
    ctx = get_script_run_ctx()
    print('=== CTX ===\n', ctx)
    add_script_run_ctx(t)
    t.start()
    G = ox.graph_from_place(cityName, network_type=opt)
    ox.save_graph_xml(G, filepath=cityName+"_RoadNetwork.xml")
    event_1.set()
    t.join()    
    st.success('数据挖掘完毕\n Data mining is complete, Stored in cityName_RoadNetwork.xml')
    
    if scatter:
        df = pd.read_xml(cityName+"_RoadNetwork.xml")
        st.dataframe(df)
        fig = px.scatter_mapbox(df, lat="lat", lon="lon", size_max=15, zoom=10,color_discrete_sequence=[user_colour])
        st.plotly_chart(fig, theme=None, use_container_width=True)    
    if roadNetwork:
        img,ax=ox.plot_graph(G, save=True,filepath="City_RoadNetwork.jpg")
        image = Image.open("City_RoadNetwork.jpg")
        st.image(image, caption=cityName)

        

# df = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [17.76, 122.4],
#     columns=['lat', 'lon'])
# df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
# df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
# df.dropna()
# print(df['lon'])
# node_num=G.number_of_nodes()


# st.map(df.head(node_num))

# st.map(df.head(node_num//10))

# import plotly.express as px


