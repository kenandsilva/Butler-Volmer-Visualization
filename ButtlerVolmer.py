"""
#Simple Python code to visualitize the Buttler Volmer equation
"""
import streamlit as st
import scipy as sp
import numpy as np
import plotly.graph_objects as go
import pandas as pd


#Streamlit code for inputs for BV


st.title("Buttler Volmer")
st.header("Inputs", divider=True)
j0 = st.number_input(label=r"Exchange Current Density ${j_0}$ in ${{A}/{cm^2}}$",step=0.0005,value=0.001,format="%.4f",placeholder="Type a number...")
st.write("The exchange current density inputed is ", j0)
alpha = st.number_input(label=r"Symmetry Factor ${\alpha}$",value=0.5,step=0.05,format="%.2f",placeholder="Type a number...")
st.write("The Symmetry Factor inputed is ", alpha)
eta = st.slider("Select a range of overponetial ${\eta}$ in V", -1.50,1.50 , (-0.05, 0.05))
st.write("Overpotential range:", eta)
eta=np.linspace(eta[0],eta[1],100000)
T = st.number_input(label="Temperature ${T}$ in K",value=293.15,step=1.0,placeholder="Type a number...")
st.write("Temperature in K is", T)
z = st.number_input(label="Number of electrons transfered ${z}$",value=1,step=1,placeholder="Type a number...")
st.write("Number of electrons transfered is", z)
st.divider()
st.header("Buttler Volmer", divider=True)


def ButtlerVolmer(j0,eta,alpha,z,T):
    """

    Parameters
    ----------
    j0    : Exchange Current density in A/cm^2.
    eta   : Overponetial in V.
    alpha : Symmetry Factor.
    z     : Number of electrons transfered.
    T     : Temperature in K.

    Returns
    -------
    df : Data frame with overpotential, anodic current , cathodic current and over all current.

    """
    ja=j0*(np.exp((alpha*z*sp.constants.physical_constants["Faraday constant"][0]*np.array(eta))/(sp.constants.R*T)))
    jc=j0*(-np.exp(-((1-alpha)*z*sp.constants.physical_constants["Faraday constant"][0]*np.array(eta))/(sp.constants.R*T)))
    j=ja+jc
    df=pd.DataFrame(np.array([eta,ja,jc,j]).T,columns=["eta","ja","jc","j"])
    return df


df=ButtlerVolmer(j0,eta,alpha,z,T)
st.latex(r'''
    j = j_0 \left[ \exp\left(\frac{\alpha z F \eta}{RT}\right) - \exp\left(-\frac{(1-\alpha) z F \eta}{RT}\right) \right]''')

#Plotting

fig = go.Figure()

fig.add_trace(go.Scatter(x=eta, y=df["ja"],
                    mode='lines',
                    name='Anodic current ja', line=dict(color='red')))
fig.add_trace(go.Scatter(x=eta, y=df["jc"],
                    mode='lines',
                    name='Cathodic current jc', line=dict(color='green')))
fig.add_trace(go.Scatter(x=eta, y=df["j"],
                    mode='lines',
                    name='Overall current j', line=dict(color='blue')))

fig.update_xaxes(
        title_text = "Over Potential (mV)",
        )

fig.update_yaxes(
        title_text = "Current Density in A/cm^2",
        title_standoff = 25)
st.plotly_chart(fig)