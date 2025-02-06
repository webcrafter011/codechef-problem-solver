from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from playwright.async_api import async_playwright
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Replace with your API key
)


async def extract_problem_statement(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector("#problem-statement", timeout=10000)
        problem_statement = await page.query_selector("#problem-statement")
        statement_text = await problem_statement.inner_text()
        await browser.close()
        return statement_text.strip()


def query_openrouter_api(problem_statement):
    try:
        completion = client.chat.completions.create(
            extra_headers={"Authorization": f"Bearer {client.api_key}"},
            model="google/gemini-2.0-flash-thinking-exp:free",
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": problem_statement}],
                }
            ],
        )
        if completion and completion.choices:
            return completion.choices[0].message.content
        else:
            return None
    except Exception as e:
        print(f"Error during API request: {e}")
        return None


@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        problem_statement = asyncio.run(extract_problem_statement(url))
        solution = query_openrouter_api(problem_statement)

        if solution:
            return jsonify(
                {"problemStatement": problem_statement, "solution": solution}
            )
        else:
            return jsonify({"error": "Failed to generate a solution"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000)
