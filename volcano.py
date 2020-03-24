import plotly.express as px
import pandas as pd
import csv
import plotly.graph_objects as go
import plotly
import chart_studio.tools as tls
'''
tls.get_embed('https://plot.ly/~test/1')

#request filename
#filen
#file = '../files/{}'.format(filename)
#file = f'../files/{filename}'
#df = pd.read_csv('df.csv')

df = pd.read_csv('dftest.csv', na_values=['#VALUE!', '#DIV/0!', '#NUM!', '#ERROR!'])
#r = lambda x: x.isnumeric()
#df[df.logFC.apply(r)]

fc = df['logFC']
df = df['logpv']


def r(file, col):
	l = file[col]
	for i in l:
		if i == '#DIV/0!':
			l[l.index(i)] = 5 
	return l
n = r(df, 'logFC')
df['logFC1'] = n

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
fig = px.scatter(df, x=df['logFC'], y=df['logpv'], color='significant')






fig.show()
print(df['logpv'])
'''

f = 'df.csv'
df = pd.read_csv('testing1234.csv', na_values=['#VALUE!', '#DIV/0!', '#NUM!', '#ERROR!'])
pv_thr = 0.05
lfc_thr = 15

significant = []
red = []
		
for i in df['logFC']:
	if float(i) >= lfc_thr:
		significant.append('high')
					#fig = px.scatter(x=df['A'], y=df['B'], color='green')
	elif float(i) <= -1 * lfc_thr:
		significant.append('low')
					#fig = px.scatter(x=df['A'], y=df['B'], color='red')	

	else:
		
		significant.append('middle')


df['significant'] = significant
fig = px.scatter(df, x=df['logFC'], y=df['logpv'], color=df['significant'])
fig.show()
