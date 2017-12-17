import os
import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.color import rgb2gray
from sklearn import svm
from sklearn.metrics import accuracy_score
from natsort import natsorted

f = open("answer.out", 'w')
sys.stdout = f

from numpy.random import seed
np.random.seed(2016)

size=20

class Data:
	element=[[0 for x in range(size)] for y in range(size)]
	label=0
	def __init__(self,e,l):
		self.element=e
		self.label=l

train=[]
mainPath='TrainingData'
total=36

# A-10 , B-11....
i=0
for subDir in os.listdir(mainPath):
	path=os.path.join(mainPath,subDir)
	for fileName in os.listdir(path):
		filePath=os.path.join(path,fileName)
		image=mpimg.imread(filePath)
		image=rgb2gray(image)
		obj=Data(image,i)
		train.append(obj)
	i=i+1
l=len(train)

np.random.shuffle(train)

trainingSet,testSet=np.split(train,[int(0.8*l)])

#print('train',len(trainingSet))
#print('test',len(testSet))


xTrain=[]
yTrain=[]

for e in trainingSet:
	x=e.element
	y=e.label
	x=x.flatten()
	xTrain.append(x)
	yTrain.append(y)

xTest=[]
yTest=[]

for e in testSet:
	x=e.element
	y=e.label
	x=x.flatten()
	xTest.append(x)
	yTest.append(y)

clf = svm.SVC(kernel='linear', C = 1.0,probability=True)
clf.fit(xTrain,yTrain)

limit=len(xTest)


#print(accuracy_score(yTest,clf.predict(xTest)))


temp=[]
listOfFiles=[]

mainPath='correct'

dirFiles=os.listdir(mainPath)
dirFiles=natsorted(dirFiles)


check=0
for subDir in dirFiles:
	path=os.path.join(mainPath,subDir)
	image=mpimg.imread(path)
	image=rgb2gray(image)
	image=image.flatten()
	listOfFiles.append(subDir)
	temp.append(image)


prob=clf.predict_proba(temp)

predictions=clf.predict(temp)

for i in range(len(prob)):
	maxElement=np.amax(prob[i])
	if(maxElement<0.11):
		continue
	val=int(predictions[i])
	ans=''
	if(val>=0 and val<=9):
		ans=str(val)
	else:
		diff=val-10
		ans=chr(ord('A')+diff)
	#print(maxElement)
	print(ans)
	#print(ans,listOfFiles[i])