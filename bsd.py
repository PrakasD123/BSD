import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Compute Reaction Forces
def compute_reactions(P1, P2, P3, a, b, c, L):
    Rb = (P1 * a + P2 * b + P3 * c) / L
    Ra = P1 + P2 + P3 - Rb
    return Ra, Rb

# Compute Shear Force and Bending Moment
def calculate_shear(x, Ra, P1, a, P2, b, P3, c, L):
    shear = []
    for i in range(len(x)):
        if x[i] <= a:
            shear.append(Ra)
        elif x[i] <= b:
            shear.append(Ra - P1)
        elif x[i] <= c:
            shear.append(Ra - P1 - P2)
        else:
            shear.append(Ra - P1 - P2 - P3)
    return np.array(shear)

def calculate_moment(x, Ra, P1, a, P2, b, P3, c, L):
    moment = []
    for i in range(len(x)):
        if x[i] <= a:
            moment.append(Ra * x[i])
        elif x[i] <= b:
            moment.append(Ra * x[i] - P1 * (x[i] - a))
        elif x[i] <= c:
            moment.append(Ra * x[i] - P1 * (x[i] - a) - P2 * (x[i] - b))
        else:
            moment.append(Ra * x[i] - P1 * (x[i] - a) - P2 * (x[i] - b) - P3 * (x[i] - c))
    return np.array(moment)

# Deflection and Rotation Calculation using Virtual Work
def calculate_deflection_rotation(x, E, I, Ra, P1, a, P2, b, P3, c, L, X):
    deflection = np.zeros(len(x))
    rotation = np.zeros(len(x))

    # Deflection due to applied loads
    for i in range(len(x)):
        if x[i] <= X:
            # Contribution to deflection due to forces
            deflection[i] = (Ra * x[i]**2 / (6 * E * I)) - (P1 * (x[i] - a)**2 / (2 * E * I)) if x[i] > a else 0
            deflection[i] += (P2 * (x[i] - b)**2 / (2 * E * I)) if x[i] > b else 0
            deflection[i] += (P3 * (x[i] - c)**2 / (2 * E * I)) if x[i] > c else 0
        else:
            # Contribution to deflection beyond X
            deflection[i] = 0  # This can be adjusted as per real deflection calc

    # Rotation (slope) calculation at X
    for i in range(len(x)):
        if x[i] <= X:
            rotation[i] = (Ra * x[i] / (2 * E * I)) - (P1 * (x[i] - a) / (E * I)) if x[i] > a else 0
            rotation[i] += (P2 * (x[i] - b) / (E * I)) if x[i] > b else 0
            rotation[i] += (P3 * (x[i] - c) / (E * I)) if x[i] > c else 0
        else:
            # Rotation after X can be adjusted similarly
            rotation[i] = 0

    return deflection, rotation

# Streamlit Interface
st.title('Shear, Bending Moment, Deflection for Simply Supported Beam')

# User Inputs
P1 = st.number_input('P1 (lbs)', value=100.0)
P2 = st.number_input('P2 (lbs)', value=100.0)
P3 = st.number_input('P3 (lbs)', value=100.0)
a = st.number_input('a (in)', value=3.0)
b = st.number_input('b (in)', value=4.0)
c = st.number_input('c (in)', value=5.0)
L = st.number_input('L (span in inches)', value=10.0)
X = st.number_input('X (location of interest in inches)', value=5.0)
E = st.number_input('E (modulus of elasticity in psi)', value=29000000.0)
I = st.number_input('I (moment of inertia in in^4)', value=100.0)

# Reaction Forces and Beam Discretization
Ra, Rb = compute_reactions(P1, P2, P3, a, b, c, L)
dx = L / 1000
x = np.arange(0, L + dx, dx)

# Calculate Shear, Bending Moment, Deflection, and Rotation
shear = calculate_shear(x, Ra, P1, a, P2, b, P3, c, L)
moment = calculate_moment(x, Ra, P1, a, P2, b, P3, c, L)
deflection, rotation = calculate_deflection_rotation(x, E, I, Ra, P1, a, P2, b, P3, c, L, X)

# Plot Shear and Bending Moment
fig, ax = plt.subplots(2, 1, figsize=(10, 6))
ax[0].plot(x, moment, label='Moment', linewidth=2)
ax[0].grid(True)
ax[0].set_title('Bending Moment Diagram')
ax[0].set_ylabel('Moment [lb·in]')
ax[0].set_xlabel('Distance [in]')

ax[1].plot(x, shear, 'r', label='Shear', linewidth=2)
ax[1].grid(True)
ax[1].set_title('Shear Force Diagram')
ax[1].set_ylabel('Shear [lb]')
ax[1].set_xlabel('Distance [in]')
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)

# Display Deflection and Rotation at X
st.write(f"Deflection at X = {X} inches: {deflection[int(X/dx)]:.6f} inches")
st.write(f"Rotation at X = {X} inches: {rotation[int(X/dx)]:.6f} radians")
