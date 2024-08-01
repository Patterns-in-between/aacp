import numpy as np
from scipy.signal import correlate
from scipy.signal import find_peaks
import fastdtw
import matplotlib.pyplot as plt

from perlin_numpy import (
    generate_perlin_noise_2d
)


# Generate a 2D Perlin noise array
noise_size = (256, 256)  # Size of the 2D noise array
perlin_noise = generate_perlin_noise_2d(noise_size, (8, 8))  # Specify the frequency

# Take a slice from the 2D noise
N = 2000 # signal length
signal1 = perlin_noise[0, :N]  # Take the first row
signal2 = perlin_noise[10, :N] # Take the second row 

# Normalize the signal to a specific range, e.g., 1 to 360
min_val, max_val = 1, 360
signal1_norm = min_val + (signal1 - signal1.min()) * (max_val - min_val) / (signal1.max() - signal1.min())
signal2_norm = min_val + (signal2 - signal2.min()) * (max_val - min_val) / (signal2.max() - signal2.min())



## 1.  Calculate the cross-correlation..
cross_corr = correlate(signal1_norm, signal2_norm, mode='full')
lag = np.argmax(cross_corr) - (len(signal1_norm) -1)
max_corr = cross_corr[np.argmax(cross_corr)]



print(f'Max correlation: {max_corr}, at lag: {lag}')

# Create subplots
plt.figure(figsize=(12, 8))

# Subplot 1: Signals
plt.subplot(2, 1, 1)
plt.plot(signal1_norm, label='Pitch')
plt.plot(signal2_norm, label='Roll', alpha=0.75)
plt.title("1D Signals Generated Using Perlin Noise")
plt.xlabel("Index")
plt.ylabel("Amplitude")
plt.legend()

# Subplot 2: Cross-Correlation
plt.subplot(2, 1, 2)
plt.plot(cross_corr, label='Cross Correlation')
plt.title("Cross-Correlation between Signals")
plt.xlabel("Lag")
plt.ylabel("Correlation")
plt.legend()

# Display the plots
plt.tight_layout()  # Adjust subplots to fit into figure area.
plt.show()




## 2. Calculate DTW 


