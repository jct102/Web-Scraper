import time
import schedule
import requests
from bs4 import BeautifulSoup


class Codes:
    """
    Represents a list of codes taken from the initialized URL
    """
    def __init__(self):
        self._codes_list = []
        self._url = ""
        self._page = requests.get(self._url)
        self._data = BeautifulSoup(self._page.content, "html.parser")

    def check_status(self, status=0):
        """Function returns True if the website has updated since last check, otherwise False"""
        if status == 0:
            entry_elements = self._data.find("div", class_="entry-content")
            ultags = entry_elements.find_all("ul")
            for litag in ultags[1].find_all("li"):
                code_string = str(litag)
                code = code_string.split()[0]
                self._codes_list.append(code)
            status += 1
        new_codes_list = []
        new_entry_elements = self._data.find("div", class_="entry-content")
        new_ultags = new_entry_elements.find_all("ul")
        for new_litag in new_ultags[1].find_all("li"):
            code_string = str(new_litag)
            code = code_string.split()[0]
            new_codes_list.append(code)
        for code in new_codes_list:
            if code not in self._codes_list:
                self._codes_list = new_codes_list
                print(True)
        else:
            print(False)

    def print_codes(self):
        """Prints list of codes"""
        if self.check_status() is True:
            with open('codes.txt', 'w') as codes:
                for code in self._codes_list:
                    codes.write(code)


my_class = Codes()
schedule.every(1).minutes.do(my_class.check_status)
schedule.every(1).minutes.do(my_class.print_codes)

while True:
    schedule.run_pending()
    time.sleep(1)
