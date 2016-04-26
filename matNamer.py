'''

Maya Material Renamer

'''

import maya.cmds as cmds

def matRenamer(MyModel):

	mySel = cmds.ls(sl=True)

	mySelShp = cmds.listRelatives(mySel, s=True)
	mySG = cmds.rename(cmds.listConnections(mySelShp, type='shadingEngine', d=True, s=False), MyModel + '_SG')
	myMat = cmds.rename(cmds.listConnections(mySG, d=False, s=True)[0], MyModel + '_M')
	myFile = cmds.rename(cmds.listConnections(myMat, d=False, s=True), MyModel + '_T')

matRenamer('MyModel')