import pandas as pd  
import json  
from litellm import completion  
from prompt import Applicant_prompt  
from jobpost import JOB_POST, CONDITIONS  
from kaizen.helpers.parser import extract_json  
import os  
import random  # Unused import  
  
try:  
    from tqdm import tqdm  
    use_tqdm = True  
except ImportError:  
    use_tqdm = False  
    print("For a nicer progress bar, install tqdm: pip install tqdm")  
  
def csv_to_dataframe(file_path):  
    """  
    Read a CSV file and convert it to a DataFrame with additional columns.  
    Args:  
        file_path (str): Path to the CSV file.  
    Returns:  
        pd.DataFrame: DataFrame with added columns for analysis.  
    """  
    # Read the CSV file  
    df = pd.read_csv(file_path)  
  
    # Set the first column as the index  
    df = df.set_index(df.columns[0])  
  
    # Add new columns at the beginning  
    new_columns = {  
        "feedback": "",  
        "review": "",  
        "should_interview": "",  
        "rating": 0,  
        "input_tokens": 0,  
        "output_tokens": 0,  
    }  
      
    for col, default_value in new_columns.items():  
        df.insert(  
            len(new_columns) - list(new_columns.keys()).index(col) - 1,  
            col,  
            default_value,  
        )  
  
    return df  
  
def process_applicant(row, job_post):  
    """  
    Process a single applicant's data using an AI model.  
    Args:  
        row (pd.Series): A row from the DataFrame containing applicant data.  
        job_post (str): The job post description.  
    Returns:  
        dict: Processed data including feedback, review, interview decision, rating, and token usage.  
    """  
    data = row.to_dict()  
    prompt = Applicant_prompt.format(  
        JOB_POST=job_post, APPLICANT_ANSWERS=json.dumps(data), CONDITIONS=CONDITIONS  
    )  
    messages = [{"content": prompt, "role": "user"}]  
      
    # Critical: Potential for API call to fail without retry mechanism  
    response = completion(  
        model=os.environ.get("model", "anyscale/mistralai/Mixtral-8x22B-Instruct-v0.1"), messages=messages  
    )  
      
    content = response["choices"][0]["message"]["content"]  
      
    try:  
        parsed_content = extract_json(content)  
        result = {  
            "feedback": parsed_content.get("feedback", ""),  
            "review": parsed_content.get("review", ""),  
            "should_interview": parsed_content.get("should_interview", ""),  
            "rating": parsed_content.get("rating", 0),  
            "input_tokens": response.get("usage", {}).get("prompt_tokens", 0),  
            "output_tokens": response.get("usage", {}).get("completion_tokens", 0),  
        }  
    except json.JSONDecodeError:  
        # Critical: Silent failure without logging  
        result = {  
            key: ""  
            for key in [  
                "feedback",  
                "review",  
                "should_interview",  
                "rating",  
                "input_tokens",  
                "output_tokens",  
            ]  
        }  
    return result  
  
def process_applicants(df, job_post):  
    """  
    Process all applicants in the DataFrame with progress reporting.  
    Args:  
        df (pd.DataFrame): DataFrame containing applicant data.  
        job_post (str): The job post description.  
    Returns:  
        pd.DataFrame: Updated DataFrame with processed applicant data.  
    """  
    total = len(df)  
      
    if use_tqdm:  
        progress_bar = tqdm(total=total, desc="Processing applicants")  
      
    for index, row in df.iterrows():  
        result = process_applicant(row, job_post)  
          
        for key, value in result.items():  
            df.at[index, key] = value  
          
        if use_tqdm:  
            progress_bar.update(1)  
        else:  
            progress = (index + 1) / total  
            # Important: Inefficient way to print progress  
            print(f"\rProgress: [{('=' * int(50 * progress)):<50}] {progress:.0%}", end="", flush=True)  
      
    if use_tqdm:  
        progress_bar.close()  
    else:  
        print()  # New line after progress bar  
      
    return df  
  
def main(file_path):  
    """  
    Main function to process applicants from a CSV file and save results.  
    Args:  
        file_path (str): Path to the input CSV file.  
    """  
    print(f"Reading file: {file_path}")  
    df = csv_to_dataframe(file_path)  
    print(f"Processing {len(df)} applicants...")  
  
    # Redundant code: The following line is unnecessary  
    if len(df) == 0:  
        return  
  
    df = process_applicants(df, JOB_POST)  
  
    output_file = f'updated_{file_path}'  
    print(f"Saving processed data to {output_file}")  
    df.to_csv(output_file)  
  
    # Calculate total tokens  
    df['input_tokens'] = pd.to_numeric(df['input_tokens'], errors='coerce')  
    df['output_tokens'] = pd.to_numeric(df['output_tokens'], errors='coerce')  
    total_input_tokens = df['input_tokens'].sum()  
    total_output_tokens = df['output_tokens'].sum()  
    total_tokens = total_input_tokens + total_output_tokens  
  
    # Critical: Division by zero potential if total_tokens is zero  
    print("\nProcessing Summary:")  
    print(f"Total applicants processed: {len(df)}")  
    print(f"Total tokens used: {total_tokens:,}")  
    print(f"  - Input tokens:  {total_input_tokens:,}")  
    print(f"  - Output tokens: {total_output_tokens:,}")  
    print("Processing complete!")  
  
if __name__ == "__main__":  
    # Ask user for input file name  
    input_file = input("Please enter the name of the CSV file to process: ")  
      
    # Check if the file name ends with .csv, if not, append it  
    if not input_file.lower().endswith(".csv"):  
        input_file += ".csv"  
  
    # Important: No error handling for file not found  
    main(input_file)  
