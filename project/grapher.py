from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from model import *

colors = ["Red","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","DarkOrange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Green","GreenYellow","HoneyDew","HotPink","IndianRed" ,"Indigo" ,"Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","RebeccaPurple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"]

class grapher(object):

	def __init__(s, model, numOfCans, numOfTrackedParticles, totalTime, optimizerName):
		s.listOfVectors = [[]] * (numOfCans + 1)
		s.model = model
		s.trackedParticle = [[]] * (numOfTrackedParticles)
		s.timePoint = [[]] * (numOfTrackedParticles)
		s.totalTime = totalTime
		s.optimizerName = optimizerName

	def addVector(s, v, i):
		s.listOfVectors[i].append(v)

	#this is the tracked particle 
	def trackParticle(s, vector , index, timePoint):
		s.trackedParticle[index].append(vector)
		s.timePoint[index].append(timePoint)

	def graphTrackedParticle(s, truePf = True):
		#check for of objectives
		if s.model.numOfObjectives() <= 2:
			fig2 = plt.figure()
			a2 = fig2.add_subplot(111)
			plt.title(s.model.name + " Objectives Tracked Particle" + " - " + s.optimizerName)
			for i in xrange(len(s.trackedParticle)):
				color = [colors[i]]
				for j in xrange(len(s.trackedParticle[i])):
					o = s.model.cal_objs_2(s.trackedParticle[i][j])
					opacity = (s.totalTime - s.timePoint[i][j])/float(s.totalTime)
					a2.scatter(o[0], o[1], c=color, alpha=opacity)
			if truePf:
				path = "./metrics/Spread/True_PF/" + s.model.name + ".txt"
				f = open(path, "r")
				ln = f.readline()
				while ln:
					o = ln.split()
					a2.scatter(o[0], o[1], alpha = 0.01)
					ln = f.readline()

		else:
			#if # of objectives > 3 this will just plot the first three objectives
			fig = plt.figure()
			ax = fig.add_subplot(111, projection='3d')
			ax.text2D(0.05, 0.95, s.model.name + " Objectives Tracked Particle" + " - " + s.optimizerName, transform=ax.transAxes)
			for i in xrange(len(s.trackedParticle)):
				color = [colors[i]]
				for j in xrange(len(s.trackedParticle[i])):
					o = s.model.cal_objs_2(s.trackedParticle[i][j])
					opacity = (s.totalTime - s.timePoint[i][j])/float(s.totalTime)
					ax.scatter(o[0], o[1], o[2], c=color, alpha=opacity)
			if truePf:
				path = "./metrics/Spread/True_PF/" + s.model.name + ".txt"
				f = open(path, "r")
				ln = f.readline()
				while ln:
					o = [float(x) for x in ln.split()]
					ax.scatter(o[0], o[1], o[2], alpha = 0.5)
					ln = f.readline()

		plt.savefig("pics/" + s.optimizerName + s.model.name + "TrackedParticleObjectives.png", bbox_inches='tight')

	#this will graph the decisions
	#each color is a unique candidate
	def graph(s):
		#check to see if the number of decisions is less than 3
		if len(s.listOfVectors[1][0]) <= 2:

			fig2 = plt.figure()
			a2 = fig2.add_subplot(111)
			plt.title(s.model.name + " Decisions" + " - " + s.optimizerName)
			for i in xrange(1, len(s.listOfVectors)):
				print(s.listOfVectors[i])
				color = [colors[i]] * len(s.listOfVectors[i])
				energies = [1.0] * len(s.listOfVectors[i])
				#this will calculate all the energies and then scale
				#them to 15 which is accepted by matplotlib
				#this will increase the size of the circle for each
				#dot on the graph in proportion to it's
				#betterness as an energy (ie the larger the dot
				#the better the candidate)

				#TODO: add this back in later
				#energies = [(s.model.energy([x, y]) * 15) \
				#	for (x, y) in zip(s.allCansX[i], s.allCansY[i])]
				#note: alpha controls conspiracy
				x = [v[0] for v in s.listOfVectors[i]]
				y = [v[1] for v in s.listOfVectors[i]]
				a2.scatter(x, y, s=energies, c=color, alpha=0.5)
		else:
			fig = plt.figure()
			ax = fig.add_subplot(111, projection='3d')
			ax.text2D(0.05, 0.95, s.model.name + " Decisions" + " - " + s.optimizerName, transform=ax.transAxes)
			for i in xrange(1, len(s.listOfVectors)):
				color = [colors[i]] * len(s.listOfVectors[i])
				energies = [1.0] * len(s.listOfVectors[i])
				#TODO: add this back in later
				# energies = [(s.model.energy([x, y, x]) * 15) \
				# 	for (x, y, z) in zip(s.allCansX[i], s.allCansY[i], s.allCansZ[i])]

				#If there are more than 3 deicions this plot with just plot the first three
				#decisions
				x = [v[0] for v in s.listOfVectors[i]]
				y = [v[1] for v in s.listOfVectors[i]]
				z = [v[2] for v in s.listOfVectors[i]]
				ax.scatter(x, y, z, s=energies, c=color, alpha=0.5)

		plt.savefig("pics/" + s.optimizerName + s.model.name + "Decisions.png", bbox_inches='tight')
	#this will graph the energies
	#each color is a unique candidate
	def graphEnergy(s, truePf = True):
		#check for of objectives
		if s.model.numOfObjectives() <= 2:

			fig2 = plt.figure()
			a2 = fig2.add_subplot(111)
			plt.title(s.model.name + " Objectives" + " - " + s.optimizerName)
			for i in xrange(1, len(s.listOfVectors)):
					color = [colors[i]] * len(s.listOfVectors[i])
					o = [s.model.cal_objs_2(v) for v in s.listOfVectors[i]]
					ox = [v[0] for v in o]
					oy = [v[1] for v in o]
					a2.scatter(ox, oy, c=color, alpha=0.5)
			if truePf:
				path = "./metrics/Spread/True_PF/" + s.model.name + ".txt"
				f = open(path, "r")
				ln = f.readline()
				while ln:
					o = ln.split()
					a2.scatter(o[0], o[1], alpha = 0.01)
					ln = f.readline()

		else:
			#if # of objectives > 3 this will just plot the first three objectives
			fig = plt.figure()
			ax = fig.add_subplot(111, projection='3d')
			ax.text2D(0.05, 0.95, s.model.name + " Objectives" + " - " + s.optimizerName, transform=ax.transAxes)
			for i in xrange(1, len(s.listOfVectors)):
					color = [colors[i]] * len(s.listOfVectors[i])
					o = [s.model.cal_objs_2(v) for v in s.listOfVectors[i]]
					ox = [v[0] for v in o]
					oy = [v[1] for v in o]
					oz = [v[2] for v in o]
					ax.scatter(ox, oy, oz, c=color, alpha=0.5)
			if truePf:
				path = "./metrics/Spread/True_PF/" + s.model.name + ".txt"
				f = open(path, "r")
				ln = f.readline()
				while ln:
					o = [float(x) for x in ln.split()]
					ax.scatter(o[0], o[1], o[2], alpha = 0.5)
					ln = f.readline()

		plt.savefig("pics/" + s.optimizerName +  s.model.name + "Objectives.png", bbox_inches='tight')

