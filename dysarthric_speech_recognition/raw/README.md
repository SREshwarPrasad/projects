# 🤖 Dysarthric Speech Digit Recognition

This project compares a BiLSTM+GRU deep learning model with a classic HMM on the task of digit recognition (0–9) spoken by dysarthric patients.

## 📁 Structure

- `notebooks/`
  - `01_hmm_baseline.ipynb`: HMM model using `hmmlearn`
  - `02_bilstm_gru.ipynb`: Deep model in PyTorch
- `src/`
  - `dataset.py`: Loads MFCCs and prepares training data
  - `model.py`: BiLSTM + GRU architecture
  - `train.py`: Training loop
  - `infer.py`: Predicts a digit from a new .wav file
- `data/`
  - Contains raw audio data or instructions to download

## 🧪 Dataset

- 770 WAV files (10 digits × ~77 speakers)
- Extracted MFCCs (39-dimensional)
- Focused on digit recognition due to large dataset size

## 🧠 Why BiLSTM + GRU?

BiLSTM captures forward and backward temporal patterns, especially useful for slurred or delayed speech. GRU adds compactness and helps stabilize learning — outperforming HMMs which rely on fixed state transitions.

## 🏃‍♂️ How to Run

```bash
cd projects/dysarthric_speech_recognition/
pip install -r requirements.txt
jupyter notebook
