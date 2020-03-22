import pandas as pd
import io
import requests
import plotly.graph_objects as go


url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
s = requests.get(url).content
df = pd.read_csv(io.StringIO(s.decode('utf-8')))

df = df.drop(['Province/State','Lat','Long'],axis = 1)
df = df.groupby(['Country/Region']).sum()
df = df.sort_values(df.columns[-1], ascending = False)

list = df.head(12).index.tolist()
#list.append('INSERT YOUR COUNTRY NAME HERE')
df_head = df[df.index.isin(list)]

mydict = df_head.T.to_dict('list')

for k in mydict:
    mydict[k] = [x for x in mydict[k] if x > 100]

df_hundred = pd.DataFrame.from_dict(mydict, orient='index')

df_t = df_hundred.T.drop(['China', 'Korea, South'], axis = 1).dropna(how='all')

fig = go.Figure()
for column in df_t:
    fig.add_trace(go.Scatter(x=df_t.index, y=df_t[column], name=column))

fig.update_layout(title_text='top 10 infected countries days since 100 infections')
fig.show()