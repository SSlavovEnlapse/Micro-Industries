import os
import json
from groq import Groq
import random

groq_api_key = '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'
client = Groq(api_key=groq_api_key)

# Function to load JSON data from file - the 3 different micro-industries
def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)
    
# Function to load JSON data from file - multiple JSONs
def load_json_files(filepath):
    json_files = []
    for filename in os.listdir(filepath):
        if filename.endswith('.json'):
            with open(os.path.join(filepath, filename), 'r') as file:
                data = json.load(file)
                json_files.append(data)
    return json_files

# Load micro-industry types
differentMI_filepath = "C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/microIndustries.json"
micro_industries_data = load_json(differentMI_filepath)
micIndustry_array = micro_industries_data.get('micro-industries', [])

# Load micro-industry profile
miProfile_filepath="C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/MicroIndustriesProfiles"
mi_profile_list = load_json_files(miProfile_filepath)

# Load call information 
miCallsInfo_filepath="C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/CallCenterCallTypesInfo"
mi_calls_list = load_json_files(miCallsInfo_filepath)

# Output directory for JSON files
output_dir="C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/ScoringTemplates"

def parse_introductions(mi_profiles):
    introductions = []
    for profile in mi_profiles:
        intro = profile["sections"]["Introduction"]
        concatenated_intro = f"{intro['definition']} {intro['scope']}"
        introductions.append(concatenated_intro)
    return introductions

# Parsing the Introduction sections from the mi_profile_list
introduction_list = parse_introductions(mi_profile_list)

def parse_activities(mi_profiles):
    activities_list = []
    for profile in mi_profiles:
        activities = profile["sections"]["Activities"]
        formatted_activities = []
        for idx, activity in enumerate(activities, 1):
            activity = activity.replace("**", "")  # Remove asterisks
            formatted_activities.append(f"{idx}. {activity}")
        activities_list.append("\n".join(formatted_activities))
    return activities_list

# Parsing the Activities sections from the mi_profile_list
activities_list = parse_activities(mi_profile_list)

def parse_types_of_businesses(mi_profiles):
    businesses_list = []
    for profile in mi_profiles:
        businesses = profile["sections"]["Types of Businesses"]
        formatted_businesses = []
        for idx, business in enumerate(businesses, 1):
            business = business.replace("**", "")  # Remove asterisks
            formatted_businesses.append(f"{idx}. {business}")
        businesses_list.append("\n".join(formatted_businesses))
    return businesses_list

# Parsing the Types of Businesses sections from the mi_profile_list
businesses_list = parse_types_of_businesses(mi_profile_list)

def format_call_types(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON from file '{filepath}'.")
        return []

    formatted_calls = []

    for call_type in data:
        formatted_call = (
            f"Contact Center Call Type: {call_type['Call Type']}\n"
            f"Contact Center Call Type Description: {call_type['Call Type Description']}\n"
            f"Contact Center Call Type Common Queries: {call_type['Common Inquiries']}\n"
        )
        formatted_calls.append(formatted_call)
    
    return formatted_calls
# Parsing Contact Center Call Type Info
calls_1_filepath = "C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/CallCenterCallTypesInfo/CallsInfo_1.json"
calls_2_filepath = "C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/CallCenterCallTypesInfo/CallsInfo_2.json"
calls_3_filepath = "C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/CallCenterCallTypesInfo/CallsInfo_3.json"
calls_for_mi1_list = format_call_types(calls_1_filepath)
calls_for_mi2_list = format_call_types(calls_2_filepath)
calls_for_mi3_list = format_call_types(calls_3_filepath)

# Validate and clean the JSON output
def validate_and_clean_json(json_str):
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                # Attempt to clean the JSON string
                cleaned_json_str = json_str[json_str.find("{"):json_str.rfind("}")+1]
                return json.loads(cleaned_json_str)

# Predefined JSON schema to pass the prompt
json_schema = {
    "Index": "",
    "Section": "",
    "Question": "",
    "Scoring": "",
    "Scoring Criteria": ""
}

# Function to find the current call list
def find_current_call_list(idx):
    if idx==0:
        current_call_list = calls_for_mi1_list
    elif idx==1:
        current_call_list = calls_for_mi2_list
    elif idx==2:
        current_call_list = calls_for_mi3_list
    else:
        print(f"No file defined for index {idx}")
    return current_call_list

system_prompt = f"""Your response should follow a predefined structure which will be passed to you as context. """

# Loop for API call
for idx, microIndustry in enumerate(micIndustry_array, start=0):

    current_call_list = find_current_call_list(idx)
    random_call_index = random.randint(0, 9)
    try:
        completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[ 
        {
                    "role": "system",
                    "content": system_prompt
        },
        {
            "role": "user",
            "content": f"""Act as an expert contact center call scoring coach with great experience in the subject. 

            I'll give you a generic Contact Center Call Scoring Template as a reference. 

            Your task is to generate a new Contact Center Call Scoring Template for a specific micro-industry, adhering to the rules and guidelines below. 

            Make sure you cover all sections and questions from the example given below in your output. Do not skip a question unless absolutely necessary to do so. 

            The micro-industry is: {microIndustry}

            The micro-industry profile is:
            {introduction_list[idx]}

            Activities
            {activities_list[idx]}

            Types of Businesses
            {businesses_list[idx]}


            Contact Center Call Type Info
            {current_call_list[random_call_index]}


            The Contact Center Call Scoring template should have the following sections:
            - Greeting 
            - Customer Identification 
            - Needs Identification 
            - Solution Proposal 
            - Value Add / Upsell 
            - Closing 
            - Rapport

            The output format should be a table with the following columns: 
            - Index (example: 1, 2, 3, ...) 
            - Section 
            - Question 
            - Scoring 
            - Scoring Criteria (write the criteria for each scoring option on a new line and be as detailed as possible)

            Your response must look like the 'Contact Center Call Scoring Template' I will provide to you. That means your response must be the same size (26 rows).Make sure you align the '|' as much as you can.
            The Contact Center Call Scoring Template to use as a general reference follows in a markdown table format:

            | Index | Section                 | Question                                                                                       | Scoring  | Scoring Criteria                                                                                  |
            |-------|-------------------------|------------------------------------------------------------------------------------------------|----------|---------------------------------------------------------------------------------------------------|
            | 1     | Greeting                | Did the agent greet the customer promptly and courteously?                                     | Yes / No | **Yes:** Agent greeted the customer within 5 seconds of connection, using phrases like "Good morning/afternoon/evening" in a friendly and upbeat tone. **No:** Agent took longer than 5 seconds to greet or used a monotone/apathetic tone. |
            | 2     | Greeting                | Did the agent introduce themselves and the company they represent?                             | Yes / No | **Yes:** Agent clearly stated their full name and the company's name within the first 10 seconds of the call, e.g., "Hello, this is [Agent's Name] from [Company Name]." **No:** Agent failed to provide their name or the company's name, or mumbled it so it was unclear. |
            | 3     | Greeting                | Did the agent thank the customer for contacting the company?                                   | Yes / No | **Yes:** Agent explicitly thanked the customer by saying something like "Thank you for calling [Company Name]." **No:** Agent did not express any form of gratitude. |
            | 4     | Customer Identification | Did the agent verify the customer's identity as appropriate?                                   | Yes / No / N/A | **Yes:** Agent followed security protocols by asking for 2-3 pieces of verification information (e.g., account number, date of birth) and confirmed them against company records. **No:** Agent skipped verification or did it improperly, risking a security breach. **N/A:** Verification not required for the nature of the call. |
            | 5     | Customer Identification | Did the agent confirm the customer's contact details and information?                          | Yes / No | **Yes:** Agent repeated back key information such as phone number, email, or address for confirmation and asked the customer to verify its accuracy. **No:** Agent did not confirm or repeated information incorrectly. |
            | 6     | Customer Identification | Did the agent ensure the customer's account information was up to date?                       | Yes / No | **Yes:** Agent asked if there were any updates to contact or account information and made necessary changes in the system. **No:** Agent did not inquire about or update any account information. |
            | 7     | Needs Identification    | Did the agent listen actively to the customer's issue without interrupting?                    | Yes / No | **Yes:** Agent allowed the customer to fully explain their issue without interruption, used verbal nods ("I understand," "Right," "Please go on") to show attentiveness. **No:** Agent interrupted the customer multiple times or appeared to be distracted. |
            | 8     | Needs Identification    | Did the agent ask relevant clarifying questions to understand the issue better?                | Yes / No | **Yes:** Agent asked specific, open-ended questions related to the issue ("Can you tell me more about...?"). **No:** Agent asked irrelevant or no clarifying questions, leading to misunderstandings. |
            | 9     | Needs Identification    | Did the agent summarize the customer's issue to confirm understanding?                        | Yes / No | **Yes:** Agent recapped the main points of the customer's issue accurately before proceeding, saying something like, "So, to confirm, you're having an issue with...". **No:** Agent did not summarize or summarized incorrectly, causing confusion. |
            | 10    | Solution Proposal       | Did the agent demonstrate knowledge of the product/service?                                    | Yes / No | **Yes:** Agent provided detailed and accurate information about the product/service, including relevant features and functionality. **No:** Agent gave incorrect information, was unsure, or had to repeatedly consult a knowledge base. |
            | 11    | Solution Proposal       | Did the agent provide an accurate and appropriate solution to the issue?                       | Yes / No | **Yes:** Agent offered a solution that directly addressed the customer's issue and explained why it would work. **No:** Agent suggested irrelevant solutions or failed to provide a solution altogether. |
            | 12    | Solution Proposal       | Did the agent explain the solution clearly and comprehensively?                                | Yes / No | **Yes:** Agent used direct and simple language to explain the solution step-by-step, ensuring the customer understood. **No:** Agent used technical jargon, spoke too quickly, or did not explain the solution fully. |
            | 13    | Solution Proposal       | Did the agent discuss any potential risks or downsides of the proposed solution?               | Yes / No / N/A | **Yes:** Agent clearly outlined any potential risks, side effects, or limitations of the solution, and suggested precautions if applicable. **No:** Agent failed to mention significant risks or limitations. **N/A:** No potential risks or downsides associated with the solution. |
            | 14    | Value Add / Upsell      | Did the agent offer any additional products or services that could benefit the customer?        | Yes / No / N/A | **Yes:** Agent identified and suggested relevant additional products or services tailored to the customer's needs without being pushy. **No:** Agent missed an opportunity for a relevant upsell. **N/A:** Upsell not applicable in the context of the call. |
            | 15    | Value Add / Upsell      | Did the agent explain the benefits of the additional products or services?                      | Yes / No / N/A | **Yes:** Agent clearly outlined how the additional product/service would benefit the customer, using specific examples or scenarios. **No:** Agent did not explain the benefits or did so inadequately. **N/A:** Upsell not applicable. |
            | 16    | Value Add / Upsell      | Did the agent handle any objections to the upsell professionally and effectively?               | Yes / No / N/A | **Yes:** Agent acknowledged the customer's objections, addressed concerns calmly, and provided additional information to alleviate doubts. **No:** Agent dismissed objections or responded defensively. **N/A:** No objections raised or upsell not applicable. |
            | 17    | Closing                 | Did the agent confirm the resolution or next steps with the customer?                          | Yes / No | **Yes:** Agent summarized what was done or what will happen next, including timeframes if applicable, and confirmed the customer’s understanding. **No:** Agent did not confirm the resolution or next steps. |
            | 18    | Closing                 | Did the agent offer any additional assistance before ending the call?                          | Yes / No | **Yes:** Agent asked an open-ended question such as, "Is there anything else I can help you with today?" **No:** Agent did not inquire if further assistance was needed. |
            | 19    | Closing                 | Did the agent close the call courteously?                                                      | Yes / No | **Yes:** Agent used a polite closing statement like, "Thank you for calling, and have a great day!" **No:** Agent ended the call abruptly or without a courteous closing. |
            | 20    | Closing                 | Did the agent ensure the customer was satisfied with the resolution before ending the call?   | Yes / No | **Yes:** Agent explicitly asked if the customer was satisfied with the resolution and if they had any more concerns. **No:** Agent did not check the customer's satisfaction level before ending the call. |
            | 21    | Rapport                 | Did the agent show empathy and understanding of the customer's concerns?                       | Yes / No | **Yes:** Agent used empathetic statements like, "I understand how frustrating this must be for you," and validated the customer’s feelings. **No:** Agent did not acknowledge the customer's emotions or came across as indifferent. |
            | 22    | Rapport                 | Did the agent personalize the interaction (e.g., using the customer's name)?                   | Yes / No | **Yes:** Agent used the customer's name multiple times during the call and referenced specific details relevant to the customer’s situation. **No:** Agent did not use the customer's name or personalize the conversation. |
            | 23    | Rapport                 | Did the agent maintain a courteous and professional tone throughout the call?                  | Yes / No | **Yes:** Agent consistently used polite language, maintained a professional demeanor, and showed respect throughout the call. **No:** Agent used informal, slang, or rude language, or was condescending. |
            | 24    | Rapport                 | Did the agent use clear and understandable language?                                           | Yes / No | **Yes:** Agent used simple, jargon-free language that was easy for the customer to understand. **No:** Agent used technical terms without explanation or spoke too quickly. |
            | 25    | Rapport                 | Did the agent handle any difficult situations or objections calmly and effectively?            | Yes / No | **Yes:** Agent stayed calm, listened actively, acknowledged the customer's frustration, and provided clear, constructive responses. **No:** Agent became defensive, raised their voice, or failed to manage the situation effectively. |
            | 26    | Rapport                 | Did the agent make the customer feel valued and appreciated?                                   | Yes / No | **Yes:** Agent made positive affirmations, thanked the customer for their business, and made feel their issue was important. **No:** Agent did not make any effort to make the customer feel valued or appreciated. |"""
        }
        ],
        temperature=1   
        )
        
        # Retrieving the response from chat completion and cleaning the JSON
        '''json_output = completion.choices[0].message.content.strip()
        cleaned_json_output = validate_and_clean_json(json_output)
        print(json.dumps(cleaned_json_output, indent=4))'''
        text_output_path = os.path.join(output_dir, "text.txt")
        with open(text_output_path, "a") as text_file:
            text_file.write(f"Micro-industry {idx+1}:\n")
            text_file.write(completion.choices[0].message.content + "\n\n")
            print(f"Output for micro-industry {idx+1} saved to text.txt")
    except Exception as e:
        print("error")