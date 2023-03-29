import librosa
import numpy as np

def normalize(data):
    mean_val = np.mean(data)
    std_val = np.std(data)
    normalized_data = (data - mean_val) / std_val
    return normalized_data

def mfccDTWScore(x, y, sr):
    xmfcc = librosa.feature.mfcc(y=x, sr=sr)
    ymfcc = librosa.feature.mfcc(y=y, sr=sr)
    z_x = (xmfcc - np.mean(xmfcc, axis=1, keepdims=True)) / np.std(xmfcc, axis=1, keepdims=True)
    z_y = (ymfcc - np.mean(ymfcc, axis=1, keepdims=True)) / np.std(ymfcc, axis=1, keepdims=True)
    d, wp = librosa.sequence.dtw(z_x, z_y)

    optimalDistance = []
    for pair in wp:
        distance = d[pair[0]][pair[1]]
        optimalDistance = np.append(optimalDistance, distance)

    normalized = normalize(optimalDistance)
    score = np.mean(normalized)

    return float(round(score, 2))

def chromaDTWScore(x, y, sr):
    xmfcc = librosa.feature.chroma_cens(y=x, sr=sr)
    ymfcc = librosa.feature.chroma_cens(y=y, sr=sr)
    d, wp = librosa.sequence.dtw(xmfcc, ymfcc)
    optimalDistance = []

    for pair in wp:
        distance = d[pair[0]][pair[1]]
        optimalDistance.append(distance)

    normalized = normalize(optimalDistance)
    score = np.mean(normalized)

    return float(round(score, 2))

def cosine(x, y):
    # Extract MFCCs from the two audio arrays
    mfcc1 = librosa.feature.mfcc(y=x)
    mfcc2 = librosa.feature.mfcc(y=y)
    # Calculate the cosine similarity between the two MFCC arrays
    mfcc1 = np.transpose(mfcc1)
    mfcc2 = np.transpose(mfcc2)
    # Calculate the cosine similarity between the two MFCC arrays
    dot_product = np.dot(mfcc1, np.transpose(mfcc2))
    norm_product = np.linalg.norm(mfcc1) * np.linalg.norm(mfcc2)
    similarity = dot_product / norm_product
    # Return the single score rank value
    return np.mean(similarity)

def main():
    x, sr = librosa.load('loops/bass\CPA_BFD_140_808_loop_chiro_Dm.wav')
    y, sr = librosa.load('loops\minimalm\Cymatics - Angels Vocal 2 Wet - 84 BPM G Min.wav')
    #mfccScore = mfccDTWScore(x, y, sr)
    #mfccScore2 = mfccDTWScore(x, x[500:], sr)
    print(cosine(x, y))
    
if __name__ == '__main__':
    main()