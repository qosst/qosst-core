import matplotlib.pyplot as plt
import numpy as np
from qosst_core.comm.filters import raised_cosine_filter

SAMPLING_RATE = 1e9
SYMBOL_RATE = 100e6
ROLL_OFFS = np.arange(0, 1.01, 0.2)

SPS = int(SAMPLING_RATE / SYMBOL_RATE)
SYMBOL_PERIOD = 1 / SYMBOL_RATE

for beta_rc in ROLL_OFFS:
    times, h_rc = raised_cosine_filter(
        int(10 * SPS), beta_rc, SYMBOL_PERIOD, SAMPLING_RATE
    )
    times_period = times * SYMBOL_RATE

    plt.plot(times_period, h_rc, label=f"$\\beta_{{RC}} = {beta_rc:.1f}$")

plt.grid()
plt.legend()
plt.xlabel("$t / T_s$")
plt.xlim(left=-3, right=3)
plt.show()
