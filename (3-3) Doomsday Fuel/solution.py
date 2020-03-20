from fractions import Fraction
from functools import reduce
from math import gcd


def solution(m):
    # Checks if s0 is absorbant state
    if reduce(lambda a, b: a + b, m[0]) == 0:
        return [1, 1]

    # Creates an nxn identity matrix
    def create_identity_matrix(n):
        result = []
        for i in range(n):
            row = [0] * n
            row[i] = 1
            result.append(row)
        return result

    # Calculates m1 - m2
    def matrix_subtraction(m1, m2):
        rows = len(m1)
        cols = len(m1[0])
        result = []
        for i in range(rows):
            dif_row = []
            m1_row = m1[i]
            m2_row = m2[i]
            for j in range(cols):
                dif_entry = m1_row[j] - m2_row[j]
                dif_row.append(dif_entry)
            result.append(dif_row)
        return result

    # Calculates m1 * m2
    def matrix_multiplication(m1, m2):
        rows = len(m1)
        cols = len(m1[0])
        res = len(m2[0])
        result = []
        for i in range(rows):
            prod_row = []
            m1_row = m1[i]
            for j in range(res):
                prod_entry = 0
                for k in range(cols):
                    prod_entry += m1_row[k] * m2[k][j]
                prod_row.append(prod_entry)
            result.append(prod_row)
        return result

    # Inverts invertible matrix m with main diagonal entries != 0
    def matrix_inverse(m):
        original = m
        rows = len(original)
        result = create_identity_matrix(rows)

        # Row echelon
        for i in range(rows):
            base_row_original = original[i]
            base_row_result = result[i]
            coef = Fraction(base_row_original[i].denominator, base_row_original[i].numerator)
            base_row_original = list(map(lambda x: x * coef, base_row_original))
            base_row_result = list(map(lambda x: x * coef, base_row_result))
            original[i] = base_row_original
            result[i] = base_row_result
            for j in range(i + 1, rows):
                check_row_original = original[j]
                check_row_result = result[j]
                pivot = check_row_original[i]
                if pivot == 0:
                    pass
                else:
                    for k in range(rows):
                        check_row_original[k] -= pivot * base_row_original[k]
                        check_row_result[k] -= pivot * base_row_result[k]
                original[j] = check_row_original
                result[j] = check_row_result
        # Reduced row echelon
        for i in range(len(result) - 1, 0, -1):
            base_row_result = result[i]
            for j in range(i):
                coef = Fraction(original[j][i])
                check_row_result = result[j]
                for k in range(len(check_row_result)):
                    check_row_result[k] -= coef * base_row_result[k]
                result[j] = check_row_result
        return result

    # Calculates lowest common multiple from a list of integers
    def lcm(l):
        return reduce(lambda a, b: a * b // gcd(a, b), l)

    # q - list of indices of transition states
    # Q - transition matrix of transient state to transient state
    # R - transition matrix of transient state to absorbant state
    q = []
    Q = []
    R = []

    # Calculates transition matrix m, populates q
    for i in range(len(m)):
        row = m[i]
        row_sum = reduce(lambda a, b: a + b, row)
        if row_sum == 0:
            m[i][i] = Fraction(1)
        else:
            q.append(i)
            m[i] = list(map(lambda a: Fraction(a, row_sum), row))

    # Populates Q and R
    for i in q:
        row = m[i]
        Q_row = []
        R_row = []
        for j in range(len(row)):
            if j in q:
                Q_row.append(row[j])
            else:
                R_row.append(row[j])
        Q.append(Q_row)
        R.append(R_row)

    # N - matrix of expected values
    # B - (i, j) entry is the probability of reaching absorbing state j starting at state i
    N = matrix_inverse(matrix_subtraction(create_identity_matrix(len(q)), Q))
    B = matrix_multiplication(N, R)

    # Finding lcm of the denominators of B[0]
    denom_list = list(map(lambda a: a.denominator, B[0]))
    denominator = lcm(denom_list)

    # ans is factored B[0] fractions with denominator appended
    ans = list(map(lambda a: a.numerator * denominator // a.denominator, B[0]))
    ans.append(denominator)
    return ans
