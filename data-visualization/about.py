import streamlit as st
import graphviz as graphviz


def show():
    st.title("About")
    st.header("What is Turbeculosis?")
    st.write("Tuberculosis (TB) is a bacterial infection that primarily affects the lungs, but can also affect other parts of the body. It is caused by the bacterium Mycobacterium tuberculosis. Symptoms of active TB include a persistent cough, chest pain, and difficulty breathing. TB is typically treated with a combination of antibiotics taken for several months. It can be transmitted through the air when an infected person coughs or sneezes. It is a serious public health concern, particularly in developing countries. People with weakened immune systems, such as those living with HIV, are at a higher risk of developing TB.")
    st.header("What is SIM-TB?")
    st.write(
        "SIM-TB is a web application for the management of tuberculosis patients.")
    st.header("Project Structure")
    st.write("The project is structured as follows:")
    st.write("The SIM-TB database contains three main tables: Patients, Cases and Examinations. Each Patient corresponds to one Case and each Case corresponds to one or more Examinations. The following diagram shows the relationship between the tables:")
    st.write()
    st.graphviz_chart('''
        digraph {
            graph [bgcolor=transparent, fontcolor=white]
            rankdir=LR
            node [shape=box, style=rounded, fontname=Handlee, fontsize=12, fontcolor=lightblue, color=lightblue]
            edge [color=lightblue]
            Patients -> Cases [arrowhead=curve]
            Cases -> Examinations [arrowhead=crow]
        }
    ''')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(""">*Patient Data: 2716*""")
    with col2:
        st.markdown(""">*Cases Data: 2717*""")
    with col3:
        st.markdown(""">*Examinations Data: 19287*""")
