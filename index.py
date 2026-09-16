
import dash
from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from app import *




df_data = pd.read_csv("supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])

df_data["City"].value_counts().index



# =============== Layout ================= #
app.layout = html.Div(children=[
              
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.H2("ASIMOV", style={"font-family": 'Voltaire', 'font-size': '60px'}),
                            html.Hr(),
                            html.P("Dashboard para análise de de vendas de supermercado."),
                            
                            html.H5("Cidades:", style={"margin-top": "10px"}),
                            dcc.Checklist(df_data["City"].value_counts().index, 
                            df_data["City"].value_counts().index, id="check_city",
                            inputStyle={"margin-right": "5px", "margin-left": "20px"}),
                                                                
                            html.H5("Variável de análise", style={"margin-top": "20px"}),
                            dcc.RadioItems(["gross income", "Ratiing"], 
                            "gross income", id="main_variable",
                            inputStyle={"margin-right": "5px", "margin-left": "20px"}),
                            
                        ], style={"height": "90vh", "margin": "20px", "pedding": "20px"})
                        
                        
                    ], md=3),
                
                    dbc.Col([ 
                        dbc.Row([    #Gerando grafico
                            dbc.Col([dcc.Graph(id="city_fig"),], lg=4, sm=12),
                            dbc.Col([dcc.Graph(id="pay_fig"),], lg=4, sm=12),
                            dbc.Col([dcc.Graph(id="gender_fig"),],lg=4 ,sm=12),
                            
                        ]),
                         dbc.Row([dcc.Graph(id="income_per_date_fig")]),
                         dbc.Row([dcc.Graph(id="income_per_product_fig")]),
                        
                            
                        ], md=9)
                ])
                
    ], style={"pedding": "0px"}) 


# ================ Callbacks ============= #
@app.callback([
           Output('city_fig', 'figure'),
           Output('pay_fig', 'figure'),
           Output('gender_fig', 'figure'),
           Output('income_per_date_fig', 'figure'),
           Output('income_per_product_fig', 'figure')],
           
              
              
            [Input('check_city', 'value'),
            Input('main_variable', 'value')])

 # Criando funcoes
def render_graphs(cities, main_variable):
    cities = ["Yangon", "Mandalay"]
    main_variable= "gross income"
    
    operation = np.sum if main_variable == "gross income" else np.mean
    
    df_filtered = df_data[df_data["City"].isin(cities)]
    
    df_city = df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    
    df_gender = df_filtered.groupby(["Gender", "City"])[main_variable].apply(operation).to_frame().reset_index()
    
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).to_frame().reset_index()
    
    df_income_time = df_filtered.groupby("Date")[main_variable].apply(operation).to_frame().reset_index()
    
    df_product_income = df_filtered.groupby(["Product line", "City"])[main_variable].apply(operation).to_frame().reset_index()
    
    #Criando os Graficos
    fig_city = px.bar(df_city, x="City", y=main_variable, template="plotly_white")
    fig_gender = px.bar(df_gender, x="Gender", y=main_variable, color="City", barmode='group')
    fig_payment = px.bar(df_payment, y="Payment", x=main_variable, orientation="h")
    fig_income_date = px.bar(df_income_time, y=main_variable, x="Date")
    fig_product_income = px.bar(df_product_income, x=main_variable, y="Product line", color="City", orientation="h", barmode="group")
    
    #Update
    #fig_city.update_layout(margin=dict(l=0, r=0, t=20, b=20),height=200, template="plotly_white")
    #fig_payment.update_layout(margin=dict(l=0, r=0, t=20, b=20),height=200, template="plotly_white")
    for fig in [fig_city, fig_gender, fig_income_date ]:
        fig.update_layout(margin=dict(l=0, r=20, t=20, b=20),height=200)
    fig_product_income.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=500, template="ggplot2")
    
    return fig_city,fig_gender,fig_payment,fig_income_date, fig_product_income 
    




# ================ Run Server ============
if __name__ == "__main__":
    app.run(port=8050, debug=True)



