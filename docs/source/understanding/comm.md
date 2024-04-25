# Comm

## Filters

One of the most important function in this module is the {py:func}`~qosst_core.comm.filters.root_raised_cosine_filter` function but to fully understand the root raised cosine filters, we need first to discuss raised cosine filters.

The raised cosine filter, that can be generated in QOSST using the {py:func}`~qosst_core.comm.filters.raised_cosine_filter` function, is defined by it's frequency response

```{math}
H_{rc}(f) = \begin{cases}
 1,
       & |f| \leq \frac{1 - \beta}{2}\cdot R_S \\
 \frac{1}{2}\left[1 + \cos\left(\frac{\pi}{\beta R_S}\left[|f| - \frac{1 - \beta}{2}\cdot R_S\right]\right)\right],
       & \frac{1 - \beta}{2}\cdot R_S < |f| \leq \frac{1 + \beta}{2}\cdot R_S \\
 0,
       & \text{otherwise}
\end{cases}
```

where {math}`R_S` is the symbol rate and {math}`\beta` a parameter of the filter called the roll-off which is between 0 and 1.

It can be seen that the ase {math}`\beta=0` corresponds to a perfect square of bandwidth {math}`R_S` in the frequency domain, that will result in a temporal response being a sinc function. Modifying the value of the roll-off will slightly change the form of the sinc in the temporal domain, but leaving the zeros the same place, *i.e.* for {math}`t=k\cdot T_S` with {math}`k\neq 0` and {math}`T_S = 1/R_S` the symbol period, as can be seen on the following plot:

```{eval-rst}
.. plot:: pyplots/rc/roll_off_temporal.py
    :include-source: true
    :align: center
    
```

This already hints why the raised cosine filter is very useful: because it minimizes intersymbol interfence. Indeed when performing the convolution, the behaviour in the temporal domain will be that at some {math}`k\cdot T_S` for {math}`k\in\mathbb{Z}`, one symbol will be maximal, and the others 0, as can be seen in the following figure:

```{eval-rst}
.. plot:: pyplots/rc/symbol_rate.py
    :include-source: true
    :align: center
    
```

Another advantage of the raised cosine filter is that is frequency response has a finite bandwidth. We already saw that the bandwidth was {math}`R_S` when the roll-off was 0, and in the general case, the bandwidth is 

```{math}
2\cdot \frac{1+\beta}{2}\cdot R_S = (1+\beta)\cdot R_S
```

As {math}`R_S` is at most 1, the bandwidth is between {math}`R_S` and {math}`2\cdot R_S` as can be seen in the following figure:

```{eval-rst}
.. plot:: pyplots/rc/roll_off_frequential.py
    :include-source: true
    :align: center
```

The effect of the roll-off on the frequency response can also be seen, as it "smoothens" the square. Please note that the frequency response for {math}`\beta=0` should be a perfect square but is not due to a finite number of samples (the fft of the filter is plotted, not the formula used in the definition).

For those reasons, the raised cosine is a very strong candidates for the CV-QKD transmissions. However, to reduce the effect of white gaussian noise in the channel, it is usual to apply a matched filter on the receiver side. Hence, it is possible to define a root raised cosine as 

```{math}

H_{rrc}(f)\cdot H_{rrc}(f) = H_{rc}(f)
```

and it can be shown that the root raised cosine is its own matched filter, so we can apply a root raised cosine at Alice's side and a root raised cosine at Bob's side, that will be in total a raised cosine filter.

## Zadoff-Chu sequence

The Zadoff-Chu sequence is a complex sequence defined by

```{math}
ZC(n) = \exp\left(-j\frac{\pi R_{ZC} n (n+c_f+2q)}{L_{ZC}}\right)
```

where {math}`L_{ZC}` is the length of the sequence and {math}`R_{ZC}<L_{ZC}` is the root of the sequence. Moreover, it is imposed that `R_{ZC}` and `L_{ZC}` are coprimes, *i.e.* that {math}`\text{gcd}(R_{ZC}, L_{ZC}) = 1`. {math}`c_f` is defined as {math}`c_f = L_{ZC} \text{mod} 2` and {math}`q` is the cyclic shift.

Here is an example of the real and imaginary part of a Zadoff-Chu sequence:

```{eval-rst}
.. plot:: pyplots/zc/zc.py
    :include-source: true
    :align: center
```

The Zadoff-Chu sequences are constant modulus and have good auto-correlation properties that results in a good candidates for frame synchronisation.
