import os
import sys
import streamlit as st
import plotly.graph_objects as go
import uuid
import sympy as sp
import math


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from neuromath.lexer.lexer import Lexer
from neuromath.parser.parser import Parser
from neuromath.interpreter.interpreter import Interpreter

st.set_page_config(page_title="NeuroMath Notebook", layout="wide")

st.title(" NeuroMath Notebook")
st.markdown("Notebook style symbolic computation interface")



if "variables" not in st.session_state:

    st.session_state.variables = {

        'pi': math.pi,
        'e': math.e,
        'π': math.pi,
        'tau': 2 * math.pi,
        'inf': float('inf')
    }

if "functions" not in st.session_state:
    st.session_state.functions = {}

if "history" not in st.session_state:
    st.session_state.history = []

if "cell_counter" not in st.session_state:
    st.session_state.cell_counter = 1



col1, col2 = st.columns([1, 6])

with col1:
    if st.button("🔄 Reset Kernel"):
        st.session_state.variables = {}
        st.session_state.functions = {}
        st.session_state.history = []
        st.session_state.cell_counter = 1
        st.success("Kernel reset!")



for entry in st.session_state.history:
    st.markdown(f"**In [{entry['cell']}]:**")
    st.code(entry["input"], language="python")

    st.markdown(f"**Out [{entry['cell']}]:**")
    st.write(entry["output"])
    st.markdown("---")



st.markdown(f"### In [{st.session_state.cell_counter}]:")
user_input = st.text_area(
    "Enter NeuroMath expression",
    key=f"input_{st.session_state.cell_counter}",
    height=200
)

if st.button("▶ Run Cell"):

    if user_input.strip() == "":
        st.warning("Empty cell.")
    else:
        try:
            # Create fresh interpreter
            interpreter = Interpreter()

            # Inject previous state
            interpreter.variables = st.session_state.variables
            interpreter.functions = st.session_state.functions

            # Lexing
            lexer = Lexer(user_input)
            tokens = lexer.tokenize()
            # Parsing
            parser = Parser(tokens)
            ast = parser.parse()


            # Interpret
            result = interpreter.interpret(ast)

            if isinstance(result,go.Figure):
                st.plotly_chart(result,key=f"output_{st.session_state.cell_counter}")

            # Save updated state
            st.session_state.variables = interpreter.variables
            st.session_state.functions = interpreter.functions

            # Clean float display
            if isinstance(result, float) and abs(result - round(result)) < 1e-9:
                result = round(result)

            if (isinstance(result, float) or isinstance(result, int)) and result > 1e10:
                result = 'inf'
            if (isinstance(result, float) or isinstance(result, int)) and result < - 1e10:
                result = '-inf'

            # Save to history
            st.session_state.history.append({
                "cell": st.session_state.cell_counter,
                "input": user_input,
                "output": result
            })

            st.session_state.cell_counter += 1

            st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")