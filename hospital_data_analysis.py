# استيراد المكتبات
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# ------------------------------
# 1. قراءة البيانات مع دعم الفاصل المنقوطة
# ------------------------------
patients = pd.read_csv("Patients.csv", sep=';')
staff = pd.read_csv("Staff.csv", sep=';')
operations = pd.read_csv("Operations.csv", sep=';')
finance = pd.read_csv("Finance.csv", sep=';')

# ------------------------------
# 2. تنظيف أسماء الأعمدة
# ------------------------------
for df in [patients, staff, operations, finance]:
    df.columns = df.columns.str.strip()           # حذف المسافات الزائدة
    df.columns = df.columns.str.replace(' ', '_') # استبدال الفراغات بـ _
    df.columns = df.columns.str.replace('\n','') # إزالة أي أسطر جديدة
    df.columns = df.columns.str.lower()           # تحويل كل شيء لأحرف صغيرة

# ------------------------------
# 3. تنظيف البيانات
# ------------------------------
patients.drop_duplicates(inplace=True)
patients.ffill(inplace=True)

staff.drop_duplicates(inplace=True)
operations.drop_duplicates(inplace=True)
finance.drop_duplicates(inplace=True)

# ------------------------------
# 4. تحويل الأعمدة الرقمية
# ------------------------------
numeric_cols_patients = ['age','length_of_stay','blood_pressure','blood_sugar','cholesterol']
for col in numeric_cols_patients:
    if col in patients.columns:
        patients[col] = pd.to_numeric(patients[col], errors='coerce')

numeric_cols_staff = ['patients_attended','avg_treatment_success']
for col in numeric_cols_staff:
    if col in staff.columns:
        staff[col] = pd.to_numeric(staff[col], errors='coerce')

numeric_cols_operations = ['success_rate']
for col in numeric_cols_operations:
    if col in operations.columns:
        operations[col] = pd.to_numeric(operations[col], errors='coerce')

numeric_cols_finance = ['revenue','expenses']
for col in numeric_cols_finance:
    if col in finance.columns:
        finance[col] = pd.to_numeric(finance[col], errors='coerce')

# ------------------------------
# 5. تحليل بيانات المرضى
# ------------------------------
disease_counts = patients['diagnosis'].value_counts()
print("الأمراض الأكثر شيوعًا:\n", disease_counts)

plt.figure(figsize=(10,6))
sns.countplot(data=patients, x='diagnosis', hue='gender')
plt.title("Distribution of diseases by gender")
plt.xticks(rotation=45)
plt.show()

avg_stay = patients.groupby('diagnosis')['length_of_stay'].mean()
print("\nمتوسط مدة الإقامة لكل مرض:\n", avg_stay)

# ------------------------------
# 6. تحليل أداء الطاقم الطبي
# ------------------------------
plt.figure(figsize=(10,6))
sns.barplot(data=staff, x='name', y='avg_treatment_success', hue='role')
plt.title("Average treatment success per employee")
plt.xticks(rotation=45)
plt.show()

dept_workload = staff.groupby('department')['patients_attended'].sum().sort_values(ascending=False)
print("\nعدد المرضى لكل قسم (ضغط العمل):\n", dept_workload)

# ------------------------------
# 7. تحليل العمليات
# ------------------------------
plt.figure(figsize=(10,6))
sns.barplot(data=operations, x='type', y='success_rate', hue='department')
plt.title("Operation success rate by type and department")
plt.xticks(rotation=45)
plt.show()

low_success = operations[operations['success_rate'] < 0.9]
print("\nالعمليات التي تحتاج تحسين:\n", low_success)

# ------------------------------
# 8. التحليل المالي
# ------------------------------
finance['profit'] = finance['revenue'] - finance['expenses']
plt.figure(figsize=(10,6))
sns.barplot(data=finance, x='department', y='profit')
plt.title("Profits per division")
plt.xticks(rotation=45)
plt.show()

low_profit = finance[finance['profit'] < finance['profit'].mean()]
print("\nالأقسام الأقل ربحًا:\n", low_profit)

# ------------------------------
# 9. توصيات عملية
# ------------------------------
print("\nتوصيات المستشفى:")
print("- زيادة عدد الطاقم في الأقسام ذات ضغط العمل العالي:", dept_workload.idxmax())
print("- تحسين بروتوكولات العمليات ذات معدل نجاح منخفض:", list(low_success['type']))
print("- إعادة تقييم الأقسام الأقل ربحًا لتقليل المصاريف أو زيادة الإيرادات:", list(low_profit['department']))
print("- مراقبة مدة الإقامة وتقليلها للأمراض ذات مدة إقامة طويلة لتحسين الكفاءة")
