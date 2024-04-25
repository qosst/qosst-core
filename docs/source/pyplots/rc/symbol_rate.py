import matplotlib.pyplot as plt

from qosst_core.comm.filters import raised_cosine_filter

SAMPLING_RATE = 1e9
SYMBOL_RATE = 100e6
ROLL_OFF = 0.5

N = 3

SPS = int(SAMPLING_RATE / SYMBOL_RATE)
SYMBOL_PERIOD = 1 / SYMBOL_RATE

times, h_rc = raised_cosine_filter(
    int(10 * SPS), ROLL_OFF, SYMBOL_PERIOD, SAMPLING_RATE
)
times_period = times * SYMBOL_RATE

plt.plot(times_period, h_rc, label="Symbol 0")
plt.axvline(0, ls="--", color="black")

for i in range(1, N):
    plt.plot(times_period + i, h_rc, label=f"Symbol {i}")
    plt.plot(times_period - i, h_rc, label=f"Symbol {-i}")
    plt.axvline(i, ls="--", color="black")
    plt.axvline(-i, ls="--", color="black")

plt.grid()
plt.legend()
plt.xlabel("$t / T_s$")
plt.xlim(left=-(N + 2), right=N + 2)
plt.show()
