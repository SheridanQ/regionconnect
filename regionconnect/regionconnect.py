#!/usr/bin/env python

# @author Xiaoxiao
# @date 01/29/2020

# version = '1.0'

import argparse
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
        2. output a file where information about the ROI will be sored.

    Usages:

    ./regionconnect/regionconnect.py ROI_MASK OUT_TXT

    or 
    Python console:
    >>from regionconnect import regionconnect as rc
    >>rc.regionconnect(ROI_MASK, OUT_TXT)

    Author email: Xiaoxiao Qi, xqi10@hawk.iit.edu

"""

def buildArgsParser():
    p = argparse.ArgumentParser(description=DESCRIPTION, 
                                formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument('ROI_mask', action='store', metavar='ROI_MASK', type=str, 
                    help="User-defined ROI mask")
    p.add_argument('output_file', action='store', metavar='OUT_TXT', type=str,
                    help="Output text file")

    return p


def _get_atlas_files(roi_shape):
    """
    :param shape:
    :return: a tuple that contains the 3 atlas helper files
    """
    import urllib.request

    if roi_shape == (256, 256, 256):
        _url_total_filename = 'https://www.nitrc.org/frs/download.php/11383/IIT_TDI_sum_256.nii.gz'
        _url_top_fib_filename = 'https://www.nitrc.org/frs/download.php/11387/IIT_WM_atlas_256.nii.gz'
        _url_top_fib_conf_filename = 'https://www.nitrc.org/frs/download.php/11390/IIT_WM_atlas_confidence_256.nii.gz'

        total_filename = resource_filename('regionconnect', 'IIT_TDI_sum_256.nii.gz')
        top_fib_filename = resource_filename('regionconnect', 'IIT_WM_atlas_256.nii.gz')
        top_fib_conf_filename = resource_filename('regionconnect', 'IIT_WM_atlas_confidence_256.nii.gz')

        if not (os.path.isfile(total_filename) and os.path.isfile(top_fib_filename) and os.path.isfile(top_fib_conf_filename)):
            print('Downloading IIT Human Brain Atlas files from www.nitrc.org/projects/iit ......')
            urllib.request.urlretrieve(_url_total_filename, total_filename)
            urllib.request.urlretrieve(_url_top_fib_filename, top_fib_filename)
            urllib.request.urlretrieve(_url_top_fib_conf_filename, top_fib_conf_filename)
        else:
            print('IIT Human Brain Atlas files exist.')

    elif roi_shape == (182, 218, 182):
        _url_total_filename = 'https://www.nitrc.org/frs/download.php/11366/IIT_TDI_sum.nii.gz'
        _url_top_fib_filename = 'https://www.nitrc.org/frs/download.php/11375/IIT_WM_atlas.nii.gz'
        _url_top_fib_conf_filename = 'https://www.nitrc.org/frs/download.php/11373/IIT_WM_atlas_confidence.nii.gz'

        total_filename = resource_filename('regionconnect', 'IIT_TDI_sum.nii.gz')
        top_fib_filename = resource_filename('regionconnect', 'IIT_WM_atlas.nii.gz')
        top_fib_conf_filename = resource_filename('regionconnect', 'IIT_WM_atlas_confidence.nii.gz')

        if not (os.path.isfile(total_filename) and os.path.isfile(top_fib_filename) and os.path.isfile(top_fib_conf_filename)):
            print('Downloading IIT Human Brain Atlas files from www.nitrc.org/projects/iit ...')
            urllib.request.urlretrieve(_url_total_filename, total_filename)
            urllib.request.urlretrieve(_url_top_fib_filename, top_fib_filename)
            urllib.request.urlretrieve(_url_top_fib_conf_filename, top_fib_conf_filename)
        else:
            print('IIT Human Brain Atlas files exist.')

    else:
        print('###')
        print('###ROI is not in the IIT space, please register your file to the IIT space first.')
        print('###')
        return

    return (total_filename, top_fib_filename, top_fib_conf_filename)


def _get_overlap(roi_mask, wm_mask):
    """
    :param roi_mask:
    :param wm_mask:
    :return: a string of percentage value
    """
    #wm_count = np.count_nonzero(wm_mask)
    roi_count = np.count_nonzero(roi_mask)
    overlap = np.logical_and(roi_mask, wm_mask)
    overlap_count = np.count_nonzero(overlap)

    return '{:.2%}'.format(overlap_count/roi_count)


def _get_dict_list(roi_img, tdi_sum_img, wm_atlas_img, conf_img):
    """
    :param roi_img: image array
    :param tdi_sum_img: image array
    :param atlas_img: image array
    :param conf_img: image array
    :return: A sorted list that contains tuples of all the pairs.
    """
    n_layers = wm_atlas_img.shape[3]
    dictionary = dict()
    total_count = 0
    for layer in range(n_layers):

        wm_atlas = wm_atlas_img[:,:,:,layer]
        conf = conf_img[:,:,:,layer]

        x,y,z = np.where(np.logical_and(wm_atlas, roi_img))

        for i in range(x.shape[0]):

            if layer==0:
                total_count += tdi_sum_img[x[i],y[i],z[i]]

            label = wm_atlas[x[i],y[i],z[i]]
            label_count = conf[x[i],y[i],z[i]] * tdi_sum_img[x[i],y[i],z[i]]

            if label in dictionary:
                dictionary[label] += label_count
            else:
                dictionary[label] = label_count

    for key in dictionary.keys():
        dictionary[key] = dictionary[key] / total_count
    # sort list by
    dict_list = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

    return dict_list


def _get_name_of_label(labelnumber):
    """
    :param label number: WM label value
    :return: string of white matter name
    """
    names={'1': 'ctx-lh-bankssts', '2': 'ctx-lh-caudalanteriorcingulate', '3': 'ctx-lh-caudalmiddlefrontal', '4': 'ctx-lh-cuneus', '5': 'ctx-lh-entorhinal', '6': 'ctx-lh-fusiform', '7': 'ctx-lh-inferiorparietal', '8': 'ctx-lh-inferiortemporal', '9': 'ctx-lh-isthmuscingulate', '10': 'ctx-lh-lateraloccipital','11': 'ctx-lh-lateralorbitofrontal', '12': 'ctx-lh-lingual', '13': 'ctx-lh-medialorbitofrontal', '14': 'ctx-lh-middletemporal', '15': 'ctx-lh-parahippocampal', '16': 'ctx-lh-paracentral', '17': 'ctx-lh-parsopercularis', '18': 'ctx-lh-parsorbitalis', '19': 'ctx-lh-parstriangularis', '20': 'ctx-lh-pericalcarine', '21': 'ctx-lh-postcentral', '22': 'ctx-lh-posteriorcingulate', '23': 'ctx-lh-precentral', '24': 'ctx-lh-precuneus', '25': 'ctx-lh-rostralanteriorcingulate', '26': 'ctx-lh-rostralmiddlefrontal', '27': 'ctx-lh-superiorfrontal', '28': 'ctx-lh-superiorparietal', '29': 'ctx-lh-superiortemporal','30': 'ctx-lh-supramarginal', '31': 'ctx-lh-frontalpole', '32': 'ctx-lh-temporalpole', '33': 'ctx-lh-transversetemporal', '34': 'ctx-lh-insula', '35': 'Left-Cerebellum-Cortex', '36': 'Left-Thalamus-Proper', '37': 'Left-Caudate', '38': 'Left-Putamen', '39': 'Left-Pallidum', '40': 'Left-Hippocampus', '41': 'Left-Amygdala', '42': 'Left-Accumbens-area', '43': 'Right-Thalamus-Proper', '44': 'Right-Caudate', '45': 'Right-Putamen', '46': 'Right-Pallidum', '47': 'Right-Hippocampus', '48': 'Right-Amygdala', '49': 'Right-Accumbens-area','50': 'ctx-rh-bankssts', '51': 'ctx-rh-caudalanteriorcingulate', '52': 'ctx-rh-caudalmiddlefrontal', '53': 'ctx-rh-cuneus', '54': 'ctx-rh-entorhinal', '55': 'ctx-rh-fusiform', '56': 'ctx-rh-inferiorparietal', '57': 'ctx-rh-inferiortemporal', '58': 'ctx-rh-isthmuscingulate', '59': 'ctx-rh-lateraloccipital', '60': 'ctx-rh-lateralorbitofrontal', '61': 'ctx-rh-lingual', '62': 'ctx-rh-medialorbitofrontal', '63': 'ctx-rh-middletemporal', '64': 'ctx-rh-parahippocampal', '65': 'ctx-rh-paracentral', '66': 'ctx-rh-parsopercularis', '67': 'ctx-rh-parsorbitalis', '68': 'ctx-rh-parstriangularis', '69': 'ctx-rh-pericalcarine', '70': 'ctx-rh-postcentral', '71': 'ctx-rh-posteriorcingulate', '72': 'ctx-rh-precentral', '73': 'ctx-rh-precuneus', '74': 'ctx-rh-rostralanteriorcingulate', '75': 'ctx-rh-rostralmiddlefrontal', '76': 'ctx-rh-superiorfrontal', '77': 'ctx-rh-superiorparietal', '78': 'ctx-rh-superiortemporal', '79': 'ctx-rh-supramarginal', '80': 'ctx-rh-frontalpole', '81': 'ctx-rh-temporalpole', '82': 'ctx-rh-transversetemporal', '83': 'ctx-rh-insula', '84': 'Right-Cerebellum-Cortex', '85': 'Axial-section-through-medulla', '86': 'Fornix-body', '87': 'Left-optic-tract', '88': 'Right-optic-tract'}

    label = int(labelnumber)
    one = str(label // 100)
    two = str(label % 100)
    label_name = str(names[one] + ' AND ' +names[two])

    return label_name


def regionconnect(roi_file, out_txt):
    """
    Input: An ROI mask image file
    Return: a list of strings that contains the information about connections
    """
    # Load roi file and atlas files
    roi = nib.load(roi_file)
    roi_shape = roi.shape

    atlas = _get_atlas_files(roi_shape)
    if not atlas:
        print("Downloads failed. Please try again. Exiting...")
        return

    # Get percentages of ROI that are used to calculate the list.
    print('Generating the output ...')
    wm_atlas= nib.load(atlas[1])
    wm_mask_img = wm_atlas.get_data()[:,:,:,0]>0 # This is the white matter mask, the first layer of labels.
    roi_img = roi.get_data()
    percentage_in = _get_overlap(roi_img, wm_mask_img)
    percentage_out = '{:.2%}'.format(1-float(percentage_in.strip('%'))/100)

    if np.count_nonzero(roi_img) > 0:
        tdi_sum_img = nib.load(atlas[0]).get_data()
        wm_atlas_img = wm_atlas.get_data()
        conf_img = nib.load(atlas[2]).get_data()
        dict_list = _get_dict_list(roi_img, tdi_sum_img, wm_atlas_img, conf_img)

    txtHead = str('###' + percentage_in + 'of the selected ROI is used in this analysis\n'+
                  '###' + percentage_out + 'of the ROI is located outside of the white matter\n'+
                  '\n'+
                  '###MOST PROBABLE CONNECTIONS:\n'+
                  '\n')
    txtTail = ''
    for item in dict_list:
        value = '{:.12%}'.format(item[1])
        name = _get_name_of_label(item[0])
        itemStr = str(str(value) + ' - ' + str(name) + '\n')
        txtTail += itemStr

    f = open(out_txt, 'w')
    f.write(str(txtHead) + str(txtTail))
    f.close()


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

    regionconnect(roi_mask_input, output_file_input)

