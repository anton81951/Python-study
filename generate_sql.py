fields = [f"string_field_{i}" for i in range(418)]
fields_sql = ", ".join(fields)

sql_query = f"""
SELECT 
  ARRAY_TO_STRING(
    ARRAY(
      SELECT field 
      FROM UNNEST([{fields_sql}]) AS field
      WHERE field IS NOT NULL AND field != ''
    ), ' '
  ) AS concatenated_text
FROM `arma-database.main.arma`
LIMIT 100;
"""

print(sql_query)
