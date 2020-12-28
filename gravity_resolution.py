#%%
'''
This is a StreamLit app to demonstrate how the ability to resolve two
objects using micrograviy varies as a function of object depth
and horizontal separation.
'''

import numpy as np
import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def point_source(x, z, x_meas, r_sphere, rho):
    '''
    Calculated the z-component of gravitational attraction
    by a point source a x and z for measurements at the surface
    at locations x_meas.
    Inputs:
    x: object x-location in meters
    z: object z-location in meters
    x_meas: measurements at z=0, xlocations in meters
    r: object radius in meters
    rho: object density in kg/m3
    Outputs:
    gz: vertical component of gravity at x_meas in gravity units
    '''
    
    G = 6.67e-11 # Universal gravitational constant in mks
    vol = (4/3) * np.pi * r_sphere**3
    mass = rho * vol
    r = np.sqrt((x-x_meas)**2 + z**2)
    gz = G*mass*z/r**3
    
    # Convert to gravity units
    gz = gz * 1e8
    return gz

# Parameters to be set by user in the app
xhi = 50
xlo = -50
zhi = 20
dx = .1
x_meas = np.arange(xlo, xhi, dx)
z = 0.95
r_sphere = 0.5
density = 2600

# Set up StreamLit App
st.title('Resolution of Gravity Anomalies')
st.sidebar.title("Parameters")
separation = st.sidebar.slider('Separation', float(2*r_sphere), float(xhi), 10.0)
z = st.sidebar.slider('Depth', float(r_sphere), float(zhi-r_sphere), 2.0)

explanation = '''
This model is for the gravity 
anomaly create by two identical
sheres. Vary their depth and
separation using the sliders.
Can you figure out a rule of
thumb as a function of depth
and separation for when you
can distinguish that there
are two objects? How would
noise in the data affect this?
'''
st.sidebar.text(explanation)

x1 = separation/2
x2 = -separation/2
gz1 = point_source(x1, z, x_meas, r_sphere, density)
gz2 = point_source(x2, z, x_meas, r_sphere, density)
gz = gz1 + gz2

# Plot the anomaly
fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
fig.add_trace(go.Line(x=x_meas, y=gz), row=1, col=1)
title = f"Depth = {z}, Separation = {separation}"
fig.update_layout(title=title)

# Plot the sources
fig.add_shape(type='circle',
              xref="x", yref="y",
              fillcolor="LightSeaGreen",
              x0=x1-r_sphere/2, y0=z-r_sphere/2,
              x1=x1+r_sphere/2, y1=z+r_sphere/2,
              row=2, col=1)
fig.add_shape(type='circle',
              xref="x", yref="y",
              fillcolor="LightSeaGreen",
              x0=x2-r_sphere/2, y0=z-r_sphere/2,
              x1=x2+r_sphere/2, y1=z+r_sphere/2,
              row=2, col=1)
fig.update_yaxes(range=[zhi, 0], row=2, col=1)

fig.update_xaxes(title='Distance(m)')
fig.update_yaxes(title='Gz (microgal)', row=1, col=1)
fig.update_yaxes(title='Depth (m)', row=2, col=1)

# Plot the figure
st.plotly_chart(fig)
    
# %%
