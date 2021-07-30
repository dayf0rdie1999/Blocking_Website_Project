# Import labraries
import ctypes, sys
import time
from datetime import datetime as dt
from urllib.parse import urlparse
import requests

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

from Website_Databases import UserDB;


def main():
    Vu_Com = WebsiteBlocker();
    Vu_Com.Sorting_Porn_Website();
    Vu_Com.Importing_Website_To_SQL();

    if is_admin():
        Vu_Com.Unblocking_Websites()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1);


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


class WebsiteBlocker():
    def __init__(self):
        self.websites = [];
        # This specifically for windows, but not for androids, it requires some changes
        self.hostsPath = r"C:\Windows\System32\drivers\etc\hosts"
        self.redirect = "127.0.0.1"
        self.new_keyWord = []
        self.origin_websites = [];
        self.mySQL_data = UserDB();

    def SearchingWebsite(self, type_name = None):
        # Query for searching
        if type_name == None:
            print("Error");
        elif type_name == "Social Media":
            print("It Can Be Done")
            self.websites.clear();
            self.query = ["facebook","instagram","twitter","Snapchat","Youtube","tiktok"];
            for query in self.query:
                for j in search(query, tld="com", num=100, start = 0, stop=25, pause= 10):
                    self.websites.append(j);
        elif type_name == "Adult Content":
            print("It Can Be Done")
            self.websites.clear();
            self.query = ["porn","nhentai","jav","hentai"];
            for query in self.query:
                for j in search(query, tld="com", num=100, start=0, stop=25, pause=10):
                    self.websites.append(j);
        elif type_name == "All Content":
            print("It Can Be Done")
            self.websites.clear();
            self.query= ["facebook","instagram","twitter","Snapchat","Youtube","tiktok","porn","nhentai","jav","hentai"];
            for query in self.query:
                for j in search(query, tld="com", num=100, start=0, stop=25, pause=10):
                    self.websites.append(j);
        else:
            print("Error!")

    def Sorting_Porn_Website(self):
        for item in self.websites:
            new_item = urlparse(item);
            new_item = new_item.netloc;
            term_Split = new_item.split('.');
            if len(term_Split) == 2:
                self.new_keyWord.append(term_Split[0]);
            if len(term_Split) == 3:
                self.new_keyWord.append(term_Split[1]);
            self.origin_websites.append(new_item);

        self.origin_websites = list(dict.fromkeys(self.origin_websites));
        self.new_keyWord = list(dict.fromkeys(self.new_keyWord));
        print("Sorting Completed")

    def Importing_Website_To_SQL(self):
        self.mySQL_data.Clear_Data()
        self.mySQL_data.insertURL_multiple(self.origin_websites)
        # self.mySQL_data.readURL();
        print("Importing Completed")

    def Blocking_Websites(self):
        self.mySQL_data.readURL();
        with open(self.hostsPath, "r+") as file:
            self.content = file.read()
            for site in self.mySQL_data.data:
                if site in self.content:
                    pass
                else:
                    file.write(self.redirect + " " + site + "\n")
        print("Blocking Completed")

    def Blocking_Single_Website(self, website_name):
        self.mySQL_data.insertURL(website_name)
        self.mySQL_data.readURL();
        with open(self.hostsPath, "r+") as file:
            self.content = file.read()
            for site in self.mySQL_data.data:
                if site in self.content:
                    pass
                else:
                    file.write(self.redirect + " " + site + "\n")

    def Unblocking_Websites(self):
        self.mySQL_data.readURL();
        with open(self.hostsPath, 'r+') as file:
            content = file.readlines()
            file.seek(0)
            for line in content:
                if not any(site in line for site in self.mySQL_data.data):
                    file.write(line)
                file.truncate()
        self.mySQL_data.Clear_Data()

    def Unblocking_Multiple_Selected_Website(self, Website_list):
        self.mySQL_data.readURL();

        # Removing everything in mySQL server
        for unblocking_site in Website_list:
            for site in self.mySQL_data.data:
                if unblocking_site == site:
                    self.mySQL_data.deleteURL(site)
                    break;
                else:
                    pass

        # Blocking only the website that is remained on the database table, else unblock the rest
        self.mySQL_data.readURL();
        with open(self.hostsPath, 'r+') as file:
            content = file.readlines()
            file.seek(0)
            for line in content:
                if any(site in line for site in self.mySQL_data.data):
                    file.write(line)
                file.truncate()


    def Unblocking_Single_Website(self, website_index=None, website_name=None):
        self.mySQL_data.readURL();

        # Looking for the website_name in the list
        if website_name == None:
            for site in self.mySQL_data.data:
                if site == self.mySQL_data.data[website_index]:
                    self.mySQL_data.deleteURL(site);
                    break;
                else:
                    pass
        elif website_index == None:
            for site in self.mySQL_data.data:
                if site == website_name:
                    self.mySQL_data.deleteURL(site);
                    break;
                else:
                    pass

        self.mySQL_data.readURL();
        with open(self.hostsPath, 'r+') as file:
            content = file.readlines()
            file.seek(0)
            for line in content:
                if any(site in line for site in self.mySQL_data.data):
                    file.write(line)
                file.truncate()

    def Checking_Website_list(self, url):
        self.mySQL_data.readURL();
        for site in self.mySQL_data.data:
            if site == url:
                return True
            else:
                pass
        return False

    def Reading_Database(self):
        self.mySQL_data.readURL();
        return self.mySQL_data.data;


    def Check_Website(self, URL):
        # Manipulating string to have a correct URL
        try:
            Heading, Body, Tail = URL.split('.');
            if Heading != "http://www":
                Heading = "http://www";
                Full_URL = Heading + '.' + Body + '.' + Tail;
            else:
                pass
        except:
            Full_URL = False
            return False;
        try:
            request = requests.get(Full_URL);
        except:
            return False
        else:
            return True


if __name__ == "__main__": main()
