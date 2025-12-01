DYSARTHRIC SPEECH RECOGNITION USING BiLSTM-GRU 

A lightweight model for Digit (0-9) Classification

The project focuses on recognizing Dysarthric Speech Pattern that deploys BiLSTM-GRU Model and comparing it against Hidden Markov Model.

Dataset: https://drive.google.com/file/d/1DCLvNL_aabzVLbur9eV8Ez0tHEO3kj3i/view?usp=drive_link

Folder Structure: 

  
    digits/
   
      ├── D0/
      │   ├── F02_B1_D0_M4.wav
      │   ├── ...
      │   └── M01_B1_D0_M?.wav
      │
      ├── D1/
      │   ├── F02_B1_D1_M4.wav
      │   ├── ...
      │   └── M01_B1_D1_M?.wav
      │
      ├── D2/
      │   ├── files...
      │
      ├── D3/
      │   ├── files...
      │
      ├── D4/
      │   ├── files...
      │
      ├── D5/
      │   ├── files...
      │
      ├── D6/
      │   ├── files...
      │
      ├── D7/
      │   ├── files...
      │
      ├── D8/
      │   ├── files...
      │
      └── D9/
          ├── files...


File Structure: 

[Gender][SpeakerID]\_[Block]\_[Digit]\_[SampleNumber].wav

Example: F02_B1_D0_M4.wav



The code: 

The sample code that I have uploaded pass with an impressive accuracy of 91%.

An example to test the model with the digit '4' has been implemented with text-to-speech design that utters the digit properly.
