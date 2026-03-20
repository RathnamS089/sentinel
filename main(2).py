from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import markdown
import requests
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
load_dotenv()
client = genai.Client()
templates = Jinja2Templates(directory="templates")

# --- MEMORY: This list stores scans while the server is running ---
scan_history = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("report.html", {
        "request": request,
        "repo": "Waiting for Input",
        "scan_target": "None",
        "report_content": "Please use the 'New Scan' button to begin.",
        "health_score": "0%",
        "history": scan_history  # Send the list to the frontend
    })

@app.get('/scan_repository', response_class=HTMLResponse)
async def scan_repository(request: Request, github_url: str):
    # 1. Parse the URL
    try:
        url_parts = github_url.rstrip('/').split('/')
        owner = url_parts[3]
        repo = url_parts[4]
    except (IndexError, AttributeError):
        return {"error": "Invalid GitHub URL format."}

    # 2. Fetch Repo Contents
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        return {"error": "Could not fetch repository."}

    # 3. Find Dependency File
    target_file = next((item for item in response.json() 
                       if item['name'] in ['pyproject.toml', 'requirements.txt']), None)
    
    if not target_file:
        return {"error": "No configuration file found."}

    # 4. Fetch File Content
    file_response = requests.get(target_file['download_url'])
    if file_response.status_code == 200:
        file_content = file_response.text  
        
        # 5. THE AI BRAIN: Structured Prompt
        prompt = """Act as a Senior Security Auditor. 
        CRITICAL: Your response MUST start with these exact two lines:
        SCORE: [0-100]
        RATING: [A, B, C, D, or F]
        
        Then, provide the detailed Markdown analysis of High/Critical vulnerabilities."""
        
        ai_response = client.models.generate_content(
            model='models/gemini-3-flash-preview',
            contents=f"{prompt}\n\nDEPENDENCY FILE:\n{file_content}"
        )
        
        # 6. PROCESSING: Extracting the "Rating" and "Score"
        raw_text = ai_response.text
        lines = raw_text.split('\n')
        
        # Extract and clean values
        display_score = lines[0].replace("SCORE:", "").strip() + "%"
        display_rating = lines[1].replace("RATING:", "").strip()
        report_body = "\n".join(lines[2:]) # The rest is the actual audit
        
        html_report = markdown.markdown(report_body)
        
        # 7. UPDATE HISTORY: Add this scan to our "Memory"
        # Create a unique ID based on the length of the history
        scan_id = len(scan_history) 

        # Save the FULL data this time
        scan_history.append({
            "id": scan_id,
            "repo": f"{owner}/{repo}",
            "target": target_file['name'],
            "score": display_score,
            "rating": display_rating,
            "content": html_report  # We save the HTML here!
        })
        
        # 8. RENDER: Send everything to report.html
        return templates.TemplateResponse("report.html", {
            "request": request,
            "repo": f"{owner}/{repo}",
            "scan_target": target_file['name'],
            "report_content": html_report,
            "health_score": display_score,
            "history": scan_history
        })

    return {"error": "Failed to read the dependency file."}
@app.get('/view_scan/{scan_id}', response_class=HTMLResponse)
async def view_scan(request: Request, scan_id: int):
    # Find the scan in our list using the ID
    if scan_id < len(scan_history):
        saved_scan = scan_history[scan_id]
        return templates.TemplateResponse("report.html", {
            "request": request,
            "repo": saved_scan["repo"],
            "scan_target": saved_scan["target"],
            "report_content": saved_scan["content"],
            "health_score": saved_scan["score"],
            "history": scan_history
        })
    return {"error": "Scan not found"}