import math


def solution(n):
    def max_steps(z):
        # Finds maximum number of steps that can be constructed with z bricks
        root = (math.sqrt(1 + (8 * z)) - 1) / 2
        return int(math.floor(root))

    def base_steps(z):
        # Finds the arithmetic sum from 1 to z inclusive
        return (z * (z + 1)) / 2

    def partition(z, k):
        # Ways of partitioning a positive integer z into exactly k parts
        if k > z:
            return 0
        elif k == z:
            return 1
        elif k == 0:
            return 0
        elif k == 1:
            return 1
        elif k == 2:
            return int(math.floor(z / 2))
        elif k == 3:
            return int(round((z ** 2) / float(12)))
        else:
            return partition(z - k, k) + partition(z - 1, k - 1)

    x = 0
    # x is the total number of combinations

    for i in range(2, max_steps(n) + 1):
        # Loop for number of steps in [2, max_steps]
        free_bricks = n - base_steps(i)
        if free_bricks == 0:
            # Accounts for no free bricks remaining
            x += 1
            break
        else:
            for j in range(1, i + 1):
                x += partition(free_bricks, j)
                # Number of ways of distributing free_bricks
    return x
    
