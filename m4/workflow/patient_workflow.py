import streamlit as st
import pandas as pd
import os

def show_patient_workflow():
    st.title("Patient Workflow")

    clinical_notes_path = 'data/clinical_notes.csv'
    if not os.path.exists(clinical_notes_path):
        st.error(f"Clinical notes file not found: {clinical_notes_path}")
        return
    clinical_notes_df = pd.read_csv(clinical_notes_path)
    clinical_notes_df.columns = [col.strip().lower() for col in clinical_notes_df.columns]

    patient_id_input = st.text_input("Enter Patient ID")

    if patient_id_input:
        patient_notes = clinical_notes_df[clinical_notes_df['patient_id'].astype(str) == patient_id_input.strip()]
        
        if patient_notes.empty:
            st.warning(f"No clinical notes found for Patient ID: {patient_id_input}")
            return

        st.subheader(f"Clinical Details for Patient ID: {patient_id_input}")
        for idx, row in patient_notes.iterrows():
            st.markdown(f"**Clinical Note:**")
            st.write(row.get('clinical_note', 'No clinical note available.'))

            st.markdown(f"**EHR Text:**")
            st.write(row.get('ehr_text', 'No EHR text available.'))

            st.markdown(f"**Image Findings:**")
            st.write(row.get('image_findings', 'No image findings available.'))

            st.markdown("---")

        # Display images if available
        image_folder = f"data/images/{patient_id_input.strip()}/"
        if os.path.exists(image_folder):
            image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if image_files:
                st.subheader("Patient Images")
                for img_file in image_files:
                    img_path = os.path.join(image_folder, img_file)
                    st.image(img_path, caption=img_file, use_column_width=True)
            else:
                st.info("No images found for this patient.")
        else:
            st.info("No image folder found for this patient.")

        # Placeholder for generated summary text
        st.subheader("Generated Summary")
        summary = "This is a placeholder AI-generated summary based on clinical notes and images."
        st.write(summary)

    else:
        st.info("Please enter a Patient ID to view workflow details.")
