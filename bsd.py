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

# Function to compute Virtual Bending Moment (for deflection and rotation)
def calculate_virtual_bending_moment(x, X, L):
    m_virtual = np.zeros_like(x)
    for j in range(len(x)):
        if x[j] < X:
            m_virtual[j] = x[j] * (L - X) / L
        else:
            m_virtual[j] = (L - x[j]) * X / L
    return m_virtual

# Function to compute deflection along the beam
def calculate_deflection(x, E, I, mb, m_virtual):
    # Initialize deflection array
    deflection = np.zeros_like(x)
    
    # Perform the integration for each point
    for i in range(1, len(x)):
        # Integrating from the start to the current position x[i]
        deflection[i] = np.trapz(mb[:i+1] * m_virtual[:i+1] / (E * I), x[:i+1])

    return deflection

# Function to compute rotation along the beam
def calculate_rotation(x, E, I, mb, m_virtual):
    # Initialize rotation array
    rotation = np.zeros_like(x)
    
    # Perform the integration for each point
    for i in range(1, len(x)):
        # Integrating from the start to the current position x[i]
        rotation[i] = np.trapz(mb[:i+1] * m_virtual[:i+1] / (E * I), x[:i+1])

    return rotation

# Streamlit Interface
st.title('Shear, Bending Moment, Deflection, and Rotation for a Simply Supported Beam')

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
m_virtual = calculate_virtual_bending_moment(x, X, L)

# Compute Deflection along the Beam
deflection = calculate_deflection(x, E, I, mb, m_virtual)

# Compute Rotation along the Beam
rotation = calculate_rotation(x, E, I, mb, m_virtual)

# Deflection and Rotation at X
deflection_at_X = deflection[int(X / dx)]
rotation_at_X = rotation[int(X / dx)]

# Plotting Moment Diagram, Shear Force Diagram, and Deflection Diagram
fig, ax = plt.subplots(4, 1, figsize=(10, 15))

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

# Deflection Diagram
ax[2].plot(x, deflection, label='Deflection', linewidth=2)
ax[2].grid(True)
ax[2].set_title('Deflection Diagram')
ax[2].set_ylabel('Deflection [in]')
ax[2].set_xlabel('Distance from Left Support [in]')

# Rotation Diagram
ax[3].plot(x, rotation, label='Rotation', linewidth=2)
ax[3].grid(True)
ax[3].set_title('Rotation Diagram')
ax[3].set_ylabel('Rotation [radians]')
ax[3].set_xlabel('Distance from Left Support [in]')

plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)

# Display Deflection and Rotation at X
st.write(f"Deflection at X = {X} inches: {deflection_at_X:.6f} inches")
st.write(f"Rotation at X = {X} inches: {rotation_at_X:.6f} radians")
