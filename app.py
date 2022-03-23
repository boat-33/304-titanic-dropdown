######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Titanic!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/plotly-dash-apps/304-titanic-dropdown'


###### Import a dataframe #######
def fit_in_bucket(value):
    if float(value) < 25.0:
        return 'under 25'
    elif float(value) > 25.0 and float(value) < 50.0:
        return 'between 25 and 50'
    elif float(value) > 50.0:
        return 'over 50'

df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter/plotly_dash_tutorial/master/00%20resources/titanic.csv")
df['Female']=df['Sex'].map({'male':0, 'female':1})
df['Passenger Age'] = df['Age'].map(lambda x: fit_in_bucket(x))
variables_list=['Survived', 'Female', 'Fare', 'Pclass']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['Passenger Age', 'Embarked'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['under 25'].index,
        y=results.loc['under 25'][continuous_var],
        name='Under 25',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['between 25 and 50'].index,
        y=results.loc['between 25 and 50'][continuous_var],
        name='Between 25 and 50',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['over 50'].index,
        y=results.loc['over 50'][continuous_var],
        name='Over 50',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Port of Embarkation'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
