import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("Beam Deflection and Rotation using Virtual Work")

#
# User Inputs
#
st.sidebar.header("User Inputs")

# Loads in pounds
P1 = st.sidebar.number_input("Enter load P1 (lb):", value=100.0)
P2 = st.sidebar.number_input("Enter load P2 (lb):", value=150.0)
P3 = st.sidebar.number_input("Enter load P3 (lb):", value=200.0)

# Distances (in inches)
a = st.sidebar.number_input("Enter distance a (in) for load P1:", value=10.0)
b = st.sidebar.number_input("Enter distance b (in) for load P2:", value=20.0)
c = st.sidebar.number_input("Enter distance c (in) for load P3:", value=30.0)

# Beam span in inches
L = st.sidebar.number_input("Enter span L (in):", value=40.0)

# Point for deflection/rotation
X = st.sidebar.number_input("Enter point X (in):", value=25.0)

# Material properties
E = st.sidebar.number_input("Enter modulus of elasticity E (psi):", value=30000000.0)
I = st.sidebar.number_input("Enter moment of inertia I (in^4):", value=100.0)

