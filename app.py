import dash
import requests
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
import msal
from dash.dependencies import Output, Input,State

import app_config
from helper_functions import _load_cache,_save_cache,_build_msal_app,_build_auth_code_flow


dash_app=dash.Dash(__name__)

Session(dash_app)
app=dash_app.server

dash_app.layout=html.Div([
    dcc.Location(id='url',refresh=False),
    html.H1("Hey there!!"),
    html.Div(id='get-div'),
    html.Div(id='get-div2'),
    html.Div(id='get-div3'),
    html.Div(id='get-div4'),
    html.Div(id='username-div'),
    html.Div(id='username-div2'),
    html.Div(id='pathname-div'),
    html.Div("This is the dash sample"),
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

@dash_app.callback(Output('get-div','children'),
Output('get-div2','children'),
Output('get-div3','children'),
Output('get-div4','children'),
Output('username-div','children'),
Output('username-div2','children'),
    Output('pathname-div','children'),
              Input('url','pathname'))
def navigating_function(pathname):

    # if(pathname=='/auth'):
    r=requests.get('https://graph.microsoft.com/v1.0/me')
    rj=r.json()
    rj_str=str(rj)
    # cache = _load_cache()
    # result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
    #     session.get("flow", {}), request.args)
    # if "error" in result:
    #     return ("Auth Error")
    # session["user"] = result.get("id_token_claims")
    # _save_cache(cache)
    # username=session['user']
    # username2=session['username']
    r2 = requests.get('https://graph.microsoft.com/v1.0/users/{id | userPrincipalName}')
    rj2 = r2.json()
    rj2_str = str(rj2)
    r3 = requests.get('https://graph.microsoft.com/User.Read')
    rj3 = r3.json()
    rj3_str = str(rj3)
    r4 = requests.get('https://graph.microsoft.com/User.ReadBasic.All')
    rj4 = r4.json()
    rj4_str = str(rj4)


    return (rj_str,rj2_str,rj3_str,rj4_str,"USERNAME:","USERNAME2:","PATHNAME: "+pathname)
    #else:
       # return("Pathname: ",pathname)
if __name__=='__main__':
    dash_app.run_server(debug=True)