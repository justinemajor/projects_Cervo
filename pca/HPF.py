import numpy as np
import matplotlib.pyplot as mpl


"""1. Creating the plot disposition"""
fig1, [ax1, ax2, ax3] = mpl.subplots(3)

"""2. Creating an arbitrary spectrum to test the method"""
# spectrum = np.array([1, 0, 10, 0, 0, 0, 5, 10, 5, 2, 0, 0, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0])
spectrum = np.random.randint(0, 15, 51)
ax1.plot(spectrum, label="raw spectrum")

"""3. Fourier transformation"""
fft = np.fft.fft(spectrum)
ax2.plot(fft, label="fft before filter")
# ax2.plot(11.5, (fft[11]+fft[12])/2, "ok", label="middle point")

"""4. Apply a "symmetrical" filter, either high-pass or low-pass"""
# Better when keeping the first point, because of a vertical translation/alignment
nCut = 20
tot = len(fft)
ff = "hpf"  # frequency filter, which has a value of either "lpf" or "hpf"

if tot % 2 == 1:
    lmi = int((tot-1)/2)  # lowerMiddleIndex
    umi = lmi + 1  # upperMiddleIndex
else:
    lmi = int(tot/2)
    umi = lmi

"""For high-pass filter (HPF)"""
if ff == "hpf":
    fft[1:1+nCut] = np.zeros(nCut)
    fft[-nCut:] = np.zeros(nCut)  # symmetrical!

"""For low-pass filter (LPF)"""
if ff == "lpf":
    lowerLimit = lmi-nCut+1
    upperLimit = umi+nCut
    fft[lowerLimit:upperLimit] = np.zeros(upperLimit-lowerLimit)

if ff not in ["lpf", "hpf"]:
    raise ValueError("The value given to the frequency filter is not an option. Please choose between 'lpf' and 'hpf'.")

ax2.plot(fft, label="fft after filter")

"""5. Reconstruct the spectrum with the filtered fft"""
dft = np.fft.ifft(fft)
ax1.plot(dft, label="spectrum after filter")

"""6. Check if the imaginary part of the reconstructed spectrum is indeed null"""
# Imaginary part is Null when filter is symmetrical (not considering the first point)
ax3.plot(np.imag(dft), label="Imaginary part of the reconstructed spectrum")

"""7. Show the results!"""
ax1.legend()
ax2.legend()
ax3.legend()
mpl.show()