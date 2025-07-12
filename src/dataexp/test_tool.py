from tools.data_tool import create_json_from_data

output = create_json_from_data.run(f"data\\titanic.csv")
with open(f'temp\\output.json', 'w+') as f:
    f.write(output)
