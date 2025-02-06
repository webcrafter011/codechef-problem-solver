# app.py
import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from playwright.async_api import async_playwright
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load your API key from .env
app.config["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Initialize the OpenAI client
# (Works with OpenRouter or direct OpenAI if you have the right credentials)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=app.config["GEMINI_API_KEY"]
)


async def extract_problem_statement(url: str) -> str:
    """
    Use Playwright to scrape the problem statement from CodeChef.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print(f"Navigating to URL: {url}")
        await page.goto(url)

        # Wait for the #problem-statement element to appear
        await page.wait_for_selector("#problem-statement", timeout=10000)

        problem_element = await page.query_selector("#problem-statement")
        statement_text = await problem_element.inner_text() if problem_element else ""
        await browser.close()
        return statement_text.strip()


def query_openrouter_api(problem_statement: str) -> str:
    """
    Call the LLM (Gemini-2.0 on OpenRouter, for example) to get the solution in Markdown.
    The prompt instructs the LLM to return code in fenced blocks.
    """
    try:
        prompt = f"""
{problem_statement}

Provide the solution code in Markdown format with the following requirements:
- Put the code in a Python code block (```python)
- Include brief explanations in Markdown
- Do not include any extra text outside the Markdown formatting
- Properly indent and format the code
"""

        completion = client.chat.completions.create(
            extra_headers={"Authorization": f"Bearer {client.api_key}"},
            model="google/gemini-2.0-flash-thinking-exp:free",
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        )

        if completion and completion.choices:
            return completion.choices[0].message.content
        return ""
    except Exception as e:
        print(f"Error querying the API: {e}")
        return ""


@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # 1) Extract the problem statement
        problem_statement = asyncio.run(extract_problem_statement(url))
        if not problem_statement:
            return jsonify({"error": "Unable to extract problem statement."}), 500

        # 2) Get the AI-generated Markdown solution
        solution_markdown = query_openrouter_api(problem_statement)
        if not solution_markdown:
            return jsonify({"error": "Failed to generate solution"}), 500

        # Return the solution as JSON
        return jsonify(
            {"markdown": solution_markdown, "problem_statement": problem_statement}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # For local dev
    app.run(host="0.0.0.0", port=5000, debug=True)
