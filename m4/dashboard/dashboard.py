import streamlit as st
import pandas as pd
import plotly.express as px

def show_dashboard():
    st.title("EHR Dashboard & Patient Search")

    # Load data
    df = pd.read_csv('data/ehr_data.csv')

    # Clean column names: strip spaces and lowercase
    df.columns = [col.strip().lower() for col in df.columns]

    # Debug: show columns and first rows
    st.write("Columns in dataset:", df.columns.tolist())
    st.write(df.head())

    # Use lowercase names now
    patient_id_col = 'patient_id'
    stroke_col = 'stroke_type'
    gender_col = 'gender'
    date_col = 'date_of_scan'
    num_images_col = 'num_images'

    # Metrics
    if patient_id_col in df.columns:
        st.metric("Total Patients", df[patient_id_col].nunique())
    else:
        st.warning(f"Column '{patient_id_col}' not found.")

    st.metric("Total Records", len(df))

    # Stroke Type Chart
    if stroke_col in df.columns:
        st.subheader("Stroke Type Distribution (Overall)")
        stroke_counts = df[stroke_col].value_counts()
        st.bar_chart(stroke_counts)
    else:
        st.info(f"Column '{stroke_col}' not found. Skipping Stroke Type chart.")

    # Gender Chart
    if gender_col in df.columns:
        st.subheader("Gender Distribution (Overall)")
        gender_counts = df[gender_col].value_counts().reset_index()
        gender_counts.columns = [gender_col, 'count']
        fig_gender = px.pie(gender_counts, values='count', names=gender_col, title='Gender Distribution')
        st.plotly_chart(fig_gender)
    else:
        st.info(f"Column '{gender_col}' not found. Skipping Gender Distribution chart.")

    # Scan Timeline
    if date_col in df.columns:
        st.subheader("Number of Scans Over Time (Overall)")
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        scans_over_time = df.groupby(df[date_col].dt.to_period('M')).size()
        scans_over_time.index = scans_over_time.index.to_timestamp()
        st.line_chart(scans_over_time)
    else:
        st.info(f"Column '{date_col}' not found. Skipping Scans Over Time chart.")

    # Search Patient
    st.sidebar.title("Search Patient")
    search_patient = st.sidebar.text_input("Enter Patient ID to search")

    if search_patient and patient_id_col in df.columns:
        patient_data = df[df[patient_id_col].astype(str).str.contains(search_patient.strip(), case=False, na=False)]
        if not patient_data.empty:
            st.subheader(f"Details for Patient(s) matching: {search_patient}")
            st.write(patient_data)

            # Patient Stroke Type Chart
            if stroke_col in patient_data.columns:
                st.subheader("Patient Stroke Type Distribution")
                stroke_type = patient_data[stroke_col].value_counts()
                st.bar_chart(stroke_type)

            # Number of Images chart
            if num_images_col in patient_data.columns:
                st.subheader("Number of Images for Patient")
                st.bar_chart(patient_data[num_images_col])

            # Scan timeline for patient
            if date_col in patient_data.columns:
                patient_data[date_col] = pd.to_datetime(patient_data[date_col], errors='coerce')
                scan_counts = patient_data.groupby(date_col).size()
                st.subheader("Scan Timeline for Patient")
                st.line_chart(scan_counts)
        else:
            st.warning("No patient found with that ID.")
    else:
        if not search_patient:
            st.info("Enter a Patient ID in the sidebar to view patient-specific details.")
        else:
            st.warning(f"Column '{patient_id_col}' not found; cannot search patients.")
