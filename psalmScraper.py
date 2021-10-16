from bs4 import BeautifulSoup
import requests
import re

def get_psalm_text(number):
  website = requests.get("https://www.churchofjesuschrist.org/study/scriptures/ot/ps/{i}?lang=eng".format(i=number))
  soup = BeautifulSoup(website.content, features="html.parser")

  marker_string = '<sup class="marker">a</sup>'

  verses_list = []

  for elm in soup.select("p[class^=verse]"):

    #remove superscripts and verse numbers from text
    elmstring = str(elm)
    elmstring_no_superscripts = re.sub(r'>[a-z]<', '><', elmstring)
    elmstring_no_superscripts_or_numbers = re.sub(r'>\d* <', '><', elmstring_no_superscripts)
    elmstring_sufficient_spaces = re.sub(r'<', ' <', elmstring_no_superscripts_or_numbers)

    #re-create the beautifulsoup object
    elm_new = BeautifulSoup(elmstring_sufficient_spaces, features="html.parser")
    verse_string = elm_new.get_text()
    verse_string_single_spaced = re.sub(' +', ' ', verse_string)
    verses_list.append(verse_string_single_spaced)

  psalm_string = ' '.join(verses_list)
  return psalm_string
