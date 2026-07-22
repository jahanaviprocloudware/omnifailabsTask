import google.generativeai as genai


def secret_key_valid(api_key):

    try:
        genai.configure(
            api_key=api_key
        )

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(
            "Hello"
        )

        return True

    except Exception as e:
        print(e)
        return False