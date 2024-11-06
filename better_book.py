import book_class                   #Personal python program that I made because I wanted to learn how classes work, plus it looks cool
from datetime import datetime       #Needed to add accurate timestamps to iterations as you make them so I don't have to calculate the different day amounts in each month when its a new year
import random                       #Used to allow the (?)lockedbook.txt to have a random "code" assigned to it
import os                           #Needed to create and delete files, also useful for reseting to fix problems
FILECODE_LINES = 4                  #const value that depends on the number of lines in filecode.txt for reading the file and writing back to the file
retryswitch = 1                     #variable that works as a switch for if the program will continue taking user input

print("_________________________")  #A title for the program using figlet (letter expander)
print(" ____   ___   ___  _  __")     
print("| __ ) / _ \ / _ \| |/ /")
print("|  _ \| | | | | | | ' / ")
print("| |_) | |_| | |_| | . \ ")
print("|____/ \___/ \___/|_|\_\ ")
print("_________________________")

def firsttime():                #When using the program for the first time, it makes two new text files to read/write and get data from
    if os.path.isfile('filecode.txt') == False:
        open('filecode.txt', "x")
        with open('filecode.txt', 'w') as text:
            text.write('a1\n1\n1\n1\n')
        open('a1lockedbook.txt', 'x')
        time = datetime.now()
        with open('a1lockedbook.txt', 'w') as book:
            book.write('This is the first line, you can add others by choosing to "write" instead of "read". You can also choose to delete different iterations or go to settings  '
                       + str(time.month)+'/'+str(time.day)+'/'+str(time.year-2000) + '\n')

def resettext():                #Resets both filecode.txt and (?)lockedbook.txt so that older versions of the txt files don't break newer versions of the python programs
    open('filecode.txt', "w")
    with open('filecode.txt', 'w') as text:
        text.write('a1\n0\n1\n1\n') #Set to no iterations ('al\n0 <---- the zero) which is different to original firsttime() settings
    open('a1lockedbook.txt', 'w')
    time = datetime.now()
    with open('a1lockedbook.txt', 'w') as book:
        book.write('')


def route_selection(uinput):    #Choses what function or class the user goes to based on input
    global retryswitch
    num = numfunc()
    code = codefunc()
    if uinput != '':
        uinput = uinput.lower()
    else:
        return
    if uinput in ['n', 'no', '1']:
        retryswitch = 0
        return
    elif uinput in ['r', 'read', '2']:
        book_class.Read(num, code, delreadfunc(), finddate(), FILECODE_LINES).read()
        retry()
    elif uinput in ['w', 'write', '3']:
        uinput = input("Text: ")
        if uinput != '':
            book_class.Write(numfunc(),codefunc(), uinput)
            num += 1
        retry()
    elif uinput in ['d', 'delete', '4']:
        book_class.Delete(num,code,uinput)
        if not os.path.isfile("filecode.txt"):
            retryswitch = 0
            return
    elif uinput in ['s', 'settings', '5']:
        settings(num)
    elif uinput in ['se', 'search', '6']:
        search(num,code,input("Month, Day, or Year? 1/2/3: "))
    elif uinput in ['re', 'reset', '7']:
        resettext()
        print("All iterations have been deleted\n")
        return
    elif uinput in ['h', 'help', '8']:
        print("\n\n\nSup faggots (respectfully), looks like you can't figure out the menu system, here's a little guide so that you can understand:\n")
        print('When given the options: No/Read/Write/Delete/Settings/Search/Reset/HELP\nYou are able to either type them out fully, select them by number(e.g. Read is "2"), or you can just type the first letter of the word')
        print('The abbrevatitions are: n/r/w/d/s/se/re/h')
        print('\nThese were made so that debugging could be done in only 3-4 keystrokes, so now you can do it too, if there are any breaks or weird print statements\n(such as lists), please let me know\nI dont like looking through them myself\n\n\n')
    else:
        print('Invalid input')
        retryswitch = 0
        return

def retry():                    #Just a loop that checks if your input is n/no when asking if you want to end
    if retryswitch == 0:
        return
    else:
        uinput = input('Again?: No/Read/Write/Delete/Settings/Search/Reset/HELP: ')
        route_selection(uinput)

def scramble():                 #Changes the file name of (?)lockedbook.py and file data of filecode.txt so that the code of lockedbook has a purpose
    code = codefunc()
    list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',1,2,3,4,5,6,7,8,9]
    l = random.randint(0,25)
    n = random.randint(26,34)
    new_code = str(list[l]) + str(list[n])
    with open(code + 'lockedbook.txt', 'r') as file:
        text = file.read()
    if os.path.exists(code + 'lockedbook.txt'):
        os.remove(code + 'lockedbook.txt')
    with open(new_code + 'lockedbook.txt', 'w') as file:
        file.write(text)
    with open('filecode.txt', 'r') as file:
        numlist = []
        for x in range(FILECODE_LINES):
            numlist.append(file.readlines())
    numlist = sum(numlist,[])
    numlist[0] = (new_code + '\n')
    with open('filecode.txt', 'w') as file:
        for x in numlist:
            file.write(str(x))

def settings(num):              #Allows you to look through the different settings and change them by changing their value in filecode.txt
    print('Settings\n\n1. Include deleted iterations: ' + str(delreadfunc()))
    print('2. See dawg: ' + str(doggyfunc()))
    uinput = input('Which settings do you want to change? Enter nothing to go back: ')
    if uinput == '':
        retry()
        return
    with open('filecode.txt', 'r') as text:
        filelist = []
        for x in range(FILECODE_LINES):
            filelist.append(text.readline())
    filelist[int(uinput)+1] = switch(filelist[int(uinput)+1])
    with open('filecode.txt','w') as text:
        for x in range(FILECODE_LINES):
            text.write(filelist[x])
    settings(num)
    return

def search(num,code,uinput):    #Lets the user find a set of iterations that depends on a day, month, year of their choosing, I might set up a choice to lookup a RANGE of dates but that's much later
    if uinput.isdigit() and uinput:
        place = int(uinput)-1
    else:
        print("You have to enter a number, sending you back...\n")
        return retry()
    readlist = []; dates = []; date = input("Number: "); list1 = []
    with open(code+'lockedbook.txt','r') as bfile:
        for x in bfile:
            readlist.append(x)
    for x in readlist:
        for y in (''.join(x[-9:].split())).split('/'):
            if len(y) == 3: y = y[:-1]
            elif not y.isdigit() and len(y) == 2:
                y = y[1:]
            dates.append(y)
    ifprint = False
    if date in dates:
        for x in range(num):
            if dates[(place+3*x)] == date:
                print('Iteration ' + str(x+1) + '\t' + (readlist[x])[-9:] + (readlist[x])[:-9] + '\n')
                ifprint = True
    if not ifprint:
        print("No iterations followed that date")
    return retry()

#Short functions that I decided to group together
def finddate():         #Is used to get all the month/day/year values from lockedbook.txt and returns as a list
    num = numfunc()
    code = codefunc()
    dates = []
    with open(code + 'lockedbook.txt', 'r') as bfile:
        for x in range(num):
            dates.append((bfile.readline())[-9:-1])
    return dates
def codefunc():         #Takes the code of the lockedbook.txtfrom filecode.txt to find it in the file system, e.g. "a1" or "f6", stupid concept but it is very old so it's nostalgic now
    code = ''
    with open('filecode.txt','r') as file:
        code = file.readline()[0:-1]
    return code
def numfunc():          #Takes number of iterations from filecode.txt, next to codefunc() because similar
    num = 0
    with open('filecode.txt','r') as file:
        codes = []
        for x in range(FILECODE_LINES):
            codes.append(file.readlines())
    num = int((sum(codes,[]))[1])
    return num
def delreadfunc():      #Setting to decide if previously deleted iterations should be included when reading as blank or "[Deleted]", returns True or False, third line in filecode.txt
    delread = 0
    with open('filecode.txt','r') as file:
        codes = []
        for x in range(FILECODE_LINES):
            codes.append(file.readlines())
    delread = int((sum(codes,[]))[2])
    return bool(delread)
def doggyfunc():        #Setting for whether or not ASCII dogs are shown at the end of the user interaction, returns True or False, fourth line in filecode.txt
    doggy = 0
    with open('filecode.txt','r') as file:
        codes = []
        for x in range(FILECODE_LINES):
            codes.append(file.readlines())
    doggy = int((sum(codes,[]))[3])
    return bool(doggy)
def switch(x):          #Switches values in text file 1/0 (Changes true to false and vice versa) used for settings rn
    if x == '0\n':
        return '1\n'
    else:
        return '0\n'


def main():                         #I dont like the idea of main functions but added it anyways, look how short it is, seems completely unnecessary right?
    firsttime()
    while retryswitch:
        uinput = input("Open book? No/Read/Write/Delete/Settings/Search/Reset/HELP: ")
        route_selection(uinput)

main()
if os.path.isfile("filecode.txt"):  #checks for filecode.txt just in case if the user cleared both text files by selecting delete and inputing "all" when selecting an iteration
    scramble()
    if doggyfunc():                 #doggy woggy
        #doglist = ["     |\_/|\n     | @ @   Woof!\n     |   <>              _\n     |  _/\------____ ((| |))\n     |               `--' |\n ____|_       ___|   |___.'\n/_/_____/____/_______|",
        #           "^..^      / \n/_/\_____/ \n   /\   /\ \n  /  \ /  \ ",
        #           "       _=,_\n    o_/6 /#\ \n    \__ |##/\n     ='|--\ \n       /   #'-.\n       \#|_   _'-. /\n        |/ \_( # |" + "\n       C/ ,--___/"]
        #print(random.choice(doglist) + "\nGet dogged on")
        pass                    #CURRENTLY BEING WORKED ON TO PREVENT "Invalid escape sequence"
else:
    print("Looks like you chose to delete everything so I'm just gonna close the program, maybe don't do that next time")
    print("End")
