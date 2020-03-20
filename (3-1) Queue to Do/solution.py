def solution(start, length):
    # s - Current start of line (inclusive)
    # length - Length of line
    # end_of_inspection - where the current line's inspection ends (inclusive)
    s = start
    check_sum = 0
    end_of_inspection = s + length - 1

    # Returns xor of the integer series [0, n]; also works for n = -1 (returns 0)
    def get_xor_from_0(n):
        rem = n % 4
        if rem == 0:
            return n
        elif rem == 1:
            return 1
        elif rem == 2:
            return n + 1
        else:
            return 0

    while s <= end_of_inspection:
        if s > 2000000000:
            # Exit when start of line is greater than max ID
            break
        else:
            if end_of_inspection <= 2000000000:
                check_sum ^= get_xor_from_0(s - 1) ^ get_xor_from_0(end_of_inspection)
                s += length
                end_of_inspection += length - 1
            else:
                check_sum ^= get_xor_from_0(s - 1) ^ get_xor_from_0(2000000000)
                break
    return check_sum
