import subprocess

def run_script(script_name, input_dir, output_dir):
    result = subprocess.run(['python', script_name,  input_dir, output_dir], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script_name}: {result.stderr}")
    else:
        print(f"Successfully ran {script_name}")
    return result.returncode

def main():
    scripts = [
        ('C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/MicroIndustriesDataCollection.py', 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/microIndustries.json', 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/MicroIndustriesProfiles'),
        ('C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/GlobalCompaniesBranches.py', 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/MicroIndustriesProfiles', 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/LeadBrandsInfo'),
        ('C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/microIndustriesCallCenterCallTypes.py', 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/MicroIndustriesProfiles', 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/CallCenterCallTypesInfo'),
        ('C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/ScoringTemplate.py', 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/CallCenterCallTypesInfo', 'C:/Users/sslavov/Desktop/python api calls/First API Call/Micro-Industries/ScoringTemplates')
    ]

    for script, input_path, output_dir in scripts:
        return_code = run_script(script, input_path, output_dir)
        if return_code != 0:
            print(f"Terminating script chain due to error in {script}")
            break

if __name__ == "__main__":
    main()
