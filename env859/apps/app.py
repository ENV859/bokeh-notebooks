# -*- coding: utf-8 -*-
"""
Created on Mon May  7 09:26:41 2018

@author: jpfay
"""

import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import ColumnDataSource, Figure
from bokeh.models.widgets import Select

def initialize_data(grpVar='FacilityType'):
    '''Retrieve the annual summaries for the selected year as a dataframe'''
    #Read in the data
    dfAll = pd.read_csv('../Data/WithdrawalSourceData.zip')
    dfAll['MG'] = dfAll['AvgDaily'] * dfAll['DaysUsed']
    #Group the data into a new dataframe
    ser=dfAll.groupby(['Year',grpVar])['MG'].sum()
    df=ser.unstack(level=grpVar).reset_index()
    return df

def get_data(df,type):
    '''Create a Bokeh CDS of the selected type'''
    return dict(x=df['Year'],y=df[type])
    
#Get the source
df = initialize_data('FacilityType')
source = ColumnDataSource(data=get_data(df,'Agricultural'))

#Plot
p = Figure(plot_width=500, plot_height=500)
p.line(x='x',y='y',source=source)

#Create and populate the select widget
optionList = df.columns.tolist()
if ('Year') in optionList: optionList.remove('Year')

select = Select(title="Select type", options=optionList)

def updatePlot(attrname,old,new):
    #type = select.value
    source.data = get_data(df,select.value)
select.on_change('value',updatePlot)

layout = column(row(select),row(p))

curdoc().add_root(layout)