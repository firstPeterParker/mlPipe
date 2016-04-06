'''
This is a script to automate the rivet rigging method

Instructions:

place this script in your scripts folder. 
Copy the script in 'How to Run:' to your script editor and run.

How to Run:

import pythonRivet
reload(pythonRivet)

pythonRivet.rivetGUI()

'''

from functools import partial
import maya.cmds as cmds

# Create the GUI for the rivet script
def rivetGUI():

	# Delete the window if it already exists 
	if cmds.window('rivetUI', exists = True):
		cmds.deleteUI('rivetUI')

	# Creating the window for the script
	cmds.window('rivetUI', rtf = True)
	cmds.columnLayout('mainCol', adj = True)
	cmds.textField( 'rivetTF', text = 'Prefix_')
	cmds.text( l = '', h = 5)
	cmds.button(
				'rivetBTN',
				l = 'Create Rivet!',
				al = 'center',
				c = partial(createRivet)
				)
	cmds.setParent('mainCol')

	# Show the GUI window
	cmds.showWindow()
	
def createRivet(*args):

	# nameing prefix for objects
	prefix = cmds.textField('rivetTF', q = True, tx=True)

	# Get the selected edges and store in a list 
	ixList = cmds.ls(sl = True, fl = True)

	# If statement to trigger if there are not two edges selected
	if len(ixList) == 2:

		# Get the object's name from the list that was stored
		nameObject = ixList[0].split('.')[0]

		# Get the object's edge index Value from the list that was stored
		edgeOne = ixList[0].split('.')[1].replace('e', '').replace('[','').replace(']','')
		edgeTwo = ixList[1].split('.')[1].replace('e', '').replace('[','').replace(']','')

		# Create the Curve from mesh node for the first selected edge and name 
		nameCFME1 = cmds.createNode('curveFromMeshEdge', n = prefix + '_Rivet1_cfme')

		# Set attributes for later connection
		cmds.setAttr(nameCFME1 + '.ihi', 1)
		cmds.setAttr(nameCFME1 + '.ei[0]', float(edgeOne))

		# Create the Curve from mesh node for the second selected edge and name 
		nameCFME2 = cmds.createNode('curveFromMeshEdge', n = prefix + '_Rivet2_cfme')

		# Set attributes for later connection
		cmds.setAttr(nameCFME2 + '.ihi', 1)
		cmds.setAttr(nameCFME2 + '.ei[0]', float(edgeTwo))

		# Create the Loft node and name 
		nameLoft = cmds.createNode('loft', n = prefix + 'Rivet_loft')

		# Set attributes for later connection
		cmds.setAttr(nameLoft + '.ic', s = 2)
		cmds.setAttr(nameLoft + '.u', True)
		cmds.setAttr(nameLoft + '.rsn', True)

		# Create the point on surface info node and name 
		namePOSI = cmds.createNode('pointOnSurfaceInfo', n = prefix + 'Rivet_pntInfo')

		# Set attributes for later connection
		cmds.setAttr(namePOSI + '.turnOnPercentage', 1)
		cmds.setAttr(namePOSI + '.parameterU', 0.5)
		cmds.setAttr(namePOSI + '.parameterV', 0.5)

		# Connect all the newly created nodes together 
		cmds.connectAttr(nameLoft + '.os', namePOSI + '.is', f=True)
		cmds.connectAttr(nameCFME1 + '.oc', nameLoft + '.ic[0]')
		cmds.connectAttr(nameCFME2 + '.oc', nameLoft + '.ic[1]')
		cmds.connectAttr(nameObject + '.w', nameCFME1 + '.im')
		cmds.connectAttr(nameObject + '.w', nameCFME2 + '.im')

		# Create the rivet locator 
		nameLocator = cmds.createNode('transform', n = prefix + 'Rivet_loc')
		locRivet = cmds.createNode('locator', n = nameLocator + 'Shape', p = nameLocator)

		# Add custom attributes to the rivet locator for user input 
		cmds.addAttr(nameLocator, k = True, ln = 'offset_u', min = -0, max = 1)
		cmds.addAttr(nameLocator, k = True, ln = 'offset_v', min = -0, max = 1)

		# Set none transform attributes to none keyable
		cmds.setAttr(nameLocator + '.tx', k = False)
		cmds.setAttr(nameLocator + '.ty', k = False)
		cmds.setAttr(nameLocator + '.tz', k = False)
		cmds.setAttr(nameLocator + '.rx', k = False)
		cmds.setAttr(nameLocator + '.ry', k = False)
		cmds.setAttr(nameLocator + '.rz', k = False)

		# Create the aimConstraint
		nameAC = cmds.createNode('aimConstraint', p = nameLocator, n = prefix + 'Rivet_aimCnstr')

		# Set the attributes for the aimConstraint
		cmds.setAttr(nameAC + '.tg[0].tw', 1)
		cmds.setAttr(nameAC + '.a', 0,1,0, type = 'double3')
		cmds.setAttr(nameAC + '.u', 0,0,1, type = 'double3')
		cmds.setAttr(nameAC + '.v', k = False)
		cmds.setAttr(nameAC + '.tx', k = False)
		cmds.setAttr(nameAC + '.ty', k = False)
		cmds.setAttr(nameAC + '.tz', k = False)
		cmds.setAttr(nameAC + '.rx', k = False)
		cmds.setAttr(nameAC + '.ry', k = False)
		cmds.setAttr(nameAC + '.rz', k = False)
		cmds.setAttr(nameAC + '.sx', k = False)
		cmds.setAttr(nameAC + '.sy', k = False)
		cmds.setAttr(nameAC + '.sz', k = False)

		# Connect all the nodes together 
		cmds.connectAttr(namePOSI + '.position', nameLocator + '.translate')
		cmds.connectAttr(namePOSI + '.n', nameAC + '.tg[0].tt')
		cmds.connectAttr(namePOSI + '.tv', nameAC + '.wu')
		cmds.connectAttr(nameAC + '.crx', nameLocator + '.rx')
		cmds.connectAttr(nameAC + '.cry', nameLocator + '.ry')
		cmds.connectAttr(nameAC + '.crz', nameLocator + '.rz')

		# Get the U and V parameter and return it as a float value
		offU = float(cmds.getAttr(namePOSI + '.parameterU'))
		offV = float(cmds.getAttr(namePOSI + '.parameterV'))

		# Set the attribute on the locator UV parameters
		cmds.setAttr(nameLocator + '.offset_u', offU)
		cmds.setAttr(nameLocator + '.offset_v', offV)

		# Connect the locator Node to the point on Surface info
		cmds.connectAttr(nameLocator + '.offset_u', namePOSI + '.parameterU')
		cmds.connectAttr(nameLocator + '.offset_v', namePOSI + '.parameterV')

	else:

		# Error message 
		cmds.error('Must selected two edges')
