import requests

def download_novel(url, file_name):
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Downloaded {file_name}")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

novels = [
    {"url": "https://www.gutenberg.org/files/1661/1661-0.txt", "file_name": "Sherlock_Holmes.txt"},
    {"url": "https://www.gutenberg.org/ebooks/1112.txt.utf-8", "file_name": "Romeo_and_Juliet.txt"},
    {"url": "https://www.gutenberg.org/ebooks/1342.txt.utf-8", "file_name": "Pride_and_Prejudice.txt"},
    {"url": "https://www.gutenberg.org/ebooks/84.txt.utf-8", "file_name": "Frankenstein.txt"},
    {"url": "https://www.gutenberg.org/ebooks/2701.txt.utf-8", "file_name": "Moby_Dick.txt"},
    {"url": "https://www.gutenberg.org/ebooks/11.txt.utf-8", "file_name": "Alices_Adventures_in_Wonderland.txt"},
    {"url": "https://www.gutenberg.org/ebooks/145.txt.utf-8", "file_name": "Middlemarch.txt"},
    {"url": "https://www.gutenberg.org/ebooks/46.txt.utf-8", "file_name": "A_Christmas_Carol.txt"},
    {"url": "https://www.gutenberg.org/ebooks/2600.txt.utf-8", "file_name": "War_and_Peace.txt"},
    {"url": "https://www.gutenberg.org/ebooks/3638.txt.utf-8", "file_name": "The_Further_Adventures_of_Zorro.txt"},
    {"url": "https://www.gutenberg.org/ebooks/2641.txt.utf-8", "file_name": "A_Room_with_a_View.txt"},
]


for novel in novels:
    download_novel(novel["url"], novel["file_name"])
