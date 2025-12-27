import streamlit as st
import basic  
st.title("BASIC Language Interpreter")

code = st.text_area("Enter code:", height=200)

if st.button("Run Code"):
    try:
        result = basic.run(code.strip())
        st.success(result)
    except Exception as e:
        st.error(str(e))
