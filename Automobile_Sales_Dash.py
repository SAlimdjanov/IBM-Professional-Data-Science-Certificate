import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloper\
    SkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {"label": "...........", "value": "Yearly Statistics"},
    {"label": "Recession Period Statistics", "value": "........."},
]

# Create the layout of the app
app.layout = html.Div(
    [
        # Add title to the dashboard
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 24},
        ),
        html.Div(
            [  # Add two dropdown menus
                html.Label("Select Statistics:"),
                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=[
                        {"label": "Yearly Statistics", "value": "Yearly Statistics"},
                        {
                            "label": "Recession Period Statistics",
                            "value": "Recession Period Statistics",
                        },
                    ],
                    value="Select Statistics",
                    placeholder="Select a report type.",
                ),
            ]
        ),
        html.Div(
            dcc.Dropdown(
                id="select-year",
                options=[{"label": str(i), "value": i} for i in data["Year"].unique()],
                value=data["Year"].min(),
            )
        ),
        html.Div(
            [  # Add a division for output display
                html.Div(
                    id="output-container",
                    className="grid-chart",
                    style={"display": "flex"},
                ),
            ]
        ),
    ]
)


# I/O Callback decorator
@app.callback(
    Output(component_id="dropdown-statistics", component_property="value"),
    Input(component_id="select-year", component_property="value"),
)
def update_input_container(selected_statistics):
    """
    Update input container based on selected stats set from drop down menu. Disable the
    dropdown if true

    Args:
        selected_statistics (str): Selection string yearly statistics or stats from
        recession period

    Returns:
        bool: True/False

    """
    if selected_statistics == "Yearly Statistics":
        return False
    return True


# Callback for plotting, updates input container based on selected statistics
@app.callback(
    Output(component_id="output-container", component_property="children"),
    Input(component_id="dropdown-statistics", component_property="value"),
    Input(component_id="select-year", component_property="value"),
)
def update_output_container(selected_statistics, input_year):
    """
    Update output container for plotting relevant statistics

    Args:
        selected_statistics (str): Selected statistics set
        input_year (int): Selected year from dropdown menu

    Returns:
        HTML div object (Graphs)

    """
    if selected_statistics == "Recession Period Statistics":
        # Filter the data for recession periods
        recession_data = data[data["Recession"] == 1]

        # Plot: Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        )
        r_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Average Automobile Sales fluctuation over Recession Period",
            )
        )
        # Plot: Calculate the average number of vehicles sold by vehicle type
        average_sales = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        r_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Automobile Sales by Vehicle Type during Recession Period",
            )
        )
        # Plot: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = (
            recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .mean()
            .reset_index()
        )
        r_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Expenditure Share by Vehicle Type During Recession",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[html.Div(children=r_chart1), html.Div(children=r_chart2)],
                style={"flex": "50%"},
            ),
            html.Div(
                className="chart-item",
                children=[html.Div(children=r_chart3)],
                style={"flex": "50%"},
            ),
        ]

    # Create and display graphs for Yearly Report Statistics
    if input_year and selected_statistics == "Yearly Statistics":
        yearly_data = data[data["Year"] == input_year]

        # Plot: Yearly Automobile sales using line chart for the whole period.
        yas = yearly_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x="Year",
                y="Automobile_Sales",
                title="Yearly Automobile Sales Line Chart",
            )
        )

        # Plot: Total Monthly Automobile sales using line chart.
        month_sales = (
            yearly_data.groupby("Month")["Automobile_Sales"].sum().reset_index()
        )
        y_chart2 = dcc.Graph(
            figure=px.line(
                month_sales,
                x="Month",
                y="Automobile_Sales",
                title="Total Monthly Automobile Sales Line Chart",
            )
        )
        # Plot: Bar chart for average number of vehicles sold during the given year
        avr_vdata = (
            yearly_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        )
        y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=f"Average Vehicles Sold by Vehicle Type in the year {input_year}",
            ),
        )
        # Plot: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = (
            yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Advertisement Expenditure by Vehicle Type",
            )
        )

        # Return the graphs for displaying yearly data
        return [
            html.Div(
                className="chart-item",
                children=[html.Div(children=y_chart1), html.Div(children=y_chart2)],
                style={"flex": "50%"},
            ),
            html.Div(
                className="chart-item",
                children=[html.Div(children=y_chart3), html.Div(children=y_chart4)],
                style={"flex": "50%"},
            ),
        ]

    return None


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
