from qosst_core.modulation import SinglePointModulation
import matplotlib.pyplot as plt

modulation = SinglePointModulation(x=1, y=1)
points = modulation.modulate(1)
plt.scatter(points.real, points.imag)
plt.title("Single Point modulation")
plt.grid()
plt.gca().set_aspect("equal")
plt.show()
