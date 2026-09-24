
import numpy as np
from scipy.optimize import minimize_scalar

#given
R = 5.0
omega = 0.40
T = 8.0

# taking arbitary values for a and L, since they are not given in the problem statement
L = 5.0
a = 1.0

# Robot A: position + heading 
def xA(t): return R*np.cos(omega*t)
def yA(t): return R*np.sin(omega*t)
def thA(t): return omega*t + np.pi/2

# Robot B: position 
def xB(t): return -(1/np.sqrt(2))*((L/T)*t + a*np.sin(2*np.pi*t/T))
def yB(t): return  (1/np.sqrt(2))*((L/T)*t - a*np.sin(2*np.pi*t/T))

# Robot B: velocity (derivative of position)
def xBdot(t): return -(1/np.sqrt(2))*(L/T + a*(2*np.pi/T)*np.cos(2*np.pi*t/T))
def yBdot(t): return  (1/np.sqrt(2))*(L/T - a*(2*np.pi/T)*np.cos(2*np.pi*t/T))

def D(t):
    return np.hypot(xB(t)-xA(t), yB(t)-yA(t))

Trev = 2*np.pi/omega                      # one full revolution of A
ts = np.linspace(0, Trev, 200_000)        # coarse grid search
i_min = np.argmin(D(ts))
t_coarse = ts[i_min]

# Fine search using scipy.optimize.minimize_scalar
res = minimize_scalar(D, bounds=(t_coarse-0.05, t_coarse+0.05), method='bounded')
t_star, D_star = res.x, res.fun

print(f"(i) t* = {t_star:.4f} s,  D(t*) = {D_star:.4f} m")

# (ii) velocity of B in A's frame
vBx, vBy = xBdot(t_star), yBdot(t_star)          # B's velocity in world
c, s = np.cos(thA(t_star)), np.sin(thA(t_star))
vBx_A =  c*vBx + s*vBy                            # R_A^T applied
vBy_A = -s*vBx + c*vBy

print(f"(ii) v_B in world = ({vBx:.4f}, {vBy:.4f}) m/s")
print(f"     v_B in frame A = ({vBx_A:.4f}, {vBy_A:.4f}) m/s")
print(f"     speed (frame-independent check) = {np.hypot(vBx_A,vBy_A):.4f} m/s")
