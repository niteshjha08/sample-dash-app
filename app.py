import dash
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
    html.Div(id='username_div'),
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

@dash_app.callback(Output('username_div','children'),
              Input('url','pathname'))
def navigating_function(pathname):

    #if(pathname=='/auth'):
    # cache = _load_cache()
    # result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
    #     session.get("flow", {}), request.args)
    # if "error" in result:
    #     return ("Auth Error")
    # session["user"] = result.get("id_token_claims")
    # _save_cache(cache)

    return ("USER: "+ session['username'])
    #else:
       # return("Pathname: ",pathname)
if __name__=='__main__':
    dash_app.run_server(debug=True)