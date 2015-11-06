import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
import os

class Tone:
    
    def __init__(self, frequency = 0, duration = 0, sample_rate = 44100, tones = 0, simple_tone = 0, over_dict = {}, num_overtones = 0):
        self.f = frequency
        self.dur = duration
        self.sr = sample_rate
        self.signal = tones
        self.orig_signal = simple_tone
        self.overtones = over_dict
        self.OT_num = num_overtones
        
    def get_tone(self, f, duration, amp = 2**10, play_sound = False):
        self.f = f
        self.dur = duration
        time_pts = np.linspace(0, self.dur, self.dur*self.sr)
    #     tone = np.int16(amp*np.sin(np.pi*2*f*time_pts))
        self.orig_signal = amp*np.sin(np.pi*2*self.f*time_pts)
        if play_sound == True:
            self.playsound(self.orig_signal)

        return self.orig_signal
    
    def get_overtone(self, multi, amp = 2**10, play_sound = False):
        f = self.f
        duration = self.dur
        time_pts = np.linspace(0, duration, duration*self.sr)
    #     tone = np.int16(amp*np.sin(np.pi*2*f*time_pts))
        overtone = amp*np.sin(np.pi*2*multi*f*time_pts)
        if play_sound:
            self.playsound(overtone)
        
        self.overtones[multi] = overtone
        
        self.OT_num += 1
        return
    
    
    def comb_tones(self):
        weights = self.overtones.copy()
        wts = 0
        for i in self.overtones:
            wt = int(raw_input('Please enter a weight# for overtone w/multi={:d}: '.format(i)))
            self.overtones[i] = (self.overtones[i], wt)
        for i in self.overtones:
            wts += self.overtones[i][1]**2
        for i in self.overtones:
            self.signal += np.int16(self.overtones[i][0]*self.overtones[i][1]/wts**.5)
        return self.signal
    
                     
    def playsound(self, outside_signal = None, sample_rate = 44100, vol = 0.5):
        from scipy.io.wavfile import write
        import os
        if outside_signal == None:
            write('tmp.wav', sample_rate, np.int16(vol*self.signal))
            os.system("afplay tmp.wav") 
            os.system("rm tmp.wav") 
        else:
            write('tmp.wav', sample_rate, np.int16(vol*outside_signal))
            os.system("afplay tmp.wav") 
            os.system("rm tmp.wav")
        return
    
                     
    def plot_sound(self, fig = None, t_lim = 0.02, s_lim = 'auto', plot_style = 'b-'):
        sound = self.signal
        time_pts = np.linspace(0, self.dur, self.dur*44100)
        if fig == None:
            plt.figure()
        plt.title("Sound Wave vs. Time")
        plt.plot(time_pts, sound, plot_style)
        plt.xlim([0, t_lim])
        if s_lim  != 'auto':
            plt.ylim([-s_lim, s_lim])
        plt.show()
        return 
                     
    def plot_fourier(self, sample_rate = 44100, freq_lim = 2000., amp_lim = 1e7):
        '''
        Given sample_rate and signal, plots the real and imaginary parts of DFT.
        '''
        signal = self.signal
        # note: This conversion to float64 is crucial -- or else the numerical error will be greater.
        #ft = np.fft.fft(np.float64(signal))
        ft = np.fft.fft(np.float64(signal))

        freq = np.fft.fftfreq(signal.shape[-1], d = 1./sample_rate)
        plt.figure()
        plt.title('Real')
        plt.plot(freq, ft.real, 'b-')
        plt.xlim([-freq_lim, freq_lim])
        plt.ylim([-amp_lim, amp_lim])             
        plt.figure()
        plt.title('Imaginary')
        plt.plot(freq, ft.imag, 'g-')
        plt.xlim([-freq_lim, freq_lim])
        plt.ylim([-amp_lim, amp_lim])
        plt.show()

        
##########################################################################

tone = Tone()
A = tone.get_tone(440., 0.5)
B = tone.get_tone(493.88, 0.5)
D = tone.get_tone(587.33, 0.5)
G = tone.get_tone(392., 0.5)

print type(A)
melody = np.concatenate((B, A, G, A, B, B, B, B, A, A, A, A), axis=0)

tone.playsound(outside_signal = melody)

##########################################################################

f1 = Tone()

simple_tone = f1.get_tone(440., 0.5)
f1.get_overtone(2)
f1.get_overtone(3)
f1.get_overtone(4)
rich_tone = f1.comb_tones()

f1.playsound()
f1.plot_sound()
f1.plot_fourier(freq_lim = 2000.)


    

