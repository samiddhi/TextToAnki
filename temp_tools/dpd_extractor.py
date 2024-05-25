import sqlite3
import pandas as pd
import json
import json_maker

### NOTE: Requires dpd.db tarball file from digital pali dictionary release

# Connect to the SQLite database
conn = sqlite3.connect('dpd.db')

# Function to query the database and return a DataFrame
def query_db(query):
    return pd.read_sql_query(query, conn)

if __name__ == "__main__":
    query = "SELECT lemma_1, inflections FROM dpd_headwords;"
    df_forward = query_db(query)

    # Process inflections from a comma-separated string to a list of strings
    df_forward['inflections'] = df_forward['inflections'].apply(
        lambda x: x.split(',') if isinstance(x, str) else x)

    # Convert DataFrame to a dictionary mapping lemmas to lists of inflections
    forward_dict = df_forward.set_index('lemma_1')['inflections'].to_dict()

    forward_mapping_filename = 'pali_forward_mapping.json'
    # Save to JSON with nice formatting using the json module
    with open(forward_mapping_filename, 'w', encoding='utf-8') as f:
        json.dump(forward_dict, f, ensure_ascii=False, indent=4)

    backward_mapping_filename = 'pali_backward_mapping.json'
    json_maker.reverse_json_writer(
        read=forward_mapping_filename,
        write=backward_mapping_filename
    )