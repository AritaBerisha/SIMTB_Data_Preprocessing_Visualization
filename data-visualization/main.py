import streamlit as st
import patients
import cases
import examinations
import about
import documentation

st.set_page_config(page_title="SIM-TB",
                   page_icon=":microscope:")

page = st.sidebar.selectbox(
    'Select Page', ["About", "Patients", "Cases", "Examinations", "Documentation"])

if page == "About":
    about.show()

if page == "Patients":
    patients.show()

if page == "Cases":
    cases.show()

if page == "Examinations":
    examinations.show()

if page == "Documentation":
    documentation.show()
