# 🔐 Cryptographic Algorithm Identifier

An end-to-end machine learning–based system to identify cryptographic algorithms from ciphertext using statistical feature extraction and pattern recognition.  
The project is deployed as a web application using **FastAPI (backend)** and **React (frontend)**.

---

## 🚀 Project Overview

Modern cryptographic algorithms are designed to produce high-entropy ciphertext, making manual identification difficult during malware analysis, digital forensics, and threat intelligence investigations.

This project addresses that challenge by:
- Generating a controlled encrypted dataset
- Extracting statistical and structural features from ciphertext
- Training an ML classifier to identify the encryption algorithm
- Deploying the trained model as a REST API
- Providing a web-based UI for real-time inference

---

## 🧠 Key Features

- 🔍 Identifies cryptographic algorithms from encrypted files
- 📊 Uses entropy, byte frequency, block repetition & structural features
- 🤖 Supervised ML classifier (Random Forest)
- 🌐 FastAPI backend with OpenAPI documentation
- ⚛️ React frontend for file upload and result visualization
- 🔒 No key recovery, no decryption (ethical cryptanalysis)

---

## 🔐 Supported Algorithms

- AES (Block Cipher)
- ChaCha20 (Stream Cipher)
- RSA (Asymmetric)
- RC4 (Legacy – for contrast)
- DES / 3DES (Legacy – for contrast)

---

## 🏗️ System Architecture

```
React Frontend
     |
     v
FastAPI Backend (/predict)
     |
     v
Feature Extraction Engine
     |
     v
ML Classifier (Random Forest)
```

---

## ⚙️ Tech Stack

### Backend
- Python 3
- FastAPI
- Scikit-learn
- PyCryptodome
- NumPy / Pandas

### Frontend
- React.js
- HTML / CSS / JavaScript

---

## ▶️ How to Run (Local)

### Backend
```bash
cd crypto-dataset
pip install -r requirements.txt
py -m uvicorn backend.app:app --reload
```

### Frontend
```bash
cd crypto-frontend
npm install
npm start
```

---

## 🛡️ Security & Ethics

This system does **NOT** break encryption or recover keys.  
It performs statistical classification only and is intended for defensive security research.

---

## 👨‍💻 Author

**Aayush Raj**  
B.Tech CSE (Cyber Security)

GitHub: https://github.com/Aayush-Raj-Singh  
LinkedIn: https://www.linkedin.com/in/aayush-raj-77a1bb237/
