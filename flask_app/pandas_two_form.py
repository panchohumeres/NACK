from flask import Flask
from flask import render_template
from flask import request
from redis import Redis, RedisError
from flask import session
import os
import socket
import pandas as pd
from flask import abort, redirect, url_for
from flask import render_template_string
#por defecto, las carpetas "static" y "templates" en la misma carpeta de la app (script python)
#flask usa jinja


# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)
app = Flask(__name__)
# Check Configuration section for more details
app.secret_key = 'You Will Never Guess'

#sobre sesiones y permanencia de variables
#https://stackoverflow.com/questions/27611216/how-to-pass-a-variable-between-flask-pages
#https://gist.github.com/macloo/67caf0e0d0718d4723d88786e1db80fb
@app.route('/pandasform')
def pandas_form():
    df={'A':[],'B':[],'C':[],'D':[]}
    session['df']=df #no se pueden guardar dfs en variables de sesion
    return render_template('hor_form.html')

@app.route('/pandasform', methods=['POST'])
def pandas_form_post():
    df=pd.DataFrame.from_dict(session['df'])

    inputs={}
    inputs['A'] = [request.form['A']]
    inputs['B']=[request.form['B']]
    inputs['C']=[request.form['C']]
    inputs['D']=[request.form['D']]

    inputs=pd.DataFrame.from_dict(inputs)
    df=df.append(inputs,ignore_index=True)

    session['df']=df.to_dict(orient='list')
    #OJO REDIRECT FOR URL FUNCIONA CON NOMBRES DE FUNCIONES!! NO URLS
    #https://teamtreehouse.com/community/flask-redirect-vs-redirecturlfor
    return redirect(url_for('render_pandas_posts')) #OJO SE DEBE REFERENCIAR LA FUNCION, NO LA URL DE "ROUTE"

@app.route('/pandas_double_form')
def render_pandas_posts():
	df=pd.DataFrame.from_dict(session['df'])
	return render_template('pandas_two_form.html',tables=[df.to_html(classes='female')], titles = ['na', 'Your inputs'])

@app.route('/pandasform_delete',methods=['POST'])
def pandasform_delete():
	df=pd.DataFrame.from_dict(session['df'])
	deletes=request.form['del']
	deletes=[int(x) for x in deletes.split(',')]
	df=df.drop(deletes)
	session['df']=df.to_dict(orient='list')
	df=pd.DataFrame.from_dict(session['df']) #hacerlo dos veces para verificar que se guarda en variable sesion
	return render_template('pandas_two_form.html',tables=[df.to_html(classes='female')], titles = ['na', 'Your inputs'],deletes=deletes)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)