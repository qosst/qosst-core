import matplotlib.pyplot as plt

from qosst_core.modulation import PCSQAMModulation

modulation = PCSQAMModulation(35, 256, nu=0.01)
points = modulation.constellation
colors = modulation.distribution
plt.scatter(points.real, points.imag, c=colors, cmap="rainbow")
plt.title("256-PCS-QAM")
plt.colorbar()
plt.grid()
plt.show()
