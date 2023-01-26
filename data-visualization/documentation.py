import streamlit as st
import pandas as pd


def show():
    st.title("Documentation")

    data_tab, preprocessing_tab, visualization_tab, libraries_tab = st.tabs(
        ['Data', 'Preprocessing', 'Visualization', 'Libraries'])

    with data_tab:
        st.header("Data")

        st.subheader("Patients")
        st.write("Query to get Patients data:")
        st.code("""
                SELECT [ID] as ID
      ,[ID_Komuna] as CountyID
      ,[Data_Regjistrimit] as RegistrationDate
      ,[Mosha] as Age
      ,[Gjinia] as Gender
  FROM [TBC_Web6].[dbo].[Pacientet]
                """)
        patientsDF = pd.read_csv("../data/patients.csv")
        if st.checkbox("Show patients data"):
            st.dataframe(patientsDF.head(10))

        st.subheader("Cases")
        st.write("Query to get Cases data:")
        st.code("""
               SELECT [ID] as ID
      ,[ID_Pacienti] as PatientID
      ,[Klasifikimi_semundjes] as Class
      ,[EP_Vendi] as Placement
      ,[Faktoret_Rrezikut] as RiskFactors
      ,[Data_Regjistrimit] as RegistrationDate
      ,[Data_Fillimit_Trajtimit] as TreatementDate
  FROM [TBC_Web6].[dbo].[Rastet]
                """)
        casesDF = pd.read_csv("../data/cases.csv")
        if st.checkbox("Show cases data"):
            st.dataframe(casesDF.head(10))

        st.subheader("Examinations")
        st.write("Query to get Examinations data:")
        st.code("""
               SELECT [ID] as ID
      ,[ID_Rasti] as CaseID
      ,[Data_Regjistrimit] as RegistrationDate
      ,[Lloji_Ekzaminimit] as ExaminationType
      ,[Rezultati_Ekzaminimit] as ExaminationResult
  FROM [TBC_Web6].[dbo].[Ekzaminimet]
                """)
        examinationsDF = pd.read_csv("../data/examinations.csv")
        if st.checkbox("Show examinations data"):
            st.dataframe(examinationsDF.head(10))

        st.subheader("Configuration")
        st.write("Query to get Cases data:")
        st.code("""
              SELECT D.[Dropdown] as Category
      ,DV.[Name] as CategoryOption
      ,[Value] as CategoryValue
  FROM [TBC_Web6].[dbo].[DropdownValues] DV inner join [TBC_Web6].[dbo].[Dropdowns] D on D.Id = DV.DropdownId;
                """)

        configurationDF = pd.read_csv("../data/configurations.csv")
        if st.checkbox("Show configuration data"):
            st.dataframe(configurationDF)

    with preprocessing_tab:
        st.header("Preprocessing")

        st.subheader("Helpers")
        st.write("Since we have to get the nominal values from configuration table, we have to create a helper function to get the values from the table.")
        st.code("""
configurationDF = pd.read_csv('../data/configurations.csv')
def configureNominalValues(column):
    configuration = {}
    for index, row in configurationDF.iterrows():
        if row['Category'] == column:
            configuration[row['CategoryValue']] = row['CategoryOption']

    return configuration
                """)
        st.write("To format data to fit visualization we've done extra processing to include bins that group dates based on month and/or year.")
        st.code("""
filteredDF['DateBin'] = filteredDF['RegistrationDate']
    for row, col in filteredDF.iterrows():
        filteredDF.loc[row, 'DateBin'] = col['DateBin'].split(
            '-')[0] + '-' + col['DateBin'].split('-')[1]

filteredDF['yearOnly'] = filteredDF['RegistrationDate']
    for row, col in filteredDF.iterrows():
        filteredDF.loc[row, 'yearOnly'] = col['yearOnly'].split(
            '-')[0]
                """)

        st.subheader("Patients")
        st.markdown("""
                    **Data Preparation**:
1. Check for Null Values
2. Get Nominal Values from Configuration
3. Transform Registration Date from Datetime to Date 
                    """)

        st.write("Check for Null Values:")
        st.code("""patientsDF.isnull().sum()""")
        st.code("""
                ID                  0
CountyID            0
RegistrationDate    0
Age                 0
Gender              0
dtype: int64
                """)
        st.write("Get Nominal Values from Configuration:")
        st.code("""
                configurationDF['Category'].replace(['KomunatLista'], 'CountyID', inplace=True)
for column in ['CountyID']:
    for key, value in configureNominalValues(column).items():
        patientsDF[column] = patientsDF[column].replace([key], value)
                """)
        st.write("Transform Registration Date from Datetime to Date:")
        st.code(
            """patientsDF['RegistrationDate'] = pd.to_datetime(patientsDF['RegistrationDate']).dt.date""")

        processedPatientsDF = pd.read_csv("../data/patients_processed.csv")
        if st.checkbox("Show processed patients data"):
            st.dataframe(processedPatientsDF.head(10))

        st.subheader("Cases")
        st.markdown("""
                    **Data Preperation**
1. Check for Null Values
2. Transform RegistrationDate from datetime to date
2. One Hot Encode Risk Factors
3. Get Nominal Values from Configuration
                    """)
        st.write("Check for Null Values:")
        st.code("""casesDF.isnull().sum()""")
        st.code("""
                ID                     0
PatientID              0
Class                  0
Placement              0
RiskFactors         2612
RegistrationDate       0
TreatementDate         0
                """)
        st.code("""
                casesDF['RiskFactors'].fillna('None', inplace=True)
                """)
        st.write("Transform RegistrationDate from datetime to date:")
        st.code(
            """casesDF['RegistrationDate'] = pd.to_datetime(casesDF['RegistrationDate']).dt.date""")
        st.write("One Hot Encode Risk Factors:")
        st.code("""
                one_hot_encoding_columns = []
for risk in casesDF['RiskFactors'].unique():
    if risk != 'None':
      for risk_factor in risk.split(','):
        if risk_factor not in one_hot_encoding_columns and risk_factor != '':
          one_hot_encoding_columns.append(risk_factor.strip())
                """)
        st.code("""
                for column in one_hot_encoding_columns:
    for index, row in casesDF.iterrows():
    if row['RiskFactors'] == 'None':
      casesDF.loc[index, column] = 0
    elif column in row['RiskFactors']:
      casesDF.loc[index, column] = 1
    else:
      casesDF.loc[index, column] = 0
                """)
        st.write("Get Nominal Values from Configuration:")
        st.code("""
                configurationDF['Category'].replace(['LokalizimiLista'], 'Class', inplace=True)
configurationDF['Category'].replace(['ExtraPulmunareSmundjaVendi'], 'Placement', inplace=True)
for column in ['Class', 'Placement']:
    for key, value in configureNominalValues(column).items():
        casesDF[column] = casesDF[column].replace([key], value)
                """)
        processedCasesDF = pd.read_csv("../data/cases_processed.csv")
        if st.checkbox("Show processed cases data"):
            st.dataframe(processedCasesDF.head(10))

        st.subheader("Examinations")
        st.markdown("""
                    **Data Preparation**
1. Check Null Values
2. Transform RegistrationDate from datetime to date
2. Get Nominal Values
3. Get Result Values
4. Remove Noisy Result Values
                    """)
        st.write("Check Null Values:")
        st.code("""examinationsDF.isnull().sum()""")
        st.code("""
                ID                   0
CaseID               0
RegistrationDate     0
ExaminationType      0
ExaminationResult    0
dtype: int64
                """)
        st.write("Transform RegistrationDate from datetime to date:")
        st.code(
            """examinationsDF['RegistrationDate'] = pd.to_datetime(examinationsDF['RegistrationDate']).dt.date""")
        st.write("Get Nominal Values:")
        st.code("""
                configurationDF['Category'].replace(['EkzaminimiLlojiTestit'], 'ExaminationType', inplace=True)
for column in ['ExaminationType']:
    for key, value in configureNominalValues(column).items():
        examinationsDF[column] = examinationsDF[column].replace([key], value)
                """)
        st.write("Get Result Values:")
        st.code("""
                resultConfiguration = {
  'Histologjia': 'RezultatiHistologjia',
  'Mikroskopia direkte': 'RezultatiMikroskopiaDirekte',
  'RTG Fillestar': 'RezultatiRTGFillestar',
  'Kultura': 'RezultatiKultura',
  'GenXpert': 'RezultatiGenXpert',
  'PPD': 'RezultatiPPD',
  'RTG Pasues': 'RezultatiRTGPasues',
  'HIV': 'HIVTestYesNo',
  'Mycobacterium TBC': 'RezultatoMycobacteriumTBC',
  'COVID-19 PCR':  'RezultatiCOVIDPCR',
  'Rtg-CT COVID-19': 'RezultatiCOVIDRtgCT',
  'Serologjik':'RezultatiSerologjik'
}

for row, column in resultConfiguration.items():
    for key, value in configureNominalValues(column).items():
        for index, exam in examinationsDF.iterrows():
            if exam['ExaminationType'] == row and exam['ExaminationResult'] == key:
                examinationsDF.loc[index, 'ExaminationResult'] = value
                """)

        st.write("Remove Noisy Result Values:")
        st.code(
            """examinationsDF = examinationsDF[examinationsDF['ExaminationResult'].apply(type) != int]""")
        processedExaminationsDF = pd.read_csv(
            "../data/examinations_processed.csv")
        if st.checkbox("Show processed examinations data"):
            st.dataframe(processedExaminationsDF.head(10))

    with visualization_tab:
        st.header("Visualization")

        st.subheader("Altair Chart")
        st.write(
            "We've used Altair Chart to show the relationship between multiple attributes.")
        st.code("""
                chart = alt.Chart(filteredDF).mark_circle().encode(
        x='Attribute1',
        y='Attribute2',
        color='Attribute3',
        size='Attribute4'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
                """)

        st.subheader("Bar Chart")
        st.write(
            "We've used Bar Chart to show the distribution for each value of each attribute.")
        st.code("""
                bars = alt.Chart(filteredDF).mark_bar(color='#ff6666').encode(
        x="Attribute",
        y="count()"
    ).interactive()

    st.altair_chart(bars, use_container_width=True)
                """)
        st.subheader("Area Chart")
        st.write(
            "We've used Area Chart to show the distribution for each value of each attribute.")
        st.code("""
                chart = alt.Chart(filteredDF).mark_area().encode(
        x='Attribute',
        y='count()',
        color='Class',
    ).interactive()
                """)

        with libraries_tab:
            st.markdown("""
                        1. [Pandas](https://pandas.pydata.org/)
                        2. [Streamlit](https://streamlit.io/)
                        3. [Altair](https://altair-viz.github.io/)
                        4. [Numpy](https://numpy.org/)
                        5. [Graphviz](https://graphviz.org/)
                        """)
