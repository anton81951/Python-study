import glob
import os
import re
import pandas as pd
from docx import Document

# 1. Шляхи до папок та файлів
orders_dir = r"C:\служба\унікальні донесення\2026.10\обробка РС наказів\накази"
excel_path = (
    r"C:\служба\унікальні донесення\2026.10\обробка РС наказів\список"
    r" контрактників виключених.xlsx"
)
output_excel_path = (
    r"C:\служба\унікальні донесення\2026.10\обробка РС"
    r" наказів\Результат_обробки_виключених.xlsx"
)


def load_excluded_contractors_ipn(excel_file):
  """Зчитує список ІПН виключених контрактників з 4-ї колонки (D) аркуша Sheet1."""
  if not os.path.exists(excel_file):
    print(f"Помилка: Файл {excel_file} не знайдено!")
    return set()

  try:
    # Читаємо Sheet1 та перетворюємо всі значення у рядковий тип (str)
    df = pd.read_excel(excel_file, sheet_name="Sheet1", dtype=str)
    # Отримуємо значення з колонки D (індекс 3)
    ipn_series = df.iloc[:, 3].dropna().str.strip()
    return set(ipn_series)
  except Exception as e:
    print(f"Помилка при читанні Excel-файлу: {e}")
    return set()


def process_order_document(doc_file, contractors_ipn):
  """Опрацьовує один документ Word, витягує фрагменти та формує підсумкові дані."""
  try:
    doc = Document(doc_file)
  except Exception as e:
    print(f"  [!] Не вдалося відкрити файл {os.path.basename(doc_file)}: {e}")
    return []

  doc_name = os.path.basename(doc_file)

  # Шукаємо загальну дату наказу (наприклад, “01” жовтня 2026 року)
  doc_text = "\n".join([p.text for p in doc.paragraphs])
  date_match = re.search(
      r'“\d{2}”\s+[а-яА-Яа-щА-ЩЬьЮюЯяЇїІіЄєҐґ]+\s+\d{4}\s+року', doc_text
  )
  general_date = date_match.group(0) if date_match else "Дата не знайдена"

  results = []

  current_paragraph = "§ 1"  # Значення за замовчуванням
  current_item_lines = []

  item_start_pattern = re.compile(r'^\s*(\d+)\.\s+')
  paragraph_pattern = re.compile(r'^\s*(§\s*\d+)')

  for p in doc.paragraphs:
    text = p.text.strip()
    if not text:
      continue

    # Перевіряємо, чи є рядок номером параграфа (наприклад, § 2)
    paragraph_match = paragraph_pattern.match(text)
    if paragraph_match:
      current_paragraph = paragraph_match.group(1)
      continue

    # Перевіряємо, чи починається рядок з нового пронумерованого пункту (наприклад, "2.")
    item_match = item_start_pattern.match(text)
    if item_match:
      if current_item_lines:
        full_fragment = "\n".join(current_item_lines)
        process_fragment(
            full_fragment,
            doc_name,
            general_date,
            current_paragraph,
            contractors_ipn,
            results,
        )

      current_item_lines = [text]
    else:
      if current_item_lines:
        current_item_lines.append(text)

  # Обробка останнього пункту в документі
  if current_item_lines:
    full_fragment = "\n".join(current_item_lines)
    process_fragment(
        full_fragment,
        doc_name,
        general_date,
        current_paragraph,
        contractors_ipn,
        results,
    )

  return results


def process_fragment(
    fragment_text,
    doc_name,
    general_date,
    section_num,
    contractors_ipn,
    results_list,
):
  """Витягує ІПН із фрагмента та перевіряє його наявність у списку виключених контрактників."""
  ipn_matches = re.findall(r'\b\d{10}\b', fragment_text)

  for ipn in ipn_matches:
    if ipn in contractors_ipn:
      results_list.append({
          'Назва документу': doc_name,
          'Загальна дата наказу': general_date,
          'Поточна сторінка / параграф': section_num,
          'Вибраний ІПН': ipn,
          'Повний текстовий фрагмент': fragment_text,
      })


# --- ОСНОВНИЙ БЛОК ВИКОНАННЯ ---
if __name__ == '__main__':
  print("1. Завантаження списку виключених контрактників з аркуша Sheet1...")
  contractors = load_excluded_contractors_ipn(excel_path)
  print(f"   Знайдено ІПН виключених: {len(contractors)}")

  # Отримуємо список усіх файлів .docx із вказаної папки
  search_pattern = os.path.join(orders_dir, '*.docx')
  docx_files = glob.glob(search_pattern)

  # Ігноруємо тимчасові файли Word (~$)
  docx_files = [f for f in docx_files if not os.path.basename(f).startswith('~$')]

  print(f"\n2. Знайдено {len(docx_files)} наказів для обробки.")

  all_results = []

  for idx, docx_path in enumerate(docx_files, start=1):
    doc_name = os.path.basename(docx_path)
    print(f"[{idx}/{len(docx_files)}] Обробка: {doc_name}...")

    file_results = process_order_document(docx_path, contractors)
    all_results.extend(file_results)

  # Збереження підсумкового Excel-файлу
  print('\n3. Формування підсумкового Excel-файлу...')
  if all_results:
    res_df = pd.DataFrame(all_results)
    res_df.to_excel(output_excel_path, index=False)
    print(f"УСПІШНО: Збережено {len(res_df)} записів у файл:")
    print(f"   -> {output_excel_path}")
  else:
    print('[!] Увага: Не знайдено жодного фрагмента із збігом по ІПН.')