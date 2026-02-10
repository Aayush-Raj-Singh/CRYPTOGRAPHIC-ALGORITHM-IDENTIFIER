import os
import csv
import secrets
import random
import argparse
from tqdm import tqdm

from Crypto.Cipher import AES, DES, DES3, ARC4, ChaCha20, PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad

# ---------------- DEFAULT CONFIG ---------------- #
DEFAULT_SAMPLES_PER_ALGO = 1000
DEFAULT_PLAINTEXT_SIZES = [128, 256, 512, 1024, 2048, 4096]
DEFAULT_STRUCTURED_RATIO = 0.35
DEFAULT_RSA_KEY_SIZES = [1024, 2048, 4096]

ALGORITHMS = ["AES", "DES", "3DES", "RC4", "ChaCha20", "RSA"]

# ---------------- UTILITIES ---------------- #

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate encrypted dataset with multiple modes and sizes."
    )
    parser.add_argument(
        "--samples-per-algo",
        type=int,
        default=DEFAULT_SAMPLES_PER_ALGO,
        help="Number of samples per algorithm (default: 1000).",
    )
    parser.add_argument(
        "--plaintext-sizes",
        type=str,
        default=",".join(str(s) for s in DEFAULT_PLAINTEXT_SIZES),
        help="Comma-separated plaintext sizes (default: 128,256,512,1024,2048,4096).",
    )
    parser.add_argument(
        "--structured-ratio",
        type=float,
        default=DEFAULT_STRUCTURED_RATIO,
        help="Ratio of structured plaintexts (0-1).",
    )
    parser.add_argument(
        "--rsa-key-sizes",
        type=str,
        default=",".join(str(s) for s in DEFAULT_RSA_KEY_SIZES),
        help="Comma-separated RSA key sizes (default: 1024,2048,4096).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional seed for reproducible plaintext patterns.",
    )
    return parser.parse_args()


def generate_plaintext(size: int, rng: random.Random, structured_ratio: float) -> bytes:
    if size <= 0:
        return b""

    if rng.random() > structured_ratio:
        return secrets.token_bytes(size)

    mode = rng.choice(["ascii", "pattern", "zero", "increment"])
    if mode == "ascii":
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 "
        return "".join(rng.choice(alphabet) for _ in range(size)).encode("utf-8")
    if mode == "pattern":
        pattern_len = rng.choice([4, 8, 16, 32])
        pattern = secrets.token_bytes(pattern_len)
        return (pattern * (size // pattern_len + 1))[:size]
    if mode == "zero":
        return bytes([0]) * size
    if mode == "increment":
        return bytes([i % 256 for i in range(size)])

    return secrets.token_bytes(size)

# ---------------- ENCRYPTION FUNCTIONS ---------------- #

def encrypt_aes(data: bytes, rng: random.Random) -> bytes:
    key_size = rng.choice([16, 24, 32])
    key = secrets.token_bytes(key_size)
    mode = rng.choice(["CBC", "CTR", "GCM", "ECB"])

    if mode == "CBC":
        iv = secrets.token_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(pad(data, 16))
    if mode == "CTR":
        nonce = secrets.token_bytes(8)
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        return nonce + cipher.encrypt(data)
    if mode == "GCM":
        nonce = secrets.token_bytes(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return nonce + ciphertext + tag
    if mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.encrypt(pad(data, 16))

    return data


def encrypt_des(data: bytes, rng: random.Random) -> bytes:
    key = secrets.token_bytes(8)
    mode = rng.choice(["CBC", "ECB"])

    if mode == "CBC":
        iv = secrets.token_bytes(8)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        return iv + cipher.encrypt(pad(data, 8))
    if mode == "ECB":
        cipher = DES.new(key, DES.MODE_ECB)
        return cipher.encrypt(pad(data, 8))

    return data


def encrypt_3des(data: bytes, rng: random.Random) -> bytes:
    key = DES3.adjust_key_parity(secrets.token_bytes(24))
    mode = rng.choice(["CBC", "ECB"])

    if mode == "CBC":
        iv = secrets.token_bytes(8)
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        return iv + cipher.encrypt(pad(data, 8))
    if mode == "ECB":
        cipher = DES3.new(key, DES3.MODE_ECB)
        return cipher.encrypt(pad(data, 8))

    return data


def encrypt_rc4(data: bytes) -> bytes:
    key = secrets.token_bytes(16)
    cipher = ARC4.new(key)
    return cipher.encrypt(data)


def encrypt_chacha20(data: bytes) -> bytes:
    key = secrets.token_bytes(32)
    cipher = ChaCha20.new(key=key)
    return cipher.nonce + cipher.encrypt(data)


def rsa_chunk_size(key_bytes: int, scheme: str) -> int:
    if scheme == "OAEP":
        hash_len = 20  # SHA1 default
        return key_bytes - 2 * hash_len - 2
    return key_bytes - 11


def encrypt_rsa(data: bytes, public_key, rng: random.Random) -> bytes:
    scheme = rng.choice(["OAEP", "PKCS1v15"])
    key_bytes = public_key.size_in_bytes()

    if scheme == "OAEP":
        cipher = PKCS1_OAEP.new(public_key)
        chunk_size = rsa_chunk_size(key_bytes, "OAEP")
    else:
        cipher = PKCS1_v1_5.new(public_key)
        chunk_size = rsa_chunk_size(key_bytes, "PKCS1v15")

    encrypted = b""
    for i in range(0, len(data), chunk_size):
        encrypted += cipher.encrypt(data[i:i + chunk_size])

    return encrypted

# ---------------- MAIN GENERATOR ---------------- #

def main():
    args = parse_args()
    rng = random.Random(args.seed)

    sizes = [int(s.strip()) for s in args.plaintext_sizes.split(",") if s.strip()]
    if not sizes:
        sizes = DEFAULT_PLAINTEXT_SIZES

    rsa_sizes = [int(s.strip()) for s in args.rsa_key_sizes.split(",") if s.strip()]
    if not rsa_sizes:
        rsa_sizes = DEFAULT_RSA_KEY_SIZES

    base_dir = "data"
    plaintext_dir = os.path.join(base_dir, "plaintext")
    encrypted_dir = os.path.join(base_dir, "encrypted")
    label_file = os.path.join(base_dir, "labels.csv")

    os.makedirs(plaintext_dir, exist_ok=True)
    os.makedirs(encrypted_dir, exist_ok=True)
    for algo in ALGORITHMS:
        os.makedirs(os.path.join(encrypted_dir, algo), exist_ok=True)

    rsa_keys = {}
    for size in rsa_sizes:
        rsa_keys[size] = RSA.generate(size).publickey()

    with open(label_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "algorithm"])

        sample_id = 0

        for algo in ALGORITHMS:
            print(f"[+] Generating samples for {algo}")

            for _ in tqdm(range(args.samples_per_algo)):
                size = rng.choice(sizes)
                plaintext = generate_plaintext(size, rng, args.structured_ratio)

                if algo == "AES":
                    ciphertext = encrypt_aes(plaintext, rng)
                elif algo == "DES":
                    ciphertext = encrypt_des(plaintext, rng)
                elif algo == "3DES":
                    ciphertext = encrypt_3des(plaintext, rng)
                elif algo == "RC4":
                    ciphertext = encrypt_rc4(plaintext)
                elif algo == "ChaCha20":
                    ciphertext = encrypt_chacha20(plaintext)
                elif algo == "RSA":
                    key_size = rng.choice(rsa_sizes)
                    ciphertext = encrypt_rsa(plaintext, rsa_keys[key_size], rng)
                else:
                    continue

                filename = f"sample_{sample_id:06d}.bin"
                filepath = os.path.join(encrypted_dir, algo, filename)

                with open(filepath, "wb") as f:
                    f.write(ciphertext)

                writer.writerow([filename, algo])
                sample_id += 1

    print("[?] Dataset generation completed successfully.")


if __name__ == "__main__":
    main()
