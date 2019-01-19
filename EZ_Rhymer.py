from lxml import html
import requests

def GetRhymes(word):
    """
    Given a word, scrapes the web (Rhymezone.com), to find words that rhyme with it.
    Returns a set of words that rhymes.
    """
    url_string = "https://www.rhymezone.com/r/rhyme.cgi?Word=" + str(word).strip() + "&typeofrhyme=perfect&org1=syl&org2=l&org3=y"
    url_string = str(url_string)
    page = requests.get(url_string)
    tree = html.fromstring(page.content)
    rhymes = tree.xpath('//b//a[@class="r"]/text()')
    rhyme_set = set(rhymes)
    rhyme_set.add(word)
    return rhyme_set

def CheckDB(word):
    """
    Given the set of word made in FindWords, creates a blank dictionary and uses GetRhymes to fill it.
    """
    fp = open("RhymeDB.txt",'r')
    boolean = False
    line_index = -1
    rhyme_set = {}
    line = fp.readline()
    line = line.strip().split(";")
    index = 0
    for rhyme_str in line:
        rhyme_list = rhyme_str.strip().strip(",").split(",")
        if (word.strip().lower() in rhyme_list):
            boolean = True
            rhyme_set = set(rhyme_list)
            line_index = index
        if (boolean == True):
            break
        index += 1
    fp.close()
    tup = (boolean,line_index,rhyme_set)
    return tup

def AddWord(word):
    """
    Uses GetRhymes to create a set of words that rhyme.
    Adds that set to RhymeDB.
    """
    num_words = 0
    rhyme_set = GetRhymes(word)
    rhyme_str = ""
    for i in rhyme_set:
        if (str(word) not in str(i)):
            rhyme_str += str(i).strip() + ","
    rhyme_str += word
    fp = open("RhymeDB.txt", "a")
    fp.write(rhyme_str.strip())
    fp.write(";")
    fp.close()
    return num_words

def ClearDB():
    fp = open("RhymeDB.txt", 'w')
    fp.close()
    return 0

def PrintDB():
    fp = open("RhymeDB.txt","r")
    line = fp.readline()
    line = line.strip().strip(";").split(";")
    for i in line:
        print(i.strip().strip(";").strip(","))
        print()
        print("-")
        print()
    return 0


def main():
    SizeDB = 0
    while True:
        user_input = (input("Enter a word ('q' to quit, cc to clear): ")).strip().lower()
        word = user_input.split()
        if (word[0].strip() == "q"):
            break
        elif (word[0] == "cc"):
            ClearDB()
            print("Database Cleared")
            SizeDB = 0
            continue
        else:
            word = word[-1].strip().lower()
            print()
            print ("++++++++++ {} ++++++++++".format(user_input))
            print()
            tup = CheckDB(word)
            if (tup[0] == True):
                SizeDB += len(tup[2])
                print("On file")
                print("Size of the Database: ", SizeDB)
                print(tup[2])
            else:
                print("New word added")
                word_added = AddWord(word)
                tup = CheckDB(word)
                if (tup[0] == True):
                    SizeDB += len(tup[2])
                    print("Size of the Database: ", SizeDB)
                    print(tup[2])
                else:
                    print("Error in CheckDB function")
            continue
    print()
    print("----------")
    print()
    PrintDB()
    print()
    print("----------")
    print()
    print("Size of the Database: ", SizeDB)
    return 0

if __name__ == "__main__":
    main()