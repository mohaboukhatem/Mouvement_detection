import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import os
from dotenv import load_dotenv
import pyrebase

# Load environment variables
load_dotenv()

# Firebase credentials from .env
credentiels = {
    "apiKey": os.getenv("API_KEY"),
    "authDomain": os.getenv("AUTH_DOMAIN"),
    "databaseURL": os.getenv("DATABASE_URL"),
    "projectId": os.getenv("PROJECT_ID"),
    "storageBucket": os.getenv("STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
    "appId": os.getenv("APP_ID"),
    "measurementId": os.getenv("MEASUREMENT_ID"),
}

# Initialize Firebase
firebase = pyrebase.initialize_app(credentiels)
db = firebase.database()

# Function to fetch Firebase data
def fetch_data():
    data = db.child("Capteur 1").get().val()
    if not data:
        return pd.DataFrame(columns=["Date", "Distance (cm)", "Status", "Notification SMS"])

    df = pd.DataFrame.from_dict(data, orient="index")
    df["Date"] = pd.to_datetime(df["Date"])  # Convert Date to datetime
    df = df.sort_values("Date", ascending=False)  # Sort by newest first

    return df

# Initialize Dash App
app = dash.Dash(__name__)

# Define font style
custom_style = {
    "font-family": "'Poppins', sans-serif", 
    "textAlign": "center"
}

# App Layout
app.layout = html.Div([
    html.H1("Movement Detection Dashboard", style={**custom_style, "font-weight": "bold"}),

    # KPI Section
    html.Div([
        html.Div([
            html.H3("Total Movements", style=custom_style),
            html.P(id="total-movements", style={"font-size": "20px"}),
        ], style={"width": "30%", "display": "inline-block", "border": "1px solid #ddd", "padding": "15px"}),

        html.Div([
            html.H3("Moyenne Distance (cm)", style=custom_style),
            html.P(id="avg-distance", style={"font-size": "20px"}),
        ], style={"width": "30%", "display": "inline-block", "border": "1px solid #ddd", "padding": "15px"}),

        html.Div([
            html.H3('Nombre Notifications', style=custom_style),
            html.P(id="notification-count", style={"font-size": "20px"}),
        ], style={"width": "30%", "display": "inline-block", "border": "1px solid #ddd", "padding": "15px"})
    ], style={"textAlign": "center", "margin-bottom": "20px"}),

    # Filter Section
    html.Div([
        html.Label("Afficher les derniers enregistrement", style={**custom_style, "font-size": "18px"}),
        dcc.Input(id="num-records", type="number", value=10, min=1, step=1, style={"width": "60px", "margin-left": "10px"}),
        html.Button("Apply", id="filter-button", n_clicks=0, style={"margin-left": "10px", "cursor": "pointer"})
    ], style={"textAlign": "center", "margin-bottom": "20px"}),

    # Data Table (Top)
    html.Div([
        html.H3("", style=custom_style),
        dash_table.DataTable(
            id="data-table",
            columns=[
                {"name": "Date", "id": "Date"},
                {"name": "Distance (cm)", "id": "Distance (cm)"},
                {"name": "Status", "id": "Status"},
                {"name": "Notification SMS", "id": "Notification SMS"},
            ],
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center", "font-family": "'Poppins', sans-serif"},
            page_size=10,
        ),
    ], style={"margin-top": "20px"}),

    # Distance Over Time Chart (Bottom)
    html.Div([
        html.H3("", style=custom_style),
        dcc.Graph(id="distance-over-time"),
    ], style={"margin-top": "20px"}),

    # Auto-refresh every 5 seconds
    dcc.Interval(id="interval-component", interval=5000, n_intervals=0)
])

# Callback to update elements dynamically
@app.callback(
    [Output("total-movements", "children"),
     Output("avg-distance", "children"),
     Output("notification-count", "children"),
     Output("distance-over-time", "figure"),
     Output("data-table", "data")],
    [Input("interval-component", "n_intervals"),
     Input("filter-button", "n_clicks")],
    [State("num-records", "value")]
)
def update_dashboard(n, n_clicks, num_records):
    df = fetch_data()
    
    if df.empty:
        return "0", "0 cm", "0", px.line(), []

    # KPIs
    total_movements = str(len(df))
    avg_distance = f"{df['Distance (cm)'].mean():.2f} cm"
    notification_count = str(df[df["Notification SMS"] == "Envoyé"].shape[0])  # Count "Envoyé"

    # Filter for recent N records
    df_filtered = df.head(num_records) if num_records else df

    # Distance Over Time Chart
    fig_distance = px.line(df_filtered, x="Date", y="Distance (cm)", title="")

    # Convert DataFrame to dictionary for Dash DataTable
    data_table = df_filtered.to_dict("records")

    return total_movements, avg_distance, notification_count, fig_distance, data_table

# Run the Dash App
if __name__ == "__main__":
    app.run(debug=True)
