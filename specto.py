from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import argparse

input_file = "/tmp/data_web_demo/sv_sicakauf/2016-06-04_171233_539051_16kHz.wav"
rate, signal = wavfile.read(input_file)

print(type(rate))

def spectrogram(signal, rate):
	if type(signal) is not np.array:
		assert(False), "signal has to be a numpy array."
		
	if type(rate) is not int:
		assert(False), "rate has to be an int."

	# make sure we have a mono signal
	assert(signal.ndim == 1)

	windur = round(0.025 * rate)
	winshift = round(0.01 * rate)
	n_frames = int((len(signal) - windur) / winshift) + 1

	# subtract DC offset
	signal = signal - signal.mean()
	
	# extract windows
	windows = [signal[i * winshift : i * winshift + windur]
           for i in range(n_frames)]

	# apply hanning window
	windows = np.vstack(windows)
	hann = 0.5*(1-np.cos(2*np.pi*np.arange(windur)/windur))
	windows = windows * hann

	if False:
		# as an Exercise: Fourier Transform as matrix multiplication
		F = [np.exp(-2 * np.pi * 1j * k * \
            np.arange(windur)/windur) \
            for k in range(windur)]
		trans = np.dot(F, windows.transpose()).transpose()
		# non-redundant part of symmetric spectrum
		n_bins = np.floor(windur / 2) + 1
	else:
		# Fast Fourier Transform:
		# - pad with zeros until next power of 2
		n_pad = int(2**np.ceil(np.log2(windur)))
		trans = np.fft.fft(windows, n=n_pad, axis=1)
		# non-redundant part of symmetric spectrum
		n_bins = int(np.floor(n_pad/2)+1)

	# select non-redundant part
	spec = trans[:, 0 : n_bins]
	powspec = np.abs(spec)**2

	plt.imshow(np.log(powspec).transpose(), origin='lower', interpolation='nearest')
	plt.show()
	
if __name__ == "__main__":
		
	parser = argparse.ArgumentParser( description = " print sum of two numbers .")
	parser.add_argument (" num1 ", help ="1st number ")
	parser.add_argument (" num2 ", help ="2nd number ")
	
	args = parser.parse_args()
	spectrogram( args.num1 , args.num2 )

