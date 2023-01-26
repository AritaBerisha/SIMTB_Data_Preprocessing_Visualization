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

    filteredDF['DateBin'] = filteredDF['RegistrationDate']
    for row, col in filteredDF.iterrows():
        filteredDF.loc[row, 'DateBin'] = col['DateBin'].split(
            '-')[0] + '-' + col['DateBin'].split('-')[1]

    filteredDF['yearOnly'] = filteredDF['RegistrationDate']
    for row, col in filteredDF.iterrows():
        filteredDF.loc[row, 'yearOnly'] = col['yearOnly'].split(
            '-')[0]

    st.subheader("Number of pulmonar and ex-pulmonar along the years")
    filteredDFClass = filteredDF[(filteredDF['Class']) != '0']
    treatmentChart = alt.Chart(filteredDFClass).mark_area().encode(
        x='DateBin',
        y='count()',
        color='Class',
    ).interactive()

    st.altair_chart(treatmentChart, use_container_width=True)

    st.subheader("Placement along the years")
    plChart = alt.Chart(filteredDF).mark_circle().encode(
        x='yearOnly',
        y='count()',
        color='Placement',
    ).interactive()

    st.altair_chart(plChart, use_container_width=True)

    st.subheader("Risk factors along the years")
    rfChart = alt.Chart(filteredDF).mark_circle().encode(
        x='DateBin',
        y='count()',
        color='RiskFactors',
    ).interactive()

    st.altair_chart(rfChart, use_container_width=True)

    st.subheader("Raport of pulmonar and ex-pulmonar")
    filteredDFClass = filteredDF[(filteredDF['Class']) != '0']
    placementChart = alt.Chart(filteredDFClass).mark_bar(color='#FF5733').encode(
        x='Class',
        y='count()',
    ).interactive()

    st.altair_chart(placementChart, use_container_width=True)

    st.subheader("Number of placements")
    filteredDFPlacement = filteredDF[(filteredDF['Placement']) != '0']
    Placement_bars = alt.Chart(filteredDFPlacement).mark_bar().encode(
        x="Placement",
        y="count()",
        color='Placement',
    ).interactive()

    st.altair_chart(Placement_bars, use_container_width=True)

    st.subheader("Number of risk factors")
    filteredDFRiskFactor = filteredDF[(filteredDF['RiskFactors']) != 'None']
    riskChart = alt.Chart(filteredDFRiskFactor).mark_bar().encode(
        x='RiskFactors',
        y='count()',
        color='RiskFactors',
    ).interactive()

    st.altair_chart(riskChart, use_container_width=True)
