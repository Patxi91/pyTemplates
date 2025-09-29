import os
import json
import re
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# --- Gemini Model Selection ---
def get_latest_flash_model(api_key):
    """
    Returns the latest available Gemini flash model name using the ListModels API.
    """
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        # Filter for flash models
        flash_models = [m.name for m in models if "flash" in m.name]
        if not flash_models:
            raise Exception("No Gemini flash models found.")
        # Sort by version number (assumes format gemini-<version>-flash)
        flash_models.sort(reverse=True)
        return flash_models[0]
    except Exception as e:
        print(f"Error fetching Gemini flash models: {e}")
        return "gemini-2.5-flash"  # fallback

# --- Configuration ---

# IMPORTANT: It's recommended to set your API key as an environment variable
# for security reasons, rather than hardcoding it.
API_KEY = os.getenv("GOOGLE_API_KEY", "TOP_SECRET_KEY") # Replace with your key if not using env var

# Your predefined skills and details.
# The availability and rate are now handled dynamically.
FRANCISCOS_SKILLS = """
- Expert knowledge as a developer and tester with Python (Pytest, Unittest, Pandas, Numpy, Jupyter Notebooks), SQL, C#, C++, and Object-Oriented Programming (OOP).
- Experience in porting local SQL databases to PostgreSQL, Azure SQL Server, MySQL.
- Experience with cloud technologies: Terraform, REST APIs (OAuth), MS Azure, GitLab/GitHub, CI/CD pipelines, Kubernetes, JSON/XML, Databricks & Snowflake.
- Experience in reporting tools: Jira/Confluence, Microfocus ALM Octane/HP-ALM, Azure DevOps.
- Certified in: MS Azure, HashiCorp Terraform, ISTQB Certified Tester & Advanced Level Test Automation Engineer (TAE).
"""

# --- Main Functions ---

def configure_genai():
    """Configures the Generative AI model with the latest flash version."""
    try:
        if not API_KEY or API_KEY == "YOUR_API_KEY":
            raise ValueError("Google Gemini API Key is not configured. Please replace 'YOUR_API_KEY' or set the GOOGLE_API_KEY environment variable.")
        latest_flash_model = get_latest_flash_model(API_KEY)
        genai.configure(api_key=API_KEY)
        print(f"Using Gemini model: {latest_flash_model}")
        return genai.GenerativeModel(latest_flash_model)
    except Exception as e:
        print(f"Error configuring Generative AI: {e}")
        return None

def fetch_and_clean_website_text(url):
    """Fetches and extracts clean text content from a URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        return clean_text
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"
    except Exception as e:
        return f"An error occurred during website processing: {e}"

def extract_job_details(model, website_text):
    """
    Uses the AI model to extract Job Title, Description, Language, and Location
    from the provided website text.
    """
    if not model:
        return None

    prompt = f"""
    Analyze the following job posting text and extract the required information.
    Provide the output ONLY in a valid JSON format like this:
    {{"job_title": "...", "job_description": "...", "language": "...", "job_location": "..."}}

    - "job_title": The official title of the job.
    - "job_description": A detailed summary of the role, responsibilities, and required qualifications. Include any keywords mentioned.
    - "language": The primary language the job posting is written in, should be the language that the description or Beschreibung is written in and not only the title (e.g., "English", "German").
    - "job_location": The city and country where the job is located. If remote, state "Remote". If not specified, state "Not specified".

    Job Posting Text:
    ---
    {website_text}
    ---
    """
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the model's response.")
        print("Model Raw Response:", response.text)
        return None
    except Exception as e:
        return f"An error occurred during job detail extraction: {e}"

def get_dynamic_availability_and_rate(location_text):
    """Determines the correct rate and currency based on the job location."""
    # Use regex to be more flexible with location matching (e.g., "Germany", "Deutschland")
    if re.search(r'\b(germany|deutschland|de)\b', location_text, re.IGNORECASE):
        rate_info = "EUR 110"
    elif re.search(r'\b(switzerland|schweiz|suisse|svizzera|ch)\b', location_text, re.IGNORECASE):
        rate_info = "CHF 130"
    else:
        # Default case if location is not Germany or Switzerland
        rate_info = "CHF 130"

    return f"- Available immediately – five days a week – at an hourly rate of {rate_info}."

def generate_tailored_cover_letter(model, job_title, job_description, skills_with_rate, job_language):
    """Generates the final cover letter based on the provided template."""
    if not model:
        return "Model not initialized."

    template_prompt = f"""
    You are Francisco Oyaga, an expert freelance developer and tester with a strong background in Python, cloud technologies, databases, and testing automation.
    You are applying for a freelance role.

    You will receive 3 inputs:
    1. Job Title
    2. Job Description
    3. Francisco’s Skills (which now include his availability and rate)

    Your task is to generate a natural, confident, and tailored job application message that aligns Francisco’s strengths with the job post. Follow these formatting and content instructions carefully:

    🧠 CONTENT INSTRUCTIONS:
    - Start with a friendly salutation (e.g., “Hi,”).
    - Write a brief 1-sentence introduction stating Francisco's interest in the role.
    - Tailor the main paragraph(s) to highlight skills most relevant to the job.
    - Present key capabilities in plain text bullet format using "- TEXT".
    - Add a short paragraph about availability and rate (this is part of the skills input).
    - Close with a warm sign-off.

    🖋️ FORMATTING RULES:
    - Output should be in plain console-style text with simple line breaks.
    - No markdown, bold, italics, or special symbols.
    - Bullets must be in this format only: "- TEXT". All in plain text.
    - Total length: ideally under 350 words.

    -----------------------------------------------------
    ✏️ INPUTS BELOW:

    Job Title:
    {job_title}

    Job Description:
    {job_description}

    Francisco’s Skills:
    {skills_with_rate}

    -----------------------------------------------------

    🎯 Generate the cover letter now.
    The final output MUST be written entirely in the following language: {job_language}
    Do not add any introductory text or explanations before the cover letter itself. Just output the final letter.
    """
    try:
        response = model.generate_content(template_prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during cover letter generation: {e}"


# --- Main Execution ---

if __name__ == "__main__":
    job_post_url = input("Please enter the URL of the job posting: ")

    print("\n1. Configuring Gemini model...")
    gemini_model = configure_genai()

    if gemini_model and job_post_url:
        print("\n2. Fetching and cleaning website content...")
        scraped_text = fetch_and_clean_website_text(job_post_url)

        if "Error" not in scraped_text:
            print("   ...Website content fetched successfully.")

            print("\n3. Extracting job details with AI...")
            job_details = extract_job_details(gemini_model, scraped_text)

            if job_details and isinstance(job_details, dict):
                job_title = job_details.get("job_title", "N/A")
                job_desc = job_details.get("job_description", "N/A")
                job_lang = job_details.get("language", "English")
                job_loc = job_details.get("job_location", "Not specified")
                print(f"   ...Details extracted: [Title: {job_title}, Language: {job_lang}, Location: {job_loc}]")

                # 4. Determine the correct rate and create the full skills text
                availability_and_rate = get_dynamic_availability_and_rate(job_loc)
                full_skills_with_rate = f"{FRANCISCOS_SKILLS.strip()}\n{availability_and_rate}"
                print(f"   ...Rate determined based on location: {availability_and_rate.split('at an hourly rate of ')[1]}")


                # 5. Generate the final cover letter
                print("\n4. Generating tailored cover letter...")
                cover_letter = generate_tailored_cover_letter(
                    model=gemini_model,
                    job_title=job_title,
                    job_description=job_desc,
                    skills_with_rate=full_skills_with_rate,
                    job_language=job_lang
                )

                # 6. Print the final result
                print("\n--- Generated Cover Letter ---")
                print(cover_letter)
                print("------------------------------")

            else:
                print("\nCould not extract job details from the website.")
                if isinstance(job_details, str):
                    print(f"Details: {job_details}")
        else:
            print(f"\nFailed to process website: {scraped_text}")
    else:
        print("\nCould not proceed. Please check your API key configuration and the URL.")