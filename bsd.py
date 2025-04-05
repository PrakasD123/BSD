
import numpy as np\
import matplotlib.pyplot as plt\
\
# Function to compute Reaction Forces\
def compute_reactions(P1, P2, P3, a, b, c, L):\
    Rb = (P1 * a + P2 * b + P3 * c) / L\
    Ra = P1 + P2 + P3 - Rb\
    return Ra, Rb\
\
# Function to calculate Shear Force\
def calculate_shear_force(x, Ra, P1, a, P2, b, P3, c, L):\
    vb = np.zeros_like(x)\
    for j in range(len(x)):\
        if x[j] <= a:\
            vb[j] = Ra\
        elif x[j] <= b:\
            vb[j] = Ra - P1\
        elif x[j] <= c:\
            vb[j] = Ra - P1 - P2\
        else:\
            vb[j] = Ra - P1 - P2 - P3\
    return vb\
\
# Function to calculate Bending Moment\
def calculate_bending_moment(x, Ra, P1, a, P2, b, P3, c, L):\
    mb = np.zeros_like(x)\
    for j in range(len(x)):\
        if x[j] <= a:\
            mb[j] = Ra * x[j]\
        elif x[j] <= b:\
            mb[j] = Ra * x[j] - P1 * (x[j] - a)\
        elif x[j] <= c:\
            mb[j] = Ra * x[j] - P1 * (x[j] - a) - P2 * (x[j] - b)\
        else:\
            mb[j] = Ra * x[j] - P1 * (x[j] - a) - P2 * (x[j] - b) - P3 * (x[j] - c)\
    return mb\
\
# Streamlit Interface\
st.title('Shear and Bending Moment Diagram for a Simply Supported Beam')\
\
# User Inputs\
P1 = st.number_input('P1 (lbs)', value=100.0)\
P2 = st.number_input('P2 (lbs)', value=100.0)\
P3 = st.number_input('P3 (lbs)', value=100.0)\
\
a = st.number_input('a (in)', value=3.0)\
b = st.number_input('b (in)', value=4.0)\
c = st.number_input('c (in)', value=5.0)\
L = st.number_input('L (span in inches)', value=10.0)\
\
X = st.number_input('X (location of interest in inches)', value=5.0)\
E = st.number_input('E (modulus of elasticity in psi)', value=29000000.0)\
I = st.number_input('I (moment of inertia in in^4)', value=100.0)\
\
# Compute Reaction Forces\
Ra, Rb = compute_reactions(P1, P2, P3, a, b, c, L)\
\
# Discretize Beam\
dx = L / 1000\
x = np.arange(0, L + dx, dx)\
\
# Calculate Shear Force and Bending Moment\
vb = calculate_shear_force(x, Ra, P1, a, P2, b, P3, c, L)\
mb = calculate_bending_moment(x, Ra, P1, a, P2, b, P3, c, L)\
\
# Plotting Moment Diagram\
plt.figure(figsize=(10, 6))\
\
# Moment Diagram\
plt.subplot(2, 1, 1)\
plt.plot(x, mb, label='Moment', linewidth=2)\
plt.grid(True)\
plt.title('Bending Moment Diagram')\
plt.ylabel('Moment [lb\'b7in]')\
plt.xlabel('Distance from Left Support [in]')\
\
# Shear Diagram\
plt.subplot(2, 1, 2)\
plt.plot(x, vb, 'r', label='Shear', linewidth=2)\
plt.grid(True)\
plt.title('Shear Force Diagram')\
plt.ylabel('Shear [lb]')\
plt.xlabel('Distance from Left Support [in]')\
\
plt.tight_layout()\
\
# Display the plot in Streamlit\
st.pyplot(plt)\
}
