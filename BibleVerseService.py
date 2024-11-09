import requests
# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv()

class BibleVerseService:
    def get_verse(self, ref : str):
        # Define the API endpoint
        api_url = f"https://api.esv.org/v3/passage/text/?q={ref}"
        api_key = os.getenv("Authorization")

        # Define headers with Authorization
        headers = {
            "Authorization": api_key
        }

        params = {
            'indent-poetry': 'true',
            'include-headings': 'false',
            'include-footnotes': 'false',
            'include-verse-numbers': 'true',
            'include-short-copyright': 'false',
            'include-passage-references': 'false'
        }

        try:
            # Send a GET request to the API
            response = requests.get(api_url, headers=headers, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Check if reference was valid
                if (len(data.get('passages')) == 0):
                    return None, "Reference is not valid"

                # Extract the verse text
                verse_text = "".join(data.get("passages", "Verse not found"))
                reference_text = data.get("query", ref)

                # Return the verse reference and text
                return reference_text, verse_text
            else:
                print(f"Error: Received status code {response.status_code}")
                return None, "Failed to retrieve verse."

        except Exception as e:
            print(f"Exception occurred: {e}")
            return None, "An error occurred while fetching the verse."
