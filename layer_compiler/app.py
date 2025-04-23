import streamlit as st
import os, sys
from io import StringIO
import pandas as pd
from treeviz import visualize_ast

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from codegen import IRGenerator
from optim import eliminate_dead_code
from vm import VM
from treeviz import visualize_ast

example_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../examples"))
examples = [f for f in os.listdir(example_dir) if f.endswith(".layer")]
example_dict = {f: open(os.path.join(example_dir, f), encoding="utf-8").read() for f in examples}

st.title("🧠 Layer Language Compiler")
st.markdown("A full compiler pipeline with lexer, parser, semantic analysis, IR, VM + Parse Tree")

mode = st.radio("Choose input mode:", ["Select example snippet", "Write your own Layer code"])
code = ""

if mode == "Select example snippet":
    selected_file = st.selectbox("Choose a .layer file:", examples)
    code = example_dict[selected_file]
else:
    code = st.text_area("Write your Layer code here:", height=250)

if st.button("🔍 Compile and Execute"):
    if not code.strip():
        st.warning("Please provide some Layer code to compile.")
        st.stop()

    # 1. Lexical Analysis
    st.subheader("🔹 Lexical Analysis")
    try:
        tokens = Lexer(code).tokenize()
        token_values = [t.value for t in tokens if t.type != 'WHITESPACE']
        st.code(token_values, language='python')

        # Show token table
        lex_table = pd.DataFrame([{
            "Type": t.type,
            "Value": t.value,
            "Position": f"{t.line}:{t.col}"
        } for t in tokens if t.type != 'WHITESPACE'])
        st.dataframe(lex_table, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Lexical Error: {e}")
        st.stop()

    # 2. Syntax Analysis (AST)
    st.subheader("🔹 Syntax Analysis (AST)")
    try:
        tree = Parser(code).parse()
        st.code(str(tree), language='python')
    except Exception as e:
        st.error(f"❌ Syntax Error: {e}")
        st.stop()

    # 3. Parse Tree
    st.subheader("🔹 Parse Tree")
    try:
        dot = visualize_ast(tree)
        st.graphviz_chart(dot.source)
    except Exception as e:
        st.error(f"❌ Tree Visualization Error: {e}")

    # 4. Semantic Analysis
    st.subheader("🔹 Semantic Analysis")
    try:
        analyzer = SemanticAnalyzer(tree)
        analyzer.analyze()
        st.success("✅ Semantic analysis passed")

        # Show symbol table
        st.subheader("📋 Symbol Table")
        symbols = analyzer.get_symbols().as_list()
        symbol_df = pd.DataFrame(symbols)
        st.dataframe(symbol_df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Semantic Error: {e}")
        st.stop()

    # 5. IR Generation
    st.subheader("🔹 Intermediate Representation (IR)")
    try:
        ir_list = IRGenerator().generate(tree)
        ir_text = "\n".join(str(instr) for instr in ir_list)
        st.code(ir_text, language='python')
    except Exception as e:
        st.error(f"❌ IR Generation Error: {e}")
        st.stop()

    # 6. Dead Code Elimination
    st.subheader("🔹 Optimized IR (Dead Code Elimination)")
    try:
        opt_ir = eliminate_dead_code(ir_list)
        opt_text = "\n".join(str(instr) for instr in opt_ir)
        st.code(opt_text, language='python')
    except Exception as e:
        st.error(f"❌ Optimization Error: {e}")
        st.stop()

    # 7. VM Execution
    st.subheader("🔹 VM Execution Output")
    try:
        output = StringIO()
        sys.stdout = output
        VM(opt_ir).run()
        sys.stdout = sys.__stdout__
        st.code(output.getvalue(), language='text')
    except Exception as e:
        sys.stdout = sys.__stdout__
        st.error(f"❌ VM Execution Error: {e}")

st.markdown("---")
st.caption("Created by Ananya & Ajay | Compiler Design Project 2025")
