'''

This script will generate a UI so that the user can copy curve shapes by selection or by name

import sys

sys.path.append(r"X:\Lani Pixels\Libraries\Maya\mayaLpPython\mattPyMdl")

import copyCurveShape
reload (copyCurveShape)

copyCurveShape.copyCrvShapeUI()

'''

import maya.cmds as cmds
from functools import partial

def copyCrvShapeUI():

	if cmds.window('copyCrvShapeWin', exists=True):
		cmds.deleteUI('copyCrvShapeWin')
	
	cmds.window('copyCrvShapeWin', t='CopyCurve', rtf=True)

	cmds.columnLayout('mainCL', adj=True)

	cmds.text(l='Search for', align='center')

	cmds.textField('searchTF')

	cmds.textField('searchTF', e=True, tx='_L_')

	cmds.separator()

	cmds.text(align='center', l='Replace with')

	cmds.textField('replaceTF')

	cmds.textField('replaceTF', e=True, tx='_R_')

	cmds.separator()

	cmds.button('copyBTN', l='copy', c=partial(copyCrvShape))

	cmds.showWindow('copyCrvShapeWin')
	cmds.window('copyCrvShapeWin', e=True, w=220, h=98)

def copyCrvShape(*args):

	sel = cmds.ls(sl=True)

	crvShape = cmds.listRelatives(sel[0], s=True)
	# print crvShape
	crvDegree = int(cmds.getAttr(crvShape[0] + '.degree'))
	# print crvDegree
	crvSpans = int(cmds.getAttr(crvShape[0] + '.spans'))
	# print crvSpans

	crvCvs = crvDegree + crvSpans
	# print crvCvs

	if len(sel) > 1:

		for ix in range(crvCvs):

			pos = cmds.xform(sel[0] + '.cv[' + str(ix) + ']', q=True, os=True, t=True)

			for iy in range(1, len(sel)):

				cmds.xform(sel[iy] + '.cv[' + str(ix) + ']', os=True, t=[-pos[0], pos[1], pos[2]])

	else:

		for ix in range(crvCvs):

			pos = cmds.xform(sel[0] + '.cv[' + str(ix) + ']', q=True, ws=True, t=True)

			searchFor = cmds.textField('searchTF', q=True, tx=True)
			switch = cmds.textField('replaceTF', q=True, tx=True)

			newCrv = sel[0].replace(searchFor, switch)

			cmds.xform(newCrv + '.cv[' + str(ix) + ']', ws=True, t=[-pos[0], pos[1], pos[2]])