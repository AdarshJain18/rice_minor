import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly import subplots
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import cv2
from PIL import Image
from io import BytesIO
import base64
# import dash_bootstrap_components as dbc

# app = dash.Dash(external_stylesheets=[dbc.themes. PULSE])

app = dash.Dash(__name__)

#server=app.server

text1="""
	lorem ipsum
"""
text2="""
lorem ipsum
"""
text3="""
lorem ipsum
"""
text4="""
lorem ipsum
"""
text5="""
lorem ipsum
"""
text6="""
lorem ipsum
"""

def get_classification(ratio):
	ratio =round(ratio,1)
	toret=""
	if(ratio>=3 and ratio<3.5):
		toret="Slender"
	elif(ratio>=2.1 and ratio<3):
		toret="Medium"
	elif(ratio>=1.1 and ratio<2.1):
		toret="Bold"
	elif(ratio>0.9 and ratio<=1):
		toret="Round"
	else:
		toret="Dust"
	return toret

classification = {"Slender":0, "Medium":0, "Bold":0, "Round":0, "Dust":0}
avg = {"Slender":0, "Medium":0, "Bold":0, "Round":0, "Dust":0}
img = cv2.imread("./assets/rice.png",0)#load in greyscale mode

#convert into binary
ret,binary = cv2.threshold(img,160,255,cv2.THRESH_BINARY)# 160 - threshold, 255 - value to assign, THRESH_BINARY_INV - Inverse binary
# print(ret)
# print(binary)
#averaging filter
kernel = np.ones((5,5),np.float32)/9
dst = cv2.filter2D(binary,-1,kernel)# -1 : depth of the destination image

kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
# print(kernel)
# print(dst)
# print(kernel2)
# erosion
erosion = cv2.erode(dst,kernel2,iterations = 1)
# print(erosion)
# dilation 
dilation = cv2.dilate(erosion,kernel2,iterations = 1)
# print(dilation)
# edge detection
edges = cv2.Canny(dilation,100,200)
# print(edges)
## Size detection
contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# print("No. of rice grains=",len(contours))
# print("No. of rice grains=",contours)
# print("No. of rice grains=",len(hierarchy))
# print("No. of rice grains=",hierarchy)
total_ar=0
# print(contours[0])
for cnt in contours:
	x,y,w,h = cv2.boundingRect(cnt)
	aspect_ratio = float(w)/h
	if(aspect_ratio<1):
		aspect_ratio=1/aspect_ratio
	# print(round(aspect_ratio,2),get_classification(aspect_ratio))
	classification[get_classification(aspect_ratio)] += 1
	if get_classification(aspect_ratio) != "Dust":
		total_ar+=aspect_ratio
	if get_classification(aspect_ratio) != "Dust":
		avg[get_classification(aspect_ratio)] += aspect_ratio

avg_ar=total_ar/len(contours)
# print(avg_ar)
# print(classification["Medium"])
# print(avg['Slender'])
if classification['Slender']!=0:
	avg['Slender'] = avg['Slender']/classification['Slender']
	# print(avg['Slender'])
if classification['Medium']!=0:
	avg['Medium'] = avg['Medium']/classification['Medium']
if classification['Bold']!=0:
	avg['Bold'] = avg['Bold']/classification['Bold']
if classification['Round']!=0:
	avg['Round'] = avg['Round']/classification['Round']
# print(img)
# print(binary)
# print(dst)
# print(erosion)
# print(dilation)
# print(edges)
cv2.imwrite("./assets/img.jpg", img)
cv2.imwrite("./assets/binary.jpg", binary)
cv2.imwrite("./assets/dst.jpg", dst)
cv2.imwrite("./assets/erosion.jpg", erosion)
cv2.imwrite("./assets/dilation.jpg", dilation)
cv2.imwrite("./assets/edges.jpg", edges)

# print(classification)
# print(avg_ar)
# print(avg)


def readb64(base64_string):
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(base64_string))
    pimg = Image.open(sbuf)
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

def update_image(pic):
	img = readb64(pic)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	classification1 = {"Slender":0, "Medium":0, "Bold":0, "Round":0, "Dust":0}
	avg1 = {"Slender":0, "Medium":0, "Bold":0, "Round":0, "Dust":0}
	#convert into binary
	ret,binary = cv2.threshold(img,160,255,cv2.THRESH_BINARY)# 160 - threshold, 255 - value to assign, THRESH_BINARY_INV - Inverse binary
	#averaging filter
	kernel = np.ones((5,5),np.float32)/9
	dst = cv2.filter2D(binary,-1,kernel)# -1 : depth of the destination image

	kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

	#erosion
	erosion = cv2.erode(dst,kernel2,iterations = 1)

	#dilation 
	dilation = cv2.dilate(erosion,kernel2,iterations = 1)

	#edge detection
	edges = cv2.Canny(dilation,100,200)

	## Size detection
	contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#print("No. of rice grains=",len(contours))
	total_ar1=0
	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		aspect_ratio = float(w)/h
		if(aspect_ratio<1):
			aspect_ratio=1/aspect_ratio
		#print(round(aspect_ratio,2),get_classification(aspect_ratio))
		classification1[get_classification(aspect_ratio)] += 1
		if get_classification(aspect_ratio) != "Dust":
			total_ar1+=aspect_ratio
		if get_classification(aspect_ratio) != "Dust":
			avg1[get_classification(aspect_ratio)] += aspect_ratio
	avg_ar1=total_ar1/len(contours)
	if classification1['Slender']!=0:
		avg1['Slender'] = avg1['Slender']/classification1['Slender']
	if classification1['Medium']!=0:
		avg1['Medium'] = avg1['Medium']/classification1['Medium']
	if classification1['Bold']!=0:
		avg1['Bold'] = avg1['Bold']/classification1['Bold']
	if classification1['Round']!=0:
		avg1['Round'] = avg1['Round']/classification1['Round']
	cv2.imwrite("./assets/img1.jpg", img)
	cv2.imwrite("./assets/binary1.jpg", binary)
	cv2.imwrite("./assets/dst1.jpg", dst)
	cv2.imwrite("./assets/erosion1.jpg", erosion)
	cv2.imwrite("./assets/dilation1.jpg", dilation)
	cv2.imwrite("./assets/edges1.jpg", edges)
	return classification1,avg1,avg_ar1

def get_image(path):
	img = Image.open(path)
	#Constants
	img_width = 710
	img_height = 550
	scale_factor = 0.5
	fig = go.Figure()
	fig.add_trace(
		go.Scatter(
			x=[0, img_width * scale_factor],
			y=[0, img_height * scale_factor],
			mode="markers",
			marker_opacity=0
		)
	)
	fig.update_xaxes(
		visible=False,
		range=[0, img_width * scale_factor]
	)
	fig.update_yaxes(
		visible=False,
		range=[0, img_height * scale_factor],
		scaleanchor="x"
	)
	fig.add_layout_image(
		dict(
			x=0,
			sizex=img_width * scale_factor,
			y=img_height * scale_factor,
			sizey=img_height * scale_factor,
			xref="x",
			yref="y",
			opacity=1.0,
			layer="below",
			sizing="stretch",
			source=img)
	)
	fig.update_layout(
		width=img_width * scale_factor,
		height=img_height * scale_factor,
		margin={"l": 0, "r": 0, "t": 0, "b": 0},
	)
	# fig.show(config={'doubleClick': 'reset'})
	return fig

def get_plot1(classification = classification, avg = avg, avg_ar = avg_ar):
	fig = subplots.make_subplots(rows=1,cols=1,specs=[[{"type":"bar"}]], shared_xaxes=True)
	#print(list(classification.keys()))
	#print(list(classification.values()))
	plot1 = go.Bar(x=list(classification.keys()), y=list(classification.values()), name="Particles")
	plot2 = go.Bar(x=list(avg.keys()), y=list(avg.values()), name="Avg. Aspect Ratio")
	fig.add_trace(plot1,1,1)
	fig.add_trace(plot2,1,1)
	fig.add_shape(
		type="line",
		x0=0,
		y0=round(avg_ar,2),
		x1=5,
		y1=round(avg_ar,2),
		line=dict(
			color="LightSeaGreen",
			width=4,
			dash="dashdot",
		),
	)
	fig.update_layout(
		width = 600,
		height = 350,
		margin = {"l": 5, "r": 5, "t": 30, "b": 5},
		title = "Average Aspect Ratio Vs Classification",
		template = "plotly_dark"
	)
	return fig

def get_plot2(classification = classification):
	fig = subplots.make_subplots(rows=1,cols=1,specs=[[{"type":"pie"}]])
	rice = sum(list(classification.values())) - classification['Dust']
	dust = classification['Dust']
	values = [rice, dust]
	labels = ["Rice", "Dust"]
	plot1 = go.Pie(labels=labels, values=values, hole=.3)
	fig.add_trace(plot1,1,1)
	fig.update_layout(
		width = 600,
		height = 350,
		margin = {"l": 65, "r": 5, "t": 60, "b": 50},
		title = "Quality Analysis",
		template = "plotly_dark"
	)
	return fig

app.layout = html.Div([
	html.Div([
		html.Div([
			# html.Img(
			# 	src="/assets/logo.jpg",
			# 	style={"height" : "40px", "width" : "40px", "border-radius":"20px"}
			# )
		],style={"float":"left","padding" : "5px 0 5px 50px"}),
		html.Div(
			children="Rice quality analysis using Image Processing",
			style={"float":"left","padding" : "10px 0 10px 10px","font-size": "20px", "font-weight" :"600", "font-family" : "Noto Sans", "text-align": "center"}
		),
		html.Div([
			html.Div([html.A("Home",href="#home")], style={"float":"left","padding":"0 10px 0 10px","align-items": "center","font-size": "15px", "font-weight" :"600"}),
			html.Div([html.A("About Project",href="#about-project")], style={"float":"left","padding":"0 10px 0 10px","align-items": "center","font-size": "15px", "font-weight" :"600"}),
			html.Div([html.A("About Us",href="#about-us")], style={"float":"left","padding":"0 10px 0 10px","align-items": "center","font-size": "15px", "font-weight" :"600"}),
			html.Div([html.A("Source Code",href="#bottom")], style={"float":"left","padding":"0 10px 0 10px","align-items": "center","font-size": "15px", "font-weight" :"600"}),
		],style={"float":"right", "padding": "10px 50px 10px 0px"})
	],className="nav"),
	html.Div([],style={"height":"50px"},id="home"),
	html.Div([
		html.Div([
			dcc.Upload([
					'Drag and Drop or ',
					html.A('Select a File')
				],
				style={
					# 'position': 'absolute',
					'width': '100%',
					'height': '60px',
					'lineHeight': '60px',
					'borderWidth': '1px',
					#'borderStyle': 'dashed',
					'borderRadius': '5px',
					'text-align': 'center', "align-items" : "center"
				 }, id="upload-image")
		], style={"text-align" : "center",'width': 'auto', 'margin': 'auto'}),
		# dcc.Upload([
		# 			'Drag and Drop or ',
		# 			html.A('Select a File')
		# 		],
		# 		style={
		# 			# 'position': 'absolute',
		# 			'width': '50%',
		# 			'height': '60px',
		# 			'lineHeight': '60px',
		# 			'borderWidth': '1px',
		# 			'borderStyle': 'dashed',
		# 			'borderRadius': '5px',
		# 			'textAlign': 'center', "align-items" : "center"
		# 		 }, id="upload-image"),
		# html.H1(children="Visualisation of Results", style={"text-align":"center", "margin":"0", "padding-bottom" : "20px", "color" : "black"}),
		html.Div([
			html.H1(children="Images", style={"text-align":"center", "margin":"0", "padding-bottom" : "20px"}),
				html.Div([
					html.Div([
						dcc.Graph(figure=get_image("./assets/img.jpg"),id="img"),
						html.P("Original Image", style={"margin":"0","padding-bottom":"10px"})
					], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
					html.Div([
						dcc.Graph(figure=get_image("./assets/binary.jpg"),id="binary"),
						html.P("Binary Image", style={"margin":"0","padding-bottom":"10px"})
					], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
					html.Div([
						dcc.Graph(figure=get_image("./assets/dst.jpg"),id="dst"),
						html.P("Destination Image", style={"margin":"0","padding-bottom":"10px"})
					], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"})
				], style = {"display": "flex", "justify-content": "center", "align-items": "center", "text-align":"center"}),
				html.Div([]),
				html.Div([
					html.Div([
						dcc.Graph(figure=get_image("./assets/erosion.jpg"),id="erosion"),
						html.P("Erosion", style={"margin":"0","padding-bottom":"10px"})
					], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
					html.Div([
						dcc.Graph(figure=get_image("./assets/dilation.jpg"),id="dilation"),
						html.P("Dilation", style={"margin":"0","padding-bottom":"10px"})
					], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
					html.Div([
						dcc.Graph(figure=get_image("./assets/edges.jpg"),id="edges"),
						html.P("Edge Detection", style={"margin":"0","padding-bottom":"10px"})
					], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"})
				], style = {"display": "flex", "justify-content": "center", "align-items": "center", "text-align":"center"})
			],style = {"color":"black", "background-color" : "burlywood", "border-radius":"40px 40px 40px 40px", "padding" : "20px 0 20px 0"},id='images'),
		# html.Div([
		# 	html.Div([
		# 		dcc.Graph(figure=get_plot1(),id="graph1"),
		# 		html.P("Original Image", style={"margin":"0","padding-bottom":"10px"})
		# 	], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
		# 	html.Div([
		# 		dcc.Graph(figure=get_plot2(),id="graph2"),
		# 		html.P("Binary Image", style={"margin":"0","padding-bottom":"10px"})
		# 	], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
		# ], style = {"display": "flex", "justify-content": "center", "align-items": "center", "text-align":"center"}),
		html.Div([]),
		html.Div([
			html.Div([
				 html.H1(children="Visualisation of Results", style={"text-align":"center", "margin":"0", "padding-bottom" : "20px", "color" : "black"}),
				# dcc.Upload([
				# 	'Drag and Drop or ',
				# 	html.A('Select a File')
				# ],
				# style={
				# 	# 'position': 'absolute',
				# 	'width': '100%',
				# 	'height': '60px',
				# 	'lineHeight': '60px',
				# 	'borderWidth': '1px',
				# 	'borderStyle': 'dashed',
				# 	'borderRadius': '5px',
				# 	'textAlign': 'center'
				#  }, id="upload-image"),
			], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
		], style = {"display": "flex", "justify-content": "center", "align-items": "center", "text-align":"center", "width" : "100%"})
	],style = {"color":"black", "padding" : "20px 0 20px 0", "color" : "whitesmoke","background-color" : "lightcoral"},id='plots'),
	html.Div([
			html.Div([
				dcc.Graph(figure=get_plot1(),id="graph1"),
				html.P("Original Image", style={"margin":"0","padding-bottom":"10px"})
			], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
			html.Div([
				dcc.Graph(figure=get_plot2(),id="graph2"),
				html.P("Binary Image", style={"margin":"0","padding-bottom":"10px"})
			], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
		], style = {"display": "flex", "justify-content": "center", "align-items": "center", "text-align":"center"}),
	# html.Div([
	# 	html.H1(children="Images", style={"text-align":"center", "margin":"0", "padding-bottom" : "20px"}),
	# 	html.Div([
	# 		html.Div([
	# 			dcc.Graph(figure=get_image("./assets/img.jpg"),id="img"),
	# 			html.P("Original Image", style={"margin":"0","padding-bottom":"10px"})
	# 		], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
	# 		html.Div([
	# 			dcc.Graph(figure=get_image("./assets/binary.jpg"),id="binary"),
	# 			html.P("Binary Image", style={"margin":"0","padding-bottom":"10px"})
	# 		], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
	# 		html.Div([
	# 			dcc.Graph(figure=get_image("./assets/dst.jpg"),id="dst"),
	# 			html.P("Destination Image", style={"margin":"0","padding-bottom":"10px"})
	# 		], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"})
	# 	], style = {"display": "flex", "justify-content": "center", "align-items": "center", "text-align":"center"}),
	# 	html.Div([]),
	# 	html.Div([
	# 		html.Div([
	# 			dcc.Graph(figure=get_image("./assets/erosion.jpg"),id="erosion"),
	# 			html.P("Erosion", style={"margin":"0","padding-bottom":"10px"})
	# 		], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
	# 		html.Div([
	# 			dcc.Graph(figure=get_image("./assets/dilation.jpg"),id="dilation"),
	# 			html.P("Dilation", style={"margin":"0","padding-bottom":"10px"})
	# 		], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"}),
	# 		html.Div([
	# 			dcc.Graph(figure=get_image("./assets/edges.jpg"),id="edges"),
	# 			html.P("Edge Detection", style={"margin":"0","padding-bottom":"10px"})
	# 		], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 20px 0 20px"})
	# 	], style = {"display": "flex", "justify-content": "center", "align-items": "center", "text-align":"center"})
	# ],style = {"color":"black", "background-color" : "burlywood", "border-radius":"40px 40px 40px 40px", "padding" : "20px 0 20px 0"},id='images'),
	html.Div([
		html.H1(children="About Project", style={"text-align":"center"}),
		html.P(children=text1),
		html.P(children=text2),
		html.P(children=text3),
		html.P(children=text4),
		html.P(children=text5),
		html.P(children=text6),
	],style = {"color":"white", "padding":"10px 50px 10px 50px","background-color" : "aqua"},id="about-project"),
	html.Div([
		html.H1(children="About Us", style={"text-align":"center", "margin":"0", "padding-bottom" : "20px"}),
		html.Div([
			html.Div([
				html.Img(src="/assets/ramu.jpg", style={"height":"120px","height":"120px","border-radius":"60px"}),
				html.P("Adarsh", style={"margin":"0"})
			], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 50px 0 50px"}),
			html.Div([
				html.Img(src="/assets/kishore.jpg", style={"height":"120px","height":"120px","border-radius":"60px"}),
				html.P("Nakshatra", style={"margin":"0"})
			], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 50px 0 50px"}),
			html.Div([
				html.Img(src="/assets/sart.jpg", style={"height":"120px","height":"120px","border-radius":"60px"}),
				html.P("Yashashwi", style={"margin":"0"})
			], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 50px 0 50px"})
		], style = {"display": "flex", "justify-content": "center", "align-items": "center", "text-align":"center"}),
		html.Div([]),
		html.Div([
			html.Div([
				html.Img(src="/assets/yash.jpg", style={"height":"120px","height":"120px","border-radius":"60px"}),
				html.P("Pranjal", style={"margin":"0"})
			], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 50px 0 50px"}),
			html.Div([
				html.Img(src="/assets/gaut.jpg", style={"height":"120px","height":"120px","border-radius":"60px"}),
				html.P("Sharwari", style={"margin":"0"})
			], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 50px 0 50px"}),
			html.Div([
				html.Img(src="/assets/gaut.jpg", style={"height":"120px","height":"120px","border-radius":"60px"}),
				html.P("Shrushti", style={"margin":"0"})
			], style = {"display": "block", "justify-content": "center", "align-items": "center", "padding":"0 50px 0 50px"})
		], style = {"display": "flex", "justify-content": "center", "align-items": "center", "text-align":"center"})
	],style = {"color":"black", "background-color" : "lightsteelblue", "border-radius":"40px 40px 0 0", "padding" : "20px 0 20px 0"},id='about-us'),
	html.Div([
		html.Div([
			html.Div([html.A("Github",href="https://www.google.com/")], style={"padding":"0 10px 0 10px","align-items": "center","font-size": "15px", "font-weight" :"600"}),
		],style={"padding": "10px 50px 10px 0px", "height": "50px","align-items": "center","background-color": "black","color": "whitesmoke","width": "100%","list-style-type": "none","margin": "0","overflow": "hidden","text-align": "center","right": "0","bottom": "0","left": "0","clear": "both","position": "relative"})
	],className="foo",id="bottom")
])

def parse_contents(contents, filename):
	print(contents)

@app.callback([Output('img', 'figure'),
			   Output('binary', 'figure'),
			   Output('dst', 'figure'),
			   Output('erosion', 'figure'),
			   Output('dilation', 'figure'),
			   Output('edges', 'figure'),
			   Output('graph1', 'figure'),
			   Output('graph2', 'figure')],
			  [Input('upload-image', 'contents')])
def update_output(list_of_contents):
	if list_of_contents is not None:
		ind = str(list_of_contents).find(",")
		cla,av,av_ar = update_image(list_of_contents[ind:])
		return get_image("./assets/img1.jpg"), get_image("./assets/binary1.jpg"), get_image("./assets/dst1.jpg"), get_image("./assets/erosion1.jpg"), get_image("./assets/dilation1.jpg"), get_image("./assets/edges1.jpg"), get_plot1(cla, av, av_ar), get_plot2(cla)
	else:
		return get_image("./assets/img.jpg"), get_image("./assets/binary.jpg"), get_image("./assets/dst.jpg"), get_image("./assets/erosion.jpg"), get_image("./assets/dilation.jpg"), get_image("./assets/edges.jpg"), get_plot1(), get_plot2()

if __name__ == '__main__':
	app.run_server(debug=False)

