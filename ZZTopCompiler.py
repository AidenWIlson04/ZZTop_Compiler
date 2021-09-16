#import necessary librarys
import spacy
import os

#load the spacy dictionary
nlp = spacy.load("en_core_web_sm")

class compiler:
    def __init__(self):
        #call openFile function
        self.openFile()
        #compile the file that was named.
        self.compileFile()
       
    def openFile(self):
        #Trys to open a file by the name of inputed file name
        try:
            self.fileName = input("Name of File: ")
            self.source = open(os.path.join("sourceFiles", self.fileName), 'r')
        #If no file exists, asks again
        except:
            print("No file by that name")
            self.fileName = input("Name of File: ")
            self.source = open(self.fileName, 'r')
        #Reads each line of the file and appends it to an array
        self.sourceLines = self.source.readlines()
        #Close file
        self.source.close()
        
    def compileFile(self):
        #line number counter
        self.lineNumber = 1
        #list of all variables/identifiers that have been defined
        self.currentVariables = []
        #Print the name of the file being compiled
        print(f"\nCompiling: {self.fileName}\n")
        #Initialise error count variable 
        self.errorCount = 0
        #If the first line of the source code isnt start print error and add to error total 
        if (self.sourceLines[0]).strip() != "Start":
            print(f"> Missing 'Start' at beginning of program")
            self.errorCount += 1
        #If the last line of the source code isnt stop print error and add to error total 
        if (self.sourceLines[-1]).strip() != "Stop":
            print(f"> Missing 'Stop' at end of program") 
            self.errorCount += 1
        #iterate through each line of the source code
        for line in self.sourceLines:
            #If the word "When" or "Start" or "Stop" is in the line skip the iteration and move to the next line
            if "When" in line.split():
                print("---------------------")
                print(line.strip())
                continue   
            if "Start" in line.split():
                print("---------------------")
                print(line.strip())
                continue
            if "Stop" in line.split():
                print("---------------------")
                print(line.strip())
                print("---------------------")
                continue
            #essentially splits the line into individual tokens 
            doc = nlp(line.strip()) 
            #seperates the lines
            print("---------------------")
            #print the original line with leading, trailing and any \n commands
            print(f"{line.strip()}")
            #print amount of errors on current line
            print(f"> Errors on line {self.lineNumber}:")
            #iterate through each token on the currently being processed line
            for token in doc:
                #if the token is the Input command
                if token.text == "Input":
                    #call checkInput function
                    self.checkInput(doc, line)
                #if the token is the Output command
                if token.text == "Output":
                    #call checkOutput function
                    self.checkOutput(doc, line)
                #if the token is the Set command
                if token.text == "Set":
                    #call checkOutput function
                    self.checkAssignment(doc, line)
            #increment line number
            self.lineNumber += 1
        print(f"\nCompilation of file '{self.fileName}' finished with {self.errorCount} error(s)\n")
                
    def checkInput(self, doc, line):
        #call the check identifier function to see if its a valid identifier
        if str(doc[-1]) == "!" and str(doc[0]) == "Input":
            self.checkIdentifier(str(doc[1]), returnBool=False)
        '''if the line being processed is not the second last line 
        (which ! doesnt need to be on) and the last character
        is not an ! print error stating there is a missing !'''
        if line != self.sourceLines[-2] and str(doc[-1]) != "!":
            print("    >Missing '!' at end of line")
            #increment total amount of errors 
            self.errorCount += 1
            
    
    def checkOutput(self, doc, line):
        self.correctOutput = self.checkIdentifier(str(doc[1]), returnBool=True)
        self.outputErrorMessage = f"    >{str(doc[1])} has not been declared"
        #If the variable to output is not in current variables
        if not (str(doc[1]) in self.currentVariables):
            if self.correctOutput == True:
                self.outputErrorMessage += ", but is valid"
            print(self.outputErrorMessage)
            #increment total amount of errors
            self.errorCount += 1
        '''if the line being processed is not the second last line 
        (which ! doesnt need to be on) and the last character
        is not an ! print error stating there is a missing !'''
        if line != self.sourceLines[-2] and str(doc[-1]) != "!":
            print("    >Missing '!' at end of line")
            #increment total amount of errors
            self.errorCount += 1
            
    def checkAssignment(self, doc, line):
        #list of unwanted operators to remove
        self.unwantedOperators = ["+", "-", "/", "*", "!"]
        self.correctSyntax = True
        if len(doc) < 5:
            print(f"    >Malformed Assignment <{str(doc)}>")
            #increment total amount of errors
            self.errorCount += 1
        try:
            if str(doc[2]) != "to":
                print(f"    >Missing 'to' after variable value being set ")
                #increment total amount of errors
                self.errorCount += 1
                self.correctSyntax = False
        except:
            pass 
        #if the line is not the second last line of the code 
        if line != self.sourceLines[-2] and str(doc[-1]) != "!":
            print("    >Missing '!' at end of line")
            #increment total amount of errors
            self.errorCount += 1
            self.correctSyntax = False
        #split the line from the to statement onwards
        self.setValue = str(doc[3:]).split()
        #iterate through the list and if the item is one of the unwanted operator, remove it form the list
        for item in self.setValue:
            if item in self.unwantedOperators:
                self.setValue.remove(item)
        #iterate through the list of words in the line
        for item in self.setValue:
            #try to see if its an integer, if the try block works, code skips over the item
            try:
                item = int(item)
            #if a value error is raised, it is not an integer
            except ValueError:
                #check to see if the item being iterated through is a valid integer
                self.correctIdentifier = self.checkIdentifier(item, returnBool=True)
                #if the item was not a correct variable and isnt in the currentVariable list
                if item not in self.currentVariables:
                    #create variable to store the error message
                    self.setIdentErrorMessage = f"    >The value '{item}' does not exist"
                    #increment total amount of errors
                    self.errorCount += 1
                    #if the variable doesnt follow correct syntax, add it to the error message
                    if self.correctIdentifier == False:
                        self.setIdentErrorMessage += ", and does not follow correct identifier syntax"
                        self.correctSyntax = False
                    #print the error message
                    print(self.setIdentErrorMessage)
        if self.correctSyntax == True:
            #check if identifier being set is valid
            self.checkIdentifier(str(doc[1]), returnBool=False)
    
    
    def checkIdentifier(self, identifier, returnBool):
        #lists of valid characters and digits that can be used in an identifier
        self.validCharUpper = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"] 
        self.validIdentifierPadder = ["a", "b", "c", "d", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        #If the identifier passed in is allowed, default is True
        self.allowedIdentifier = True
        #make a varaible with a list containing every element of the passed in identifier
        self.identifierList = list(identifier)
        #if the first character is not a capital letter error saying its not apart of the valid character list
        if self.identifierList[0] not in self.validCharUpper:
            #incrememnt line errors
            self.errorCount += 1
            print(f"    >First letter of {identifier} must be in <ABCDEFGHIJ>")
            #set the allowedIdentifier bool to false
            self.allowedIdentifier = False
        #if the element is not an allowed digit or lower char, error saying it is not a valid identifier
        for element in self.identifierList[1:]:
            if (element not in self.validIdentifierPadder):
                #increment total amount of errors
                self.errorCount += 1
                print(f"    >{identifier} invalid from second character onwards, must be in <abcd> or <0123456789>")
                self.allowedIdentifier = False
        #if the return bool is false append the valid identifier to a list of current vars
        if returnBool == False:
            if self.allowedIdentifier == True:
                self.currentVariables.append(identifier) 
        #if return bool is true return the bool saying its an approved variable
        else:
            return self.allowedIdentifier   
                          
if __name__ == "__main__":
    compiler()
    
