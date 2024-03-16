import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly, render_widget
import palmerpenguins # This package provides the Palmer Penguins dataset
import pandas as pd
import seaborn as sns
from shiny import App, reactive, render, req
import ipyleaflet as ipyl 

# Palmer Penguins Dataset
# Column names for the penguins data set include:
# - species: Penguin species (Chinstrap, Adelie, or Gentoo)
# - island:  island name (Dream, Torgersen, or Biscoe)
# - bill_length_mm:  length of the bill in millimeters
# - bill_depth_mm:  depth of the bill in millimeters
# - flipper_length_mm:  length of the flipper in millimeters
# - body_mass_g:  body mass in grams
# - sex:  MALE or FEMALE

# Load the dataset into a pandas Dataframe
#Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# Name your page
ui.page_opts(title="Palmer Penguins JGanyo", fillable=True)

# Creates user sidebar user interactive 
#and level 2 heading 'Sidebar'
with ui.sidebar(open= "open"): 
    ui.h2 ("Sidebar")

    # Creates a dropdown input to choose a column 
    ui.input_selectize(
        "selected_attribute",
        "Select Penguin Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )


    #Create numeric input for the number of Plotly histogram bins 
    ui.input_numeric("plotly_bin_count", "Number of Bins", 25) 
   
    #Create Slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 1, 50, 5) 

    #Create a checkbox group input
    ui.input_checkbox_group(
        "selected_species_list", 
        "Species", 
        ["Adelie", "Gentoo", "Chinstrap" ], 
        selected=["Adelie", "Gentoo", "Chinstrap"], 
        inline=True,)
    
# Add a hyperlink to GitHub Repo
    ui.a("Ganyo GitHub",
         href="https://github.com/JackieGanyo/cintel-02-data", 
         target="_blank")
    
    #Set horizontal rule
    ui.hr() 

# create a layout to include 2 cards with a data table and data grid
with ui.layout_columns():
     with ui.accordion(id="acc", open="open"):
        with ui.accordion_panel("Data Table"):
            @render.data_frame
            def penguin_datatable():
                return render.DataTable(penguins_df)

        with ui.accordion_panel("Data Grid"):
            @render.data_frame
            def penguin_datagrid():
                return render.DataGrid(penguins_df)

#Set horizontal rule
ui.hr()

#Create histograms and scatterplots using Plotly and Seaborn

with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Plotly Histogram"):

        # Create a function to render the Plotly histogram
        @render_plotly
        def plotly_histogram():
            return px.histogram(penguins_df, y="species")
           
    with ui.nav_panel("Seaborn Histogram"):
            # Create a function to render the Seaborn histogram
            @render.plot
            def seaborn_histogram():
                    sns.set_style("whitegrid") # Set Seaborn style to white
                    seaborn_histogram = sns.histplot(penguins_df, y="species")
                    
                    return seaborn_histogram
                
    with ui.nav_panel("Scatterplot"):
        ui.card_header("Plotly Scatterplot: Species")
                 
        @render_plotly
        def ploty_scatterplot():
            selected_species_list = input.selected_species_list()
            filtered_df = penguins_df[penguins_df["species"].isin(selected_species_list)]
            plotly_scatter = px.scatter(
                filtered_df,
                x="body_mass_g",
                y="bill_length_mm",
                color="species",
                size_max=7,
                labels={
                    "body_mass_g": "Body Mass (g)",
                    "bill_length_mm": "Bill Length (mm)",
                },
            )
            return plotly_scatter

#Create interactive map of penguins by location

penguin_islands = {
    "Biscoe": (-65.7474, -65.9164),
    "Dream": (-64.7333, -64.2333),
    "Torgersen": (-64.7667, -64.0833),
}
ui.input_select("center", "Centers", choices=list(penguin_islands.keys()))


@render_widget
def map():
    return ipyl.Map(zoom=4)


@reactive.effect
def _():
    map.widget.center = penguin_islands[input.center()]
