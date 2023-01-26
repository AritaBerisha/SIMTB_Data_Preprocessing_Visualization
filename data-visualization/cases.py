import datetime
import streamlit as st
import pandas as pd
import altair as alt


def show():
    st.title("Cases")

    casesDF = pd.read_csv("../data/cases_processed.csv")

    pClass = st.sidebar.radio('Class', ['All', 'Ex-Pulmonar', 'Pulmonar'])
    if pClass == 'Ex-Pulmonar':
        filtered_placements = list(
            filter(lambda x: x != '0', casesDF['Placement'].unique()))
        placement = st.sidebar.multiselect(
            'Placement', filtered_placements)
    min_date = datetime.datetime.strptime(
        min(casesDF['RegistrationDate']), '%Y-%m-%d')
    max_date = datetime.datetime.strptime(
        max(casesDF['RegistrationDate']), '%Y-%m-%d')
    dates = st.sidebar.slider(
        'Dates', min_date, max_date, (min_date, max_date))

    risk_factors = []
    for case in casesDF.columns[7:]:
        risk_factors.append(case)

    risk_factors_selected = st.sidebar.multiselect(
        'Risk Factors', risk_factors)

    if pClass == 'Pulmonar':
        filteredDF = casesDF[(casesDF['Class'] == pClass) & (casesDF['RegistrationDate'] >= dates[0].strftime(
            '%Y-%m-%d')) & (casesDF['RegistrationDate'] <= dates[1].strftime('%Y-%m-%d'))]
    if pClass == 'Ex-Pulmonar':
        filteredDF = casesDF[(casesDF['Class'] == pClass) & (casesDF['Placement'].isin(placement) if len(placement) > 0 else True) & (
            casesDF['RegistrationDate'] >= dates[0].strftime('%Y-%m-%d')) & (casesDF['RegistrationDate'] <= dates[1].strftime('%Y-%m-%d'))]
    if pClass == 'All':
        filteredDF = casesDF[(casesDF['RegistrationDate'] >= dates[0].strftime(
            '%Y-%m-%d')) & (casesDF['RegistrationDate'] <= dates[1].strftime('%Y-%m-%d'))]
    if len(risk_factors_selected) > 0:
        filteredDF = filteredDF[filteredDF[risk_factors_selected].any(axis=1)]
