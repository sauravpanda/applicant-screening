Applicant_prompt = """
Help me review this candidates who have applied for a python qa engineer role at our startup.
We are looking for hard working and enthusiastic people to join us. We have asked them to fill this long form to evaluate if they are ready for boring hard work.
We would love freshers who dont have any experience.

{CONDITIONS}

Give me output in a json format as shown below:
{{
    "feedback": "<FEEDBACK_BASED_ON_FORM>",
    "review": "<REVIEW_BASED_ON_FORM>",
    "should_interview": "<SHOULD_WE_INTERVIEW_AS_YES_OR_NO>",
    "rating": "<NUMERICAL_RATING_OUT_OF_100>"
}}

Here is our JOB POST:
{JOB_POST}

Here are Applicant answers as JSON:
{APPLICANT_ANSWERS}
"""
