from bokeh.plotting import figure, output_file, show, ColumnDataSource, save
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap
from bokeh.models import ColorBar
#from bokeh.palettes import Blues12
from bokeh.embed import components
import pandas as pandas
import matplotlib.pyplot as plt


df = pandas.read_csv('data/forestfires.csv')
#print(df.groupby(['month']).count())
#print(df.head())
#a = df.groupby(['month']).count()
#print(a)



month_names = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
months = df['month'].value_counts()
#print(months.index)
months = months.reindex(month_names)
group_month = df.groupby('month')

avg_temp = df.groupby('month').mean()
avg_temp = avg_temp.reindex(month_names)
avg_temp = avg_temp['temp']
months2 = group_month.sum()
#print(months2['area'])
#print(avg_temp['temp'])
#plt.plot(avg_temp['temp'])
#plt.show()


#plt.plot(df['temp'].groupby(['month']))
#plt.show()

#plt.plot(months)
#plt.show()

#car = df['Car']
#hp = df['Horsepower']

#column data source
#source = ColumnDataSource(df)
#print(source)
#month_list = source.data['month'].tolist()
source = ColumnDataSource(dict(y=month_names, right=months))
#print(source.data['right'])
#print(source.data)
#print(month_list)

output_file('index.html')

# Car list
#car_list = source.data['Car'].tolist()
from bokeh.palettes import inferno
colours = inferno(12)
#colours = ['#FFA58A','#FF8770','#FF6957','#FF4B3E','#E22727']
from bokeh.transform import linear_cmap, LogColorMapper
from bokeh.palettes import YlOrRd
mapper = linear_cmap(field_name='right', palette='Viridis256' ,low=max(source.data['right']) ,high=min(source.data['right']))
#mapper = LogColorMapper(palette='Viridis256', low=min(source.data['right']) ,high=max(source.data['right']))
#print(mapper)


chart_font = 'Helvetica'
chart_title_font_size = '16pt'
chart_title_alignment = 'center'
axis_label_size = '14pt'
axis_ticks_size = '12pt'
default_padding = 30
chart_inner_left_padding = 0.015
chart_font_style_title = 'bold'


# Add plots
p = figure(
	#y_range=month_names,
	x_range=month_names,
	plot_width=700,
	plot_height=500,
	title = 'Number of fires per month',
	y_axis_label = 'Number of fires',
	tools="pan, box_select, zoom_in, zoom_out, save, reset",
)

# Render glyph
p.vbar(
	x='y',
	top='right',
	bottom=0,
	width=0.4,
	#fill_color=linear_cmap(field_name='data', palette=colours ,low=min(source.data['right']) ,high=max(source.data['right'])),
	fill_color=mapper,
	line_width=0,
	source=source,
	legend='y'
)

'''
fill_color=factor_cmap(
		'y',
		palette=mapper,
		factors=month_names
	),
'''

# Add legend
#p.legend.orientation='vertical'
#p.legend.location='top_right'
#p.legend.label_text_font_size= '10px'

color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0))
p.add_layout(color_bar, 'right')

#p.xgrid.visible = False
#p.ygrid.visible = False
p.title.text_font_size = chart_title_font_size
p.title.text_font  = chart_font
p.title.align = chart_title_alignment
p.title.text_font_style = chart_font_style_title
p.y_range.start = 0
p.x_range.range_padding = chart_inner_left_padding
p.xaxis.axis_label_text_font = chart_font
p.xaxis.major_label_text_font = chart_font
p.xaxis.axis_label_standoff = default_padding
p.xaxis.axis_label_text_font_size = axis_label_size
p.xaxis.major_label_text_font_size = axis_ticks_size
p.yaxis.axis_label_text_font = chart_font
p.yaxis.major_label_text_font = chart_font
p.yaxis.axis_label_text_font_size = axis_label_size
p.yaxis.major_label_text_font_size = axis_ticks_size
p.yaxis.axis_label_standoff = default_padding


# Add Tooltips
hover = HoverTool()
hover.tooltips = """
	<div>	
		<h3>@y</h3>
		<div><strong>Number of Fires: </strong>@right</div>
	</div>

"""

p.add_tools(hover)

#Save file
save(p)

'''
# Print out div and script
script, div = component(p)
print(div)
print(script)
'''

'''
p.hbar(
	y='y',
	right='right',
	left=0,
	height=0.4,
	#fill_color=factor_cmap(
		#'month',
		#palette=Blues8,
		#factors=month_names
	#),
	fill_alpha=0.9,
	source=source,
	legend_label='Month'
)
'''
