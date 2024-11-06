from datetime import datetime
import os
class Variables():
    def __init__(self, num, code):
        self.number_of_iterations = num         #Number of iterations in text file
        self.start_of_textfile_code = code      #code to access the text file, (a-z)+(0-9)+(textfilename)


class Write(Variables):     #Writes a user input to the text file by copying the file's data, and then writing a list to it with the new input
    def __init__(self, number_of_iterations, start_of_textfile_code, user_input):
        super (Write, self).__init__(number_of_iterations, start_of_textfile_code)  #Takes the number of iterations and the code at the start of the text file from Variables()
        writelist = []
        print(user_input)
        with open(self.start_of_textfile_code + 'lockedbook.txt', 'a') as bfile:  #Takes the user input and modifies it to become ready to attach to the text file
            time = datetime.now()
            date = str(time.month)+'/'+str(time.day)+'/'+str(time.year-2000)
            while len(date) < 8:
                date = ' ' + date
            bfile.write(user_input+date+'\n')

        with open('filecode.txt', 'r') as text_file:    #Reads the previous iterations to add the user input to a list
            for x in range(4):#4 is the number of lines in filecode.txt
                writelist.append(text_file.readline())

        with open('filecode.txt', 'w') as text_file:    #Writes the list to the text file
            text_file.write(writelist[0])
            text_file.write(str(int(writelist[1]) + 1) + '\n')
            text_file.write(writelist[2])
            text_file.write(writelist[3])
        self.number_of_iterations += 1

class Read(Variables):      #Reads the text file and allows the user to decide which iteration to read or to read all of them
    def __init__(self, number_of_iterations, start_of_textfile_code, delreadfunc, finddate, num_of_lines_in_filecode):
        super (Read, self).__init__(number_of_iterations, start_of_textfile_code)   #Takes the number of iterations and the code at the start of the text file from Variables()                
        self.delreadfunc = delreadfunc  #Function to determine if you can read if a iteration is deleted, True or False
        self.finddate = finddate        #Function used to get the dates of all the iterations as a list
        self.num_of_lines_in_filecode = num_of_lines_in_filecode
    def inputcheck(user_input):     #Checks to see if an input is empty and if so returns to retry()
        if user_input == '':
            return False
        else:
            return True

    def readback(self):             #Reads the iteration number and dates, works with delreadfunc()
        readlist = []
        deleted = 0
        dates = self.finddate
        with open(self.start_of_textfile_code + 'lockedbook.txt', 'r') as bfile:
            for x in range(self.number_of_iterations):
                readlist.append('Iteration ' + str(x+1) + '\t' + dates[x])
                readlist.append((bfile.readline())[:-9] + '\n')
                if (readlist[-1] == '[Deleted]\n' or readlist[-1] == ('[Deleted]' + dates[x] + '\n')) and self.delreadfunc == False:
                    readlist.pop()
                    readlist.pop()
                    deleted += 1
        for x in range((self.number_of_iterations - deleted)*2):
            if readlist == '[Deleted]':
                pass
            elif readlist[x] != '':
                print(readlist[x])

    def nexti(self,user_input):     #Reads next iteration after read() selects a iteration
        readlist = []
        user_input += 1
        with open(self.start_of_textfile_code + 'lockedbook.txt', 'r') as bfile:
            for x in range(self.number_of_iterations):
                readlist.append(bfile.readline())
            if readlist[user_input]:
                if readlist[user_input] == '[Deleted]\n':
                    print('The iteration you have chosen has been deleted\n')
                else:
                    print(((self.finddate)[user_input]) + '\n' + ((readlist[user_input])[:-9]))
        new_user_input = input('Next iteration?y/n/b: ')
        if Read.inputcheck(new_user_input) == False:
            return
        if new_user_input == 'y' or new_user_input == 'yes' or new_user_input == '1':
            if (self.number_of_iterations-1) != user_input and user_input >= 0:
                Read.nexti(self, user_input)
            else:
                print("Can't go any further\n")
        elif new_user_input == 'b' or new_user_input == 'back' or new_user_input == '3':
            if user_input > 0:
                Read.backi(self, user_input)
            else:
                print("Can't go back any further\n")
        else:
            return user_input
    
    def backi(self,user_input):     #Reads last iteration after read() selects a iteration
        readlist = []
        user_input-=1
        with open(self.start_of_textfile_code + 'lockedbook.txt', 'r') as bfile:
            for x in range(self.number_of_iterations):
                readlist.append(bfile.readline())
            if readlist[user_input]:
                if readlist[user_input] == '[Deleted]\n':
                    print('The iteration you have chosen has been deleted\n')
                else:
                    print(self.finddate[user_input] + '\n' + (readlist[user_input])[:-9])
        new_user_input = input('Next iteration?y/n/b: ')
        if Read.inputcheck(new_user_input) == False:
            return
        if new_user_input == 'y' or new_user_input == 'yes' or new_user_input == '1':
            if (self.number_of_iterations-1) != user_input and user_input >= 0:
                Read.nexti(self, user_input)
            else:
                print("Can't go any further\n")
        elif new_user_input == 'b' or new_user_input == 'back' or new_user_input == '3':
            if user_input > 0:
                Read.backi(self, user_input)
            else:
                print("Can't go back any further\n")
        else:
            return

    def read(self):
        user_input = input('Which iteration do you want to read? all/num: ')
        if user_input == '':
            return
        readlist = []
        if user_input.isdigit():
            if int(user_input) > self.number_of_iterations:
                user_input = self.number_of_iterations
                with open(self.start_of_textfile_code + 'lockedbook.txt', 'r') as bfile:
                    for x in range(self.number_of_iterations):
                        readlist.append(bfile.readline())
                singleiteration = readlist[self.number_of_iterations-1]
                print(singleiteration[-9:])
                user_input = self.number_of_iterations-1
                new_user_input = input('Next iteration?y/n/b: ')
                if new_user_input == 'y' or new_user_input == 'yes' or new_user_input == '1':
                    if (self.number_of_iterations-1) != user_input and user_input >= 0:
                        Read.nexti(self, user_input)
                    else:
                        print("Can't go any further")
                elif new_user_input == 'b' or new_user_input == 'back' or new_user_input == '3':
                    if user_input > 0:
                        Read.backi(self, user_input)
                    else:
                        print("Can't go any further")
                else:
                    return
            else:
                user_input = int(user_input)-1
                with open(self.start_of_textfile_code + 'lockedbook.txt', 'r') as tfile:
                    for x in range(self.number_of_iterations):
                        readlist.append((tfile.readline())[:-9])
                dates = self.finddate
                if readlist[user_input] == '[Deleted]\n' and self.delreadfunc == False:
                    print('The iteration you have chosen has been deleted\n')
                else:
                    print(dates[user_input] + '\n' + readlist[user_input])
                new_user_input = input('Next iteration?y/n/b: ')
                if new_user_input == 'y' or new_user_input == 'yes' or new_user_input == '1':
                    if (self.number_of_iterations-1) != user_input and user_input >= 0:
                        Read.nexti(self, user_input)
                    else:
                        print("Can't go any further")
                elif new_user_input == 'b' or new_user_input == 'back' or new_user_input == '3':
                    if user_input > 0:
                        Read.backi(self, user_input)
                    else:
                        print("Can't go any further")
                else:
                    return
        elif user_input == 'all' or user_input == 'a' or user_input == 'ALL':
            codescheck = []
            with open("filecode.txt", 'r') as codefile:     #Gets iteration amount to prevent resettext() in book_with_class.py making a mistake
                for lines in range(self.num_of_lines_in_filecode):
                    codescheck.append(codefile.readline())
            iteration_amount = int((codescheck[1])[:-1])
            if self.delreadfunc:
                Read.readback(self)
            else:  
                dates = self.finddate
                with open(self.start_of_textfile_code + 'lockedbook.txt', 'r') as tfile:
                    for x in range(self.number_of_iterations):
                        readlist.append('Iteration ' + str(x+1) + '\t' + dates[x])
                        readlist.append((tfile.readline())[:-9] + '\n')
                        if readlist[-1] == '[Deleted]\n' and self.delreadfunc == False:
                            readlist.pop()
                            readlist.pop()
                for x in readlist:
                    if x != '':
                        print(x)
                        iteration_amount += 1
            if iteration_amount == 0:
                print("There are currently no iterations that are able to be read\n")
            return
        else:
            print('Invalid input')
            return


class Delete():             #Allows the user to delete a specific iteration, 
    def __init__(self, number_of_iterations, start_of_textfile_code, user_input):
        with open(start_of_textfile_code + 'lockedbook.txt', 'r') as file:
            if file.read() != '':
                user_input = input('What iteration do you want to delete? Number: ')
                if user_input == 'all':
                    file.close()
                    os.remove("filecode.txt")
                    os.remove(start_of_textfile_code + "lockedbook.txt")
                    return
                if user_input == '' or not user_input.isdigit():
                    return
                elif int(user_input) > number_of_iterations:
                    user_input = number_of_iterations
                    second_user_input = input("Number too high, delete last iteration? y/n: ")
                    if second_user_input == '':
                        return
                    elif second_user_input == 'y' or second_user_input == 'yes' or second_user_input == '1' or second_user_input == 'YES':
                        pass
                    else:
                        Delete(number_of_iterations, start_of_textfile_code, user_input)
            else:
                print("No items to delete")
                return
        new_text_to_be_written = []
        with open(start_of_textfile_code + 'lockedbook.txt', 'r') as file:   
            for x in range(number_of_iterations+1):
                readline = file.readline()
                new_text_to_be_written.append(readline)
        time = datetime.now()
        date = str(time.month)+'/'+str(time.day)+'/'+str(time.year-2000)
        while len(date) < 8:
            date = ' ' + date
        new_text_to_be_written[int(user_input)-1] = (f'[Deleted]{date}\n')
        with open(start_of_textfile_code + 'lockedbook.txt', 'w') as file:
            for x in range(number_of_iterations):
                file.write((new_text_to_be_written[x]))
