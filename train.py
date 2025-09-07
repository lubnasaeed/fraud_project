import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# 1) قراءة البيانات
df = pd.read_csv("creditcard.csv")

# (اختياري) خذي عينة لتسريع التجربة الأولى، خصوصًا لو جهازك ضعيف
df = df.sample(n=60000, random_state=42)

# 2) فصل الميزات عن الهدف
X = df.drop(columns=["Class"])
y = df["Class"]

# 3) تقسيم Train/Test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# 4) توحيد مقياس لبعض الأعمدة (Time, Amount) إن وُجدت
scaler = None
cols_to_scale = [c for c in ["Time", "Amount"] if c in X.columns]
if cols_to_scale:
    scaler = StandardScaler()
    # نعمل نسخة عشان نتفادى التحذيرات
    X_train = X_train.copy()
    X_test = X_test.copy()
    X_train[cols_to_scale] = scaler.fit_transform(X_train[cols_to_scale])
    X_test[cols_to_scale] = scaler.transform(X_test[cols_to_scale])

# 5) نموذج بسيط: Logistic Regression مع موازنة الفئات
model = LogisticRegression(max_iter=200, class_weight="balanced", solver="liblinear")
model.fit(X_train, y_train)

# 6) تقييم
pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]

print("\n=== Report ===")
print(classification_report(y_test, pred, digits=4))
print("ROC-AUC:", round(roc_auc_score(y_test, proba), 4))

# 7) حفظ النموذج والأدوات
joblib.dump(model, "model.joblib")
joblib.dump(scaler, "scaler.joblib")  # ممكن تكون None
joblib.dump(list(X.columns), "features.joblib")
print("\nSaved: model.joblib, scaler.joblib, features.joblib ✅")
