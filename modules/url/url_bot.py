from modules.module import module ;
import urllib.request
import urllib.parse
import html;
import re ;
from bcolors import bcolors ;


def findTitleOther(url):
    title = "";
    try:
        webpage = urllib.request.urlopen(url, timeout=5).read()
        webpage = html.unescape(webpage.decode(encoding="utf8"))
        title = webpage.split('<title>')[1].split('</title>')[0]
        title += '<br>'+url+'<br>';
    except:
        pass
    return title

def findTitleYouTube(url):
    title = "";
    try:
        webpage = urllib.request.urlopen(url, timeout=5).read()
        webpage = html.unescape(webpage.decode(encoding="utf8"))
        webpage = webpage.split("https://www.youtube.com/watch?v")[1];
        title = webpage.split("content=\"")[1].split('\"')[0]
        title += '<br>'+url+'<br>';
    except:
        pass
    return title


class url_bot(module):

    url_regex = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.IGNORECASE)

    def __init__(self, keyword = "url_bot", is_permanent = False): # <- template ... Here goes your default module name
        super().__init__(keyword, is_permanent) ;
        self.module_name = "url_bot"
        self.whatis = "Get small description from url"
        self.__version__ = "0.0.1"
        self.help = "None"

    @module.login_check_dec
    def process_msg_passive(self, cmd, sender, room):
        reg_match = re.finditer(url_bot.url_regex, cmd);
        ret = "" ;
        for match in reg_match: # si une url valide est trouvée ...
            url = match.group(0) ;
            print("{}>>> current url: {}{}".format(bcolors.OKBLUE,url,bcolors.ENDC))
            if url.find("youtu") > 0: # not perfect, should be modified with regex.
                ret += findTitleYouTube(url);
            elif url.find("twitter.") > 0:
                pass # do nothing for now ...
            else:
                ret+= findTitleOther(url);
        if ret != "":
            ret= "<blockquote>"+ret+"</blockquote>"
        return ret;

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=KXatvzWAzLU";
    title = findTitleYouTube(url)
    parsed_url = urllib.parse.urlparse(url);
    print(title)
    print(parsed_url.netloc)
