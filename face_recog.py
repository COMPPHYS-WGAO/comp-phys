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

phys_dict = {0: 'Bohr', 1: 'Einstein'}
bohr = 10
flat_bohr = []
ein = 11
flat_ein = []
y = []

# first load the images and flatten them and store the flattened image objects into a list with length=21, 
# then concatenate them into a 21x2700 array
for i in range(bohr):
    im = mpimg.imread('bohr'+str(i)+'.jpeg')
    flat_bohr.append(interpol_im(im, dim1 = 45, dim2 = 60))
    y.append(0)
for i in range(ein):
    im = mpimg.imread('ein'+str(i)+'.jpeg')
    flat_ein.append(interpol_im(im, dim1 = 45, dim2 = 60))
    y.append(1)

# concatenate into a 21x2700 array
X = np.vstack((np.array(flat_bohr), np.array(flat_ein)))

###################################### Training ########################################
 
### instantiating PCA and CLF
md_pca, X_proj = pca_X(X)
md_clf = svm_train(X_proj, y)

### all the training data's predictions are correct
# for i in range(21):
#     p = md_clf.predict(X_proj[i].reshape(1, -1))
#     print(p, y[i])

###################################### Validation ########################################

print('Below is the Validation part')

perc = 0
tot = 21

for select_idx in range(21):
    
    Xtrain = np.delete(X, select_idx, axis = 0)
    ytrain = np.delete(y, select_idx)
    
    md_pca.fit(Xtrain)   # fit PCA axis onto the leaved-one-out data
    
    Xtrain_proj = md_pca.transform(Xtrain)
    
    Xtest = X[select_idx].reshape(1, -1)
    ytest = y[select_idx]
    Xtest_proj = md_pca.transform(Xtest)

### if uses line55, the success rate will become about 81%
### because for every loop, it re-trains the svm with a 'less complete' data reference
#     md_clf = svm_train(Xtrain_proj, ytrain)

    p = md_clf.predict(Xtest_proj)[0]
    
    if ytest == p:
        perc += 1.
        print('Pred: {} Ans: {}'.format(p, ytest))
    else:
        print('Pred: {} Ans: {} <--- incorrect; image index: {}'.format(p, ytest, select_idx))
    

print('The percentage of correct predictions (for validation) is: {:1f}%'.format(perc*100./tot))

######################################## Testing #####################################

md_pca.fit(X)   # Re-fit the PCA axis onto X, the original data set

pre1 = phys_dict[pca_svm_pred('unseen_phys1.jpg', md_pca, md_clf, dim1 = 45, dim2 = 60)[0]]
print('PCA+SVM prediction for physicist 1: {}'.format(pre1))

pre2 = phys_dict[pca_svm_pred('unseen_phys2.jpg', md_pca, md_clf, dim1 = 45, dim2 = 60)[0]]
print('PCA+SVM prediction for physicist 2: {}'.format(pre2))

