# SHL Assessment Recommender - Submission Guide

## 📋 Quick Start for Submission

This guide helps you generate all required submission materials for the SHL AI Intern assignment.

---

## 🚀 Step 1: Initialize the Vector Database

First, ensure the vector database is created from scraped data:

```bash
# From project root
cd app
python rag.py
```

**Expected Output:**
```
✅ Found JSON data at: data/shl_assessments_complete.json
🚀 Success! Created vector DB with 389 assessments
📁 ChromaDB stored at: app/chroma_db
```

---

## 🔧 Step 2: Start the API Server

Start the FastAPI server in one terminal:

```bash
# From project root
uvicorn app.api:app --reload
```

**Verify it's running:**
```bash
# In another terminal
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "SHL Assessment Recommender API is running"
}
```

---

## 📊 Step 3: Run Evaluation (Optional but Recommended)

Evaluate your system on training data to get metrics for the approach document:

```bash
# From project root
cd evaluation
python evaluate.py
```

**What it does:**
- Loads train data from `Gen_AI Dataset.xlsx`
- Calculates Mean Recall@5 and Recall@10
- Saves results to `evaluation_results_k5.json` and `evaluation_results_k10.json`

**Note:** Make sure `Gen_AI Dataset.xlsx` is in the parent directory (`c:\Users\conne\Downloads\SHL\`)

---

## 📝 Step 4: Generate Test Predictions CSV

Generate predictions for the test set:

```bash
# From project root
cd predictions
python generate_predictions.py
```

**What it does:**
- Loads test queries from `Gen_AI Dataset.xlsx`
- Gets recommendations for each query
- Saves to `abhay_gupta.csv` in required format

**Output File:** `predictions/abhay_gupta.csv`

**Format:**
```csv
Query,Assessment_url
"Query 1","https://www.shl.com/..."
"Query 1","https://www.shl.com/..."
"Query 2","https://www.shl.com/..."
```

---

## 📄 Step 5: Complete the Approach Document

1. Open `docs/approach_document.md`
2. Fill in the evaluation metrics from Step 3
3. Add your deployment URLs (after deployment)
4. Export to PDF:

**Option A: Using Markdown to PDF converter**
```bash
# Install pandoc if needed
# Then convert
pandoc docs/approach_document.md -o docs/abhay_gupta_approach.pdf
```

**Option B: Manual conversion**
- Copy content to Google Docs
- Format nicely
- Export as PDF

---

## 🌐 Step 6: Deploy Your Application

### Deploy API (Render - Free Tier)

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repo
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.api:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:** Add `GOOGLE_API_KEY`
6. Deploy and get your API URL

### Deploy Streamlit App (Streamlit Cloud - Free)

1. Push code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Create new app
4. Connect your GitHub repo
5. Set main file: `streamlit_app.py`
6. Add secrets: `GOOGLE_API_KEY`
7. Deploy and get your app URL

**Update API URL in Streamlit:**
- Edit `streamlit_app.py` line 184
- Change API endpoint to your deployed URL

---

## 📦 Submission Checklist

Before submitting, ensure you have:

- [ ] **API Endpoint URL** - From Render deployment
- [ ] **Web App URL** - From Streamlit Cloud deployment
- [ ] **GitHub Repository URL** - Your public repo
- [ ] **Approach Document PDF** - `abhay_gupta_approach.pdf`
- [ ] **Test Predictions CSV** - `abhay_gupta.csv`

---

## 🔍 Troubleshooting

### API not connecting
```bash
# Check if API is running
curl http://localhost:8000/health

# Check logs
uvicorn app.api:app --reload --log-level debug
```

### ChromaDB not found
```bash
# Recreate vector database
cd app
python rag.py
```

### Excel file not found
```bash
# Ensure Gen_AI Dataset.xlsx is in parent directory
# Path should be: c:\Users\conne\Downloads\SHL\Gen_AI Dataset.xlsx
```

### Import errors
```bash
# Install all dependencies
pip install -r requirements.txt

# Install additional packages if needed
pip install pandas openpyxl
```

---

## 📊 File Structure

```
shl-project/
├── app/
│   ├── api.py              # FastAPI endpoints
│   ├── rag.py              # Vector DB setup
│   ├── scraper.py          # Data scraping
│   └── chroma_db/          # Vector storage
├── data/
│   └── shl_assessments_complete.json
├── evaluation/
│   ├── evaluate.py         # Evaluation script
│   └── evaluation_results_k*.json
├── predictions/
│   ├── generate_predictions.py
│   └── abhay_gupta.csv     # SUBMIT THIS
├── docs/
│   ├── approach_document.md
│   └── abhay_gupta_approach.pdf  # SUBMIT THIS
├── streamlit_app.py
├── requirements.txt
├── .env                    # Your API key
└── README.md
```

---

## 🎯 Quick Commands Reference

```bash
# 1. Initialize vector DB
cd app && python rag.py

# 2. Start API
uvicorn app.api:app --reload

# 3. Run evaluation
cd evaluation && python evaluate.py

# 4. Generate predictions
cd predictions && python generate_predictions.py

# 5. Start Streamlit (optional, for local testing)
streamlit run streamlit_app.py
```

---

## 📧 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify file paths are correct

---

**Good luck with your submission! 🚀**
