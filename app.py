import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="كشف الاحتيال", page_icon="🛡️", layout="centered")

st.title("🛡️ نظام كشف الاحتيال")
st.markdown("هذا النظام يستخدم **الذكاء الاصطناعي** لاكتشاف العمليات البنكية المشبوهة.")

model = joblib.load("model.joblib")
scaler = joblib.load("scaler.joblib")
feature_cols = joblib.load("features.joblib")

uploaded = st.file_uploader("📂 ارفع ملف العمليات (CSV)", type=["csv"])


def preprocess(df: pd.DataFrame):
    # تأكد من الأعمدة والترتيب
    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        st.error(f"الأعمدة الناقصة: {missing}")
        return None
    df = df[feature_cols].copy()

    # طبق الـ scaler لو موجود وعلى Time/Amount فقط
    if scaler is not None:
        cols_to_scale = [c for c in ["Time", "Amount"] if c in df.columns]
        if cols_to_scale:
            df.loc[:, cols_to_scale] = scaler.transform(df[cols_to_scale])

    return df

if uploaded is not None:
    try:
        raw = pd.read_csv(uploaded)
        st.subheader("📊 معاينة البيانات")
        st.dataframe(raw.head())

        X = preprocess(raw)
        if X is not None:
            proba = model.predict_proba(X)[:, 1]
            preds = (proba >= 0.5).astype(int)

            result = raw.copy()
            result["fraud_risk"] = proba.round(4)
            result["prediction"] = preds

            st.success(f"تمت المعالجة ✅ عدد السجلات: {len(result)}")
            st.write("أول 20 صف بالنتيجة:")
            st.dataframe(result.head(20))

            st.download_button(
                "تحميل النتائج CSV",
                data=result.to_csv(index=False).encode("utf-8"),
                file_name="predictions.csv",
                mime="text/csv"
            )

            fraud_pct = (result["prediction"].mean() * 100)
            st.metric("نسبة المعاملات المصنفة كاحتيال", f"{fraud_pct:.2f}%")

        st.caption("ملاحظة: النموذج تعليمي تجريبي، لا يُستخدم في الإنتاج.")
    except Exception as e:
        st.error(f"خطأ أثناء القراءة/المعالجة: {e}")
