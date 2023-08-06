import requests
from bs4 import BeautifulSoup
import openai

api_key = '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'
div_inner_text = "" 
openai.api_key = api_key


def get_first_link_from_search_result(url):
    try:
        # Fetch the HTML content of the provided URL
        response = requests.get(url)
        response.raise_for_status()  # Check for successful response

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first div with class 'search-result'
        search_result_div = soup.find('div', class_='search-result')

        if search_result_div:
            # Find the first link within the div
            first_link = search_result_div.find('a')

            if first_link:
                # Get the URL of the first link
                first_link_url = first_link.get('href')
                return first_link_url

    except Exception as e:
        print("An error occurred:", e)
        return None

def get_inner_text_of_div_by_class(url, div_class):
    try:
        # Fetch the HTML content of the provided URL
        response = requests.get(url)
        response.raise_for_status()  # Check for successful response

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the specified div with the given class
        target_div = soup.find('div', class_=div_class)

        if target_div:
            # Get the inner text of the div
            inner_text = target_div.get_text()
            return inner_text.strip()

    except Exception as e:
        print("An error occurred:", e)
        return None
  
def ask_seratAi(question):
    prompt = (
        f'Serat, an Islamic scholar, is asked: {question}, how does he respond?'
        f'in first person about his view on the movie?'
        f'have 2 line breaks then put a relevant ayah to his answer.'
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )


    return response.choices[0].text.strip()


#move up
print("Serat.ai: Salaam! Let's get straight to business here: what movie are you investigating today?")

while True:
    user_question = input("You: ")
    search_url = 'https://kids-in-mind.com/search-desktop.htm?fwp_keyword=' + user_question

    first_link_url = get_first_link_from_search_result(search_url)

   

       # if div_inner_text:
            #print("Inner text of the target div:")
            #print(div_inner_text)
    if user_question.lower() in ["exit", "quit", "salam"]:
        print("Serat.ai: Wa alaikum ussalam wa rahmatullah!")
        break
    seratAi_response = ask_seratAi(div_inner_text)
    print(f"Serat.ai: {seratAi_response}")
    if first_link_url:
      print("\n Learn more through our review reference:", first_link_url)
  
      target_div_class = "review"
      div_inner_text = get_inner_text_of_div_by_class(first_link_url, target_div_class)