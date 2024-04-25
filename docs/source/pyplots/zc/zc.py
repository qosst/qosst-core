import matplotlib.pyplot as plt
import numpy as np
from qosst_core.comm.zc import zcsequence

SAMPLING_RATE = 1e9
ROOT = 1
LENGTH = 227

sequence = zcsequence(ROOT, LENGTH, cyclic_shift=0)
times = np.arange(len(sequence)) / SAMPLING_RATE

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(times, sequence.real, color="black")
ax2.plot(times, sequence.imag, color="black")
ax2.set_xlabel("Time [s]")
ax1.set_ylabel("Real part")
ax2.set_ylabel("Imag part")
ax1.grid()
ax2.grid()
plt.show()
