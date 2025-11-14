import streamlit as st
from dashboard.dashboard import show_dashboard
from workflow.patient_workflow import show_patient_workflow

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Patient Workflow"])

    if page == "Dashboard":
        show_dashboard()
    elif page == "Patient Workflow":
        show_patient_workflow()

if __name__ == "__main__":
    main()
