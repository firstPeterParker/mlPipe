'''

this script is getting the joint data from the selected joint and it's hierarchy


'''

import maya.cmds as cmds 

root = cmds.ls(sl=True)[0]

joints = []

joints.append(root)

for ix in reversed(root.listRelatives(ad=True)):
	joints.append(ix)

joint_data = {}

for ix in joints:

	attr_dict = {}

	attr_dict ["rotate"] = cmds.xform(ix, q=True, ws=True, ro=True)
	attr_dict ["translate"] = cmds.xform(ix, q=True, ws=True, t=True)
	attr_dict ["joint_parent"] = str(ix.getParent())

	joint_data[str(ix.name())] = attr_data

for k, v in joint_iteritems():
	print k, v