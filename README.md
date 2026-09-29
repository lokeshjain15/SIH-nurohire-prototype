# NeuroHire - AI Hiring & Assessment Platform (SIH Prototype)

An intelligent recruitment and candidate evaluation prototype built for Smart India Hackathon (SIH). **NeuroHire** combines neural network candidate scoring, resume/JD similarity matching, targeted technical assessments, and interview evaluation to deliver objective hiring readiness scores.

---

## 🚀 Key Features

1. **Intelligent Resume & JD Parsing**:
   - Automated skill extraction, education parsing, and experience analysis from PDF/DOCX resumes.
   - Job description (JD) breakdown into required vs. preferred skills.
   - Cosine similarity matching using TF-IDF vectorization.

2. **Neural Network Candidate Scoring**:
   - Deep learning model trained with Keras/TensorFlow to predict candidate suitability based on weighted multi-dimensional features.

3. **Targeted Technical Assessment**:
   - Generates skill-gap assessment questions dynamically targeting missing required or preferred skills for each candidate.
   - Evaluates answers to compute an assessment readiness score with clear strengths and weaknesses.

4. **Candidate Ranking & Historical Records**:
   - Interactive dashboard ranking all candidates by suitability score.
   - Combined Readiness score blending resume evidence and technical assessment results.

5. **Multimodal Interview Engine (Preview)**:
   - Voice/audio response processing and transcription endpoints for automated candidate screening.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn, SQLite
- **Machine Learning / NLP**: TensorFlow/Keras, Scikit-learn, NumPy, Pandas, Joblib, PyPDF, python-docx
- **Frontend**: React, Vite, Modern Responsive CSS

---

## 📂 Project Structure

```plaintext
NeuroHire_SIH_Integrated_Phase1/
├── backend/
│   ├── app.py                      # FastAPI REST API server
│   ├── assessment_engine.py        # Technical assessment generation & evaluation
│   ├── certificate_recommender.py  # Learning path / certification recommendations
│   └── interview_engine.py         # Interview screening logic
├── database/
│   ├── database.py                 # SQLite helper & schema management
│   └── neurohire.db                # SQLite database for evaluations & assessments
├── frontend/
│   ├── src/                        # React components and styling
│   ├── package.json                # Frontend dependencies
│   └── vite.config.js              # Vite configuration
├── models/
│   ├── neurohire_model.keras       # Trained Keras neural network model
│   └── scaler.pkl                  # Feature scaler
├── src/
│   ├── education_extractor.py      # Degree and education parsing
│   ├── experience_extractor.py     # Work experience parsing
│   ├── jd_parser.py                # Job description extractor
│   ├── predictor.py                # Neural network prediction pipeline
│   ├── resume_parser.py            # PDF/DOCX resume text extraction
│   ├── similarity.py               # TF-IDF cosine similarity
│   ├── skill_extractor.py          # Skill dictionary & matching logic
│   └── train_model.py              # Model training script
├── requirements.txt                # Python backend dependencies
└── README.md                       # Project documentation
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Node.js (v18+) and npm installed
- Git installed

---

### 2. Backend Setup

1. **Open a terminal in the project root directory**:
   ```bash
   cd NeuroHire_SIH_Integrated_Phase1
   ```

2. **Create and activate a Python virtual environment**:
   - **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**:
   ```bash
   uvicorn backend.app:app --reload
   ```
   - The backend will start at: `http://127.0.0.1:8000`
   - Interactive Swagger API docs: `http://127.0.0.1:8000/docs`

---

### 3. Frontend Setup

1. **Open a second terminal window and navigate to `frontend`**:
   ```bash
   cd frontend
   ```

2. **Install frontend dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```
   - Open your browser at the local URL shown (typically `http://localhost:5173`).

---

## 🎯 Step-by-Step Demo Flow

1. **Evaluate Candidate(s)**:
   - Paste a Job Description (JD) and upload one or multiple candidate resumes (PDF/DOCX).
   - Click **Evaluate**.
2. **Review Candidate Ranking**:
   - Inspect candidates ranked by match score, extracted skills, and recommendations.
3. **Run Technical Assessment**:
   - Select a candidate and open **Technical Assessment** from the navigation.
   - Click **Generate Assessment** to create targeted questions for identified skill gaps.
   - Fill in responses and click **Submit Assessment** to view the combined readiness score.

---

## 👥 Team & Collaboration
To contribute or clone this repository:
```bash
git clone https://github.com/lokeshjain15/SIH-nurohire-prototype.git
cd SIH-nurohire-prototype
```
