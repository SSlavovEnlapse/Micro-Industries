import os
import json
from groq import Groq

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def load_json_files(filepath):
    json_files = []
    for filename in os.listdir(filepath):
        if filename.endswith('.json'):
            with open(os.path.join(filepath, filename), 'r') as file:
                data = json.load(file)
                json_files.append(data)
    return json_files

# Validate and clean the JSON output
def validate_and_clean_json(json_str):
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Attempt to clean the JSON string
        cleaned_json_str = json_str[json_str.find("["):json_str.rfind("]")+1]
        return json.loads(cleaned_json_str)

def main(input_dir, output_dir):
    groq_api_key = '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'
    client = Groq(api_key=groq_api_key)

    input_file = 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/microIndustries.json'
    micro_industries_data = load_json(input_file)
    mi_profile_list = load_json_files(input_dir)

    json_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "Call Direction": {
                    "type": "string",
                    "enum": ["inbound", "outbound"]
                },
                "Call Type": {
                    "type": "string"
                },
                "Call Type Description": {
                    "type": "string"
                },
                "Common Inquiries": {
                    "type": "string",
                    "pattern": "^[a-zA-Z, ]+$"
                }
            },
            "required": ["Call Direction", "Call Type", "Call Type Description", "Common Inquiries"]
        }
    }

    for idx, micro_industry_profile in enumerate(mi_profile_list, start=1):
        micro_industry_type = micro_industries_data.get('micro-industry', '')
        try:
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[ 
                    {
                        "role": "system",
                        "content": f"""generate information based on the following requirements and JSON schema:\n- \"Call Direction\"- can be \"inbound\" or \"outbound\" only\n- \"Call Type\" - examples here are: Information Inquiry, Customer Complaint and Feedback, etc.\n- \"Call Type Description\" - be as detailed and verbose as possible in your description for each call type\n- \"Common Inquiries\" - this is a comma-separated list of the most common inquiries for this call type. Examples include: Opening Hours, Product Options, Special Offers, etc.\n\n.This  is the schema, make sure you format the data correctly :\n\n{json.dumps(json_schema)}.Your response should be strictly in JSON format, DO NOT include any other sentences and text that is not in JSON format.Return only the JSON object"""
                    },
                    {
                        "role": "user",
                        "content": f"""Act as an expert coach and consultant in contact center call evaluation and scoring with great experience in the subject. I'll give you a micro-industry and its profile. Your job is to create a list of the top 5 most-prevalent inbound contact center call types and the top 5 most-prevalent outbound contact center call types.Give information on exactly 5 inbound calls and exactly 5 outbound calls.\n\nThe micro-industry is:{micro_industry_type}.The profile of the micro-industry follows:{micro_industry_profile}.Return the result in a JSON array."""
                    }
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )

            json_output = completion.choices[0].message.content.strip()
            cleaned_json_output = validate_and_clean_json(json_output)

            output_filename = f"CallsInfo_{idx}.json"
            output_filepath = os.path.join(output_dir, output_filename)
            with open(output_filepath, "w") as f:
                json.dump(cleaned_json_output, f, indent=4)
                print(f"Generated JSON saved to: {output_filepath}")
                
        except Exception as e:
            print(f"Error generating JSON for micro-industry {idx}: {e}")

if __name__ == "__main__":
    input_dir = 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/LeadBrandsInfo'
    output_dir = 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/CallCenterCallTypesInfo'

    main(input_dir, output_dir)
