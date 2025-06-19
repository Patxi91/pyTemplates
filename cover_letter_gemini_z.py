import os
import json
import re
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# --- Configuration ---

# IMPORTANT: It's recommended to set your API key as an environment variable
# for security reasons, rather than hardcoding it.
API_KEY = os.getenv("GOOGLE_API_KEY", "API_KEY") # Replace with your key if not using env var

# Zoe's predefined skills and contact information
ZOES_SKILLS = """
- Music Therapy – Designing and delivering evidence-based therapeutic music interventions for mental health and emotional well-being across diverse clinical settings.
- Digital Health Innovation – Applying digital tools and strategies, including app development and audio platforms, to enhance preventive mental health care and user engagement.
- Content Strategy & Podcasting– Creating, scaling, and marketing health-focused audio content that translates clinical insights into accessible, engaging experiences.
- User-Centered Research – Conducting interviews and behavioral research to ensure that health solutions align with real user needs and emotional contexts.
- Multilingual Communication (English, German, Chinese) – Effectively communicating across languages and cultures in professional, therapeutic, and academic settings.
- Cross-Cultural Healthcare Collaboration– Working with interdisciplinary teams across countries to co-develop mental health programs sensitive to cultural and systemic differences.
"""

ZOES_AVAILABILITY_AND_CONTACT = """
I am available to begin immediately in a flexible capacity, both remotely and on-site in Zürich.

For any further questions, I am at your disposal.

Best regards,
Yu-Jung (Zoe) Weng
zoeweng1111@gmail.com | +41 778075805
https://www.linkedin.com/in/zoe-weng/
"""

# --- Main Functions ---

def configure_genai():
    """Configures the Generative AI model."""
    try:
        if not API_KEY or API_KEY == "YOUR_API_KEY":
            raise ValueError("Google Gemini API Key is not configured. Please replace 'YOUR_API_KEY' or set the GOOGLE_API_KEY environment variable.")
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel('gemini-1.5-flash')
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
    Uses the AI model to extract Job Title, Description, and Language from the text.
    (This function is reusable for both scripts).
    """
    if not model:
        return None

    prompt = f"""
    Analyze the following job posting text and extract the required information.
    Provide the output ONLY in a valid JSON format like this:
    {{"job_title": "...", "job_description": "...", "language": "..."}}

    - "job_title": The official title of the job.
    - "job_description": A detailed summary of the role, responsibilities, and required qualifications. Include any keywords mentioned.
    - "language": The primary language the job posting is written in (e.g., "English", "German").

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

def generate_zoe_cover_letter(model, job_title, job_description, skills, availability_contact, job_language):
    """Generates the final cover letter for Zoe based on her specific template."""
    if not model:
        return "Model not initialized."

    template_prompt = f"""
    You are Yu-Jung (Zoe) Weng, a trilingual music therapist and digital health professional based in Zürich, with international clinical and research experience, and founder of a widely downloaded therapeutic music content.
    You are applying for a permanent role.

    You will receive 3 inputs:
    1. Job Title
    2. Job Description
    3. Zoe’s Skills

    Your task is to generate a natural, confident, and tailored job application message that aligns Zoe’s strengths with the job post. Follow these formatting and content instructions carefully:

    🧠 CONTENT INSTRUCTIONS:
    - Start with a friendly salutation (e.g., “Hi,”).
    - Write a brief 1-sentence introduction stating Zoe's interest in the role.
    - Tailor the main paragraph(s) to highlight skills most relevant to the job (based on both Zoe’s skills and new ones mentioned in the job description). Be concise, specific, and relevant.
    - If needed, infer experience or transferable skills for tech mentioned in the job that Zoe hasn’t listed but would likely handle confidently.
    - Present key capabilities in plain text bullet format using "- TEXT".
    - Conclude the letter with the provided availability and contact information.

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

    Zoe’s Skills:
    {skills}

    Zoe's Availability and Contact Info (to be placed at the end):
    {availability_contact}
    -----------------------------------------------------

    🎯 Generate the cover letter now.
    Combine the introduction, the tailored skills bullet points, and the availability/contact block into one single, cohesive message.
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
    job_post_url = input("Please enter the URL of the job posting for Zoe: ")

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
                print(f"   ...Details extracted: [Title: {job_title}, Language: {job_lang}]")

                # 4. Generate the final cover letter for Zoe
                print("\n4. Generating tailored cover letter for Zoe...")
                cover_letter = generate_zoe_cover_letter(
                    model=gemini_model,
                    job_title=job_title,
                    job_description=job_desc,
                    skills=ZOES_SKILLS,
                    availability_contact=ZOES_AVAILABILITY_AND_CONTACT,
                    job_language=job_lang
                )

                # 5. Print the final result
                print("\n--- Generated Cover Letter for Zoe ---")
                print(cover_letter)
                print("--------------------------------------")

            else:
                print("\nCould not extract job details from the website.")
                if isinstance(job_details, str):
                    print(f"Details: {job_details}")
        else:
            print(f"\nFailed to process website: {scraped_text}")
    else:
        print("\nCould not proceed. Please check your API key configuration and the URL.")