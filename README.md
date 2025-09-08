# 🛡️ Fraud Detection (Demo)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fraudproject-dteaj5t8y7zjuxsjnovgdf.streamlit.app/)

مشروع تعليمي لاكتشاف الاحتيال في المعاملات البنكية باستخدام **Machine Learning** وواجهة **Streamlit**.

## ✨ المزايا
- تدريب Logistic Regression مع class_weight='balanced'
- تقييم ROC-AUC و Classification Report
- واجهة Streamlit لرفع CSV وإرجاع `fraud_risk` و `prediction`

## 🚀 التشغيل محليًا
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 train.py
streamlit run app.py

