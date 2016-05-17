'''

this script is getting the joint data from the selected joint and it's hierarchy


'''

import maya.cmds as cmds
import json

def hierarchy_data():

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

	joint_data.append(k)
	joint_data.append(v)

	return joint_data


def write_json_file():

	filename = cmds.fileDialog2(fm=0, okc="Save Template", dir=starting_dir, ff="*.template")[0]

	temp_file = open(filename, "w")

	json.dump(joint_data, temp_file)
	temp_file.close()

def read_json_file():

	filename = cmds.fileDialog2(fm=1, okc="Load Template", dir=starting_dir, ff="*.template")[0]

	json_file = open(filename)
	joint_data = json.load(json_file)
	json_file.close()