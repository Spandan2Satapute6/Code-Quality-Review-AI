import os
import json
from groq import Groq


class AIReviewService:

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    @staticmethod
    def review_file(file):

        print("\n==============================")
        print("Sending to AI:", file["filename"])
        print("==============================")

        prompt = f"""
You are a Senior Software Architect, Security Engineer, and Code Reviewer with 15+ years of experience.

Review the following source code thoroughly.

Filename:
{file["filename"]}

Source Code:
{file["content"]}

Evaluate the code based on:

1. Code Quality
2. Readability
3. Maintainability
4. Security
5. Performance
6. Error Handling
7. Best Practices
8. Naming Conventions
9. Scalability
10. Architecture

IMPORTANT:

Return ONLY valid JSON.

Do NOT use markdown.

Do NOT use ```.

Do NOT explain anything outside JSON.

Return exactly this format:

{{
    "score": 90,

    "severity": "Low",

    "summary": "Short summary",

    "issues": [
        "Issue 1",
        "Issue 2"
    ],

    "security": [
        "Security finding"
    ],

    "performance": [
        "Performance finding"
    ],

    "maintainability": [
        "Maintainability finding"
    ],

    "best_practices": [
        "Best practice"
    ],

    "recommendations": [
        "Recommendation"
    ],

    "suggestions": [
        "Suggestion"
    ],

    "verdict": "Good"
}}
"""

        try:

            response = AIReviewService.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                max_tokens=1500
            )

            result = response.choices[0].message.content.strip()

            print("\n========== RAW AI RESPONSE ==========")
            print(result)
            print("=====================================\n")

            if result.startswith("```json"):
                result = result.replace("```json", "").replace("```", "").strip()
            elif result.startswith("```"):
                result = result.replace("```", "").strip()

            return json.loads(result)

        except Exception as e:

            print("AI ERROR:", str(e))

            return {
                "score": 0,
                "severity": "Unknown",
                "summary": "AI review failed.",
                "issues": [str(e)],
                "security": [],
                "performance": [],
                "maintainability": [],
                "best_practices": [],
                "recommendations": [],
                "suggestions": [],
                "verdict": "Failed"
            }