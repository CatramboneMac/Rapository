from lxml import html
import requests
import pickle
#import mysql.connector

#mydb = mysql.connector.connect(host="localhost", user="root", passwd="24ShotClock!")
#mycurser = mydb.cursor()
#mycurser.execute("show database")
#for i in mycurser:
#    print(i)

# def FindWords(filename):
#     """
#     Given a filename, opens the file that contains hella words (xlsx, csv, or txt).
#     Creates a set containing the words in the file.
#     """
#     fp = open(filename,"r")
#     word_list = []
#     first_line = fp.readline().strip()
#     if ( (first_line.find(",") == -1) ):
#         for line in fp:
#             line = line.strip()
#             word_list.append(line)
#     else:
#         row_list = first_line.strip().split(",")
#         for word in row_list:
#             word.strip()
#             word_list.append(word)
#     word_set = set(word_list)
#     return word_set

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

# def PullRhyme(word):
#     """
#     Uses CheckDB to search the database for a word.
#     If it finds it:
#         -Pulls and returns the list of rhymes
#     If it does not:
#         -Uses AddWord to add the word (and it's rhymes) to the DB
#         -Returns a list of rhyming words.
#     """
#     rhyme_set = {}
#     boolean = CheckDB(word)
#     if (boolean == True):
#         fp = open("RhymeDB.txt","r")
#         break_bool = False
#         for line in fp:
#             line = line.strip().split(";")
#             index = -1
#             for i in line:
#                 index += 1
#                 for j in i:
#                     if (j == word):
#                         rhyme_list = line[index]
#                         rhyme_set = set(rhyme_list)
#                         break_bool = True
#                         break
#                     if (break_bool == True):
#                         break
#             if (break_bool == True):
#                 break     
#         fp.close()
#     return rhyme_set


def main():
    # filename = "words.csv" #input("Enter a file containing words: ")
    # word_set = FindWords(filename)
    #for word in word_set:
    #    word = word.strip()
    #    boolean = CheckDB(word)
    #    if (boolean == False):
    #        word_added = AddWord(word)
    #        print(word_added)
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