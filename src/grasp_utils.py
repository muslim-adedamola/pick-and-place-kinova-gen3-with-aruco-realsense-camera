import numpy as np

def compute_approach_and_grasp(T_base_O,
                               approach_offset,
                               grasp_offset, lift_offset):
    """
    Returns:
      T_base_A : approach pose
      T_base_G : grasp pose
      T_base_L : lift pose
    """

    T_base_G = T_base_O.copy()

    # Move DOWN to grasp surface
    T_base_G[2, 3] -= grasp_offset

    T_base_A = T_base_G.copy()
    T_base_A[0, 3] += approach_offset

    T_base_L = T_base_A.copy()
    T_base_L[2, 3] += lift_offset

    return T_base_A, T_base_G, T_base_L
