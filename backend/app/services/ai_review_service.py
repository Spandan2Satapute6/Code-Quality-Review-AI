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
You are a Senior Software Architect, Security Engineer, Technical Writer, and Code Reviewer.

Review the following source code.

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

Also generate:

11. Module Documentation
12. README

Return ONLY valid JSON.

Expected JSON format:

{{
  "score": 90,
  "severity": "Low",
  "summary": "Overall summary",

  "issues": [],
  "security": [],
  "performance": [],
  "maintainability": [],
  "best_practices": [],
  "recommendations": [],
  "suggestions": [],
  "verdict": "Good",

  "module_documentation": {{
    "module_name": "",
    "purpose": "",
    "main_components": [],
    "dependencies": [],
    "workflow": "",
    "usage": "",
    "summary": ""
  }},

  "readme": {{
    "title": "",
    "overview": "",
    "features": [],
    "installation": "",
    "usage": "",
    "folder_structure": "",
    "dependencies": [],
    "license": "MIT"
  }}
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
                max_tokens=2000
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
                "verdict": "Failed",

                "module_documentation": {
                    "module_name": "",
                    "purpose": "",
                    "main_components": [],
                    "dependencies": [],
                    "workflow": "",
                    "usage": "",
                    "summary": ""
                },

                "readme": {
                    "title": "",
                    "overview": "",
                    "features": [],
                    "installation": "",
                    "usage": "",
                    "folder_structure": "",
                    "dependencies": [],
                    "license": "MIT"
                }
            }