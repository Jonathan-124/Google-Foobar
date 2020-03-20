import math, fractions


class Vector:
    # Initialize with list of two ints
    # Has 3 attributes: x-coordinate, y-coordinate, and gcd of x and y
    def __init__(self, v):
        self.x = v[0]
        self.y = v[1]
        self.gcd = math.gcd(v[0], v[1])

    def vector(self):
        return [self.x, self.y]

    # Returns tuple direction vector in simplest reduced integer form
    def reduced_direction(self):
        if self.gcd == 0:
            return 0, 0
        else:
            return self.x / self.gcd, self.y / self.gcd

    # Returns magnitude of vector
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


def vector_addition(v1, v2):
  # Takes two vectors, returns their sum as a Vector object
    vx_new = v1.x + v2.x
    vy_new = v1.y + v2.y
    return Vector([vx_new, vy_new])


class ClosestVectorDict(dict):
    # Key - reduced_direction of the Vector class, i.e. a 2-tuple of ints
    # Value - magnitude of vector instance
    # closest_update keeps shortest magnitude if two keys are same (i.e. two vectors have the same reduced_direction)
    def closest_update(self, key, value):
        if key not in self:
            self[key] = value
        elif self[key] > value:
            self[key] = value
        else:
            pass


def solution(dimensions, your_position, guard_position, distance):
    # direct - direction vector from your_pos to guard_pos
    direct = Vector([guard_position[0] - your_position[0], guard_position[1] - your_position[1]])

    if direct.magnitude() > distance:
        return 0
    else:
        # Reflections - list of 4 integers
        # Entries are reflection distances from left wall, right wall, top wall, and bottom wall
        my_reflections = [2 * your_position[0],
                          2 * (dimensions[0] - your_position[0]),
                          2 * (dimensions[1] - your_position[1]),
                          2 * your_position[1]]
        guard_reflections = [2 * guard_position[0],
                             2 * (dimensions[0] - guard_position[0]),
                             2 * (dimensions[1] - guard_position[1]),
                             2 * guard_position[1]]

        # Dicts of vectors that hit me/guard using 2-tuple vectors as keys and their magnitude as values
        # Keys are reduced_direction tuples of a direction vector
        # If two vectors have the same direction, the dict only keeps the one with shorter magnitude
        # i.e. only keep the shorter vector that hits if two vectors in the same direction
        my_dict = ClosestVectorDict()
        guard_dict = ClosestVectorDict()

        # Dictionary of lambda functions
        # Takes two inputs: ref_list (list) of me/guard and n (int)
        # Returns distance to self after n reflections starting from the left, right, top, and bottom walls
        function_dict = {
            0: (lambda ref_list, n: -(n / 2) * (ref_list[0] + ref_list[1]) if n % 2 == 0 else -(n // 2) * (
                        ref_list[0] + ref_list[1]) - ref_list[0]),
            1: (lambda ref_list, n: (n / 2) * (ref_list[0] + ref_list[1]) if n % 2 == 0 else (n // 2) * (
                        ref_list[0] + ref_list[1]) + ref_list[1]),
            2: (lambda ref_list, n: (n / 2) * (ref_list[2] + ref_list[3]) if n % 2 == 0 else (n // 2) * (
                        ref_list[2] + ref_list[3]) + ref_list[2]),
            3: (lambda ref_list, n: -(n / 2) * (ref_list[2] + ref_list[3]) if n % 2 == 0 else -(n // 2) * (
                        ref_list[2] + ref_list[3]) - ref_list[3]),
        }

        # List of four shooting direction quadrants
        # [left-top, left-bottom, right-top, right-bottom]
        four_directions = [[0, 2], [0, 3], [1, 2], [1, 3]]

        # Populates guard_dict with vectors of shots that hit the guard within range
        for i in four_directions:
            # j, k are num of reflections off the left/right and top/bottom walls respectively
            j, k = 0, 0
            leftright_func = function_dict[i[0]]
            updown_func = function_dict[i[1]]

            # initialize x and y distances of guard to guard-reflection
            guard_leftright_dist = 0
            guard_updown_dist = 0

            # initialize shot vector from me to guard
            guard_vector = direct
            guard_dist = guard_vector.magnitude()

            while guard_dist <= distance:
                while guard_dist <= distance:
                    # Start inner while loop if guard within range after j left/right bounces and k top/bottom bounces
                    # Updates guard_dict with vector of shot within range
                    # Repopulate distance and vector variables after k+= 1, one more bounce in the top/bottom direction
                    guard_dict.closest_update(guard_vector.reduced_direction(), guard_vector.magnitude())
                    k += 1
                    guard_updown_dist = updown_func(guard_reflections, k)
                    guard_vector = vector_addition(direct, Vector([guard_leftright_dist, guard_updown_dist]))
                    guard_dist = guard_vector.magnitude()
                # Exit inner while loop if guard out of range after j left/right bounces and k top/bottom bounces
                # Reset top/bottom bounces to 0, add one more bounce in the left/right direction
                # Repopulate distance and vector variables, update guard_dict
                j += 1
                k = 0
                guard_leftright_dist = leftright_func(guard_reflections, j)
                guard_updown_dist = 0
                guard_vector = vector_addition(direct, Vector([guard_leftright_dist, guard_updown_dist]))
                guard_dist = guard_vector.magnitude()
                # Restart outer while loop if guard_dist at j left/right bounces and 0 top/bottom bounces is within range

        # Populates my_dict with vectors of shots that hit the me within range
        # Same concept as loop for guard above
        for i in four_directions:
            j, k = 0, 0
            leftright_func = function_dict[i[0]]
            updown_func = function_dict[i[1]]

            my_leftright_dist = 0
            my_updown_dist = 0

            my_vector = Vector([0, 0])
            my_dist = my_vector.magnitude()

            while my_dist <= distance:
                while my_dist <= distance:
                    my_dict.closest_update(my_vector.reduced_direction(), my_vector.magnitude())
                    k += 1
                    my_updown_dist = updown_func(my_reflections, k)
                    my_vector = Vector([my_leftright_dist, my_updown_dist])
                    my_dist = my_vector.magnitude()
                j += 1
                k = 0
                my_leftright_dist = leftright_func(my_reflections, j)
                my_updown_dist = 0
                my_vector = Vector([my_leftright_dist, my_updown_dist])
                my_dist = my_vector.magnitude()

        # Create new dict by filtering guard_dict with reduced_direction tuple as key and magnitude as value
        # Only keep k:v pairs where either the shot only hits guard and not me, or if the shot hits the guard first
        shots = {k: v for (k, v) in guard_dict.items() if k not in my_dict or v < my_dict[k]}

        # The length of the shots dict is the number of ways to hit the guard
        return len(shots)
    
