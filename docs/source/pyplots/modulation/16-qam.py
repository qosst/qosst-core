from qosst_core.modulation import QAMModulation
import matplotlib.pyplot as plt

modulation = QAMModulation(1, 16)
points = modulation.constellation
plt.scatter(points.real, points.imag)
plt.title("16-QAM")
plt.grid()
plt.gca().set_aspect("equal")
plt.show()
