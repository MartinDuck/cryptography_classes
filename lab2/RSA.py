import random

primes = [p for p in range(1000, 9999) if all(p % i != 0 for i in range(2, int(p**0.5) + 1))]
p = random.choice(primes)
q = random.choice(primes)
while q == p:
    q = random.choice(primes)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    d, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y


n = p * q
phi = (p - 1) * (q - 1)

e = 65537
if gcd(e, phi) != 1:
    e = 3
    while gcd(e, phi) != 1:
        e += 2

d = extended_gcd(e, phi)[1]
d = d % phi

public_key = (e, n)
private_key = (d, n)

original_message = "Kocham kryptografie! RSA Jest super fajny i bezpieczny!"
print(f"Liczby pierwsze: p={p}, q={q}")
print(f"Klucz Publiczny: {public_key}")
print(f"Klucz Prywatny: ({d}, {n})\n")
print(f"Oryginalna wiadomosc ({len(original_message)} znakow):\n'{original_message}'\n")

encrypted_msg = [pow(ord(char), e, n) for char in original_message]
print(f"Zaszyfrowane dane (pierwsze 5 jednostek): {encrypted_msg[:5]}...")

decrypted_chars = [chr(pow(char, d, n)) for char in encrypted_msg]
decrypted_message = "".join(decrypted_chars)

print(f"\nOdszyfrowana wiadomosc:\n'{decrypted_message}'")
print(f"\nCzy wiadomosci sa identyczne? {'TAK' if original_message == decrypted_message else 'NIE'}")