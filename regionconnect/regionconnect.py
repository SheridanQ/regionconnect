#!/usr/bin/env python

# @author Xiaoxiao
# @date 01/27/2020

# version = '1.0'

import argparse
import glob
import logging
import os
from pkg_resources import resource_filename

import nibabel as nib
import numpy as np

DESCRIPTION = """
	Evaluate connectivity of a user-defined white matter ROI

	This is based on the IIT Human Brain Atlas, see
	https://www.nitrc.org/projects/iit/

	This algorithm has 2 steps:
		1. take the mask of user-defined ROI in the IIT Human Brain Atlas space
		2. output a file whre information about the ROI will be sored.

	Author email: Xiaoxiao Qi xqi10@hawk.iit.edu

"""

def buildArgsParser():
	p = argparse.ArgumentParser(description=DESCRIPTION, 
								formatter_class=argparse.RawTextHelpFormatter)

	p.add_argument('ROI_mask', action='store', metavar='ROI_MASK', type=str, 
					help="User-defined ROI mask")
	p.add_argument('output_file', action='store', metavar='OUTTXT', type=str,
					help="Output text file")

	return p


def _get_atlas_files(roi_shape):
	"""
	:param shape:
	:return: a tuple that contains the 3 atlas helper files
	"""
	if roi_shape == (256, 256, 256):
		total_filename = resource_filename('regionconnect', 'atlas/IIT_TDI_sum_256.nii.gz')
		top_fib_filename = resource_filename('regionconnect', 'atlas/IIT_WM_atlas_256.nii.gz')
		top_fib_conf_filename = resource_filename('regionconnect', 'atlas/IIT_WM_atlas_confidence_256.nii.gz')

	elif roi_shape == (182, 218, 182):
		total_filename = resource_filename('regionconnect', 'atlas/IIT_TDI_sum.nii.gz')
		top_fib_filename = resource_filename('regionconnect', 'atlas/IIT_WM_atlas.nii.gz')
		top_fib_conf_filename = resource_filename('regionconnect', 'atlas/IIT_WM_atlas_confidence.nii.gz')

	else:
		print('###')
		print('###ROI is not in IIT space, please register your file to the IIT space first.')
		print('###')
		return

	return (total_filename, top_fib_filename, top_fib_conf_filename)

def _get_overlap(roi_mask, wm_mask):
	#wm_count = np.count_nonzero(wm_mask)
	roi_count = np.count_nonzero(roi_mask)
	overlap = np.logical_and(roi_mask, wm_mask)
	overlap_count = np.count_nonzero(overlap)

	return '{:.0%}'.format(overlap_count/roi_count)

def _get_dict(roi_img, tdi_sum_img, wm_atlas_img, conf_img):
	"""
	:param roi_img: image array
	:param tdi_sum_img: image array
	:param atlas_img: image array
	:param conf_img: image array
	:return: A dictionary that contains all the pairs.
	"""
	n_layers = wm_atlas_img.shape[3]
	print(n_layers)




def get_list(roi_file):
	"""
	Input: An ROI mask image file
	Return: a list of strings that contains the information about connections
	"""
	# Load roi file and atlas files
	roi = nib.load(roi_file)
	roi_shape = roi.shape

	atlas = _get_atlas_files(roi_shape)
	if not atlas:
		print("Exiting...")
		return

	# Get percentages of ROI that are used to calculate the list.
	wm_atlas= nib.load(atlas[1])
	wm_mask_img = wm_atlas.get_data()[:,:,:,0]>0 # This is the white matter mask, the first layer of labels.
	roi_img = roi.get_data()
	percentage_in = _get_overlap(roi_img, wm_mask_img)
	percentage_out = '{:.0%}'.format(1-float(percentage_in.strip('%')))

	if np.count_nonzero(roi_img) > 0:
		tdi_sum_img = nib.load(atlas[0]).get_data()
		wm_atlas_img = wm_atlas.get_data()
		conf_img = nib.load(atlas[2]).get_data()
		dict = _get_dict(roi_img, tdi_sum_img, wm_atlas_img, conf_img)




# lines = ['A Story', 'by Me', '', 'An aardvark escaped from the zoo.', '', 'The End']
# story = '\n'.join(lines)



if __name__ == "__main__":
	# parse
	parser = buildArgsParser()
	args = parser.parse_args()

	roi_mask_input = args.ROI_mask
	output_file_input = args.output_file

	if not os.path.isfile(roi_mask_input):
		parser.error('"{0}" must be a file!'.format(roi_mask_input))

	if os.path.isfile(output_file_input):
		parser.error('"{0}" exists! Please change the file name. '.format(output_file_input))

	get_list(roi_mask_input)


