from urllib.request import Request, urlopen
from urllib.request import urlretrieve
import urllib.request
from bs4 import BeautifulSoup as bs
import webbrowser
user = input("Please Enter a movie name: ")


#lower
i1 = user.lower()

#add space replace
i2 = i1.replace(" ", "+")

url = Request('https://www.google.com/search?tbm=isch&source=hp&biw=1366&bih=637&ei=ns6PWtj9L8rI0ATG-ZWwCw&q=' + str(i2)  + '&oq=' + str(i2) + '&gs_l=img.3..0l10.1716.2402.0.2937.8.6.0.0.0.0.268.767.2-3.3.0....0...1ac.1.64.img..5.3.757.0...0.wwV7uiPO8hE', headers={'User-Agent': 'Mozilla/5.0'})


html = urlopen(url)
contents = html.read()
soup = bs(contents, "lxml")

#crawling for the exact data that we need that is the release date

image = soup.findAll("img")
for i in image:
    print(i["src"])
image_name = str(i2) + ".jpg"
# urllib.request.urlretrieve(str(link["src"]), image_name)


