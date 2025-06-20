import os
import json
import re
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import sys # For exiting gracefully

# --- Configuration ---

API_KEY = os.getenv("GOOGLE_API_KEY", "API_KEY") # <<< REMEMBER TO SET YOUR API KEY HERE OR AS ENV VAR!

BASE_CV_LATEX_FILE = "cv_4.tex"
TAILORED_CV_LATEX_FILE = "cv_francisco.tex"

def configure_genai():
    try:
        if not API_KEY or API_KEY == "API_KEY":
            raise ValueError("Google Gemini API Key is not configured. Please replace the placeholder or set the GOOGLE_API_KEY environment variable.")
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Error configuring Generative AI: {e}")
        return None

def fetch_and_clean_website_text(url):
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
    if not model:
        return None

    prompt = f"""
    Analyze the following job posting text and extract the required information.
    Provide the output ONLY in a valid JSON format like this:
    {{"job_title": "...", "job_description": "...", "language": "...", "job_location": "..."}}

    - "job_title": The official title of the job.
    - "job_description": A detailed summary of the role, responsibilities, and required qualifications. Include any keywords mentioned.
    - "language": The primary language the job posting is written in (e.g., "English", "German").
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
        print("Error: Failed to decode JSON from the model's response during job detail extraction.")
        print("Model Raw Response:", response.text)
        return None
    except Exception as e:
        return f"An error occurred during job detail extraction: {e}"

def read_base_latex_cv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Base LaTeX CV file '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading base LaTeX CV file: {e}")
        return None

def generate_tailored_latex_cv(model, base_cv_content, job_details):
    if not model:
        return "Model not initialized."

    job_title = job_details.get("job_title", "N/A")
    job_desc = job_details.get("job_description", "N/A")
    job_lang = job_details.get("language", "English")

    prompt = f"""
    You are an expert LaTeX and resume formatting assistant, specializing in ATS (Applicant Tracking System) optimization. Your goal is to generate the most highly optimized and professional resume in LaTeX format for a specific job application.
    You will be provided with:
    1.  The complete content of an existing base resume in LaTeX.
    2.  Details of a job posting (title, description, and target language).

    Your task is to generate a **complete and compilable LaTeX document** for a resume that is **highly and aggressively tailored** to the given job posting for maximum keyword matching and relevance.

    **CRITICAL INSTRUCTIONS FOR KEYWORD OPTIMIZATION, CONTENT ADAPTATION, AND LATEX SYNTAX (Read Carefully):**

    **1. Aggressive Content Modification for Keyword Optimization:**
    -   **Deeply analyze the `JOB POSTING DETAILS`** (job title, full description, responsibilities, required qualifications, specific technologies, tools, and soft skills). Identify all critical keywords, phrases, and core requirements.
    -   **Re-engineer the content from the `BASE RESUME LATEX CONTENT`** to directly address and integrate these keywords. This involves:
        -   **Prioritizing and prominently featuring** experiences, skills, and projects that are most relevant to the job.
        -   **Significantly rephrasing, reordering, or combining** bullet points and descriptive text to maximize the density and impact of job-specific keywords.
        -   **Focusing the "Summary" or "About Me" section** (if present in the base CV, or create one if missing and appropriate) to immediately highlight your strongest matches to the job.
        -   **Tailoring skill lists:** Present skills that are directly mentioned or strongly implied by the job description first, and potentially de-emphasize less relevant ones (but do not remove skills entirely unless they are completely irrelevant to your career path).
        -   **Quantify achievements:** Where possible and applicable from your base content, rephrase achievements to include metrics or quantifiable results if they align with the job's needs.
    -   **Factual Accuracy(Strict Constraint):** Keep EXPERIENCE dates in the same order from new to oldest, keep company names, degree names, university names, or personal contact details and then under my pior experience Generate any new responsabilities that create the perfect track record match for the job. Feel free to modify or fabricate tasks so they include the main job post keywords.

    **2. LaTeX Structure and Syntax for Optimal Presentation:**
    -   Generate a complete and compilable LaTeX document.
    -   **Adapt the LaTeX document structure to enhance readability and keyword visibility.** While informed by `BASE RESUME LATEX CONTENT`, you have significant flexibility to reorder sections (e.g., place "Skills" higher if critical for the job), adjust sectioning commands (e.g., use `\section` or `\rSection` as most effective), and optimize environment usage (e.g., `itemize`, `tabular`) to best showcase the tailored content. Always aim for a clean, professional, and easily parsable format by ATS.
    -   Ensure consistent and professional formatting throughout.
    -   **Include necessary packages:** If the `base_cv_content` uses specific packages (e.g., `geometry`, `resume` class, `titlesec`, `fontawesome5`, `marvosym`), ensure these are included in the generated document's preamble.
    -   **Escape ALL LaTeX special characters:** Ensure all literal instances of characters that have special meaning in LaTeX (such as '&', '#', '$', '%', '{{', '}}', '_', '^', '~', '\\', '<', '>') are escaped with a backslash (e.g., '\\&', '\\#', '\\$', '\\%', '\\{{', '\\}}', '\\_', '\\^', '\\textasciitilde', '\\textbackslash', '\\textless', '\\textgreater') when they are part of the displayed text and not part of a LaTeX command or environment. Crucially, do not use '&' as an alignment tab unless it is explicitly inside a tabular, align, or similar environment where it is designed for alignment. If it's part of regular text, it must be '\\&'.
    -   **Avoid Overfull Hboxes:** Strive to ensure that lines of text do not exceed the document margins.
        * Rephrase sentences to be more concise.
        * Allow for natural hyphenation where possible.
        * Do NOT add `\sloppy` unless explicitly requested, as it can degrade formatting.
        * Consider the overall layout and line breaks to prevent text from running into the margins.
    -   Ensure all LaTeX commands are correctly closed (e.g., `\begin{{environment}}` has a corresponding `\end{{environment}}) and the document is compilable.

    **3. Language and Length:**
    -   The entire resume MUST be generated in the language specified in `Target Language for Resume`. Translate section headers and content as necessary, based *only* on the base content.
    -   Keep the overall length concise and impactful (aim for 1-2 pages, prioritizing relevance and keyword density over exhaustive detail).

    Do NOT include any explanatory text before or after the LaTeX code. ONLY output the complete LaTeX code.

    ---
    
    BASE RESUME LATEX CONTENT:
    {base_cv_content}

    ---
    JOB POSTING DETAILS:
    Job Title: {job_title}
    Job Description: {job_desc}
    Target Language for Resume: {job_lang}
    ---

    Generate the tailored LaTeX resume now:
    """

    try:
        print("Sending request to Gemini model for resume generation...")
        response = model.generate_content(prompt)
        tailored_latex = response.text.strip().replace('```latex', '').replace('```', '')
        return tailored_latex
    except Exception as e:
        print(f"An error occurred during tailored resume generation: {e}")
        return None

def write_latex_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\nSuccessfully generated tailored CV: '{file_path}'")
        print(f"Remember to compile it using pdflatex (e.g., 'pdflatex {file_path}') to get the PDF.")
    except Exception as e:
        print(f"Error writing tailored LaTeX CV file: {e}")

if __name__ == "__main__":
    job_post_url = input("Please enter the URL of the job posting: ")

    print("\n1. Configuring Gemini model...")
    gemini_model = configure_genai()
    if not gemini_model:
        sys.exit("Exiting due to Gemini model configuration error.")

    print(f"\n2. Reading base LaTeX CV from '{BASE_CV_LATEX_FILE}'...")
    base_cv_content = read_base_latex_cv(BASE_CV_LATEX_FILE)
    if not base_cv_content:
        sys.exit(f"Exiting due to error reading base CV file '{BASE_CV_LATEX_FILE}'.")

    print("\n3. Fetching and cleaning website content...")
    scraped_text = fetch_and_clean_website_text(job_post_url)

    if "Error" in scraped_text:
        sys.exit(f"\nFailed to process website: {scraped_text}")
    else:
        print("   ...Website content fetched successfully.")

    print("\n4. Extracting job details with AI...")
    job_details = extract_job_details(gemini_model, scraped_text)

    if not job_details or not isinstance(job_details, dict):
        sys.exit("\nCould not extract job details from the website. Exiting.")
    else:
        print(f"   ...Details extracted: [Title: {job_details.get('job_title', 'N/A')}, Language: {job_details.get('language', 'N/A')}, Location: {job_details.get('job_location', 'N/A')}]")

    print("\n5. Generating tailored LaTeX CV using AI...")
    tailored_latex_content = generate_tailored_latex_cv(gemini_model, base_cv_content, job_details)

    if tailored_latex_content:
        write_latex_file(TAILORED_CV_LATEX_FILE, tailored_latex_content)
    else:
        print("\nFailed to generate tailored LaTeX CV content. No file was created.")
