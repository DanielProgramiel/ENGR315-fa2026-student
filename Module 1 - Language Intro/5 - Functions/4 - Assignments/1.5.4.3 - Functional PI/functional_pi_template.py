import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###
    a = 1
    b = 1/math.sqrt(2)
    t = 1/4
    p = 1
    a_new = (a + b)/2
    pi_estimate = 0
    while abs(pi_estimate - math.pi) > target_error:
        a_new = (a + b)/2
        b_new = math.sqrt(a*b)
        t_new = t - p*(a_new - a)**2
        p_new = 2*p
        a = a_new
        b = b_new
        t = t_new
        p = p_new
        pi_estimate = (a + b)**2/(4*t)
    # change this so an actual value is returned
    return pi_estimate




desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
