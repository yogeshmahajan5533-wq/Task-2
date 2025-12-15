# Pixel Manipulation Image Encryption using Python

## 📌 Overview
This project implements a **password-based image encryption and decryption system** using **pixel manipulation techniques** in Python.

The encryption works by:
- Converting an image into pixel data
- Randomly shuffling pixel positions using a password-based seed
- Applying an XOR operation on pixel values
- Reversing the process using the same password to recover the original image

The encrypted image appears completely distorted and unreadable without the correct password.

---

## 🔐 Encryption Approach Used

This project uses **two core techniques**:

### 1️⃣ Pixel Permutation
- The image pixels are flattened into a 1D array
- A **deterministic random permutation** is generated using a password-derived seed
- Pixels are rearranged based on this permutation

### 2️⃣ XOR-based Encryption
- The password is hashed using **SHA-256**
- The hash bytes are used as an XOR mask
- Each pixel channel (RGBA) is XORed with the mask

Since XOR is reversible, applying the same operation during decryption restores the original values.

---

## 🧠 Key Concept
> **Same password = same seed + same permutation + same XOR mask**

If the password changes, decryption will fail and the image remains corrupted.

---

## 🛠️ Technologies Used
- **Python 3**
- **NumPy** – Fast numerical and array operations
- **Pillow (PIL)** – Image loading and saving
- **Hashlib** – Secure password hashing (SHA-256)

---

## 📂 Project Structure
├── image_crypto.py # Encryption & decryption logic
├── image.png # Original image
├── encrypted_img.png # Encrypted image
├── decrypted_img.png # Decrypted image
└── README.md # Documentation

## ⚙️ How the Code Works

### Password Processing
```python
h = hashlib.sha256(password.encode('utf-8')).digest()
seed = int.from_bytes(h[:8], 'big')
key = h

SHA-256 hash ensures deterministic behavior
First 8 bytes → random seed
Full hash → XOR key

### Encryption Steps

1.Load image and convert to RGBA
2.Flatten image into (N, 4) pixel array
3.Generate permutation using numpy.random.default_rng(seed)
4.Rearrange pixels
5.XOR pixels with key-based mask
6.Save encrypted image

### Decryption Steps

1.Load encrypted image
2.Regenerate the same permutation
3.XOR pixels to remove encryption
4.Apply inverse permutation
5.Restore original image

▶️ How to Run the Program

    Install Dependencies :
        pip install pillow numpy

    Run the Script :
        python image_crypto.py

Sample Interaction :
 
Simple Image Encryption Tool
Do you want to (E)ncrypt or (D)ecrypt? e
Enter input image path: input.png
Enter output image path: encrypted.png
Enter password: mypassword