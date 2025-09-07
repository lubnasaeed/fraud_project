import pandas as pd

df = pd.read_csv("creditcard.csv")
print("عدد الصفوف والأعمدة:", df.shape)
print("\nأول 5 صفوف:")
print(df.head())
print("\nأعمدة الداتا:")
print(df.columns.tolist())
print("\nتوزيع الفئة (Class):")
print(df['Class'].value_counts(normalize=True))
