# erste Übung Dreiklang

import numpy as np
import matplotlib.pyplot as plt

from scipy.io import wavfile


# Parameter
## Abtastwerte pro Sekunde
rate = 16000

## Frequenz für Sinusschwingung/Höhe des Sinustons
f = 440

## Länge des Signals in [sec]
duration = 5

print(float(f))
print(type(float(f)))

# Synthetisieren des Signals
## Abtastwerte [ms, da Divison durch 'rate']
sample_points = np.arange(duration * rate) / rate

print(sample_points)
len(sample_points)

## Werte des Sinussignals erzeugen
#signal = np.sin(2 * np.pi * f * sample_points)

grundton = np.sin(2 * np.pi * f * sample_points)
terz = np.sin(2 * np.pi * 5/4 * f * sample_points)
quinte = np.sin(2 * np.pi * 2/3 * f * sample_points)

signal = (grundton + terz + quinte) / 3 # mit oder ohne /3 ?

print(signal)
print('signal: %s %s %s'%(signal[0], signal[5], signal[-1]))
print('Wertebreich des signals: [%s, %s]'%(min(signal), max(signal)))
signal.shape

# Plotten des erzeugten Sinussignals
##%matplotlib inline

#plt.plot(sample_points[0:400], signal[0:400])

plt.plot(sample_points[0:400], grundton[0:400], label='grundton')
plt.plot(sample_points[0:400], terz[0:400], label='terz')
plt.plot(sample_points[0:400], quinte[0:400], label='quinte')
plt.plot(sample_points[0:400], signal[0:400], label='signal')
plt.legend()
plt.show()

# 16 bit Quantisierung zum Schreiben des .wav-Files
## Ein Signalwert wird als 16-bit Zahl gespeichert --> maximaler und minimaler Wert des Signals ist begrenzt
num_bits = 16

print('Anzahl darstellbarer Werte: \t2**16 = %s'%(2**num_bits))
print('Mögliche Werte:             \t[0, %s]\n'%(2**num_bits-1))

print('Aufteilung des Wertebereichs zur Darstellung von negativen und positiven Signalwerten:')
print('0.5 * 2**16 = %s\n'%(2**num_bits/2))
print('Zahl "0" nicht vergessen:')
print('Wertebereich (16-bit int):  \t[%d, ..., %d, ..., %d]\n'%(-1*2**num_bits/2, 0, (2**num_bits/2)-1))

max_signal_value = (2**num_bits/2)-1

print('Der Einfachheit halber - Verwende Wertebereich [%d, %d]'%(-1*max_signal_value, max_signal_value))

signal_quantized = (max_signal_value * signal).astype(np.int16)

print(signal_quantized)
print('Wertebreich des signals: [%s, %s]'%(min(signal_quantized), max(signal_quantized)))

type(signal_quantized)
signal_quantized.shape

plt.plot(sample_points[0:400], signal_quantized[0:400], label='signal_quant')
plt.legend()
plt.show()

path_on_your_pc = "./dreiklang.wav"
wavfile.write(path_on_your_pc, rate, signal_quantized)
