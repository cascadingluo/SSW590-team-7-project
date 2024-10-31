import pandas as pd

# Load the JSONL file
file_path = './ava_dataset.jsonl'
data = pd.read_json(file_path, lines=True)

# Select only the 'patterns' and 'responses' columns and rename them
data_converted = data[['patterns', 'responses']].copy()
data_converted.columns = ['text_input', 'output']

# Convert lists within the 'text_input' and 'output' columns to strings for CSV compatibility
data_converted['text_input'] = data_converted['text_input'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
data_converted['output'] = data_converted['output'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

# Save the modified data to a CSV file
csv_file_path = 'ava_dataset_converted.csv'
data_converted.to_csv(csv_file_path, index=False)

print(f"CSV file saved at {csv_file_path}")
