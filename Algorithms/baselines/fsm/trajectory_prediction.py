import numpy as np

def init(t1):
    t0 = 0
    theta0 = 0.1 # vehicle orientation
    theta_T_0 = 0 # assume the lane has no curvature.
    gamma0 = 0 # assume the lane has  no curvature.
    a0 = 1 # initial acceleration
    v0 = 15 # initial velocity
    y0 = 3.6 # assume the next lane is 3.6 meters far

    d0 = 0 # assume it start from the lanecenter.
    d0_dot = v0 * np.sin(theta0 - theta_T_0)
    d0_ddot = np.sqrt(a0 ** 2 + gamma0 * v0 ** 2) * np.sin(theta0 - theta_T_0)
    s0 = 0
    s0_dot = v0 * np.cos(theta0 - theta_T_0)
    s0_ddot = np.sqrt(a0 ** 2 + gamma0 * v0 ** 2) * np.cos(theta0 - theta_T_0)

    d1 = y0 # assume it ends at target lane center
    d1_dot = 0
    d1_ddot = 0
    s1 = None # s1 is unknown
    s1_dot = v0 + a0 * t1
    s1_ddot = np.sqrt(a0 ** 2 + gamma0 * v0 ** 2) * np.cos(theta0 - theta_T_0)
    init = [d0, d0_dot, d0_ddot, s0, s0_dot, s0_ddot]
    final = [d1, d1_dot, d1_ddot, s1_dot, s1_ddot]
    return init, final

def predict(init, final):
    i

    coeffs = [[t0 ** 5, t0 ** 4, t0 ** 3, t0 ** 2, t0 ** 1, 1],
              [t1 ** 5, t1 ** 4, t1 ** 3, t1 ** 2, t1 ** 1, 1],
               ]
    long_params =
if __name__ == '__main__':

    t1 = np.arange(1, 7, 0.2)  # time of the maneuver