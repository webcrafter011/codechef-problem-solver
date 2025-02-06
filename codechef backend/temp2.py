import asyncio
from playwright.async_api import async_playwright
from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Replace with your valid OpenRouter API key
)


# Asynchronous function to extract the problem statement from CodeChef using Playwright
async def extract_problem_statement(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Launch headless browser
        page = await browser.new_page()
        await page.goto(url)  # Navigate to the CodeChef problem page

        # Wait for the problem statement to load
        await page.wait_for_selector("#problem-statement", timeout=10000)

        # Extract the text of the problem statement
        problem_statement = await page.query_selector("#problem-statement")
        statement_text = await problem_statement.inner_text()
        await browser.close()  # Close the browser

        return statement_text.strip()


# Function to query the OpenRouter API (Google's Gemini model)
def query_openrouter_api(problem_statement):
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "Authorization": f"Bearer {client.api_key}",  # Add the Authorization header
            },
            model="google/gemini-2.0-flash-thinking-exp:free",  # Using Gemini model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": problem_statement,
                        },
                    ],
                }
            ],
        )

        # Return the generated message content
        if completion and completion.choices:
            return completion.choices[0].message.content
        else:
            print("No completion or choices found in the API response.")
            return None
    except Exception as e:
        print(f"Error during API request: {e}")
        return None


# Main function to extract problem statement and generate the answer
async def main():
    url = input("Enter the CodeChef problem URL: ")
    problem_statement = await extract_problem_statement(
        url
    )  # Extract problem statement asynchronously
    print(
        f"Problem Statement: {problem_statement} only provide me with code without any sort of explaination of the code strictly provide code only"
    )

    # Generate the answer using OpenRouter API (Google's Gemini model)
    answer = query_openrouter_api(problem_statement)
    if answer:
        print(f"Answer: {answer}")
    else:
        print("Failed to generate an answer")


# Run the program asynchronously
asyncio.run(main())
