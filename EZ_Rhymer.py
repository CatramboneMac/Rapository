from lxml import html
import requests

def GetRhymes(word):
    url_string = "https://www.rhymezone.com/r/rhyme.cgi?Word=" + str(word).strip() + "&typeofrhyme=perfect&org1=syl&org2=l&org3=y"
    url_string = str(url_string)
    page = requests.get(url_string)
    tree = html.fromstring(page.content)
    rhymes = tree.xpath('//b//a[@class="r"]/text()')
    rhyme_set = set(rhymes)
    return rhyme_set

def main():
    fp = open("words.csv", "r")
    i = 0
    rhyme_dict = {}
    for line in fp:
        i += 1
        line = line.strip().split()
        base_rhyme = line[0].strip()
        rhyme_set = GetRhymes(base_rhyme)
        rhyme_dict[base_rhyme] = rhyme_set
    for i in rhyme_dict:
        print(i)
        print()
        print(rhyme_dict[i])
    
    return 0

if __name__ == "__main__":
    main()
