import random
def powerMod(a, b, n):
    if b == 0:
        # if b is 0, then a^b (mod n)= 1
        return 1
    if b % 2 == 0:
        # if b is even, return (a^2)^(b/2) (mod n)
        return powerMod((a*a) % n, b//2, n)
    # if b is odd, return (a*((a^(b - 1)) mod n)) (mod n)
    return (a*powerMod(a, b - 1, n)) % n

for _ in range(100):
    a = random.randint(0, 100)
    b = random.randint(0, 100)
    n = random.randint(1, 100)
    assert(powerMod(a, b, n) == pow(a, b, n))
    