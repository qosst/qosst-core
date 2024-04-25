from qosst_core.modulation import PSKModulation
import matplotlib.pyplot as plt

modulation = PSKModulation(1, 4)
points = modulation.constellation
plt.scatter(points.real, points.imag)
plt.title("4-PSK")
plt.grid()
plt.gca().set_aspect("equal")
plt.show()
