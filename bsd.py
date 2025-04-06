666import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit interface
st.title("Beam Analysis Calculator")
st.write("Enter the parameters for beam analysis below:")

# Input fields in Streamlit
P1 = st.number_input("Load at point a (lbs)", value=5.0)
P2 = st.number_input("Load at point b (lbs)", value=10.0)
P3 = st.number_input("Load at point c (lbs)", value=15.0)
a = st.number_input("Position of P1 (inches)", value=5.0)
b = st.number_input("Position of P2 (inches)", value=10.0)
c = st.number_input("Position of P3 (inches)", value=15.0)
L = st.number_input("Length of beam (inches)", value=20.0)
X = st.number_input("Point for rotation calculation (inches)", value=17.0)
E = st.number_input("Modulus of elasticity (psi)", value=29000000.0)
I = st.number_input("Moment of inertia (in^4)", value=0.55)

if st.button("Calculate and Plot"):
    # Original code starts here - unchanged
    # Calculate Reaction Forces
    Rb = (P1 * a + P2 * b + P3 * c) / L
    Ra = P1 + P2 + P3 - Rb

    # Discretize Beam (Fine enough for integration)
    dx = L / 1000
    x = np.arange(0, L + dx, dx)

    # Calculate Shear Force and Bending Moment
    def calculate_shear(x, Ra, P1, a, P2, b, P3, c, L):
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

    # Shear Force and Bending Moment calculations
    vb = calculate_shear(x, Ra, P1, a, P2, b, P3, c, L)
    mb = calculate_bending_moment(x, Ra, P1, a, P2, b, P3, c, L)

    # Plotting the Shear and Moment Diagrams
    plt.figure(figsize=(12, 8))

    # Plot Moment Diagram
    plt.subplot(2, 1, 1)
    plt.plot(x, mb, label='Bending Moment', linewidth=2)
    plt.grid(True)
    plt.title('Bending Moment Diagram')
    plt.ylabel('Moment [lb·in]')
    plt.xlabel('Distance from Left Support [in]')

    # Plot Shear Diagram
    plt.subplot(2, 1, 2)
    plt.plot(x, vb, 'r', label='Shear Force', linewidth=2)
    plt.grid(True)
    plt.title('Shear Force Diagram')
    plt.ylabel('Shear [lb]')
    plt.xlabel('Distance from Left Support [in]')

    plt.tight_layout()
    # Original code ends here

    # Display the plot in Streamlit
    st.pyplot(plt)

    # Display reaction forces
    st.write(f"Reaction force at A (Ra): {Ra:.2f} lbs")
    st.write(f"Reaction force at B (Rb): {Rb:.2f} lbs")
