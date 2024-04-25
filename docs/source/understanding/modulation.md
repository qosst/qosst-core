# Modulation

The `qosst_core.modulation` module offers several format of modulation for CV-QKD:

* [Gaussian](#gaussian) ({py:class}`GaussianModulation <qosst_core.modulation.gaussian.GaussianModulation>`);
* [Phase Shift Keying](#phase-shift-keying-psk) ({py:class}`PSKModulation <qosst_core.modulation.psk.PSKModulation>`);
* [Quadrature Amplitude Modulation](#quadrature-amplitude-modulation-qam) ({py:class}`QAMModulation <qosst_core.modulation.qam.QAMModulation>`);
* [Probabilistic Constellation Shaping Quadrature Amplitude Modulation](#probabilistic-constellation-shaping-qam-pcs-qam) ({py:class}`PCSQAMModulation <qosst_core.modulation.pcsqam.PCSQAMModulation>`);
* [Binomial Quadrature Amplitude Modulation](#binomial-quadrature-amplitude-modulation-binomial-qam) ({py:class}`BinomialQAM <qosst_core.modulation.binomialqam.BinomialQAM>`);
* [Single point modulation](#single-point) ({py:class}`SinglePointModulation <qosst_core.modulation.singlepoint.SinglePointModulation>`).

They can all be used in the CV-QKD software as they respect the same coding formalism and inherits from the {py:class}`qosst_core.modulation.modulation.Modulation` class.

In general, the modulation can be used as follows:

```{code-block} python

from qosst_core.modulation import PSKModulation

modulation = PSKModulation(1, 4) # 1 for the variance, 4 for the size i.e. 4-PSK (or QPSK)
points = modulation.modulate(1000) # Generate 1000 random symbols from this modulation
```

If you are using the {py:class}`GaussianModulation <qosst_core.modulation.gaussian.GaussianModulation>`, the size parameter is unused, and a good behaviour is to put 0.

For an extended documentation on the modulations, check the [API documentation](../api/modulation.md).

In the following we present each modulation and an example code, with plot.

## Gaussian

The Gaussian modulation is modulating both quadratures with a Gaussian distribution with same variance (or standard deviation).

Here is a plot of a Gaussian distribution:

```{eval-rst}
.. plot:: pyplots/modulation/gaussian.py
    :include-source: true
    :align: center
    
```
## Phase Shift Keying (PSK)

The Phase Shift Keying modulation (PSK) is a modulation with fixed amplitude. It places the points on a circle with a constant angle difference (it also happened to be the unitary roots). For a size {math}`M`, the set of points is

```{math}
X + j Y = \exp\left(jK\frac{2\pi}{M}\right)
```

with {math}`K` following a uniform distribution on {math}`(0, M-1)`

```{math}
K\sim U(0,M-1)
```

up to a global scaling.

For {math}`M` to be a valid size for a {math}`M`-PSK, it should be a power of 2 (at least in our context).

We now plot examples of the constellation for {math}`M`-PSK ({math}`M=4`, {math}`M=8`) but by plotting the constellation (set of points) directly, and not actually generating data.

### 4-PSK

```{eval-rst}
.. plot:: pyplots/modulation/4-psk.py
    :include-source: true
    :align: center
    
```

### 8-PSK

```{eval-rst}
.. plot:: pyplots/modulation/8-psk.py
    :include-source: true
    :align: center
    
```

## Quadrature Amplitude Modulation (QAM)

The Quadrature Amplitude modulation (QAM) is a modulation displayed on a grid of size {math}`\sqrt{M}\times\sqrt{M}`. The points are placed uniformly on this grid according to the following distribution:

```{math}
X +jY \sim \left(2\times U\left(-\frac{\sqrt{M}}{2}, \frac{\sqrt{M}}{2} -1\right)+1\right) + j\left(2\times U\left(-\frac{\sqrt{M}}{2}, \frac{\sqrt{M}}{2} -1\right) + 1\right)
```
where {math}`U` is once again the uniform distribution and up to a global scaling.

For {math}`M` to be a valid size for a {math}`M`-QAM, it should be a power of 2 and a square, meaning that {math}`\sqrt{M}` should be an integer (at least in our context).

We now plot examples of the constellation for {math}`M`-QAM ({math}`M=4`, {math}`M=16` and {math}`M=256`) but by plotting the constellation (set of points) directly, and not actually generating data.

### 4-QAM

```{eval-rst}
.. plot:: pyplots/modulation/4-qam.py
    :include-source: true
    :align: center
```

### 16-QAM

```{eval-rst}
.. plot:: pyplots/modulation/16-qam.py
    :include-source: true
    :align: center
```


### 256-QAM

```{eval-rst}
.. plot:: pyplots/modulation/256-qam.py
    :include-source: true
    :align: center
```

## Probabilistic Constellation Shaping QAM (PCS-QAM)

The Probabilistic Constellation Shaping Quadrature Amplitude Modulation (PCS-QAM) is a modulation where the constellation is the same as the QAM, but this time the point are not chosen uniformly on the grid, but are chosen to approximate Gaussian.

A way to define it it to say that for each point {math}`(x,y)` on the QAM lattice, the probability of the point to be chosen is 

```{math}
p(x,y) \propto \exp(-\nu(x^2+y^2))
```

where {math}`\nu` is a parameter related to the variance, and up to a global scale.

For {math}`M` to be a valid size for a {math}`M`-PCSQAM, it should be a power of 2 and a square, meaning that {math}`\sqrt{M}` should be an integer (at least in our context).

In the following we plot examples for {math}`M=4`, {math}`M=16` and {math}`M=256`.

### 4-PCS-QAM

```{eval-rst}
.. plot:: pyplots/modulation/4-pcsqam.py
    :include-source: true
    :align: center
```


### 16-PCS-QAM

```{eval-rst}
.. plot:: pyplots/modulation/16-pcsqam.py
    :include-source: true
    :align: center
```

### 256-PCS-QAM

```{eval-rst}
.. plot:: pyplots/modulation/256-pcsqam.py
    :include-source: true
    :align: center
```

## Binomial Quadrature Amplitude Modulation (Binomial QAM)

### 4-BINOMIAL-QAM

```{eval-rst}
.. plot:: pyplots/modulation/4-binomialqam.py
    :include-source: true
    :align: center
```


### 16-BINOMIAL-QAM

```{eval-rst}
.. plot:: pyplots/modulation/16-binomialqam.py
    :include-source: true
    :align: center
```

### 256-BINOMIAL-QAM

```{eval-rst}
.. plot:: pyplots/modulation/256-binomialqam.py
    :include-source: true
    :align: center
```

## Single point

The single point modulation is just a single point and just should be used for test purposes.

Here is an example with the point {math}`(1,1)`.

```{eval-rst}
.. plot:: pyplots/modulation/singlepoint.py
    :include-source: true
    :align: center
```