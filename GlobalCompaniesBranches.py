import os
from groq import Groq
import json

groq_api_key = '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'
client = Groq(api_key=groq_api_key)

def load_json_files(filepath):
    json_files = []
    for filename in os.listdir(filepath):
        if filename.endswith('.json'):
            with open(os.path.join(filepath, filename), 'r') as file:
                data = json.load(file)
                json_files.append(data)
    return json_files

#Filepath of MI1, MI2 ,MI3
jsonfiles_filepath="C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/MicroIndustriesProfiles"

#micro industris info in JSON list
json_data_list = load_json_files(jsonfiles_filepath)
#json schema used as a tempalte for the answer of the completion

output_path="C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/LeadBrandsInfo/"

for idx, miLeadBrands in enumerate(json_data_list, start=1):
    completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "system",
            "content": "You are expected to generate a JSON object based on the following schema: {{\n        \"market_leader_branches\": [\n            {{\n                \"company_name\": \"Company Name\",\n                \"dominating_countries\": [\"Country1\", \"Country2\"],\n                \"annual_earnings\": \"Annual Earnings\",\n                \"total_customers\": NumberOfCustomers,\n                \"ceo\": {{\n                    \"name\": \"CEO Name\"\n                }}\n            }}\n        ]\n    }}. Extract as much data as you can, make sure everything fits in the JSON structure.\"},"
        },
        {
            "role": "user",
            "content": f"Consider the 'Top Brands' section in {miLeadBrands}. Provide information about company(brand) name, dominating countries, annual earnings, total cistomers and ceo name."
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    response_format={"type": "json_object"},
    stop=None,
    )
    response = completion.choices[0].message.content.strip()
    output_filename = f"response_{idx}.json"  # Dynamically generate filename based on idx
    with open(output_path+output_filename, 'w') as outfile:
        json.dump(json.loads(response), outfile, indent=4)
    print(completion.choices[0].message)
