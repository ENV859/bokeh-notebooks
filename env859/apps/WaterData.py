# WaterData.py
#
# A Bokeh-based application that reads water withdrawal data
# and creates a simple interface to plot selected summaries
# based on different facility types
#
# To run this app, run the following command from a DOS shell
#  (which runs the Bokeh server from your machine):
#  %localappdata%\ESRI\conda\envs\my_vis\python.exe -m bokeh serve app.py
#
# Fall 2018
# John.Fay@duke.edu

#Import pandas (to read the data into a dataframe
import pandas as pd

# Import the bokeh objects
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import ColumnDataSource, Figure
from bokeh.models.widgets import Select

##Define functions that will be called by the app-------------------------------
def initialize_data(grpVar='FacilityType'):
    '''Retrieve the annual summaries for the selected year as a dataframe'''
    #Read in the data
    dfAll = pd.read_csv('../Data/WithdrawalSourceData.csv')
    dfAll['MG'] = dfAll['AvgDaily'] * dfAll['DaysUsed']
    #Group the data into a new dataframe
    ser=dfAll.groupby(['Year',grpVar])['MG'].sum()
    df=ser.unstack(level=grpVar).reset_index()
    return df

def get_data(df,type):
    '''Create a Bokeh column data source of the selected type'''
    return dict(x=df['Year'],y=df[type])

def updatePlot(attrname,old,new):
    '''Callback function that updates the data source based on the item selected'''
    source.data = get_data(df,new)
    
##Code------------------------------------------------------------------------
#Read the data in, grouped and summarized by the given field
df = initialize_data('FacilityType')

#Create a bokeh column data source object from the data
source = ColumnDataSource(data=get_data(df,'Agricultural'))

#Create the plot object from the column data source object
p = Figure(title='Annual discharge (MG/year)',
           plot_width=800,
           plot_height=300)
p.line(x='x',y='y',source=source)

#Create and populate the select widget
optionList = df.columns.tolist()
if ('Year') in optionList: optionList.remove('Year')

#Create the select (dropdown) object
select = Select(title="Select type", options=optionList)

#Run the 'updatePlot' function if the select value changes
select.on_change('value',updatePlot)

#Construct a layout for our app page
# This will arrange our two objects (the plot and the select dropdown)
# in a single column
layout = column(row(p),row(select))

#Add the layout to our app
curdoc().add_root(layout)