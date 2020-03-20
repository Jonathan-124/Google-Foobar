import fractions


def solution(pegs):
    # Determines if n is even or odd
    def even(n):
        if (n % 2) == 0:
            return True
        else:
            return False

    i, j, r = 0, 0, 0
    radii_sums = []
    radii = []

    # Creates radii_sums list by calculating the distance between two pegs
    # This is the sum of the radii between two pegs
    while i < len(pegs) - 1:
        radii_sums.append(pegs[i+1] - pegs[i])
        i += 1

    # An nxn matrix, n is the number of equations we have and also the number of radii variables
    # Row Echelon of matrix
    while j < len(radii_sums):
        if even(j):
            r -= radii_sums[j]
            j += 1
        else:
            r += radii_sums[j]
            j += 1

    # Calculates the radius of the last peg, last operation depends on if n is odd or even, adds it to radii list
    if even(j):
        r = fractions.Fraction(r, -1)
        radii.append(r)
    else:
        r = fractions.Fraction(r, -3)
        radii.append(r)

    # Calculates r_n-1, r_n-2,..., r_1, adds each result to the end of radii list
    while radii_sums:
        r = radii_sums.pop() - r
        if r < 1:
            return [-1, -1]
        else:
            radii.append(r)

    return [radii[-1].numerator, radii[-1].denominator]
