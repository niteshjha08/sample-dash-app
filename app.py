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
# from helper_functions import _load_cache,_save_cache,_build_msal_app


dash_app=dash.Dash(__name__)
Session(dash_app)
app=dash_app.server
# from werkzeug.middleware.proxy_fix import ProxyFix
# dash_app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
from werkzeug.middleware.proxy_fix import ProxyFix
dash_app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
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
def authorized(pathname):
    print("PATHNAME:",pathname)
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    print("AUTH URI:", session["flow"]["auth_uri"])
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
       # return("Pathname8: ",pathname)

def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        app_config.REDIRECT_PATH)
def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)



def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

if __name__=='__main__':
    dash_app.run_server(debug=True)