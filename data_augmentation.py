# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 18:30:56 2019

@author: Gabriel Hsu
"""

import numpy as np
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter


def elastic_transform(image, mask, ins, weight, alpha, sigma, random_state=None):
    """Elastic deformation of images as described in [Simard2003]_.
    .. [Simard2003] Simard, Steinkraus and Platt, "Best Practices for
       Convolutional Neural Networks applied to Visual Document Analysis", in
       Proc. of the International Conference on Document Analysis and
       Recognition, 2003.
       
       Modified from: https://gist.github.com/erniejunior/601cdf56d2b424757de5
    """
    if random_state is None:
        random_state = np.random.RandomState(None)

    shape = image.shape
    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dz = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha

    x, y, z = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), np.arange(shape[2]))
    indices = np.reshape(y+dy, (-1, 1)), np.reshape(x+dx, (-1, 1)), np.reshape(z+dz, (-1, 1))

    distored_image = map_coordinates(image, indices, order=1, mode='reflect')
    distored_mask = map_coordinates(mask, indices, order=1, mode='reflect')
    distorted_ins = map_coordinates(ins, indices, order=1, mode='reflect')
    distorted_weight = map_coordinates(weight, indices, order=1, mode='reflect')
	
    return distored_image.reshape(image.shape), distored_mask.reshape(mask.shape), distorted_ins.reshape(ins.shape),distorted_weight.reshape(weight.shape)

def gaussian_blur(image):
    return gaussian_filter(image, sigma=1)

def gaussian_noise(image):
     mean = 0
     var = 0.1
     sigma = var**0.5
     gauss = 50*np.random.normal(mean,sigma,image.shape)
     gauss = gauss.reshape(image.shape)
     return image + gauss
 
def crop_z(image, ins, gt, weight, z):
    crop_img = np.copy(image)
    crop_ins = np.copy(ins)
    crop_gt = np.copy(gt)
    crop_weight = np.copy(weight)
    if np.random.rand() <= 0.5:
        crop_img[:z,:,:] = image.min()
        crop_ins[:z,:,:] = ins.min()
        crop_gt[:z,:,:] = gt.min()
        crop_weight[:z,:,:] = weight.min()
    else:
        crop_img[z:,:,:] = image.min()
        crop_ins[z:,:,:] = ins.min()
        crop_gt[z:,:,:] = gt.min()
        crop_weight[z:,:,:] = weight.min()
    return crop_img, crop_ins, crop_gt, crop_weight



