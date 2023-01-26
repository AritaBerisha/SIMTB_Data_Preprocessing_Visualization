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
