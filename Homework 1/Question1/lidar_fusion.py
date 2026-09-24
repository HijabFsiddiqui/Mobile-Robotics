import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

A = pd.read_csv("scan_posA.csv")
B = pd.read_csv("scan_posB.csv")


T_AB = np.array([
    [-1,  0, 0.0],
    [ 0, -1, 1.4],
    [ 0,  0, 1.0]
])



B_xy = B[["x", "y"]].values
ones = np.ones((B_xy.shape[0], 1))
B_homogeneous = np.hstack((B_xy, ones))


B_transformed = (T_AB @ B_homogeneous.T).T


B_transformed_x = B_transformed[:, 0]
B_transformed_y = B_transformed[:, 1]

plt.scatter(A["x"], A["y"], label="Scan A")

plt.scatter(
    B_transformed_x,
    B_transformed_y,
    label="Scan B transformed"
)

plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.axis("equal")
plt.legend()
plt.grid()

plt.savefig("fused_lidar.png", dpi=150)
