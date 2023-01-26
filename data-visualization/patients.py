import datetime
import streamlit as st
import pandas as pd
import altair as alt


def show():
    st.title("Patients")
    st.write("This is the patients page")

    patientsDF = pd.read_csv("../data/patients_processed.csv")

    gender = st.sidebar.radio('Gender', ['All', 'F', 'M'])
    age = st.sidebar.slider('Age', min(
        patientsDF['Age']), max(patientsDF['Age']), (0, 100))
    county = st.sidebar.multiselect(
        'County', patientsDF['CountyID'].unique())
    min_date = datetime.datetime.strptime(
        min(patientsDF['RegistrationDate']), '%Y-%m-%d')
    max_date = datetime.datetime.strptime(
        max(patientsDF['RegistrationDate']), '%Y-%m-%d')
    dates = st.sidebar.slider(
        'Dates', min_date, max_date, (min_date, max_date))

    if gender != 'All' and len(county) > 0:
        filteredDF = patientsDF[(patientsDF['Gender'] == gender) & (patientsDF['Age'] > age[0]) & (patientsDF['Age'] < age[1]) & (patientsDF['CountyID'].isin(
            county)) & (patientsDF['RegistrationDate'] >= dates[0].strftime('%Y-%m-%d')) & (patientsDF['RegistrationDate'] <= dates[1].strftime('%Y-%m-%d'))]
    if gender != 'All' and len(county) == 0:
        filteredDF = patientsDF[(patientsDF['Gender'] == gender) & (patientsDF['Age'] > age[0]) & (patientsDF['Age'] < age[1]) & (
            patientsDF['RegistrationDate'] >= dates[0].strftime('%Y-%m-%d')) & (patientsDF['RegistrationDate'] <= dates[1].strftime('%Y-%m-%d'))]
    if gender == 'All' and len(county) > 0:
        filteredDF = patientsDF[(patientsDF['Age'] > age[0]) & (patientsDF['Age'] < age[1]) & (patientsDF['CountyID'].isin(
            county)) & (patientsDF['RegistrationDate'] >= dates[0].strftime('%Y-%m-%d')) & (patientsDF['RegistrationDate'] <= dates[1].strftime('%Y-%m-%d'))]
    if gender == 'All' and len(county) == 0:
        filteredDF = patientsDF[(patientsDF['Age'] > age[0]) & (patientsDF['Age'] < age[1]) & (
            patientsDF['RegistrationDate'] >= dates[0].strftime('%Y-%m-%d')) & (patientsDF['RegistrationDate'] <= dates[1].strftime('%Y-%m-%d'))]

    filteredDF['DateBin'] = filteredDF['RegistrationDate']
    for row, col in filteredDF.iterrows():
        filteredDF.loc[row, 'DateBin'] = col['DateBin'].split(
            '-')[0] + '-' + col['DateBin'].split('-')[1]

    st.subheader(
        "Number of patients during the years, filtered by age and city")
    chart = alt.Chart(filteredDF).mark_circle().encode(
        x='RegistrationDate',
        y='Age',
        color='CountyID',
        size='Gender'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    st.subheader("Number of patients filtered by their age")
    age_bars = alt.Chart(filteredDF).mark_bar(color='#ff6666').encode(
        x="Age",
        y="count()"
    ).interactive()

    st.altair_chart(age_bars, use_container_width=True)

    st.subheader("Number of patients filtered by their gender")
    gender_bars = alt.Chart(filteredDF).mark_bar(color='#ff9900').encode(
        x="Gender",
        y="count()"
    ).interactive()

    st.altair_chart(gender_bars, use_container_width=True)

    st.subheader("Number of patients filtered by their city")
    county_bars = alt.Chart(filteredDF).mark_bar(color='#6699ff').encode(
        x="CountyID",
        y="count()"
    ).interactive()

    st.altair_chart(county_bars, use_container_width=True)
