import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
print("hello world")
dash_app=dash.Dash(__name__)
app=dash_app.server
dash_app.layout=html.Div([
    html.H1("Hey there!!"),
    html.Div("This is the dash tutorial"),
    dcc.Graph(
        id='sample1',
        figure={
            'data':[{'x':[1,2,3],'y':[7,8,9],'type':'bar','name':'NJ'},
                    {'x':[5,2,3],'y':[17,18,19],'type':'bar','name':'NJ2'}],
            'layout':{
                'title':'Simple Bar Chart',
                'plot_bgcolor':'#D3D3D3'
            }}
    )])
if __name__=='__main__':
    dash_app.run_server(debug=True)