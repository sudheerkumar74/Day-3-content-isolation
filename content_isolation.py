
import os
from dotenv import load_dotenv
from openai import OpenAI

# Step 1: Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# Step 2: Check whether API key exists
if not API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY is missing. "
        "Please add it to your .env file."
    )

# Step 3: Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

# Step 4: Sample resume text
sample_resume_text = """
Akhila Kethireddy
Contact: +91 9876543210
Email: akhila@example.com

Experience: GenAI Engineer Intern at Craftechco (2026).
Built automated data validation microservices using regular expressions.

Skills: Python, JavaScript, Anthropic API, Firebase Firestore.
"""

# Step 5: System prompt for strict data extraction
system_instruction = """
You are a strict data extraction microservice engine.

Your sole task is to extract these details from the resume:
1. Full Name
2. Email
3. Primary Skills

CRITICAL RULES:
1. Enclose the extracted data strictly inside
   <data> and </data> tags.
2. Do not include introductory greetings.
3. Do not include conversational filler.
4. Do not include concluding notes.
5. Do not invent information missing from the resume.
6. Return only the required details inside the tags.

Expected format:
<data>
Full Name: ...
Email: ...
Primary Skills: ...
</data>
"""


# Step 6: Function to call the LLM and extract structured data
def extract_structured_payload(raw_text):
    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            temperature=0.0,
            max_tokens=1000,
            messages=[
                {
                    "role": "system",
                    "content": system_instruction
                },
                {
                    "role": "user",
                    "content": (
                        "Extract the required details from this "
                        f"resume:\n{raw_text}"
                    )
                }
            ]
        )

        # Step 7: Read the model response
        output = response.choices[0].message.content

        if not output:
            return "Validation Error: Empty response from LLM"

        output = output.strip()

        # Step 8: Validate XML boundary tags
        if not output.startswith("<data>"):
            return (
                "Validation Error: Missing opening <data> tag\n"
                f"Received response: {output}"
            )

        if not output.endswith("</data>"):
            return (
                "Validation Error: Missing closing </data> tag\n"
                f"Received response: {output}"
            )

        # Step 9: Return only the validated response
        return output

    except Exception as error:
        return f"Operational Engine Error: {error}"


# Step 10: Execute the pipeline
if __name__ == "__main__":
    print("=== Day 3 XML Extraction Framework ===")

    result = extract_structured_payload(sample_resume_text)

    print("\n--- Extracted Candidate Details ---")
    print(result)

