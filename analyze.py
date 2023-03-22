import librosa
import numpy as np

def mfccDTWScore(x, y, sr):
    xmfcc = librosa.feature.mfcc(y=x, sr=sr)
    ymfcc = librosa.feature.mfcc(y=y, sr=sr)
    d, wp = librosa.sequence.dtw(xmfcc, ymfcc)
    optimalDistance = []

    for pair in wp:
        distance = d[pair[0]][pair[1]]
        optimalDistance.append(distance)

    score = np.sum(optimalDistance)/len(optimalDistance)
    return score

def chromaDTWScore(x, y, sr):
    xmfcc = librosa.feature.chroma_cens(y=x, sr=sr)
    ymfcc = librosa.feature.chroma_cens(y=y, sr=sr)
    d, wp = librosa.sequence.dtw(xmfcc, ymfcc)
    optimalDistance = []

    for pair in wp:
        distance = d[pair[0]][pair[1]]
        optimalDistance.append(distance)

    score = np.sum(optimalDistance)/len(optimalDistance)
    return score