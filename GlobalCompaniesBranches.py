import os
import sys
from groq import Groq
import json

def load_json_files(filepath):
    json_files = []
    for filename in os.listdir(filepath):
        if filename.endswith('.json'):
            with open(os.path.join(filepath, filename), 'r') as file:
                data = json.load(file)
                json_files.append(data)
    return json_files

def main(input_dir, output_dir):
    groq_api_key = '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'
    client = Groq(api_key=groq_api_key)

# Validate and clean the JSON output
    def validate_and_clean_json(json_str):
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Attempt to clean the JSON string
            cleaned_json_str = json_str[json_str.find("{"):json_str.rfind("}")+1]
            return json.loads(cleaned_json_str)


    # Load micro industries info in JSON list
    json_data_list = load_json_files(input_dir)

    for idx, miLeadBrands in enumerate(json_data_list, start=1):
        try:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are expected to generate a JSON object based on the following schema: {{\n        \"market_leader_branches\": [\n            {{\n                \"company_name\": \"Company Name\",\n                \"dominating_countries\": [\"Country1\", \"Country2\"],\n                \"annual_earnings\": \"Annual Earnings\",\n                \"total_customers\": NumberOfCustomers,\n                \"ceo\": {{\n                    \"name\": \"CEO Name\"\n                }}\n            }}\n        ]\n    }}. Extract as much data as you can, make sure everything fits in the JSON structure."
                    },
                    {
                        "role": "user",
                        "content": f"Consider the 'Top Brands' section in {miLeadBrands}. Provide information about company(brand) name, dominating countries, annual earnings, total customers and ceo name."
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
            validated_completion = validate_and_clean_json(response)
            output_filename = f"response_{idx}.json"  # Dynamically generate filename based on idx
            output_filepath = os.path.join(output_dir, output_filename)
            with open(output_filepath, 'w') as outfile:
                json.dump(validated_completion, outfile, ensure_ascii=False, indent=4)
            print(f"Generated JSON saved to: {output_filepath}")

        except Exception as e:
            print(f"Error generating JSON for lead brand {idx}: {e}")

if __name__ == "__main__":

    input_dir = 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/MicroIndustriesProfiles'
    output_dir = 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/LeadBrandsInfo'

    main(input_dir, output_dir)

