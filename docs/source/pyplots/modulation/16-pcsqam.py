import matplotlib.pyplot as plt

from qosst_core.modulation import PCSQAMModulation

modulation = PCSQAMModulation(3, 16, nu=0.1)
points = modulation.constellation
colors = modulation.distribution
plt.scatter(points.real, points.imag, c=colors, cmap="rainbow")
plt.title("16-PCS-QAM")
plt.colorbar()
plt.grid()
plt.show()
