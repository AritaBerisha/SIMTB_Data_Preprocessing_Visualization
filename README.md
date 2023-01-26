# SIMTB_Data_Preprocessing_Visualization

### About

Tuberculosis (TB) is a bacterial infection that primarily affects the lungs, but can also affect other parts of the body. It is caused by the bacterium Mycobacterium tuberculosis. Symptoms of active TB include a persistent cough, chest pain, and difficulty breathing. TB is typically treated with a combination of antibiotics taken for several months. It can be transmitted through the air when an infected person coughs or sneezes. It is a serious public health concern, particularly in developing countries. People with weakened immune systems, such as those living with HIV, are at a higher risk of developing TB.

### What is SIM-TB?

SIM-TB is a web application for the management of tuberculosis patients.

### Project Structure

The SIM-TB database contains three main tables: Patients, Cases and Examinations. Each Patient corresponds to one Case and each Case corresponds to one or more Examinations. The following diagram shows the relationship between the tables:

>*Patient Data: 2716*</br>
>*Cases Data: 2717*<br>
>*Examinations Data: 19287*

### This Project

The Project deals with the data preprocessing and visualization concerning the above mentioned tables.

### Project Setup

First the modules for this project need to be installed. 

```
pip install -r requirements.txt
```

After the installation is done, we navigate to the folder containing the *main.py* file.

```
cd data-visualization
```

To run the program execute the command below:

```
streamlit run main.py
```