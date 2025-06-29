# Dysarthric Speech Recognition

A machine learning project for recognizing spoken digits (0–9) by dysarthric speakers using BiLSTM+GRU and HMM models for comparison.

---

## 🎯 Objective

To build a robust speech recognition system tailored for dysarthric speech by:

- Extracting MFCC features from audio
- Classifying spoken digits using a BiLSTM+GRU deep learning model
- Comparing performance with a classical HMM-based approach

---

## 🧠 Models

| Model        | Description                                             |
|--------------|---------------------------------------------------------|
| **BiLSTM + GRU** | Combines bidirectional LSTM and GRU layers for better temporal learning. |
| **HMM (Hidden Markov Model)** | A statistical baseline model for sequence prediction. |

---

## 🎧 Dataset

- **Type**: Audio `.wav` files
- **Samples**: 770 total (77 samples for each digit from 0 to 9)
- **Source**: Collected from dysarthric speakers
- **Structure**:

- data/raw/
├── D0/
├── D1/
├── ...
└── D9/


Each folder contains 77 audio files for the corresponding digit label.

---

## 🔧 Features

- MFCC (Mel Frequency Cepstral Coefficients) with 39 coefficients
- Fixed length time padding (100 frames)
- Label encoding using scikit-learn

---

## 🚀 Getting Started

### 1. Clone this Repository

```bash
git clone https://github.com/SREshwarPrasad/projects.git
cd projects/dysarthric_speech_recognition

