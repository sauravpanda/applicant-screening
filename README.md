# AI-Powered QA Engineer Application Reviewer

## Overview

This project automates the process of reviewing applications for a QA Engineer position using AI. It was created to efficiently handle a large number of applications (159 forms) received within a short timeframe (60 hours), which would have been challenging for a small team to process manually alongside other workloads.

The script utilizes the Mistral AI model to analyze candidate responses and provide insights, ratings, and recommendations for each applicant.

## Features

- Reads applicant data from a CSV file
- Processes each application using the Mistral AI model
- Provides feedback, review, interview recommendation, and rating for each candidate
- Calculates and displays token usage statistics
- Supports progress tracking with optional tqdm integration
- Saves results to a new CSV file
- Allows customization of evaluation criteria

## Requirements

- Python 3.x
- pandas
- litellm
- kaizen (for the `extract_json` function)
- tqdm (optional, for better progress visualization)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/sauravpanda/applicant-screening.git
   cd applicant-screening
   ```

2. Install the required packages:
   ```
   pip install pandas litellm tqdm kaizen-cloudcode
   ```

   Or if you're using Poetry:
   ```
   poetry install
   ```

## Usage

1. Update the job post description in `jobpost.py`.

2. Modify the `CONDITIONS` variable in the script to set specific evaluation criteria.

3. Prepare your CSV file with applicant data.

4. Run the script:
   ```
   python main.py
   ```
   Or with Poetry:
   ```
   poetry run python main.py
   ```

5. When prompted, enter the name of your CSV file (with or without the .csv extension).

6. The script will process the applications and save the results in a new CSV file prefixed with "updated_".

## Output

```
Please enter the name of the CSV file to process: cloudcode_qa_engineer_ans.csv
Reading file: cloudcode_qa_engineer_ans.csv
Processing 159 applicants...
Processing applicants:  14%|█████████████████████████████████████████▎                                                                                                                                                                                                                                                    | 23/159 [01:44<11:32,  5.10s/it]/Users/sauravpanda/Github/cloudcode-OSS/applicant-screening/main.py:119: FutureWarning: Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value '85' has dtype incompatible with int64, please explicitly cast to a compatible dtype first.
  df.at[index, key] = value
Processing applicants: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 159/159 [11:01<00:00,  4.16s/it]
Saving processed data to updated_cloudcode_qa_engineer_ans.csv

Processing Summary:
Total applicants processed: 159
Total tokens used: 297,657
  - Input tokens:  260,247
  - Output tokens: 37,410
Processing complete!

```


The script will generate:
- A new CSV file with added columns for AI-generated feedback, review, interview recommendation, and rating.
- A summary of the processing, including the number of applicants processed and token usage statistics.

## Customization

- Modify the `CONDITIONS` variable to adjust the specific evaluation criteria for candidates.
- You can update the `Applicant_prompt` in `prompt.py` to fine-tune the instructions given to the AI model for evaluating candidates.

## Note

This tool is designed to assist in the initial screening process. It's recommended to use the AI-generated insights as a supplement to, not a replacement for, human judgment in the hiring process.

## License

MIT License

## Contributing

Contributions to improve the script or extend its functionality are welcome. Please feel free to submit pull requests or open issues for any bugs or feature requests.