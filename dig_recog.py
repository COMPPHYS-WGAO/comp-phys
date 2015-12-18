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

from pattern_recog_func import interpol_im, pca_X, rescale_pixel, svm_train, pca_svm_pred

################################################

dig_data = load_digits()
X = dig_data.data
y = dig_data.target
index = 15
dig_img = dig_data.images
unseen = mpimg.imread('unseen_dig.png')
flatten_unseen = interpol_im(unseen, plot_new_im = False)
rescaled_unseen = rescale_pixel(X, flatten_unseen, index, plot_ref = True, plot_unseen = True)

print('Mean pixel value of the rescaled image and the X[{}] image are: {}, {}, repectively'.format(index, np.mean(rescaled_unseen), np.mean(X[15])))
print('The rescaled unseen has all the pixel values as integers, flatten array shown as following:')
print(rescaled_unseen)

###################### Trianing ##########################

dig_data = load_digits()
X = dig_data.data
y = dig_data.target

md_clf = svm_train(X[0:60], y[0:60], gamma = 0.001, C = 100)

####################### Validation #########################

perc = 0
start = 60
end = 80
mis = 0
for i in range(start, end):
    pre = md_clf.predict(X[i].reshape(1, -1))[0]
    ans = y[i]
#     print(pre)
    if ans == pre:
        perc += 1
    else:
        plt.imshow(X[i].reshape((8,8)), cmap = 'binary')
        plt.grid('off')
        plt.show()
        print('Above is the mis-identified image')
        print('-----> index, actual digit, svm_prediction: {:} {:} {:}'.format(i,ans, pre))
        mis += 1
print('Total number of mis-identifications: {:d}'.format(mis))
print('Success rate: {:}'.format(perc/(end-start)))

###################### Testing ##########################

faltten_unseen_pre = md_clf.predict(flatten_unseen.reshape(1, -1))[0]
rescaled_unseen_pre = md_clf.predict(rescaled_unseen.reshape(1, -1))[0]

print('The prediction for the rescaled unseen: {}; answer: 5'.format(rescaled_unseen_pre))
print('The prediction for the un-rescaled unseen: {}; answer: 5'.format(faltten_unseen_pre))

