import os
import json
from groq import Groq  # Assuming 'groq' module is correctly imported and available

# Function to load JSON data from file
def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

# Initialize Groq client
groq_api_key = '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'
client = Groq(api_key=groq_api_key)

# Define JSON schema for micro-industries
json_schema = {
    "micro-industry": "",
    "sections": {
        "Introduction": {
            "definition": "",
            "scope": ""
        },
        "Types of Businesses": [],
        "Activities": [],
        "Top Brands": {
            "Americas": [],
            "EMEA": [],
            "Asia-Pacific": []
        }
    }
}

# Directory to save generated JSON files
output_dir = "C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/"

# Load micro-industry data
midata_file = "C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/microIndustries.json"
micro_industries_data = load_json(midata_file)
micIndustry_array = micro_industries_data.get('micro-industries', [])

# Process each micro-industry
for idx, microIndustry in enumerate(micIndustry_array, start=1):
    # Prompt for Groq API
    prompt = f"""Act as a business expert with a great deal of understanding and experience in the various industries and micro-industries. 
                Explain the following micro-industry: {microIndustry}. Write the content in the following main sections: "Introduction", 
                "Types of Businesses" and "Activities", as follows:
                - "Introduction" which provides a definition of the micro-industry, which briefly explains the purpose of the micro industry 
                  and what is the micro-industry about (this should be exactly 1 paragraph), followed by an explanation of the scope of this 
                  micro-industry and its relevance within its broader industry (this should be exactly 1 paragraph as well).
                - "Types of Businesses" The micro-industry comprises of a diverse array of businesses. List the most prevalent types of businesses 
                  in this paragraph. List the types of businesses in a bulleted list. Use the following format: "**Retail Stores**: Large chain 
                  stores and small local shops that sell tools, materials, and supplies for DIY projects."
                - "Activities" Explain and list the activities covered and offered by the micro-industry in this paragraph. List the activities in 
                  a bulleted list. Use the following format: "**Renovation Projects**: Updating kitchens, bathrooms, living spaces, and other areas 
                  to improve functionality and aesthetics."
                - "Top Brands": the top brands for this micro industry, grouped by regions - Americas, EMEA, Asia-Pacific.
                the information must match this JSON schema:"""

    # Generate JSON based on the schema and prompt
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are expected to generate a JSON object based on the following schema:\n\n{json.dumps(json_schema)}. Extract as much data as you can, make sure everything fits in the JSON structure."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            stream=False,
            response_format={"type": "json_object"}
        )

        # Extract and save JSON output
        json_output = completion.choices[0].message.content.strip()
        output_filename = f"MI{idx}.json"
        output_filepath = os.path.join(output_dir, output_filename)
        with open(output_filepath, "w") as f:
            json.dump(json.loads(json_output), f, indent=4)
            print(f"Generated JSON saved to: {output_filepath}")

    except Exception as e:
        print(f"Error generating JSON for micro-industry {idx}: {e}")

# End of script
   