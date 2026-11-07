import json
import pandas as pd

file_path = r"C:\Users\User\Downloads\1580.lutskrada.gov.ua.json"
output_csv = r"C:\Users\User\Downloads\1580.lutskrada.gov.ua.csv"

# 1. Завантажуємо JSON для аналізу структури
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. Виводимо структуру у консоль для перевірки
print("--- Тип кореневого елемента ---")
print(type(data))

if isinstance(data, dict):
    print("\n--- Ключі верхнього рівня ---")
    print(list(data.keys()))
elif isinstance(data, list) and len(data) > 0:
    print("\n--- Ключі першого елемента списку ---")
    if isinstance(data[0], dict):
        print(list(data[0].keys()))

# 3. Трансформуємо в CSV
# json_normalize автоматично розгортає вкладені словники/об'єкти
if isinstance(data, list):
    df = pd.json_normalize(data)
elif isinstance(data, dict):
    # Якщо основні дані лежать у якомусь конкретному ключі (наприклад, data['data'] або data['items'])
    # pandas спробує розгорнути весь словник:
    df = pd.json_normalize(data)

# 4. Зберігаємо в CSV з кодуванням utf-8-sig (щоб коректно відкривалося в Excel з кирилицею)
df.to_csv(output_csv, index=False, encoding="utf-8-sig", sep=";")

print(f"\nФайл успішно збережено в: {output_csv}")
print(f"Розмірність таблиці: {df.shape[0]} рядків, {df.shape[1]} колонок.")