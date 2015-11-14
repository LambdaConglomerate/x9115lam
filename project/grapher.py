import matplotlib.pyplot as plt
from model import *

colors = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","DarkOrange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Green","GreenYellow","HoneyDew","HotPink","IndianRed" ,"Indigo" ,"Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","RebeccaPurple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"]

class grapher(object):

	def __init__(s, model, numOfCans):
		s.allCansX = {}
		s.allCansY = {}
		for i in xrange(numOfCans):
			s.allCansX.update({i: []})
			s.allCansY.update({i: []})

		s.model = model

	def addVector(s, v, i):
		x, y = v[0], v[1]
		s.allCansX[i].append(x)
		s.allCansY[i].append(y)

	#this will graph the decisions
	#each color is a unique candidate
	def graph(s):
		plt.title(s.model.name + " Decisions")
		for i in s.allCansX:
			color = [colors[i]] * len(s.allCansY[i])
			#this will calculate all the energies and then scale
			#them to 15 which is accepted by matplotlib 
			#this will increase the size of the circle for each 
			#dot on the graph in proportion to it's
			#betterness as an energy (ie the larger the dot
			#the better the candidate)
			energies = [(s.model.energy([x, y]) * 15) \
				for (x, y) in zip(s.allCansX[i], s.allCansY[i])]
			#note: alpha controls conspiracy
			plt.scatter(s.allCansX[i], s.allCansY[i], s=energies, c=color, alpha=0.5)

		plt.show()

	#this will graph the energies 
	#each color is a unique candidate
	def graphEnergy(s):
		plt.title(s.model.name + " Energies")
		for i in s.allCansX:
			color = [colors[i]] * len(s.allCansX[i])
			o1 = [s.model.calculateObjective([x,y], 0) for (x,y) in zip(s.allCansX[i], s.allCansY[i])]
			o2 = [s.model.calculateObjective([x,y], 1) for (x,y) in zip(s.allCansX[i], s.allCansY[i])]
			plt.scatter(o1, o2, c=color, alpha=0.5)
		plt.show()

