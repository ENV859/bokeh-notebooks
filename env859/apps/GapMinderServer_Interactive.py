'''
Same as GapMinderServer_Static.py but here we add a slider to interact
with the data. The slider is a Bokeh, not iPyWidget object, and to add
it to our document, we need to import the bokeh.layouts column class
which can hold and arrange multiple items on the page. We then add this 
layout to our current doc. 

Slider: https://bokeh.pydata.org/en/latest/docs/reference/models/widgets.sliders.html#bokeh.models.widgets.sliders.Slider
'''

##-----------IMPORTS--------------------
#Import the curdoc object 
from bokeh.io import curdoc 

#Import the figure object
from bokeh.plotting import figure

#Import models
from bokeh.models import (
    ColumnDataSource, 
    HoverTool, 
    LinearInterpolator, 
    CategoricalColorMapper,
    NumeralTickFormatter,
    Slider #<---------------Import the Bokeh slider widget
)

#Import the Spectral6 palette
from bokeh.palettes import Spectral6

#Import Bokeh layout column -- to arrange items on our page
from bokeh.layouts import column


##----------DATA-------------------------    
#import the data as a dataframe then as a ColumnDataSource object
import pandas as pd
data = pd.read_csv('../data/gapminder.csv',thousands=',',index_col='Year')
theCDS = ColumnDataSource(data.loc[2010])
    
##----------PLOT-------------------------  
#Create a styling dictionary for our plot
PLOT_OPS = {'title':'2010',
            'height':500,
            'width':900,
            'x_axis_type':'log',
            'x_axis_label':'Log(Income)',
            'y_axis_label':'Life expectancy (years)',
            'x_range':(100,100000),
            'y_range':(0,100),
            'toolbar_location':"below"
           }

#Create the population size mapper
size_mapper = LinearInterpolator(x=[data.loc[2010]['population'].min(),
                                    data.loc[2010]['population'].max()],
                                 y=[5,50])
    
#Create the region color mapper
color_mapper = CategoricalColorMapper(factors=data.loc[2010]['region'].unique(),
                                      palette=Spectral6)

hover = HoverTool(tooltips='@Country')
p = figure(**PLOT_OPS)
p.circle(x='income',
         y='life',
         source=theCDS,
         size={'field':'population','transform':size_mapper},
         color={'field':'region','transform':color_mapper},
         alpha=0.6,
         legend='region'
        )
p.legend.border_line_color = 'red'
p.right = p.legend
p.xaxis.formatter = NumeralTickFormatter(format='$0,')
p.add_tools(hover)

##----------UPDATE FUNCTION------------
def update(attr, old, new):
    #Set the year to be the value of the 'new' parameter
    year=new
    new_data = ColumnDataSource(data.loc[year]).data #Select data from a different year
    theCDS.data = new_data #Update the data in the ColumnDataSource to the revised data
    p.title.text=str(year) #Update the title of our plot
    #push_notebook()       #No push needed! Link between script and server is automatic
    

##----------WIDGET---------------------
#Create the year slider
slider = Slider(start=1960,end=2010,value=2010,title='Year')

#Hook it to the update function
slider.on_change('value',update)

##----------ADD ITEMS TO THE DOCUMENT---
#Create a layout of the plot and the slider
layout = column(p,slider)

#Show the layout to the current doc
curdoc().add_root(layout)