import matplotlib.pyplot as plt

from qosst_core.modulation import BinomialQAMModulation

modulation = BinomialQAMModulation(1, 4)
points = modulation.constellation
colors = modulation.distribution
plt.scatter(points.real, points.imag, c=colors, cmap="rainbow")
plt.title("4-Binomial-QAM")
plt.colorbar()
plt.grid()
plt.show()
