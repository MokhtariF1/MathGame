from math import sqrt


def shirzad_prime(shir_number):
    if shir_number == 1:
        return False
    for i in range(2, int(sqrt(shir_number) + 1)):
        if shir_number % i == 0:
            return False
    return True
