import sys
import json
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
json_file_path = 'vxunderground_messages.json'
keywords_file_path = 'keywords.txt'

def find_keywords(text, keywords):
    if pd.isna(text):
        return ''
    matched = [keyword for keyword in keywords if keyword.lower() in text.lower()]
    return '; '.join(matched)

with open(keywords_file_path, 'r', encoding='utf-8') as f:
    keywords = [line.strip() for line in f if line.strip()]
    
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

    messages = data["messages"]
    df = pd.DataFrame(messages)
    filtered_data = df[['date', 'edit_date', 'id', 'message']].copy()

    filtered_data.loc[:, 'matched_keywords'] = filtered_data['message'].apply(lambda x: find_keywords(x, keywords))

    # Eşleşen kelimelere sahip olanları filtrele
    mask = filtered_data['matched_keywords'] != ''
    filtered_data = filtered_data[mask].reset_index()

    # 'index' sütununu 'message_index' olarak yeniden adlandır
    filtered_data.rename(columns={'index': 'message_index'}, inplace=True)

    # JSON çıktısı
    output_json_path = 'filtered_messages.json'
    filtered_data.to_json(output_json_path, orient='records', lines=True, force_ascii=False)

    # CSV çıktısı
    output_csv_path = 'filtered_messages.csv'
    filtered_data.to_csv(output_csv_path, index=False, encoding='utf-8-sig')

    print(f"Filtered data has been written to {output_json_path} and {output_csv_path}")
