###############################################################################
#
#   1/19/19
#   Rapository.py
#   Erich Hairston and Mac Catrambone
#   
#   This program intends to assist songwriters in finding words that rhyme.
#   It uses user input and web scraping to compile a database of rhymes
#   Ultimately, we would like it to suggest only the top ten most common rhymes
#   
#   Things to do:
#       Try using an Excel file as our database instead of a Text file
#       X Be able to determine the number of words in the database at any time
#       Always be updating which rhymes are used most frequently
#       Look into using mySQL for the database
#       Jump to search instead of looping through
#       User interface (Make it pretty and easy to use)
#
##############################################################################


from lxml import html
import requests

def GetRhymes(word):
    """
    Given a word, scrapes the web (Rhymezone.com) to find words that rhyme with it.
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
    Checks for a specific word in our database.
    Returns a tuple of the form (boolean, index, set)
    If it finds the word:
        Retrieves the rhymeset from the database.
        (True, position in the DB, rhymeset)
    If it does not:
        (False, -1, {} )
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
    """
    Clears the database
    """
    fp = open("RhymeDB.txt", 'w')
    fp.close()
    return 0

def PrintDB():
    """
    Prints every rhymeset in the dictionary in an organized manner.
    """
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
        user_input = (input("Enter a word ('q' to quit, 'cc' to clear): ")).strip().lower()
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
                print("On file\n")
                print(tup[2],"\n")
                print("Size of the Database: ", SizeDB, "\n")
            else:
                print("New word added\n")
                words_added = AddWord(word)
                tup = CheckDB(word)
                if (tup[0] == True):
                    SizeDB += len(tup[2])
                    print(tup[2], "\n")
                    print("Size of the Database: ", SizeDB,"\n")
                else:
                    print("Error in CheckDB function\n")
            continue
    print("\n----------\n")
    PrintDB()
    print("\n----------\n")
    print("Size of the Database: ", SizeDB)
    return 0

if __name__ == "__main__":
    main()
