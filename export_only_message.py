import sys
import json
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
json_file_path = 'vxunderground_messages.json'
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    messages = data["messages"]
    df = pd.DataFrame(messages)
    filtered_data = df[['date', 'edit_date', 'id', 'message']]
    output_json_path = 'mesajlar.json'
    filtered_data.to_json(output_json_path, orient='records', lines=True, force_ascii=False)
    output_csv_path = 'mesajlar.csv'
    filtered_data.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"Dosyalar oluşturuldu")
