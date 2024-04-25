import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from qosst_core.comm.filters import raised_cosine_filter

SAMPLING_RATE = 1e9
SYMBOL_RATE = 100e6
ROLL_OFFS = np.arange(0, 1.01, 0.2)

SPS = int(SAMPLING_RATE / SYMBOL_RATE)
SYMBOL_PERIOD = 1 / SYMBOL_RATE

COLORS = [color for color in mcolors.TABLEAU_COLORS]

for i, beta_rc in enumerate(ROLL_OFFS):
    times, h_rc = raised_cosine_filter(
        int(100 * SPS), beta_rc, SYMBOL_PERIOD, SAMPLING_RATE
    )
    N = len(h_rc)
    fftfreq = np.fft.fftfreq(N, 1 / SAMPLING_RATE)
    fft = np.fft.fft(h_rc)
    plt.plot(
        fftfreq[: N // 2] / SYMBOL_RATE,
        np.abs(fft)[: N // 2],
        label=f"$\\beta_{{RC}} = {beta_rc:.1f}$",
        color=COLORS[i],
    )
    plt.plot(fftfreq[N // 2 :] / SYMBOL_RATE, np.abs(fft)[N // 2 :], color=COLORS[i])

plt.grid()
plt.legend()
plt.xlabel("$f/R_s$")
plt.xlim(left=-1.5, right=1.5)
plt.show()
