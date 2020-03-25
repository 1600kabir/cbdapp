from flask import Flask, render_template, url_for, redirect, request
from webui import WebUI
from flask_wtf import Form
from wtforms import FileField, SelectField, SubmitField
import json
from werkzeug.utils import secure_filename
import os
from parse import *
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kabir1234'
#ui = WebUI(app, debug=True)
data_file = 'data.json'


def read_data(f):
	with open(f, 'r') as df:
		return json.loads(df.read())

def dump_data(f, d):
	with open(f, 'w') as df:
		json.dump(d, df, indent=4)
 
class UploadForm(Form):
	file = FileField('CSV File')

class Dropdown(Form):
	dropdown = SelectField('Select File')

class SelectFile(Form):
	select_file = SelectField('Select File')

class SubmitForm(Form):
	button = SubmitField('Load Table')

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/genelists', methods=['GET', 'POST'])
def genelists():
	file_name = 'dftest2.csv'
	f3 = []
	l3 = []
	final = []
	data = read_data(data_file)
	upload_form = UploadForm()
	dropdown = Dropdown()
	load_table = SubmitForm()
	select_f = SelectFile()
	load_table.button.choices = []
	if upload_form.validate_on_submit() and upload_form.file.data:
		filename = secure_filename(upload_form.file.data.filename)
		upload_form.file.data.save('files/{}'.format(filename))
		data = read_data(data_file)
		dropdown.choices = zip(data, data)
		data.append(filename)
		dump_data(data_file, data)
	if select_f.validate_on_submit():
		file_name = select_f.select_file.data
		
	if load_table.validate_on_submit():
		print(file_name)
		f = '../cbdapp-1/'+str(file_name)
		print(f)
		with open(f) as csvDataFile:
			csvReader = csv.reader(csvDataFile)
			for row in csvReader:
				f = row[2:5]
				l = row[5:8]
				if "0" not in f: 
					if l.count("0") == 3:
						f3.append(row[0])
				if "0" not in l: 
					if f.count("0") == 3:
						l3.append(row[0])
			l1 = len(f3)
			l2 = len(l3)
			if l1 != l2:
				if l1 > l2:
					d = l1-l2
					for i in d:
						l3.append('none')
				if l2 > l1:
					d = l2-l1
					for i in range(d):
						f3.append('none')
			final = zip(f3, l3)
				
	return render_template('list.html', upload_form=upload_form, data=data, dropdown=dropdown, final=final, load_table=load_table, select_f=select_f)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
	graphJSON = {}
	data = read_data(data_file)
	pv_thr = SubmitForm()
	lfc_thr = SubmitForm()
	list_of_files = Dropdown()
	load_graph = SubmitForm()
	load_graph.button.choices = []
	
	if load_graph.validate_on_submit():
		f = 'df.csv'
		df = pd.read_csv('dftest2.csv', na_values=['#VALUE!', '#DIV/0!', '#NUM!', '#ERROR!'])
		pv_thr = 0.05
		lfc_thr = 15

		significant = []
		red = []
				
		for i in df['logFC']:
			if float(i) >= lfc_thr:
				significant.append('high')
							#fig = px.scatter(x=df['A'], y=df['B'], color='green')
			elif float(i) <= -1 * int(lfc_thr):
				significant.append('low')
							#fig = px.scatter(x=df['A'], y=df['B'], color='red')	

			else:
				
				significant.append('middle')


		df['significant'] = significant
		fig = px.scatter(df, x=df['logFC'], y=df['logpv'], color=df['significant'])

			
			#fig = px.scatter(df, x=df['logFC'], y=df['logpv'], color='significant')
		plot_obj = [fig]
		graphJSON = json.dumps(plot_obj, cls=plotly.utils.PlotlyJSONEncoder)
		print(plot_obj)
		#print('goihalghusujrhgopihrgahgoufogh')
			#get filename

		#filename = str(request.form.get('df'))
		#print(filename)
		
	
	f = 'df.csv'
	df = pd.read_csv('dftest2.csv', na_values=['#VALUE!', '#DIV/0!', '#NUM!', '#ERROR!'])
	pv_thr = 0.05
	lfc_thr = 15

	significant = []
	red = []
			
	for i in df['logFC']:
		if float(i) >= lfc_thr:
			significant.append('high')
						
		elif float(i) <= -1 * lfc_thr:
			significant.append('low')
							

		else:
			
			significant.append('middle')


	df['significant'] = significant
	fig = px.scatter(df, x=df['logFC'], y=df['logpv'], color=df['significant'])
	plot_obj = [fig]
	graphJSON = json.dumps(plot_obj, cls=plotly.utils.PlotlyJSONEncoder)
	print(plot_obj)
		
	return render_template('graph.html', pv_thr=pv_thr, lfc_thr=lfc_thr, list_of_files=list_of_files, load_graph=load_graph, data=data, graphJSON=graphJSON)


if __name__ == '__main__':
	app.run()
