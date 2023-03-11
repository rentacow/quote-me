import logging
import openai
import json
import os


def get_a_quote():  # Define a function to get a quote when called

    # Set the OpenAI API key to the value of the `OPENAI_API_KEY` environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Set up JSON and error log file path
    json_file_path = "quotes.json"
    error_log_path = "errors.log"

    # Define prompt for the GPT-3 completion
    prompt = "Give a few words of wisdom for a submarine captain, in the form of a quote: "

    # Generate a completion using the OpenAI API
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            temperature=0.8,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=[" -"]
        )
    except Exception as e:  # Log the error if there's a problem
        logging.basicConfig(filename=error_log_path, level=logging.ERROR, format='%(asctime)s %(message)s')
        logging.error('An error occurred: %s', e)
        return f"An error occurred!!! {e}"

    # Add the raw API response to a JSON file
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(response)
    with open(json_file_path, "w") as f:
        json.dump(data, f)

    # function returns a nicely formatted quote
    return response["choices"][0]["text"].strip()


if __name__ == "__main__":  # Run this code as a script by calling the function
    print(f'Quote of the Day: {get_a_quote()}')
    # input('\nPress enter or return to quit.')  # optional debugging interrupt
