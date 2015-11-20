
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from skimage import feature
import os

def extract_shape_v0(im_file, blowup = 1., plot_img = False, plot_contour = False, plot_contour_pts = False):

    
    im = mpimg.imread(im_file)
    # Take one of RGB(A) channels
    if len(im.shape) > 2:
        im = im[:, :, 0]
    
    if plot_img:
        plt.figure()
        plt.title('Original Shape')
        plt.imshow(im, cmap = plt.cm.gray)

    # Note: by convention, in this case, y values comes from the 0th index.
    # Otherwise one has to transpose the image and the contour will appear sideways 
    x = np.arange(im.shape[1])*blowup  
    y = np.arange(im.shape[0])*blowup
    
    # Have to flip y to get the orientation right, again just a peculiar convention we have to work around
    # Note the [::] notation: a[3:20:2] means from the 3rd element to the 20th element, choose every 2nd element.
    y = y[::-1]
    #x = x[::1]
    

    # In case I want to shift x.
    #x_shift = 200
    #x += x_shift

    X, Y = np.meshgrid(x, y)
    
    plt.figure()
    plt.title('Contours')
    # Note the dimensions of x and y may NOT the same, thus the necessity of the 
    # tranpose operation (an oddity, I admit...)
    CS = plt.contour(X, Y, im, 1)
    levels = CS.levels
    print 'contour level', levels
    if not plot_contour:
        plt.close()

    cs_paths = CS.collections[0].get_paths()

    print 'number of contour path', len(cs_paths)

#     p = cs_paths[0]
#     v = p.vertices
#     x_arr = v[:,0]
#     y_arr = v[:,1]
    x_arr = []
    y_arr = []
    for i in range(len(cs_paths)):
        p = cs_paths[i]
        v = p.vertices
        x_arr.append(v[:,0])
        y_arr.append(v[:,1])

    if plot_contour_pts:
        plt.figure()
        plt.title("Verify the contour points are correct")
        for i in range(len(x_arr)):
            plt.scatter(x_arr[i], y_arr[i])

    return x_arr, y_arr   # now x_arr and y_arr are lists of arrays


def FD(x, y, plot_FD = False, y_lim = None):

    N = len(x)
    n = np.arange(N)


    z = x + y*1j

    Z = np.fft.fft(z)

    if plot_FD:
        plt.figure()
        plt.title('FD real and imag')
        plt.plot(Z.real, 'b-')
        plt.plot(Z.imag, 'g-')
        if y_lim != None:
            plt.ylim([-y_lim, y_lim])

    return Z


def filt_FD(Z, n_keep, no_zeroth = True):
    N = len(Z)
    n = np.arange(len(Z))
    print 'Nyquist index', N/2
    # in case I want the centroid position.
    filt0 = n > 0 if no_zeroth else 1
    filt1 = filt0*(n <= n_keep)
    
    filt2 = (n > ((N-1) - n_keep))
    print 'Number of components from both sides:', filt1.sum(), filt2.sum()
    filt = filt1 + filt2
    #print Z.real[N/2]
    return Z*filt


# I'm giving away the following 2 functions for free!
def recover_shape(Z):
    z_rec = np.fft.ifft(Z)

    x_rec = z_rec.real
    y_rec = z_rec.imag
    
    return x_rec, y_rec


def get_FD_abs(x, y, order = 10, norm = True, no_zeroth = True):
    
#     x, y = extract_shape_v0('letterE.jpg')

#     order = 10
    fd_mag = []
    x_rec = []
    y_rec = []
    for i in range(len(x)): # run thru each element in the list

        Z = FD(x[i], y[i])
        # automatically determine no_zeroth 
        # by putting the argument into the filt_FD function
        Z_filt = filt_FD(Z, order, no_zeroth)    
        if norm:
            Z_filt = size_norm(Z_filt)
        
#         Z_filt = Z_filt > 0 if no_zeroth else 1
        
        x_reco, y_reco = recover_shape(Z_filt)
        x_rec.append(x_reco)
        y_rec.append(y_reco)
       
        non_zeros = []
        for i in Z_filt:
            if i != 0:
                non_zeros.append(i)
#         np.array(non_zeros)

        fd_maga = np.abs(np.array(non_zeros))
        fd_mag.append(fd_maga)
#     plt.figure()
#     plt.plot(x_rec, y_rec)
    return fd_mag, x_rec, y_rec

def size_norm(Z):
    return Z/np.sqrt( np.abs(Z[1])*np.abs(Z[-1]) )





if __name__ == "__main__":

    import doctest
    import argparse
    from math import log, log1p



    parser = argparse.ArgumentParser()
    parser.add_argument('-order', type = float)
    parser.add_argument('--no-norm', dest='norm', \
    action='store_false')
    parser.add_argument('-zeroth', dest = 'no_zeroth', \
    action='store_false')
    parser.set_defaults(no_zeroth=True, norm=True)
    args = parser.parse_args()
    order = args.order
    no_zeroth = args.no_zeroth
    norm = args.norm

    x1, y1 = extract_shape_v0('number1.png')
    x2, y2 = extract_shape_v0('number2.png')
    x6, y6 = extract_shape_v0('number6.png')
    
    
    fd_mag1, x_rec1, y_rec1 = get_FD_abs(x1, y1, order, norm, no_zeroth)
    fd_mag2, x_rec2, y_rec2 = get_FD_abs(x2, y2, order, norm, no_zeroth)
    fd_mag6, x_rec6, y_rec6 = get_FD_abs(x6, y6, order, norm, no_zeroth)

    plt.figure()
    #plt.xlim(-.02, .02)
    #plt.ylim(-.02, .02)
    plt.title("Numbers Recovered From FD's")
    for i in range(len(x_rec1)): 
        plt.plot(x_rec1[i], y_rec1[i])
    for j in range(len(x_rec2)): 
        plt.plot(x_rec2[j], y_rec2[j])
    for k in range(len(x_rec6)): 
        plt.plot(x_rec6[k], y_rec6[k])
    plt.savefig('rec_numbers126.pdf')
    plt.show()

    plt.figure()
    
    plt.title("Magnitudes of FD's for 1, 2 and 6")
    for i in range(len(fd_mag1)):
        plt.plot(fd_mag1[i], 'bo')
    for i in range(len(fd_mag2)):
        plt.plot(fd_mag2[i], 'gx')
    for i in range(len(fd_mag6)):
        plt.plot(fd_mag6[i], 'r^')
    plt.savefig(' FourierDescriptor_numbers126.pdf')
    plt.show()
