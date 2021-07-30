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


    if is_admin():
        Vu_Com.Unblocking_Websites();
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
        self.origin_websites = ['www.pornhub.com', 'www.xnxx.com', 'www.xvideos.com', 'www.fuq.com', 'www.youporn.com', 'www.statnews.com', 'www.porn.com', 'www.forhertube.com', 'mydamplips.com', 'www.bbc.com', 'xhamster.com', 'www.dailymail.co.uk', 'www.forbes.com', 'www.ixxx.com', 'www.tiava.com', 'en.vidmo.org', 'krebsonsecurity.com', 'www.webroot.com', 'www.thumbzilla.com', 'en.wikipedia.org', 'www.youjizz.com', 'teencumpot.com', '0dayporn.com', 'www.theguardian.com', 'www.xvideos.es', 'cabinporn.com', 'www.reddit.com', 'www.independent.co.uk', 'www.rollingstone.com', 'en.paradisehill.cc', 'pornhail.com', 'pornmilo.com', 'animalporn.rocks', 'www.bellesa.co', 'xfantazy.com', 'www.cnn.com', 'www.largepornfilms.com', 'gofucker.net', 'www.redtube.com', 'goingconcern.com', 'motherless.com', 'www.channel4.com', 'twister.porn', 'www.fapvidhd.com', 'www.fapvid.com', 'www.pornfuror.com', 'porn.porn', 'en.luxuretv.com', 'www.vice.com', 'sxyprn.net', 'www.theyarehuge.com', 'maturepornvideo.pro', 'happy-porn.com', 'www.ebonypulse.tv', '111.90.150.188', 'porno-apk.com', 'xixiporn.com', 'www.qorno.com', 'www.maturetube.com', 'www.fortnite-porn.com', 'twitter.com', 'girlsonporn.com', 'www.porngray.com', 'sopornmovies.com', 'beastiegals.com', 'www.pornsintube.com', 'whataporn.tv', 'www.porn.biz', 'www.hdsexdino.com', 'www.psychguides.com', 'www.hqbutt.com', 'www.porn00.org', 'www.cybercivilrights.org', 'www.sopornvideos.com', 'www.vox.com', 'www.goldporntube.com', 'www.spicytrannyhd.com', 'www.sweetshow.com', 'shooshtime.com', 'petrol.porn', 'www.youteenporn.net', 'anon-v.com', 'www.wifesharing.pro', 'www.pornv.io', 'www.xporn.su', 'www.porn.sc', 'www.sunporno.com', 'www.maxiporn.com', 'asianporn.life', 'hentaihaven.xxx', 'hanime.tv', 'animeidhentai.com', 'hentaidude.com', 'hentaihaven.red', 'www.hentai-foundry.com', 'hentaimama.io', 'online.hentaistream.com', 'theporndude.com', 'doujins.com', 'hentaihaven.me', '9hentai.com', 'store.steampowered.com', 'hentaiplay.net', 'hentaifox.com', 'spankbang.com', 'hentaikisa.com', 'teenspirithentai.com', 'www.fakku.net', 'www.underhentai.net', 'www.hentais.tube', 'hentaipulse.com', 'nekopoi.care', 'www.urbandictionary.com', 'hentairead.com', 'www.dictionary.com', 'hentaifromhell.org', 'hentai.mg-renders.net', 'www.hentaicomics.pro', 'hentai.animestigma.com', 'kisshentai.net', 'thatpervert.com', 'www.lolhentai.net', 'hentaihaven.vip', 'hentaispark.com', 'www.newgrounds.com', 'hentai2read.com', 'hentaigamer.org', 'myhentaicomics.com', 'www.hentaiheroes.com', 'www.hentaitube.online', 'anime.freehentaistream.com', 'nearhentai.com', 'www.hentaibaka.pro', 'hentaigasm.com', 'tmohentai.com', 'ahegao.online', 'imhentai.com', 'hentaicore.org', 'www.xanimeporn.com', 'www.onlyhgames.com', 'myhentaigallery.com', 'ohentai.org', 'allporncomic.com', 'store.nutaku.net', 'haho.moe', 'www.hentaimanga.pro', 'www.hentaicon.com', 'pururin.io', 'www.hentaicloud.com', 'www.porn300.com', 'hentaisun.com', 'narutopixxx.com', 'e-hentai.org', 'hot-sex-tube.com', 'pagehentai.com', 'ani.erokuni.net', 'www.hentaivideoworld.com', 'hentai-comic.com', 'mangahentai.me', 'verhentai.top', 'whentai.com', 'www.h-suki.com', 'hentaigasm.tv', 'fullporn.online', 'chochox.com', 'league-of-hentai.com', 'thehentaiworld.com', 'www.hentairules.net', 'www.naughtyhentai.com', 'lumendatabase.org', 'jav.sh', 'javseen.tv', 'jav.guru', 'jav.la', 'javxxx.me', 'jav247.net', 'www5.javmost.com', 'en.wiktionary.org', 'www.ethnologue.com', 'bestjavporn.com', 'javhd.zone', 'javhd.today', 'sextop.net', 'hpjav.tv', 'vjav.com', 'www.zenra.net', 'www.incestflix.com', 'actionjav.com', 'www.delfi.lt', 'www.jamesarthurvineyards.com', 'www.linkedin.com', 'javxxxtube.com', 'jav.land', 'avcrempie.com', 'www.instagram.com', 'www.facebook.com', 'tubeqd.tv', 'subjav.com', 'javhd.com', 'eu-jav.com', 'javsub.co', 'javleak.com', 'www.vz.lt', 'jerkhd.com', 'japanesebeauties.net', 'jav.photos', 'www.free-porn.info', 'sexloading.com', 'www.javgayhd.com', 'javforme.ninja', 'javhub.net', 'cosplay.jav.pw', 'www.yourdictionary.com', 'www.ozeex.com', 'onejav.com', 'javhd.pics', 'javstream.us', 'www.9xxx.net', 'javfree.biz', '123jav.me', 'javplay.me', 'www.glassdoor.com', 'javopen.co', 'javladies.com', 'www.xvideos2.com', 'jpxxx.tv', 'www.15min.lt', 'javqq.com', 'www.lrytas.lt', 'mobile.odir.us', 'javbtc.com', 'watchjavonline.com', 'javmodel.com', 'javflash.net', 'www.lrt.lt', 'www.diena.lt', 'www.flickr.com', 'javnow.net', 'theartistunion.com', 'javloli.com', 'newjavxxx.com', 'jav.im', 'javmovs.com', 'bebokep.net', 'mustjav.com', 'www.javporn.net', 'top-jav.com', 'forums.hardwarezone.com.sg', 'www.chillingeffects.org'];
        self.mySQL_data = UserDB();

    def SearchingWebsite(self, type_name = None):
        # Query for searching
        if type_name == None:
            print("Error");
        elif type_name == "Social Media":
            print("It Can Be Done")
            # self.websites.clear();
            # self.query = ["facebook","instagram","twitter","Snapchat","Youtube","tiktok"];
            # for query in self.query:
            #     for j in search(query, tld="com", num=10, start = 0, stop=5, pause= 10):
            #         self.websites.append(j);
        elif type_name == "Adult Content":
            print("It Can Be Done")
            # self.websites.clear();
            # self.query = ["porn","nhentai","jav","hentai"];
            # for query in self.query:
            #     for j in search(query, tld="com", num=10, start=0, stop=5, pause=10):
            #         self.websites.append(j);
        elif type_name == "All Content":
            print("It Can Be Done")
            # self.websites.clear();
            # self.query= ["facebook","instagram","twitter","Snapchat","Youtube","tiktok","porn","nhentai","jav","hentai"];
            # for query in self.query:
            #     for j in search(query, tld="com", num=10, start=0, stop=5, pause=10):
            #         self.websites.append(j);
        else:
            print("Error!")

    def Sorting_Porn_Website(self):
        for item in self.websites:
            new_item = urlparse(item);
            print(new_item)
            new_item = new_item.netloc;
            term_Split = new_item.split('.');
            if len(term_Split) == 2:
                self.new_keyWord.append(term_Split[0]);
            if len(term_Split) == 3:
                self.new_keyWord.append(term_Split[1]);
            self.origin_websites.append(new_item);

        self.origin_websites = list(dict.fromkeys(self.origin_websites));
        self.new_keyWord = list(dict.fromkeys(self.new_keyWord));
        for item in self.origin_websites:
            if item == "www.youtube.com":
                self.origin_websites.remove("www.youtube.com");
            elif item == "www.facebook.com":
                self.origin_websites.remove("www.facebook.com");
            else:
                pass
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
