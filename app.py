import streamlit as st
import pandas as pd
import numpy as np
 
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Finance Advisor",
    page_icon="💸",
    layout="wide"
)
 
# ---------------- UI THEME ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
 
*, body, .stApp {
    font-family: 'DM Sans', sans-serif;
}
 
.stApp {
    background: #0f0f13;
    color: #e8e8f0;
}
 
/* Sidebar */
section[data-testid="stSidebar"] {
    background: #16161f !important;
    border-right: 1px solid #2a2a3a;
}
 
/* All text */
h1, h2, h3, h4, h5, h6, p, div, span, label {
    color: #e8e8f0 !important;
}
 
/* Title */
h1 {
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
    background: linear-gradient(90deg, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
 
h2, h3 {
    font-weight: 600 !important;
    color: #c4b5fd !important;
}
 
/* Inputs */
input, textarea, .stTextInput input, .stNumberInput input {
    background: #1e1e2e !important;
    border: 1px solid #2a2a3a !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
 
input:focus, textarea:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 2px rgba(167,139,250,0.15) !important;
}
 
/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #a78bfa, #f472b6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s ease !important;
}
 
.stButton > button:hover {
    opacity: 0.85 !important;
}
 
/* File uploader */
[data-testid="stFileUploader"] {
    background: #1e1e2e !important;
    border: 1.5px dashed #2a2a3a !important;
    border-radius: 14px !important;
    padding: 1rem !important;
}
 
/* Metric cards */
[data-testid="stMetric"] {
    background: #1e1e2e;
    border: 1px solid #2a2a3a;
    border-radius: 14px;
    padding: 1rem 1.4rem;
}
 
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #a78bfa !important;
}
 
[data-testid="stMetricLabel"] {
    color: #888 !important;
    font-size: 0.85rem !important;
}
 
/* Success / warning / error boxes */
.stSuccess {
    background: #1a2e1a !important;
    border: 1px solid #2d5a2d !important;
    border-radius: 10px !important;
    color: #4ade80 !important;
}
 
.stWarning {
    background: #2e2a1a !important;
    border: 1px solid #5a4d2d !important;
    border-radius: 10px !important;
}
 
/* Divider */
hr {
    border-color: #2a2a3a !important;
    margin: 1.5rem 0 !important;
}
 
/* Score badge */
.score-badge {
    display: inline-block;
    padding: 0.4rem 1.2rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}
 
.score-good { background: #14532d; color: #4ade80; }
.score-mid  { background: #713f12; color: #fbbf24; }
.score-bad  { background: #7f1d1d; color: #f87171; }
 
/* Advice card */
.advice-card {
    background: #1e1e2e;
    border: 1px solid #2a2a3a;
    border-left: 4px solid #a78bfa;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.9rem;
    line-height: 1.8;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)
 
# ---------------- TITLE ----------------
st.title("💸 AI Finance Advisor")
st.caption("Upload your expense CSV and get instant financial insights.")
st.divider()
 
# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 👤 Your Profile")
    name = st.text_input("Your name", placeholder="e.g. Charu")
    user_budget = st.number_input("Monthly Budget (₹)", min_value=0, step=500)
    st.divider()
    st.markdown("### 📂 Upload Data")
    uploaded_file = st.file_uploader("Expense CSV", type=["csv"])
    st.caption("CSV must have columns: `date`, `description`, `amount (in inr)`, `category`")
 
if name:
    st.success(f"Welcome back, **{name}** 👋")
 
# ---------------- MEMORY ----------------
if "history" not in st.session_state:
    st.session_state.history = []
 
# ---------------- FUNCTIONS ----------------
 
def load_data(file):
    for enc in ['utf-8', 'latin1', 'ISO-8859-1']:
        try:
            file.seek(0)
            return pd.read_csv(file, encoding=enc)
        except Exception:
            continue
    st.error("❌ Unable to read file. Please upload a valid CSV.")
    return None
 
 
def preprocess_data(df):
    df.columns = df.columns.str.strip().str.lower()
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', dayfirst=True)
    df['description'] = df['description'].str.lower().str.strip()
    df['monthyear'] = df['date'].dt.to_period('M')
    return df
 
 
def analyze_spending(df):
    expense_df = df[df['amount (in inr)'] > 0].copy()
    monthly_spending = expense_df.groupby('monthyear')['amount (in inr)'].sum()
    category_spending = expense_df.groupby('category')['amount (in inr)'].sum()
    return expense_df, monthly_spending, category_spending
 
 
def calculate_score(expense_df, monthly_spending, user_budget):
    total_spending = expense_df['amount (in inr)'].sum()
    monthly_std = monthly_spending.std() if len(monthly_spending) > 1 else 0
 
    spending_score = max(0, 100 - (total_spending / 5000))
    consistency_score = max(0, 100 - (monthly_std / 50))
 
    latest_month_spending = monthly_spending.iloc[-1]
 
    if user_budget == 0:
        budget_score = 50
    else:
        ratio = latest_month_spending / user_budget
        if ratio <= 1:
            budget_score = 100
        elif ratio <= 1.2:
            budget_score = 70
        else:
            budget_score = 30
 
    score = (spending_score * 0.3 + consistency_score * 0.3 + budget_score * 0.4)
    return round(score, 2)
 
 
def budget_analysis(user_budget, actual_spending):
    if user_budget == 0:
        return "⚠️ No budget set"
    diff = actual_spending - user_budget
    if diff > 0:
        return f"⚠️ Over budget by ₹{round(diff, 2)}"
    else:
        return f"✅ Saved ₹{round(abs(diff), 2)} this month"
 
 
def unnecessary_spending(df):
    waste_cats = ['entertainment', 'shopping', 'food']
    waste = df[df['category'].str.lower().isin(waste_cats)]
    total = df['amount (in inr)'].sum()
    waste_total = waste['amount (in inr)'].sum()
    return (waste_total / total * 100) if total != 0 else 0
 
 
def category_budgeting(df, user_budget):
    cat_spend = df.groupby('category')['amount (in inr)'].sum()
    total = cat_spend.sum()
    return {cat: round((val / total) * user_budget, 2) for cat, val in cat_spend.items()} if total != 0 else {}
 
 
def generate_advice(score, waste_percent, budget_status, category_suggestions):
    lines = []
 
    if score >= 70:
        lines.append("✅ Financial health: GOOD")
    elif score >= 40:
        lines.append("⚠️  Financial health: MODERATE")
    else:
        lines.append("🚨 Financial health: POOR — action needed")
 
    lines.append(f"📊 Budget status: {budget_status}")
 
    if waste_percent > 40:
        lines.append(f"🚨 Non-essential spending is {round(waste_percent, 1)}% of total — consider cutting back")
    elif waste_percent > 20:
        lines.append(f"⚠️  Non-essential spending at {round(waste_percent, 1)}% — moderate, watch this")
    else:
        lines.append(f"✅ Non-essential spending at {round(waste_percent, 1)}% — well controlled")
 
    if category_suggestions:
        lines.append("\n📂 Suggested budget allocation based on your habits:")
        for cat, amt in category_suggestions.items():
            lines.append(f"   {cat.title():<20} ₹{amt}")
 
    return "\n".join(lines)
 
 
# ---------------- MAIN ----------------
 
if uploaded_file is not None:
 
    df = load_data(uploaded_file)
    if df is None:
        st.stop()
 
    df = preprocess_data(df)
 
    # Append to session history & combine
    st.session_state.history.append(df)
    combined_df = pd.concat(st.session_state.history, ignore_index=True)
 
    # Core analysis
    expense_df, monthly_spending, category_spending = analyze_spending(df)
    score = calculate_score(expense_df, monthly_spending, user_budget)
 
    latest_month_key = expense_df['monthyear'].max()
    latest_month = expense_df[expense_df['monthyear'] == latest_month_key]
    latest_month_spending = monthly_spending.iloc[-1]
 
    waste_percent = unnecessary_spending(latest_month)
    budget_status = budget_analysis(user_budget, latest_month_spending)
    category_suggestions = category_budgeting(latest_month, user_budget)
    advice = generate_advice(score, waste_percent, budget_status, category_suggestions)
 
    st.divider()
 
    # ---- METRICS ROW ----
    col1, col2, col3, col4 = st.columns(4)
 
    with col1:
        st.metric("💳 Total Spent (Latest Month)", f"₹{round(latest_month_spending, 2)}")
 
    with col2:
        st.metric("🎯 Monthly Budget", f"₹{user_budget}" if user_budget > 0 else "Not set")
 
    with col3:
        savings = user_budget - latest_month_spending if user_budget > 0 else 0
        st.metric("💰 Saved / Over", f"₹{round(savings, 2)}" if user_budget > 0 else "—")
 
    with col4:
        st.metric("🏅 Health Score", f"{score} / 100")
 
    st.divider()
 
    # ---- SCORE BADGE ----
    st.subheader("🏅 Financial Health Score")
    if score >= 70:
        badge_class = "score-good"
        label = "GOOD"
    elif score >= 40:
        badge_class = "score-mid"
        label = "MODERATE"
    else:
        badge_class = "score-bad"
        label = "POOR"
 
    st.markdown(f'<span class="score-badge {badge_class}">{label} — {score}/100</span>', unsafe_allow_html=True)
 
    score_bar = score / 100
    st.progress(score_bar)
 
    st.divider()
 
    # ---- CHARTS ----
    col_left, col_right = st.columns(2)
 
    with col_left:
        st.subheader("📈 Monthly Spending Trend")
        monthly_trend = combined_df.groupby('monthyear')['amount (in inr)'].sum().reset_index()
        monthly_trend['monthyear'] = monthly_trend['monthyear'].astype(str)
        st.line_chart(monthly_trend.set_index('monthyear'))
 
    with col_right:
        st.subheader("📂 Spending by Category")
        st.bar_chart(category_spending)
 
    st.divider()
 
    # ---- ADVICE ----
    st.subheader("🤖 AI Financial Advice")
    st.markdown(f'<div class="advice-card">{advice}</div>', unsafe_allow_html=True)
 
else:
    # Empty state
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem; color: #555;">
        <div style="font-size: 3rem;">📂</div>
        <h3 style="color: #666 !important; margin-top: 1rem;">Upload your expense CSV to get started</h3>
        <p style="color: #444 !important;">Use the sidebar to upload your file and set your monthly budget.</p>
    </div>
    """, unsafe_allow_html=True)