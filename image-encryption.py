import hashlib
import numpy as np
from PIL import Image


# Convert password → deterministic seed + key
def password_to_seed_and_key(password: str):
    h = hashlib.sha256(password.encode('utf-8')).digest()
    seed = int.from_bytes(h[:8], 'big')     # first 8 bytes → seed
    key = h                                 # full 32 bytes → XOR key
    return seed, key


# ---------------- ENCRYPT ----------------
def encrypt_image(input_path, output_path, password):
    img = Image.open(input_path).convert("RGBA")
    arr = np.array(img)

    h, w, c = arr.shape
    flat = arr.reshape(-1, c)   # flatten pixels

    seed, key = password_to_seed_and_key(password)
    rng = np.random.default_rng(seed)

    N = flat.shape[0]

    # Generate pixel permutation
    perm = rng.permutation(N)

    # Apply permutation
    permuted = flat[perm]

    # XOR step
    key_bytes = np.frombuffer(key, dtype=np.uint8)
    xor_mask = np.tile(key_bytes[:c], N).reshape(N, c)

    encrypted = np.bitwise_xor(permuted, xor_mask)

    encrypted = encrypted.reshape(h, w, c)
    Image.fromarray(encrypted).save(output_path)
    print(f"[✔] Encrypted image saved to {output_path}")


# ---------------- DECRYPT ----------------
def decrypt_image(input_path, output_path, password):
    img = Image.open(input_path).convert("RGBA")
    arr = np.array(img)

    h, w, c = arr.shape
    flat = arr.reshape(-1, c)

    seed, key = password_to_seed_and_key(password)
    rng = np.random.default_rng(seed)

    N = flat.shape[0]

    # Same permutation generated again
    perm = rng.permutation(N)

    # Build inverse permutation
    inv_perm = np.empty_like(perm)
    inv_perm[perm] = np.arange(N)

    # XOR unmask
    key_bytes = np.frombuffer(key, dtype=np.uint8)
    xor_mask = np.tile(key_bytes[:c], N).reshape(N, c)

    unxored = np.bitwise_xor(flat, xor_mask)

    # Reverse permutation
    original = unxored[inv_perm]

    original = original.reshape(h, w, c)
    Image.fromarray(original).save(output_path)
    print(f"[✔] Decrypted image saved to {output_path}")


# ---------------- MAIN DEMO ----------------
if __name__ == "__main__":
    print("Simple Image Encryption Tool")

    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().lower()
    inp = input("Enter input image path: ").strip()
    out = input("Enter output image path: ").strip()
    password = input("Enter password: ").strip()

    if choice == "e":
        encrypt_image(inp, out, password)
    elif choice == "d":
        decrypt_image(inp, out, password)
    else:
        print("Invalid option.")
