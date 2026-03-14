# OptiQueueAI - Smart Medical Triage System

OptiQueueAI is a medical software application that integrates Deep Learning with clinical workflow management. It automates patient registration, performs retinal scan analysis, and matches patients with specialized doctors based on diagnostic results.

## Live Demo
[Open OptiQueueAI Application](https://optiqueue-ai.streamlit.app/)

## Key Features
- Real-time Dashboard: Track clinical load, total registrations, and system accuracy metrics.
- AI Diagnostic Lab: Utilizes a Convolutional Neural Network to detect conditions including Cataracts, Glaucoma, and Uveitis.
- Specialist Matchmaker: Filters the medical staff database based on the diagnosis, years of experience, and success rates.
- Record Management: Administrative portal to view, manage, and delete patient records from the database.

## Tech Stack
- Frontend: Streamlit (Python)
- AI Engine: TensorFlow / Keras
- Database: SQLite3
- Deployment: Streamlit Community Cloud and Google Drive

## Operating Procedure
1. Patient Intake: Enter patient details including name, age, and gender in the intake portal.
2. AI Screening: Upload a retinal image scan. The AI analyzes the image and provides a diagnosis with a confidence score.
3. Smart Referral: The system suggests specific doctors based on the detected pathology.
4. Database Administration: Authorized users can manage the patient database and delete records as required.

---
Developed as a Smart Medical Triage Solution - 2026
