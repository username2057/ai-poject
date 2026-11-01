# ResumeAI – Intelligent Resume Screening and Shortlisting Platform

## Overview and abstract

ResumeAI extracts text and work-related evidence from PDF, DOCX, TXT, and RTF resumes, predicts a professional category with a trained text classifier, and compares resume evidence with a recruiter-provided job description. It provides an ordered review queue and manual review statuses. It never rejects candidates or makes a hiring decision. The initial dataset builder generates labeled synthetic examples for a reproducible demonstration; these data and resulting metrics are not representative of real applicants. A public academic dataset source and manual acquisition steps are documented in `docs/DATASET_DOCUMENTATION.md`.

## Problem and objectives

Resume screening is time-consuming and varies across reviewers. This project demonstrates a modular, auditable workflow for organizing resumes, surfacing skill evidence, comparing it against role requirements, and keeping decisions with a human recruiter. Objectives are document parsing, privacy-aware preprocessing, supervised category classification, explainable job matching, persistent review records, analytics, and export.

## Existing and proposed system

Manual review typically involves repeated opening, reading, and sorting of files. The proposed decision-support workflow extracts searchable text, assigns a predicted category when a trained model exists, reports matching and unverified skill evidence, and stores human review actions. Scores are configurable demonstrations, not validated selection criteria.

## Technologies

Python, scikit-learn, TF-IDF, Logistic Regression, Linear SVM, Multinomial Naive Bayes, Random Forest, optional Sentence Transformers, PyMuPDF, python-docx, FastAPI, Streamlit, SQLAlchemy/SQLite, pandas, Plotly/Matplotlib, Joblib, pytest.

## Requirements and setup (Windows)

Use Python 3.10 or later. From PowerShell in this folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/download_dataset.py
python scripts/inspect_dataset.py
python scripts/preprocess_dataset.py
python scripts/train_models.py
python scripts/evaluate_models.py
pytest -v
python run.py
```

The app is at `http://localhost:8501`, API at `http://127.0.0.1:8000`, and API docs at `/docs`. To run separately, use `python -m uvicorn app.backend.api:api --reload` and `python -m streamlit run app/main.py`. Configure settings through environment variables; `.env.example` documents supported variables. Sentence Transformers downloads its recommended embedding model on first use when available; an offline TF-IDF cosine fallback is used if it cannot load.

## Architecture and modules

- `app/utils`: document parsing and upload validation.
- `app/ml`: contact redaction, skills/education/experience extraction, classifier and matching.
- `app/database.py`: SQLite schema and SQLAlchemy session.
- `app/backend/api.py`: upload, jobs, matching, review, analytics and health routes.
- `app/main.py`: Streamlit dashboard, upload, matching, review, analytics and export pages.
- `scripts/`: synthetic data acquisition, inspection, preprocessing, training and reporting.

## Dataset

The included acquisition script creates synthetic role descriptions for 15 job categories. This fallback is explicitly synthetic, not a public dataset, not authentic candidate resumes, and unsuitable to claim real-world accuracy. To use a public dataset, obtain it separately, verify its license and terms, then provide a CSV with `text` and `category` columns in `data/raw/`. Keep source and license details in `docs/DATASET_DOCUMENTATION.md`. No API credentials are needed by the synthetic fallback. For Kaggle sources, follow Kaggle's official credential instructions and do not commit secrets.

## ML, evaluation, and matching

Four TF-IDF classifiers are fitted. A stratified train/validation/test split uses seed 42; validation macro-F1 selects a model, and the held-out test is evaluated after selection. Reports are generated only by actual script execution. Metrics include accuracy, macro/weighted F1, class report, confusion matrix, and model comparison. `match_resume` combines semantic cosine similarity, required-skill coverage, preferred-skill coverage, and an experience component. Sentence Transformer embeddings are optional at runtime; the fallback is lexical TF-IDF similarity. Component scores are exposed and are not probabilities.

## Database schema

SQLite tables: `candidates`, `resumes`, `job_descriptions`, `screening_results`, `extracted_skills`, `recruiter_reviews`, and `model_metadata`. The schema stores extracted text for demonstration. Configure retention with `RETENTION_DAYS`; deletion automation should be applied before production use. Do not upload resumes without appropriate authorization and retention practices.

## API

- `GET /api/health`
- `POST /api/resumes/upload` (multipart `files`)
- `GET /api/resumes`
- `DELETE /api/resumes/{resume_id}`; `POST /api/retention/purge` (manual retention purge)
- `POST /api/jobs`, `GET /api/jobs`
- `POST /api/match?job_id=...`
- `POST /api/shortlist?resume_id=...&status=...&notes=...`
- `GET /api/analytics`

Interactive OpenAPI documentation is served at `/docs`.

Model outputs are saved to `models/`; the latest executed evaluation is in `reports/model_evaluation/`; figures are in `reports/figures/`. The retention purge endpoint is manual and requires an authorized operator; it is not scheduled.

## Expected outputs and user guide

Upload resumes, create a role description, enter required/preferred skills and experience, inspect ranked evidence, then set each candidate to Needs review, Manual review, or Shortlisted and record notes. Exports are available in CSV and Excel. A candidate absent from a skill's evidence list is unverified, not necessarily unqualified. Category prediction confidence is classifier confidence, not candidate quality.

## Responsible AI, limitations, future work

Protected or irrelevant attributes are not intentionally extracted into model features; email, phone, and URLs are redacted before model inference. Names are not used as features. Model and ranking results require human review and may be wrong. Synthetic data, limited skill vocabulary, heuristic extraction, document parsing errors, and possible proxy bias limit use. No fairness audit is provided because no lawful demographic data is supplied. Future work includes licensed real-world evaluation, OCR with Tesseract, authenticated access, encrypted storage, deletion automation, stronger skills ontology, calibration, and a privacy-protected fairness audit.

## Screenshots and references

Screenshots may be added after running the application; none are claimed here. Dataset source and license are described in the dataset documentation. See `docs/REFERENCES.md` for tool references. Experimental metrics belong in `docs/EXPERIMENTAL_RESULTS.md` after training.
