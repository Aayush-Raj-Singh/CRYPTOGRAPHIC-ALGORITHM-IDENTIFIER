import os
import csv
import secrets
from tqdm import tqdm

from Crypto.Cipher import AES, DES, DES3, ARC4, ChaCha20, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad

# ---------------- CONFIG ---------------- #

BASE_DIR = "data"
PLAINTEXT_DIR = os.path.join(BASE_DIR, "plaintext")
ENCRYPTED_DIR = os.path.join(BASE_DIR, "encrypted")
LABEL_FILE = os.path.join(BASE_DIR, "labels.csv")

SAMPLES_PER_ALGO = 500
PLAINTEXT_SIZES = [256, 512, 1024, 2048]

# ---------------------------------------- #

os.makedirs(PLAINTEXT_DIR, exist_ok=True)
os.makedirs(ENCRYPTED_DIR, exist_ok=True)

ALGORITHMS = ["AES", "DES", "3DES", "RC4", "ChaCha20", "RSA"]

for algo in ALGORITHMS:
    os.makedirs(os.path.join(ENCRYPTED_DIR, algo), exist_ok=True)

# ---------------- UTILITIES ---------------- #

def generate_plaintext(size: int) -> bytes:
    """
    Generates high-entropy random plaintext.
    """
    return secrets.token_bytes(size)

# ---------------- ENCRYPTION FUNCTIONS ---------------- #

def encrypt_aes(data: bytes) -> bytes:
    key = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data, 16))

def encrypt_des(data: bytes) -> bytes:
    key = secrets.token_bytes(8)
    iv = secrets.token_bytes(8)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data, 8))

def encrypt_3des(data: bytes) -> bytes:
    key = DES3.adjust_key_parity(secrets.token_bytes(24))
    iv = secrets.token_bytes(8)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data, 8))

def encrypt_rc4(data: bytes) -> bytes:
    key = secrets.token_bytes(16)
    cipher = ARC4.new(key)
    return cipher.encrypt(data)

def encrypt_chacha20(data: bytes) -> bytes:
    key = secrets.token_bytes(32)
    cipher = ChaCha20.new(key=key)
    return cipher.nonce + cipher.encrypt(data)

def encrypt_rsa(data: bytes, public_key) -> bytes:
    cipher = PKCS1_OAEP.new(public_key)
    chunk_size = 190  # RSA-2048 safe chunk
    encrypted = b""

    for i in range(0, len(data), chunk_size):
        encrypted += cipher.encrypt(data[i:i+chunk_size])

    return encrypted

# ---------------- MAIN GENERATOR ---------------- #

def main():
    rsa_key = RSA.generate(2048)
    rsa_public = rsa_key.publickey()

    with open(LABEL_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "algorithm"])

        sample_id = 0

        for algo in ALGORITHMS:
            print(f"[+] Generating samples for {algo}")

            for _ in tqdm(range(SAMPLES_PER_ALGO)):
                size = secrets.choice(PLAINTEXT_SIZES)
                plaintext = generate_plaintext(size)

                if algo == "AES":
                    ciphertext = encrypt_aes(plaintext)
                elif algo == "DES":
                    ciphertext = encrypt_des(plaintext)
                elif algo == "3DES":
                    ciphertext = encrypt_3des(plaintext)
                elif algo == "RC4":
                    ciphertext = encrypt_rc4(plaintext)
                elif algo == "ChaCha20":
                    ciphertext = encrypt_chacha20(plaintext)
                elif algo == "RSA":
                    ciphertext = encrypt_rsa(plaintext, rsa_public)
                else:
                    continue

                filename = f"sample_{sample_id:06d}.bin"
                filepath = os.path.join(ENCRYPTED_DIR, algo, filename)

                with open(filepath, "wb") as f:
                    f.write(ciphertext)

                writer.writerow([filename, algo])
                sample_id += 1

    print("[✔] Dataset generation completed successfully.")

if __name__ == "__main__":
    main()
