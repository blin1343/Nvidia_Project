import pandas as pd
import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


st.markdown("---")
label = pd.DataFrame({"Column 1": [1,2,3,4,5]})
st.title("Hi! I am Streamlit Web App")
st.subheader("Hi! I am your subheader")
st.header("I am header")
st.text("Hi I am text function and programmers uses me inplace of paragraph tag")

st.markdown("**Hello** World")
st.latex(r"\begin{pmatrix}a&b\\c&d\end{pmatrix}")

code = """
print("hello world")
"""
def change():
    print("changed")

state = st.checkbox("Checkbox", value = True, on_change=change, key = "checker")

st.sidebar.write("Hello this is my side bar")

x=np.linspace(0,10,100)

fig = plt.figure()
plt.plot(x, np.sin(x))
st.write(fig)

if state:
    st.write("Hi")

st.radio("what country do u live in", options = ("US", "UK", "China"))

st.code(code)
st.write("## H2")
st.metric(label="Wind Speed",value="120ms\^-1",delta="1.4")
st.table(label)
st.dataframe(label)