# Financial-advisor-
# 💸 AI-Powered Personal Finance Advisor

A data science web application that analyses personal expense data to deliver financial health scoring, transaction classification, anomaly detection, and personalised budget advice — built as a Final Year Project.

---

## 🚀 Live Demo

👉 [Click here to open the app](https://charubhalla14-afk-g7v63r26fyrsvna8mi4kzv.streamlit.app/)

---

## 📌 Project Overview

Most people have no clear picture of their spending habits. This project solves that by taking a simple expense CSV file and running it through a full ML pipeline to give users:

- A **Financial Health Score** out of 100
- **Automatic transaction categorisation** using NLP
- **Unusual transaction detection** using unsupervised ML
- **Personalised budget advice** based on their actual habits
- A clean, interactive **web dashboard**

---

## 🧠 ML Pipeline

| Module | Technique | Purpose |
|---|---|---|
| Data Preprocessing | Pandas, datetime parsing | Clean and structure raw CSV data |
| Exploratory Analysis | Matplotlib, groupby aggregation | Visualise spending patterns |
| Transaction Classification | TF-IDF + Logistic Regression | Auto-categorise transactions from descriptions |
| Anomaly Detection | Isolation Forest | Flag unusual or suspicious transactions |
| Health Scoring | Weighted composite scoring | Quantify overall financial wellbeing |
| Advice Generation | Rule-based engine | Generate personalised, actionable advice |

---

## 📂 Project Structure

```
finance-advisor/
├── app.py               # Streamlit web application
├── requirements.txt     # Python dependencies
├── .streamlit/
│   └── config.toml      # UI theme configuration
└── README.md
```

---

## 📊 Features

- **Upload your CSV** — supports any expense file with date, description, amount, and category columns
- **Monthly Spending Trend** — line chart showing how spending changes over time
- **Category Breakdown** — bar chart showing where money is being spent
- **Financial Health Score** — composite score based on spending, consistency, and budget adherence
- **Budget vs Actual** — instantly see if you're over or under budget
- **AI Advice** — specific recommendations based on your data

---

## 🗂️ CSV Format

Your expense file should have these columns:

| Column | Format | Example |
|---|---|---|
| `date` | dd-mm-yyyy | 15-03-2024 |
| `description` | text | swiggy order |
| `amount (in inr)` | number | 450 |
| `category` | text | Food |

---

## ⚙️ Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/finance-advisor.git
cd finance-advisor

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — web app framework
- **Pandas & NumPy** — data processing
- **Scikit-learn** — TF-IDF, Logistic Regression, Isolation Forest
- **Matplotlib** — data visualisation

---

## 👩‍💻 Author

**Charu**
Final Year Data Science Student

---

## 📄 License

This project is for academic purposes.
