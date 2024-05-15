import numpy as np
from scipy.signal import welch, correlate


def rms(x):
    return np.sqrt(np.mean(x**2))


def welch528(sig, fs):
    f, Pxx = welch(sig, fs=fs, nperseg=150)
    return np.max(Pxx)


def autocorr528(sig, numLags):
    return np.max(
        correlate(sig, sig, mode="full")[len(sig) - 1 : len(sig) - 1 + numLags]
    )


def extractFeatures528(data, fs, numLags):
    ax = data[:, 0]
    ay = data[:, 1]
    az = data[:, 2]
    gx = data[:, 3]
    gy = data[:, 4]
    gz = data[:, 5]

    extractedFeatures = {}

    # Mean
    extractedFeatures["mean_ax"] = np.mean(ax)
    extractedFeatures["mean_ay"] = np.mean(ay)
    extractedFeatures["mean_az"] = np.mean(az)
    extractedFeatures["mean_gx"] = np.mean(gx)
    extractedFeatures["mean_gy"] = np.mean(gy)
    extractedFeatures["mean_gz"] = np.mean(gz)

    # Root Mean Square
    extractedFeatures["rms_ax"] = rms(ax)
    extractedFeatures["rms_ay"] = rms(ay)
    extractedFeatures["rms_az"] = rms(az)
    extractedFeatures["rms_gx"] = rms(gx)
    extractedFeatures["rms_gy"] = rms(gy)
    extractedFeatures["rms_gz"] = rms(gz)

    # Auto-correlation
    extractedFeatures["autocorr_ax"] = autocorr528(ax, numLags)
    extractedFeatures["autocorr_ax"] = autocorr528(ay, numLags)
    extractedFeatures["autocorr_ax"] = autocorr528(az, numLags)
    extractedFeatures["autocorr_ax"] = autocorr528(gx, numLags)
    extractedFeatures["autocorr_ax"] = autocorr528(gy, numLags)
    extractedFeatures["autocorr_ax"] = autocorr528(gz, numLags)

    # Power Spectral Density
    extractedFeatures["psd_ax"] = welch528(ax, fs)
    extractedFeatures["psd_ay"] = welch528(ay, fs)
    extractedFeatures["psd_az"] = welch528(az, fs)
    extractedFeatures["psd_gx"] = welch528(gx, fs)
    extractedFeatures["psd_gy"] = welch528(gy, fs)
    extractedFeatures["psd_gz"] = welch528(gz, fs)

    return extractedFeatures
