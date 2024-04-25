import matplotlib.pyplot as plt
import numpy as np

from qosst_core.modulation import GaussianModulation

modulation = GaussianModulation(1)
points = modulation.modulate(100000)
heatmap, xedges, yedges = np.histogram2d(points.real, points.imag, bins=30)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.imshow(heatmap.T, extent=extent, origin="lower", cmap="rainbow")
plt.title("Gaussian")
plt.colorbar()
plt.grid()
plt.show()
