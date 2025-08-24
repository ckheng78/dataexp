from tools.data_tool import create_json_from_data
from pathlib import Path

file_path = Path('data') / 'titanic.csv'
temp_path = Path('temp')
temp_path.mkdir(exist_ok=True)  # Ensure temp directory exists
temp_path = temp_path / 'output.json'

output = create_json_from_data.run(file_path)
with open(temp_path, 'w+') as f:
    f.write(output)
