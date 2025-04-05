import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to compute Reaction Forces
def compute_reactions(P1, P2, P3, a, b, c, L):
    Rb = (P1 * a + P2 * b + P3 * c) / L
    Ra = P1 + P2 + P3 - Rb
    return Ra, Rb

# Function to calculate Shear Force
def calculate_shear_force(x, Ra, P1, a, P2, b, P3, c, L):
    vb = np.zeros_like(x)
    for j in range(len(x)):
        if x[j] <= a:
            vb[j] = Ra
        elif x[j] <= b:
            vb[j] = Ra - P1
        elif x[j] <= c:
            vb[j] = Ra - P1 - P2
        else:
            vb[j] = Ra - P1 - P2 - P3
    return vb

# Function to calculate Bending Moment
def calculate_bending_moment(x, Ra, P1, a, P2, b, P3, c, L):
    mb = np.zeros_like(x)
    for j in range(len(x)):
        if x[j] <= a:
            mb[j] = Ra * x[j]
        elif x[j] <= b:
            mb[j] = Ra * x[j] - P1 * (x[j] - a)
        elif x[j] <= c:
            mb[j] = Ra * x[j] - P1 * (x[j] - a) - P2 * (x[j] - b)
        else:
            mb[j] = Ra * x[j] - P1 * (x[j] - a) - P2 * (x[j] - b) - P3 * (x[j] - c)
    return mb

# Function to compute Virtual Bending Moment for Deflection and Rotation
def calculate_virtual_bending_moment(x, X, L):
    bm = np.zeros_like(x)
    for j in range(len(x)):
        if x[j] < X:
            bm[j] = x[j] * (L - X) / L
        else:
            bm[j] = X - (X / L) * x[j]
    return bm

# Function to compute virtual work for each load P1, P2, P3
def calculate_virtual_work(x, a, b, c, P1, P2, P3, L):
    m1 = np.zeros_like(x)
    m2 = np.zeros_like(x)
    m3 = np.zeros_like(x)
    
    # Virtual Work due to P1
    for j in range(len(x)):
        if x[j] < a:
            m1[j] = x[j] * ((P1 - (P1 * a)) / L)
        else:
            m1[j] = a - x[j] * (P1 * a) / L
    
    # Virtual Work due to P2
    for j in range(len(x)):
        if x[j] < b:
            m2[j] = x[j] * ((P2 - (P2 * b)) / L)
        else:
            m2[j] = b - x[j] * (P2 * b) / L

    # Virtual Work due to P3
    for j in range(len(x)):
        if x[j] < c:
            m3[j] = x[j] * ((P3 - (P3 * c)) / L)
        else:
            m3[j] = c - x[j] * (P3 * c) / L
            
    return m1, m2, m3

# Function to compute Deflection along the Beam
def calculate_deflection(x, E, I, bm, m1, m2, m3):
    delta = np.zeros_like(x)
    # Deflection Computation using Virtual Work (EI is constant)
    for i in range(1, len(x)):
        delta[i] = np.trapz(bm[:i+1] * m1[:i+1] / (E * I), x[:i+1]) + np.trapz(bm[:i+1] * m2[:i+1] / (E * I), x[:i+1]) + np.trapz(bm[:i+1] * m3[:i+1] / (E * I), x[:i+1])
    return delta

# Function to compute Rotation along the Beam
def calculate_rotation(x, E, I, bm, m1, m2, m3):
    theta = np.zeros_like(x)
    # Rotation Computation using Virtual Work (EI is constant)
    for i in range(1, len(x)):
        theta[i] = np.trapz(bm[:i+1] * m1[:i+1] / (E * I), x[:i+1]) + np.trapz(bm[:i+1] * m2[:i+1] / (E * I), x[:i+1]) + np.trapz(bm[:i+1] * m3[:i+1] / (E * I), x[:i+1])
    return theta

# Streamlit Interface
st.title('Shear, Bending Moment, Deflection for a Simply Supported Beam')

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

# Compute Reaction Forces
Ra, Rb = compute_reactions(P1, P2, P3, a, b, c, L)

# Discretize Beam
dx = L / 1000
x = np.arange(0, L + dx, dx)

# Calculate Shear Force and Bending Moment
vb = calculate_shear_force(x, Ra, P1, a, P2, b, P3, c, L)
mb = calculate_bending_moment(x, Ra, P1, a, P2, b, P3, c, L)

# Calculate Virtual Bending Moment for Deflection and Rotation
bm = calculate_virtual_bending_moment(x, X, L)

# Compute virtual work for loads P1, P2, and P3
m1, m2, m3 = calculate_virtual_work(x, a, b, c, P1, P2, P3, L)

# Compute Deflection and Rotation along the Beam
deflection = calculate_deflection(x, E, I, bm, m1, m2, m3)
rotation = calculate_rotation(x, E, I, bm, m1, m2, m3)

# Deflection and Rotation at X
deflection_at_X = deflection[int(X / dx)]
rotation_at_X = rotation[int(X / dx)]

# Plotting Moment Diagram and Shear Force Diagram
fig, ax = plt.subplots(2, 1, figsize=(10, 10))

# Moment Diagram
ax[0].plot(x, mb, label='Moment', linewidth=2)
ax[0].grid(True)
ax[0].set_title('Bending Moment Diagram')
ax[0].set_ylabel('Moment [lb·in]')
ax[0].set_xlabel('Distance from Left Support [in]')

# Shear Diagram
ax[1].plot(x, vb, 'r', label='Shear', linewidth=2)
ax[1].grid(True)
ax[1].set_title('Shear Force Diagram')
ax[1].set_ylabel('Shear [lb]')
ax[1].set_xlabel('Distance from Left Support [in]')

plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)

# Display Deflection and Rotation at X
st.write(f"Deflection at X = {X} inches: {deflection_at_X:.6f} inches")
st.write(f"Rotation at X = {X} inches: {rotation_at_X:.6f} radians")
