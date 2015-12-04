
from scipy import signal
from scipy import misc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from sklearn.decomposition import PCA
from skimage import transform, data, io
from scipy.interpolate import interp2d

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def make_let_im(let_file, dim = 16, y_lo = 70, y_hi = 220, x_lo = 10, x_hi = 200, edge_pix = 150, plot_let = False):

    letter = mpimg.imread(let_file)

    letter = letter[y_lo:y_hi, x_lo:x_hi, 0]
    for i in range(letter.shape[1]):
        if letter[0:edge_pix, i].any() == 0:   # here is to remove the edge
            letter[0:edge_pix, i] = 1
    
    plt.imshow(letter, cmap='gray')
    plt.grid('off')
    plt.show()
        
    x = np.arange(letter.shape[1])
    y = np.arange(letter.shape[0])

    f2d = interp2d(x, y, letter)

    x_new = np.linspace(0, letter.shape[1], dim)    # dim = 16
    y_new = np.linspace(0, letter.shape[0], dim)

    letter_new = f2d(x_new, y_new)
    letter_new -= np.mean(letter_new)
    
    if plot_let: 
        plt.imshow(letter_new, cmap = 'gray')
        plt.grid('off')
        plt.show()
        
    letter_flat = letter_new.flatten()   # letter_flat is a 1-dimensional array containing 256 elements
    
    return letter_new, letter_flat
   

def alphabet_pca(X, n_comp = 10):
    pca = PCA(n_comp)  
    Xproj = pca.fit_transform(X)
    pca_comps = pca.components_
    
    return pca, Xproj, pca_comps


def show_pca_im(Xproj, pca_comps, dim = 16, let_idx = 0):
    
    n_comp = pca_comps.shape[0]
    print(pca_comps.shape)

    f, axes = plt.subplots(1, n_comp, figsize = (10, 2), subplot_kw=dict(xticks=[], yticks=[]))
    for i in range(n_comp):
        axes[i].imshow(pca_comps[i].reshape((dim, dim)), cmap='binary')

    dig_im = np.zeros((dim, dim))
    coeffs = Xproj[let_idx]
    
    print('coeffs.shape', coeffs.shape)
    for i in range(n_comp):
        dig_im += coeffs[i]*pca_comps[i].reshape((dim, dim))

    fig, ax = plt.subplots(1, 1, figsize = (2, 2))
    ax.imshow(dig_im, cmap='binary')
    # To turn off grid (under seaborn, the default for grid is on.)
    ax.grid(False)
    ax.axis('off')
    plt.show()
    
    

if __name__ == "__main__":

    import doctest
    import argparse
    from math import log, log1p



    parser = argparse.ArgumentParser()
    parser.add_argument('-let_idx', type = int)
    parser.add_argument('-n_comp', type = int)

    args = parser.parse_args()
    n_comp = args.n_comp
    let_idx = args.let_idx
    
    X = np.zeros((26, 256))
    for i in range(len(letters)):

        filename = 'letter'+letters[i]+'.png'    # call the files
        let_im, let_im_flat = make_let_im(filename)
        X[i, :] = let_im_flat
    
    pca, Xproj, pca_comps = alphabet_pca(X, n_comp = n_comp)
    show_pca_im(Xproj, pca_comps, let_idx = let_idx)
