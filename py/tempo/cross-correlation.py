import numpy as np
from scipy.signal import correlate
from scipy.signal import find_peaks
from fastdtw import fastdtw
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean

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


signal1_normf = signal1_norm.flatten()
signal2_normf = signal2_norm.flatten()

## 1.  Calculate the cross-correlation..
cross_corr = correlate(signal1_norm, signal2_norm, mode='full')
lag = np.argmax(cross_corr) - (len(signal1_norm) -1)
max_corr = cross_corr[np.argmax(cross_corr)]



print(f'Max correlation: {max_corr}, at lag: {lag}')








## 2. Calculate DTW 


# print("Signal 1 Shape:", signal1_normf.shape)
# print("Signal 1 Shape:", signal2_norm.shape)

distance, path = fastdtw(signal1_norm, signal2_norm, dist=lambda x, y: np.abs(x - y))


# Print the DTW distance
print(f'DTW distance: {distance}')


## Create subplots
plt.figure(figsize=(24,8))

# Subplot 1: Signals
plt.subplot(3, 1, 1)
plt.plot(signal1_norm, label='Pitch')
plt.plot(signal2_norm, label='Roll', alpha=0.75)
plt.title("1D Signals Generated Using Perlin Noise")
plt.xlabel("Index")
plt.ylabel("Amplitude")
plt.legend()

# Subplot 2: Cross-Correlation
plt.subplot(3, 1, 2)
plt.plot(cross_corr, label='Cross Correlation')
plt.title("Cross-Correlation between Signals")
plt.xlabel("Lag")
plt.ylabel("Correlation")
plt.legend()


# Subplot 3: DTW 

plt.subplot(3, 1, 3)
plt.plot([point[0] for point in path], [point[1] for point in path], label='DTW Path')
plt.title(f"DTW Path between Signals (Distance: {distance:.2f})")
plt.xlabel("Signal 1 Index")
plt.ylabel("Signal 2 Index")
plt.legend()

# # Display the plots
plt.tight_layout()  # Adjust subplots to fit into figure area.
plt.show()

