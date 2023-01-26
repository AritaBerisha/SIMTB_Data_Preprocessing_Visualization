import datetime
import numpy as np
import streamlit as st
import pandas as pd
import altair as alt


def show():
    st.title("Examinations")

    examinationsDF = pd.read_csv("../data/examinations_processed.csv")

    examinations_types = np.insert(
        examinationsDF['ExaminationType'].unique(), 0, 'All')
    examination_type = st.sidebar.selectbox(
        'Examination Type', examinations_types)
    if examination_type != 'All':
        result_filter = examinationsDF[examinationsDF['ExaminationType']
                                       == examination_type]
        examination_result = st.sidebar.multiselect(
            'Examination Result', result_filter['ExaminationResult'].unique())
    min_date = datetime.datetime.strptime(
        min(examinationsDF['RegistrationDate']), '%Y-%m-%d')
    max_date = datetime.datetime.strptime(
        max(examinationsDF['RegistrationDate']), '%Y-%m-%d')
    dates = st.sidebar.slider(
        'Dates', min_date, max_date, (min_date, max_date))

    if examination_type == 'All':
        filteredDF = examinationsDF[(
            examinationsDF['RegistrationDate'] >= dates[0].strftime('%Y-%m-%d')) & (examinationsDF['RegistrationDate'] <= dates[1].strftime('%Y-%m-%d'))]
    if examination_type != 'All':
        filteredDF = examinationsDF[(examinationsDF['ExaminationType'] == examination_type) & (examinationsDF['ExaminationResult'].isin(examination_result) if examination_result else True) & (
            examinationsDF['RegistrationDate'] >= dates[0].strftime('%Y-%m-%d')) & (examinationsDF['RegistrationDate'] <= dates[1].strftime('%Y-%m-%d'))]

    filteredDF['yearOnly'] = filteredDF['RegistrationDate']
    for row, col in filteredDF.iterrows():
        filteredDF.loc[row, 'yearOnly'] = col['yearOnly'].split(
            '-')[0]

    filteredDF['DateBin'] = filteredDF['RegistrationDate']
    for row, col in filteredDF.iterrows():
        filteredDF.loc[row, 'DateBin'] = col['DateBin'].split(
            '-')[0] + '-' + col['DateBin'].split('-')[1]

    st.subheader("Number of examination types along the years")
    chart = alt.Chart(filteredDF).mark_circle().encode(
        x='yearOnly',
        y='count()',
        color='ExaminationType',
        size='ExaminationType'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    st.subheader("Number of examination results along the years")
    reschart = alt.Chart(filteredDF).mark_circle().encode(
        x='yearOnly',
        y='count()',
        color='ExaminationResult',
        size='ExaminationResult'
    ).interactive()

    st.altair_chart(reschart, use_container_width=True)

    st.subheader("Number of examination types and results are the same")
    resTypechart = alt.Chart(filteredDF).mark_circle().encode(
        x='ExaminationType',
        y='count()',
        color='ExaminationResult',
        size='ExaminationResult'
    ).interactive()

    st.altair_chart(resTypechart, use_container_width=True)

    st.subheader("Number of times each examination type has been done")
    type_bars = alt.Chart(filteredDF).mark_bar(color='#33FFB5').encode(
        x="ExaminationType",
        y="count()"
    ).interactive()

    st.altair_chart(type_bars, use_container_width=True)

    st.subheader("Number of times each examination result has been the same")
    result_bars = alt.Chart(filteredDF).mark_bar(color='#ff6666').encode(
        x="ExaminationResult",
        y="count()"
    ).interactive()

    st.altair_chart(result_bars, use_container_width=True)