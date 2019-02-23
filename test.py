# import vnquant.DataLoader as dl
# loader = dl.DataLoader('VND', '2018-02-02','2018-04-02')
# loader.download()


import plotly.plotly as py
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot,iplot


init_notebook_mode(connected=True)
import plotly.graph_objs as go

x=np.array([2,5,8,0,2,-8,4,3,1])
y=np.array([2,5,8,0,2,-8,4,3,1])


data = [go.Scatter(x=x,y=y)]
fig = go.Figure(data = data,layout = go.Layout(title='Offline Plotly Testing',width = 800,height = 500,
                                           xaxis = dict(title = 'X-axis'), yaxis = dict(title = 'Y-axis')))


plot(fig,show_link = False)