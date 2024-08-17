import csv

txt_file_path = r'C:\Users\anton\OneDrive\Documents\GitHub\Python-study\edraa_opendata_text.txt'
csv_file_path = r'C:\Users\anton\OneDrive\Documents\GitHub\Python-study\edraa_opendata_text.csv'

with open(txt_file_path, 'r', encoding='utf-8') as txt_file, open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file)
    
    for line in txt_file:
        stripped_line = line.strip()
        
        columns = stripped_line.split(',')
        
        writer.writerow(columns)

print(f"Data successfully converted to {csv_file_path}")
