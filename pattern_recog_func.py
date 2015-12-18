from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns; sns.set()
from sklearn import decomposition
from sklearn.decomposition import PCA
from sklearn.datasets import load_digits
from sklearn import svm
import matplotlib.image as mpimg
from scipy.interpolate import interp2d
from sklearn import preprocessing

import warnings
warnings.filterwarnings("ignore")

###########################################################################

def interpol_im(im, dim1 = 8, dim2 = 8, plot_new_im = False, cmap = 'binary', axis_off = False):
    im = im[:, :, 0]
    
    x = np.arange(im.shape[1])
    y = np.arange(im.shape[0])

    f2d = interp2d(x, y, im)

    x_new = np.linspace(0, im.shape[1], dim1)    
    y_new = np.linspace(0, im.shape[0], dim2)

    im_new = -f2d(x_new, y_new)

    if plot_new_im: 
        plt.imshow(im_new, cmap = 'binary')
        plt.grid('off')
        plt.show()

    im_flat = im_new.flatten()   
    
    return im_flat

###########################################################################

def pca_X(X, n_comp = 10):
    
    md_pca = PCA(n_components = n_comp, whiten=True)
    Xproj = md_pca.fit_transform(X)
    
    return (md_pca, Xproj)

###########################################################################

def rescale_pixel(X, unseen, ind = 0, plot_ref = False, plot_unseen = False):
    
    X_train = X[ind]
    
    if plot_ref: 
        print('Below is the X[{}] image:'.format(ind))
        plt.imshow(X_train.reshape((8,8)))
        plt.grid('off')
        plt.show()
    
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(min(X_train), max(X_train)))
    unseen_scaled = min_max_scaler.fit_transform(X_train, unseen).astype(int)
    
    if plot_unseen:
        print('Below is the unseen image:')
        plt.imshow(unseen.reshape((8,8)))
        plt.grid('off')
        plt.show()
    
    return unseen_scaled

###########################################################################

def svm_train(X, y, gamma = 0.001, C = 100):

    md_clf = svm.SVC(gamma=0.001, C=100.)

    md_clf.fit(X, y)

    return md_clf

###########################################################################

def pca_svm_pred(imfile, md_pca, md_clf, dim1 = 45, dim2 = 60):
    im = mpimg.imread(imfile)
    flat_im = interpol_im(im, dim1, dim2, plot_new_im = True)
    im_proj = md_pca.transform(flat_im)
    pre = md_clf.predict(im_proj.reshape(1, -1))
    return pre

