import random

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

n = random.choice([p for p in range(1000, 2000) if is_prime(p)]) 
g = random.randint(2, n-1)


print(f"Parametry Publiczne")
print(f"Liczba pierwsza (n): {n}")
print(f"Pierwiastek pierwotny (g): {g}\n")

x = random.randint(100, 900)  
X = pow(g, x, n)              

y = random.randint(100, 900) 
Y = pow(g, y, n)              

print(f"Klucze Prywatne")
print(f"Osoba A (x): {x}")
print(f"Osoba B (y): {y}\n")

print(f"Wymiana Publiczna")
print(f"A wysyla do B: {X}")
print(f"B wysyla do A: {Y}\n")

k_A = pow(Y, x, n)

k_B = pow(X, y, n)

print(f" Wynik ")
print(f"Klucz sesji obliczony przez A: {k_A}")
print(f"Klucz sesji obliczony przez B: {k_B}")

if k_A == k_B:
    print("\nSUKCES: Klucze sa identyczne")
else:
    print("\nlŁAD: Klucze się roznia")