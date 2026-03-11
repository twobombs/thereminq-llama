import os
import sys
import json
import re
import openai
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from fpdf import FPDF

# --- 1. CONFIGURATION ---
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://192.168.2.134:8033/v1")
REASONING_URL = os.getenv("REASONING_URL", "http://192.168.2.137:8033/v1")

# Deep Scrape Limits 
MAX_SEARCH_RESULTS = 4
CHARS_PER_PAGE = 15000 

# Timeout Fix
CLIENT_TIMEOUT = (10.0, 600.0)

# Client Setup
orch_client = openai.OpenAI(
    base_url=ORCHESTRATOR_URL, 
    api_key="not-needed",
    timeout=CLIENT_TIMEOUT
)
reason_client = openai.OpenAI(
    base_url=REASONING_URL, 
    api_key="not-needed",
    timeout=CLIENT_TIMEOUT
)

# --- 2. DEEP WEB SCRAPING TOOL (WITH SMART FILTERING) ---
def perform_web_search(query):
    print(f"🔍 [Orchestrator] Searching Web for: {query}")
    try:
        results = DDGS().text(query, max_results=10) 
        if not results: return "No results found."

        combined_content = ""
        headers = {"User-Agent": "Mozilla/5.0"}
        banned_domains = ["youtube.com", "youtu.be", "vimeo.com", "tiktok.com", "instagram.com"]
        valid_pages_scraped = 0

        for res in results:
            if valid_pages_scraped >= MAX_SEARCH_RESULTS: break
                
            url = res.get("href", "")
            title = res.get("title", "Unknown Title")
            snippet = res.get("body", "")
            
            if any(domain in url for domain in banned_domains):
                print(f"   ⏭️ [Skipping Video Link]: {url}")
                continue
            
            print(f"   🔗 Deep Reading: {url}")
            try:
                page_resp = requests.get(url, headers=headers, timeout=10) 
                if page_resp.status_code == 200:
                    soup = BeautifulSoup(page_resp.text, 'html.parser')
                    for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                        element.extract()
                    
                    text = soup.get_text(separator=' ', strip=True)
                    text = re.sub(r'\s+', ' ', text)
                    if len(text) > CHARS_PER_PAGE:
                        text = text[:CHARS_PER_PAGE] + "... [CONTENT TRUNCATED]"
                else:
                    text = f"Failed to load page. Snippet fallback: {snippet}"
            except requests.exceptions.RequestException:
                text = f"Connection error. Snippet fallback: {snippet}"
            
            combined_content += f"\n\n--- Source: {title} ---\nURL: {url}\nCONTENT:\n{text}\n"
            valid_pages_scraped += 1

        return combined_content
    except Exception as e:
        return f"Search Error: {str(e)}"

# --- 3. PDF GENERATION ---
def sanitize_filename(query):
    clean_name = re.sub(r'[^\w\s-]', '', query).strip().replace(' ', '_')
    return clean_name[:50] + ".pdf"

def save_to_pdf(query, content):
    filename = sanitize_filename(query)
    print(f"\n💾 [System] Saving output to {filename}...")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", style="B", size=14)
    pdf.multi_cell(0, 10, text=f"Query: {query}")
    pdf.ln(5)
    pdf.set_font("helvetica", size=11)
    safe_content = content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, text=safe_content)
    pdf.output(filename)
    return filename

# --- 4. THE WORKFLOW ENGINE (NOW WITH STREAMING) ---
def run_orchestration_loop(user_query):
    # STEP A: Tool Planning
    print("🤖 [Orchestrator] Planning strategy...")
    tools = [{
        "type": "function",
        "function": {
            "name": "perform_web_search",
            "description": "Scrape in-depth research articles from the internet.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    }]

    response = orch_client.chat.completions.create(
        model="nemotron-orchestrator-8b",
        messages=[{"role": "user", "content": user_query}],
        tools=tools
    )

    context = ""
    msg = response.choices[0].message
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            context += perform_web_search(args['query'])
    else:
        print("💡 [Orchestrator] No search required.")

    # STEP B: Reasoning (Streaming)
    print("\n🧠 [Reasoner] Processing deep logic (Live Draft):\n" + "-"*50)
    draft = ""
    reasoning_stream = reason_client.chat.completions.create(
        model="qwen-3.5-35b",
        messages=[
            {"role": "system", "content": "Analyze provided facts to answer the user's query. Synthesize complex research. Be precise. Avoid guessing."},
            {"role": "user", "content": f"FACTS:\n{context}\n\nUSER TASK: {user_query}"}
        ],
        stream=True # <--- Enable Streaming
    )
    
    # Iterate through the chunks as they arrive
    for chunk in reasoning_stream:
        content = chunk.choices[0].delta.content
        if content:
            sys.stdout.write(content)
            sys.stdout.flush()
            draft += content
    print("\n" + "-"*50)

    # STEP C: Sanity Check & Formatting (Streaming)
    print("\n⚖️ [Orchestrator] Verifying and formatting final report (Live Edit):\n" + "="*50)
    editor_prompt = f"""
    FACTS FROM WEB: 
    {context}
    
    DRAFT ANSWER: 
    {draft}
    
    TASK: You are the final-stage Editor. Review the Draft Answer against the Facts. 
    - If the draft has logic errors or hallucinations, rewrite it into a corrected final response.
    - If the draft is perfect, just output the draft as-is, polished for the user.
    
    CRITICAL RULE: DO NOT include meta-commentary, audit notes, or explain your grading process. Output ONLY the final, polished report intended for the user.
    """

    verification = ""
    verification_stream = orch_client.chat.completions.create(
        model="nemotron-orchestrator-8b",
        messages=[
            {"role": "system", "content": "You are an expert editor. Output only the final document text without any meta-commentary."},
            {"role": "user", "content": editor_prompt}
        ],
        stream=True # <--- Enable Streaming
    )

    for chunk in verification_stream:
        content = chunk.choices[0].delta.content
        if content:
            sys.stdout.write(content)
            sys.stdout.flush()
            verification += content
    print("\n" + "="*50)

    return verification

# --- 5. CLI EXECUTION ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
        print(f"🚀 [System] Custom CLI query: '{user_prompt}'")
    else:
        user_prompt = "research on the negative energy spike when teleporting a qubit according to ER=EPR and devise a strategy to execute the thesis on a quantum computer that shows that ER=EPR is an example of quantum gravity"
        print(f"🏠 [System] Default mode: Deep Research Test...")

    try:
        # The printing is now handled inside the function via streaming
        final_result = run_orchestration_loop(user_prompt)
        
        saved_file = save_to_pdf(user_prompt, final_result)
        print(f"✅ [Success] Report generated: {os.path.abspath(saved_file)}")
    except Exception as e:
        print(f"\n❌ [Error] The workflow failed: {str(e)}")
