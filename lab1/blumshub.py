import secrets
import math


def get_seed(n: int) -> int:
    """Generuje ziarno, które jest względnie pierwsze z n."""
    if n <= 1000:
        return 
    while True:
        seed = secrets.randbelow(n - 1000) + 1000
        if math.gcd(seed, n) == 1:
            return seed

class BlumBlumShub:
    def __init__(self, p: int, q: int, seed: int = None):

        self.n = p * q

        if seed is None:
            seed = get_seed(self.n)

        self.state = pow(seed, 2, self.n)

    def next_bit(self) -> int:
        """Generuje pojedynczy bit."""
        self.state = pow(self.state, 2, self.n)
        return self.state % 2

    def generate_bits(self, length: int) -> list:
        """Generuje listę bitów o określonej długości."""
        return [self.next_bit() for _ in range(length)]

    def generate_int(self, bit_length: int) -> int:
        """Generuje liczbę całkowitą o zadanej długości bitowej."""
        result = 0
        for _ in range(bit_length):
            result = (result << 1) | self.next_bit()
        return result


