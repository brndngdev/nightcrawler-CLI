from bs4 import BeautifulSoup
import requests
import re
import sys
import time
from tabulate import tabulate


dataset = []
choice = 0
picking = True
headers = {
    "User-Agent": "Spiderbot"
}

def box(message):
    width = len(message) + 2

    print("┌" + "─" * width + "┐")
    print("│ " + message + " │")
    print("└" + "─" * width + "┘")


def crawlQuotes():
    url = "https://quotes.toscrape.com/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text,"html.parser")
    quotes = soup.find_all("div",{"class" : "quote"})

    #print(quotes)

    for quote in quotes: # looping over an array of all the quote boxes
        tagArray = []
        text = quote.find("span",{"class" : "text"})
        author = quote.find("small",{"class" : "author"})

        tags = quote.find("div",{"class" : "tags"})
        tagList = tags.find_all("a",{"class" : "tag"})

        for tag in tagList:
            #print(tag.text)
            tagArray.append(tag.text)


        dataset.append([text.text, author.text , tagArray])

    table = tabulate(dataset,headers = ["Quote", "Author", "Themes"], tablefmt = "grid")
    print(table)

def crawlWikipedia():
    endof = input("Enter a valid topic: ") # enter topic

    print("*")
    time.sleep(0.1)
    print("**")
    time.sleep(0.1)
    print("***")
    time.sleep(0.1)

    # formatting for url
    endof = endof.replace(" ", "_")
    endof = endof.lower()
    endof = endof[0].upper() + endof[1:]

    url = "https://en.wikipedia.org/wiki/" + endof

    print("fetching url: \n" + url + "\n")

    sectionList = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    if response.status_code != 200:   # checking for 404 error or if we're not allowed in
        box("Page not found, going back to the main page")
        time.sleep(2.5)
        scrapingTime()
        return

    sections = soup.find_all("section") # getting sections
    for section in sections:
        sectionList.append(section.get("aria-labelledby"))

    section = soup.find("section", {"aria-labelledby": "Overview"})  # looking for if theres an overview
    if section:
        paragraphs = section.find_all("p") # Finding all paragraphs

        for paragraph in paragraphs:
            text = paragraph.get_text()
            text = re.sub(r"\[.*?\]", "", text) # removing hashtag text like edit and stuff
            dataset.append(text + "\n") # adding new line after every paragraph
            print(text)  # show it to the user

        time.sleep(1.5)
        choice = input("Press enter to continue back to the main menu.")
        if choice == "":
            scrapingTime()
            return

    else:
        box("No Overview section found, would you like to search in a section that's in the page?")

        while True: # infinite loop

            choice = input("Would you like to explore other sections? (yes or no): ").lower()

            if choice == "no":
                print("Bye bye!")
                time.sleep(1.5)
                scrapingTime()
                return

            elif choice == "yes":
                box("Okay! showing you the other sections of this page (CASE SENSITIVE):")
                print(str(sectionList))

                desiredSection = input("Enter desired section: ")       # validating for section search
                desiredSection = desiredSection.replace(" ", "_")

                section = soup.find("section", {"aria-labelledby": desiredSection}) # finding sections
                if section:
                    paragraphs = section.find_all("p") # finding all paragraphs (html marked as p)
                    print("****************************************************************************************")

                    for paragraph in paragraphs:
                        text = paragraph.get_text()
                        text = re.sub(r"\[.*?\]", "", text)
                        print(text)


                    box("would you still like to keep crawling or stop?")

                    while True:
                        choice = input("Enter your choice (keep crawling (1), or stop (2)?): ")

                        if choice == "1":
                            crawlWikipedia()
                            return

                        elif choice == "2":
                            sys.exit()
                            return



                    break

                else:
                    print("Section not found.")












   # print("".join(dataset))

   # sectionText.
    #print(soup)
    #print(section.text)




#print(response.text)

def scrapingTime():
    print(r"""\
    *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  
               ____                      ,
              /---.'.__             ____//
                   '--.\           /.---'
              _______  \\         //
            /.------.\  \|      .'/  ______
           //  ___  \ \ ||/|\  //  _/_----.\__
          |/  /.-.\  \ \:|< >|// _/.'..\   '--'
             //   \'. | \'.|.'/ /_/ /  \\
            //     \ \_\/" ' ~\-'.-'    \\
           //       '-._| :-: |'-.__     \\
          //           (/'==='\)'-._\     ||
          ||                        \\    \|
          ||                         \\    '
          |/                          \\
                                       ||
                                       ||
                                       \\
                                        '
                           
    *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
                                              
    [!] "Thank you for using NIGHTCRAWLER page scraper and web crawler! what would you like to do?"
    
    [1] Scrape a table of quotes!
    [2] Scrape information from Wikipedia!
    [3] Information
    [4] EXIT
                """)


    while picking == True:
        try:
            choice = int(input("Enter your choice: "))

            if choice < 1 or choice > 4:
                box("Please enter a valid number")

            else:
                break


        except ValueError:
            box("Please enter a valid number")


    match choice:
        case 1:
            crawlQuotes()
        case 2:
            crawlWikipedia()
        case 3:
            box("This CLI doesnt pull disambiguation paragraphs like bullet points because that's quiite complicated, you can pull paragraphs and text though!")
            print("credits to: brndn")
            time.sleep(3)
            scrapingTime()
        case 4:
            box("Goodbye")

scrapingTime()