from modules.module import module ;
import urllib.request
import urllib.parse
import html;
import re ;
from bcolors import bcolors ;
import time;

# Some Constants
title_regex = re.compile("\\?\"author\\?\":\\?\"");
youtube_url = "https://www.youtube.com/watch?v="

def findTitleOther(url, delay=0):
    ret = "";
    try:
        req = urllib.request.Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'})
        webpage = urllib.request.urlopen(req, timeout=5).read()
        webpage = html.unescape(webpage.decode(encoding="utf8"))
        title = webpage.split('<title>')[1].split('</title>')[0]
        ret += '<br>'+url+'<br>';
    except:
        pass
    if ret:
        time.sleep(delay)
    return title

def findTitleYouTube(url, delay=0):
    ret = "";
    try:
        video_id = url.split("watch?v=")[1]
        video_id = video_id.split("&")[0];
        video_url = "\""+youtube_url+video_id+"\""
        print(video_url)
        webpage = urllib.request.urlopen(url, timeout=5).read()
        webpage = html.unescape(webpage.decode(encoding="utf8"))
        webpage = webpage.replace("\\","") # pas très propre, à refaire avec regex plus tard (author = re.findall(title_regex, webpage)) ?
        ###############################################
        author = (webpage.split("\"author\":\""));
        author = author[1];
        author = author.split("\"")[0];
        ###############################################
        title = webpage.split(video_url);
        title = title[1]
        title = title.split("content=\"");
        title = title[1]
        title = title.split('\"')[0]
        ret = '<b>{}</b> \u2014 {}<br>{}<br>'.format(author.capitalize(), title.capitalize(), url);
    except:
        pass
    if ret:
        time.sleep(delay)
    return ret


class url_bot(module):

    url_regex = re.compile("(https?|ftp|ssh|mailto):\/\/[\u00C0-\u017Fa-z0-9\/:%_+.,#?!@&=-]+", re.IGNORECASE)

    def __init__(self, keyword = "url_bot", is_permanent = False): # <- template ... Here goes your default module name
        super().__init__(keyword, is_permanent) ;
        self.module_name = "url_bot"
        self.whatis = "Get small description from url"
        self.__version__ = "0.0.1"
        self.help = "None"

    @module.login_check_dec
    def process_msg_passive(self, cmd, sender, room):
        if len(cmd)>0 and cmd[0] == ">": # Cette condition permet de ne pas traiter les citations (i.e. lien déjà posté).
            return "";
        reg_match = re.finditer(url_bot.url_regex, cmd);
        ret = "" ;
        for match in reg_match: # si une url valide est trouvée ...
            url = match.group(0) ;
            print("{}>>> current url: {}{}".format(bcolors.OKBLUE,url,bcolors.ENDC))
            if url.find("youtu") > 0: # not perfect, should be modified with regex.
                ret += findTitleYouTube(url, delay=1);
            elif url.find("twitter.") > 0:
                pass # do nothing for now ...
            else:
                ret+= findTitleOther(url, delay=1);
        if ret != "":
            ret= "<blockquote>"+ret+"</blockquote>"
        return ret;

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=KXatvzWAzLU";
    title = findTitleYouTube(url)
    parsed_url = urllib.parse.urlparse(url);
    print(title)
    print(parsed_url.netloc)
