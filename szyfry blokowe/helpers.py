import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import time
from typing import Tuple

import os
import time
from typing import Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def prepare_encryption(input_filepath: str, mode_name: str = "CTR") -> Tuple[bytes, modes.Mode, bytes]:
    mode_name = mode_name.upper()
    
    with open(input_filepath, 'rb') as file:
        file_data = file.read()

    iv_or_nonce = os.urandom(16) 
    needs_padding = False

    if mode_name == 'CTR':
        mode = modes.CTR(iv_or_nonce)
    elif mode_name == 'CBC':
        mode = modes.CBC(iv_or_nonce)
        needs_padding = True 
    elif mode_name == 'CFB':
        mode = modes.CFB(iv_or_nonce)
    elif mode_name == 'OFB':
        mode = modes.OFB(iv_or_nonce)
    elif mode_name == 'ECB':
        mode = modes.ECB()
        needs_padding = True 
        iv_or_nonce = b""   
    else:
        raise ValueError(f"Nieobsługiwany tryb: {mode_name}")

    if needs_padding:
        padder = padding.PKCS7(128).padder()
        data_to_encrypt = padder.update(file_data) + padder.finalize()
    else:
        data_to_encrypt = file_data

    return data_to_encrypt, mode, iv_or_nonce

def encrypt_data(key: bytes, data_to_encrypt: bytes, iv_or_nonce: bytes, mode: modes.Mode, output_filepath: str = None) -> Tuple[float, bytes]:
    timer_start = time.perf_counter()

    cipher = Cipher(algorithms.AES(key), mode)
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data_to_encrypt) + encryptor.finalize()

    timer_end = time.perf_counter()

    encrypted_content = iv_or_nonce + encrypted_data if iv_or_nonce else encrypted_data

    if output_filepath:
        with open(output_filepath, 'wb') as file: 
            file.write(encrypted_content)

    return timer_end - timer_start,  encrypted_content

def decrypt_data(key: bytes, encrypted_file: bytes, mode: str, output_filepath: str = None) -> Tuple[float, bytes]:
    mode_name = mode.upper()
    
    raw_content = encrypted_file

    if mode_name == 'ECB':
        iv = b""
        actual_ciphertext = raw_content
        mode = modes.ECB()
    else:
        iv = raw_content[:16]
        actual_ciphertext = raw_content[16:]
        
        if mode_name == 'CTR': mode = modes.CTR(iv)
        elif mode_name == 'CBC': mode = modes.CBC(iv)
        elif mode_name == 'CFB': mode = modes.CFB(iv)
        elif mode_name == 'OFB': mode = modes.OFB(iv)
        else: raise ValueError(f"Nieobsługiwany tryb: {mode_name}")

    timer_start = time.perf_counter()

    cipher = Cipher(algorithms.AES(key), mode)
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(actual_ciphertext) + decryptor.finalize()

    timer_end = time.perf_counter()
    
    if mode_name in ['CBC', 'ECB']:
        unpadder = padding.PKCS7(128).unpadder()
        final_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    else:
        final_data = decrypted_padded_data

    if output_filepath:
        with open(output_filepath, 'wb') as file:
            file.write(final_data)

    return timer_end - timer_start, final_data


def generate_file_of_size(filepath: str, size_in_bytes: int):
    
    with open(filepath, 'wb') as file:
        file.write(os.urandom(size_in_bytes))

def flip_random_bits_in_middle(encrypted_data: bytes, num_bits: int = 1) -> bytes:
        
        if not encrypted_data:
            raise ValueError("Encrypted data must not be empty")
        
        middle_index = len(encrypted_data) // 2

        flipped_bytes = bytearray(encrypted_data)

        for i in range(num_bits):
            original_byte = encrypted_data[middle_index + i]
            bit_to_flip = 1 << (os.urandom(1)[0] % 8)
            flipped_byte = original_byte ^ bit_to_flip
            flipped_bytes[middle_index + i] = flipped_byte

        return bytes(flipped_bytes)

def manual_cbc_encrypt(plaintext, key, iv):

    #Preparing the cipher for AES encryption in ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    
    block_size = 16
    ciphertext = b""
    previous_block = iv 

    #Iterating through the plaintext in blocks
    for i in range(0, len(plaintext), block_size):
        current_block = plaintext[i:i + block_size]
        
        #XORing the current plaintext block with the previous ciphertext block (or IV for the first block).
        mixed_block = bytes(a ^ b for a, b in zip(current_block, previous_block))
    
        encrypted_block = encryptor.update(mixed_block)
        ciphertext += encrypted_block
    
        #Updating the previous block to be the current encrypted block for the next iteration.
        previous_block = encrypted_block
        
    return ciphertext

