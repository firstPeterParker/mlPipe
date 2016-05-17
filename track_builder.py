'''

Track building script

description: This script is meant to take a given path and import the maya ascii files
			 that are in that folder. The other functionality will allow the use to re-build
			 the track  iteratively. 

How to use:

import sys	           (scripts path)
sys.path.append(r"C:/Users/Matthew/Desktop/")

import track_builder as tb
reload(tb)

# Class instance
TB = tb.TrackBuilder()

# File reference method (directory where files are located)       
TB.reference_in_files("C:/Users/Matthew/Desktop/trackMayaFolder")

# Build the track forward
TB.build_track_forward()

# Build the track backwards
TB.build_track_backward()

'''

import os
import maya.cmds as cmds

class TrackBuilder:
	# Creates a new file once the instance of the class is called
	def __init__(self):
		# Create new file
		cmds.file(new=True, force=True)

	# References in Geometry from the given filepath
	def reference_in_files(self, path):
		
		filepath = path

		# Reference in all .ma files inside the given filepath 
		for each in os.listdir(filepath):
			if each.endswith(".ma"):
				cmds.file('{0}/{1}'.format(filepath, each), reference=True, namespace="reftrack")

		# Create variable to store the mesh and locators
		self.track_mesh = cmds.ls("*Mesh", recursive=True)
		self.track_end = cmds.ls("*End", recursive=True)

		# Create a group for the mesh and locators
		self.assets_grp = cmds.group(empty=True, name="trackGeo_Grp")

		# Parent the mesh and locators under the new group
		cmds.parent(self.track_mesh, self.assets_grp)
		cmds.parent(self.track_end, self.assets_grp)

	# This will build the references track in a forward manner
	def build_track_forward(self):

		# Create variable to store the mesh and locators
		self.track_mesh = cmds.ls("*Mesh", recursive=True)
		self.track_end = cmds.ls("*End", recursive=True)

		# Create a constraint from mesh to locator
		for ix in range(len(self.track_mesh)):
			cmds.parentConstraint(self.track_mesh[ix], self.track_end[ix], maintainOffset=True)

		# Main track building function
		for ix in range(len(self.track_mesh)):
			if not ix == 0:
				cmds.delete(cmds.parentConstraint(self.track_end[ix-1], self.track_mesh[ix]))

		# Delete constraints to clean the scene 
		for each in self.track_end:
			cmds.delete(cmds.listConnections(each, type="constraint", s=True, d=False)[0])

	# This will build the references track in a backward manner
	def build_track_backward(self):

		# Create variable to store the mesh and locators
		self.track_mesh = cmds.ls("*Mesh", recursive=True)
		self.track_end = cmds.ls("*End", recursive=True)

		# Create a constraint from locator to mesh 
		for ix in range(len(self.track_mesh)):
			cmds.parentConstraint(self.track_end[ix], self.track_mesh[ix], maintainOffset=True)

		# Main track building function
		for ix in range(len(self.track_end)):
			if not ix == 0:
				cmds.delete(cmds.parentConstraint(self.track_mesh[ix-1], self.track_end[ix]))

		# Delete constraints to clean the scene 
		for each in self.track_mesh:
			cmds.delete(cmds.listConnections(each, type="constraint", s=True, d=False)[0])