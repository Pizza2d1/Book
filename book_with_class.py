#Expanded idea of journaltest.py to have a navigatable journal/book that allows you to search day, month, year, and iteration.
#Need to add a more friendly user interface that works in both python terminals-
#-and making the program more concise (less but bigger functions?), maybe add-
#-a function that reads filecode.txt and put its data in global variables so read() and write() dont have to manually do it, dates-
#-have finally been added which was a pain in the butt, I might do another setting that changes (month/day/year) to (hour:minute \t day/month).
#THIS CREATES TWO NEW TEXT FILES ON YOUR COMPUTER: filecode.txt and a1lockedbook.txt

import book_class
from datetime import datetime
import random
import os
FILECODE_LINES = 4  #const value that depends on the number of lines in filecode.txt for reading the file and writing back to the file
retryswitch = 1     #variable that works as a switch for if the program will continue taking user input

print('   ___________  \n  /           \ \n |    BOOK     |\n  \___________/')  #a dumb title
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

def route_selection(uinput):    #Choses what function or class the user goes to based on input
    global retryswitch
    num = numfunc()
    code = codefunc()
    if uinput != '':
        uinput = uinput.lower()
    else:
        return
    if uinput == 'r' or uinput == 'read' or uinput == '1' or uinput == 'READ':
        book_class.Read(num, code, delreadfunc(), finddate()).read()
        retry(num,code)
    elif uinput == 'write' or uinput == 'w' or uinput == '2' or uinput == 'WRITE':
        uinput = input("Text: ")
        if uinput != '':
            book_class.Write(numfunc(),codefunc(), uinput)
            num += 1
        retry(num,code)
    elif uinput == 'n' or uinput == 'no' or uinput == '2' or uinput == 'NO':
        retryswitch = 0
        return
    elif uinput == 'd' or uinput == 'delete' or uinput == '3' or uinput == 'DELETE':
        book_class.Delete(num,code,uinput)
        if not os.path.isfile("filecode.txt"):
            retryswitch = 0
            return
    elif uinput == 's' or uinput == 'settings' or uinput == '4' or uinput == 'SETTINGS':
        settings(num)
    elif uinput == 'se' or uinput == 'search' or uinput == '5' or uinput == 'SEARCH':
         search(num,code,input("Month, Day, or Year? 1/2/3: "))
    else:
        print('Invalid input')
        retryswitch = 0
        return

def retry(num,uinput):          #Just a loop that checks if your input is n/no when asking if you want to end
    num = numfunc()
    code = codefunc()
    if retryswitch == 0:
        return
    else:
        uinput = input('Again?: N̲o/R̲ead/W̲rite/D̲elete/S̲ettings/S̲e̲arch: ')
        route_selection(uinput)

def scramble():                 #Changes the file name of (?)lockedbook.py and file data of filecode.txt
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

def settings(num):              #Allows you to have different settings
    print('Settings\n\n1. See deleted iterations: ' + str(delreadfunc()))
    print('2. See dawg: ' + str(doggyfunc()))
    uinput = input('Which settings do you want to change? Enter nothing to go back: ')
    if uinput == '':
        retry(num,uinput)
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

def search(num,code,uinput):    #Lets the user find a set of iterations that depends on a day, month, year of their choosing
    if uinput.isdigit: place = int(uinput)-1; readlist = []; dates = []; date = input("Number: "); list1 = []
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
    return retry(num,uinput)

#Short functions
def finddate():         #Is used to get all the month/day/year values from lockedbook.txt
    num = numfunc()
    code = codefunc()
    dates = []
    with open(code + 'lockedbook.txt', 'r') as bfile:
        for x in range(num):
            dates.append((bfile.readline())[-9:-1])
    return dates
def codefunc():         #Takes the code (a letter and a number) to find file from filecode.txt
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
def delreadfunc():      #Takes value of setting 1, returns True or False
    delread = 0
    with open('filecode.txt','r') as file:
        codes = []
        for x in range(FILECODE_LINES):
            codes.append(file.readlines())
    delread = int((sum(codes,[]))[2])
    return bool(delread)
def doggyfunc():        #Takes value of setting 1, returns True or False
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


def main():     #I dont like the idea of main functions but added it anyways, look how short it is, seems completely unnecessary right?
    firsttime()
    while retryswitch:
        uinput = input("Open book? N̲o/R̲ead/W̲rite/D̲elete/S̲ettings/S̲e̲arch: ")
        route_selection(uinput)

main()
if os.path.isfile("filecode.txt"):  #checks for filecode.txt just in case if the user cleared both text files by selecting delete and inputing "all" when selecting an iteration
    scramble()
    if doggyfunc():                 #doggy woggy
        doglist = ["     |\_/|\n     | @ @   Woof!\n     |   <>              _\n     |  _/\------____ ((| |))\n     |               `--' |\n ____|_       ___|   |___.'\n/_/_____/____/_______|", "^..^      / \n/_/\_____/ \n   /\   /\ \n  /  \ /  \ ", "       _=,_\n    o_/6 /#\ \n    \__ |##/\n     ='|--\ \n       /   #'-.\n       \#|_   _'-. /\n        |/ \_( # |" + "\n       C/ ,--___/"]
        
        print(random.choice(doglist) + "\nGet dogged on")
else:
    print("End")
