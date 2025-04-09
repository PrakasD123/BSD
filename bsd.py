import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Beam Analysis: Shear, Moment, Deflection & Rotation")

# User Inputs
st.header("User Inputs")

P1 = st.number_input("Enter load P1 (lb):", value=100.0)
P2 = st.number_input("Enter load P2 (lb):", value=150.0)
P3 = st.number_input("Enter load P3 (lb):", value=200.0)

a = st.number_input("Enter distance a (in) for load P1:", value=10.0)
b = st.number_input("Enter distance b (in) for load P2:", value=20.0)
c = st.number_input("Enter distance c (in) for load P3:", value=30.0)

L = st.number_input("Enter span L (in):", value=40.0)

X = st.number_input("Enter point X (in) where deflection and rotation are to be calculated:", value=25.0)

E = st.number_input("Enter modulus of elasticity E (psi):", value=29000000.0)
I = st.number_input("Enter moment of inertia I (in^4):", value=100.0)

if st.button("Run Analysis"):

    # Reaction Forces
    Rb = (P1 * a + P2 * b + P3 * c) / L
    Ra = (P1 + P2 + P3) - Rb

    # Shear Force and Bending Moment
    dx = L / 10000.0
    x = np.arange(0, L + dx, dx)
    M = np.zeros_like(x)
    V = np.zeros_like(x)

    for i, xi in enumerate(x):
        if xi <= a:
            M[i] = Ra * xi
            V[i] = Ra
        elif xi <= b:
            M[i] = Ra * xi - P1 * (xi - a)
            V[i] = Ra - P1
        elif xi <= c:
            M[i] = Ra * xi - P1 * (xi - a) - P2 * (xi - b)
            V[i] = Ra - P1 - P2
        else:
            M[i] = Ra * xi - P1 * (xi - a) - P2 * (xi - b) - P3 * (xi - c)
            V[i] = Ra - P1 - P2 - P3

    # Plot Diagrams
    st.subheader("Shear Force and Bending Moment Diagrams")
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    ax[0].plot(x, M, linewidth=2)
    ax[0].grid(True)
    ax[0].set_title("Bending Moment Diagram")
    ax[0].set_xlabel("Distance from Left Support [in]")
    ax[0].set_ylabel("Bending Moment [lb-in]")

    ax[1].plot(x, V, 'r', linewidth=2)
    ax[1].grid(True)
    ax[1].set_title("Shear Force Diagram")
    ax[1].set_xlabel("Distance from Left Support [in]")
    ax[1].set_ylabel("Shear Force [lb]")

    st.pyplot(fig)

    # Virtual Work for Deflection and Rotation
    m_t = np.zeros_like(x)
    m_t_deriv = np.zeros_like(x)
    for i, xi in enumerate(x):
        if xi <= X:
            m_t[i] = xi * (L - X) / L
            m_t_deriv[i] = (L - X) / L
        else:
            m_t[i] = X * (L - xi) / L
            m_t_deriv[i] = -X / L

    delta = np.trapz(M * m_t, x) / (E * I)
    theta = np.trapz(M * m_t_deriv, x) / (E * I)

    # Display Results
    st.subheader(f"Results at x = {X:.2f} in")
    st.write(f"**Deflection, Δ = {delta:.6e} in**")
    st.write(f"**Rotation, θ  = {theta:.6e} rad**")
