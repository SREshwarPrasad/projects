<h2> DSR using BiLSTM-GRU </h2>

<h3>About:</h3>
The project focuses on recognizing Dysarthric Speech Pattern that deploys BiLSTM-GRU Model and comparing it against Hidden Markov Model.
The audio that are trained are the digits from the original UASpeech dataset (University of Illinois).  
The model is trained using 770 files across all digits. 

<h3> Algorithms: </h3>
i) BiLSTM-GRU (bilstm_gru.ipynb) 

ii) HMM (hmm.ipynb)  

<h3> Folder Structure: </h3> 

    digits/
      |   
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


<h3> File Structure:   </h3>    
[Gender][SpeakerID]_[Block]_[Digit]_[SampleNumber].wav  

*Example:* F02_B1_D0_M4.wav  

```
F02   _   B1   _   D0   _   M4   .wav  
│         │        │        │  
│         │        │        └──► Sample Number (4th recording)  
│         │        └──────────► Digit Spoken (0)  
│         └────────────────────► Block / Session Number (1)  
└──────────────────────────────► Speaker ID (Female Speaker 02)  
 ```

➤ F02 - Female speaker #02  
➤ B1 - Block/session 1 (multiple sessions per speaker)  
➤ D0  - Digit '0' was spoken  
➤ M4 - This is the 4th sample/utterance of that digit in the session    
➤ .wav - Audio file (WAV format)

<h3>Result: </h3>

<table>
  <tr>
    <td align ="center"> <b> MODEL </b> </td>
    <td align ="center"> <b> ACCURACY </b> </td>
  </tr>
  
  <tr>
    <td align ="center"> BiLSTM-GRU </td>
    <td align ="center"> 92% </td>
  </tr>
  
  <tr>
    <td align ="center"> HMM </td>
    <td align ="center"> 59% </td>
  </tr>
</table>
<h3>Dataset: </h3>
https://drive.google.com/file/d/1DCLvNL_aabzVLbur9eV8Ez0tHEO3kj3i/view?usp=drive_link

<h3> Terms: </h3>
i) DSR - Dysarthric Speech Recognition <br>            
ii) BiLSTM - Bidirectional Long Short-Term Memory <br>          
iii) GRU - Gated Recurrent Unit    <br>        
iv) HMM - Hidden Markov Model         <br>  
