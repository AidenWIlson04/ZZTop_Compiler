#import necessary librarys
import spacy

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
            self.source = open(self.fileName, 'r')
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
        print(f"\nCompiling: {self.fileName}\n")
        #iterate through each line of the source code
        for line in self.sourceLines:
            #Counter for the amount of errors on the current line
            self.amountOfLineErrors = 0
            #essentially splits the line into individual tokens
            doc = nlp(line.strip()) 
            #seperates the lines
            print("***********")
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
                    #print total amount of errors on current line
                    print(f"    >Total errors on line: {self.amountOfLineErrors}")
                if token.text == "Output":
                    #call checkOutput function
                    self.checkOutput(doc, line)
                    #print total amount of errors on current line
                    print(f"    >Total errors on line: {self.amountOfLineErrors}")
                if token.text == "Set":
                    self.checkAssignment(doc, line)
                     #print total amount of errors on current line
                    print(f"    >Total errors on line: {self.amountOfLineErrors}")
            #increment line number
            self.lineNumber += 1
                
    def checkInput(self, doc, line):
        #call the check identifier function to see if its a valid identifier
        if str(doc[-1]) == "!" and str(doc[0]) == "Input":
            self.checkIdentifier(str(doc[1]), returnBool=False)

        #if the line being processed is not the second last line 
        #(which ! doesnt need to be on) and the last character
        #is not an ! print error stating there is a missing !
        
        if line != self.sourceLines[-2] and str(doc[-1]) != "!":
            print("    >Missing '!' at end of line")
            #increment total amount of errors on current line
            self.amountOfLineErrors += 1
    
    def checkOutput(self, doc, line):
        print(self.currentVariables)
        if not (str(doc[1]) in self.currentVariables):
            print(f"    >{str(doc[1])} has not been declared")
            self.amountOfLineErrors += 1    

        if line != self.sourceLines[-2] and str(doc[-1]) != "!":
            print("    >Missing '!' at end of line")
            #increment total amount of errors on current line
            self.amountOfLineErrors += 1



    def checkAssignment(self, doc, line):
        #Check to see if the variable has already been declared
        #If it hasnt check if its a valid identifier
        #do split() on the value and iterate over it. While iterating check in this order 
        #If the variable is in self.currentVaribles, then try to make it an integer
        self.unwantedOperators = ["+", "-", "/", "*"]
        self.correctSyntax = True
        if len(doc) > 2:
            if str(doc[2]) != "to":
                print(f"    >Missing 'to' after variable value being set ")
                self.amountOfLineErrors += 1
                self.correctSyntax = False
                ''' ^^^ Isnt setting to false?'''
        if len(doc) < 5:
            print(f"    >Malformed Assignment <{str(doc)}>")
            self.checkIdentifier(str(doc[1]), returnBool=False)
            self.amountOfLineErrors += 1
            self.correctSyntax = False
        if self.correctSyntax == True:
            if str(doc[1]) in self.currentVariables:
                self.setValue = str(doc[4:]).split()
                #["J3", "-", "1", "+", "xA1"]
                for item in self.setValue:
                    if item in self.unwantedOperators:
                        self.setValue.remove(item)
                #["J3", "1", "xA1"]
                for item in self.setValue:
                    try:
                        item = int(item)
                    except ValueError:
                        if item not in self.currentVariables:
                            print(f"    >The value <{item}> does not exist.")
                            self.correctSyntax = False
                            #increment total amount of errors on current line
                            self.amountOfLineErrors += 1   
            else:               
                self.setValue = str(doc[3:]).split()
                #["J3", "-", "1", "+", "xA1"]
                for item in self.setValue:
                    if item in self.unwantedOperators:
                        self.setValue.remove(item)
                #["J3", "1", "xA1"]
                for item in self.setValue:
                    try:
                        item = int(item)
                    except ValueError:
                        if item not in self.currentVariables:
                            print(f"    >The value {item} does not exist.")
                            self.correctSyntax = False
                            #increment total amount of errors on current line
                            self.amountOfLineErrors += 1 
                if self.correctSyntax == True:
                    self.checkIdentifier(str(doc[1]), returnBool=False) 

        if line != self.sourceLines[-2] and str(doc[-1]) != "!":
            print("    >Missing '!' at end of line")
            self.amountOfLineErrors += 1
            self.correctSyntax = False
        if self.correctSyntax == True:
            self.checkIdentifier(str(doc[1])) 
        
    
    def checkIdentifier(self, identifier, returnBool):
        #lists of valid characters and digits that can be used in an identifier
        self.validCharUpper = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"] 
        self.validIdentifierPadder = ["a", "b", "c", "d", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        #self.validDigit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        #If the identifier passed in is allowed, default is True
        self.allowedIdentifier = True
        #make a varaible with a list containing every element of the passed in identifier
        self.identifierList = list(identifier)
        #if the first character is not a capital letter error saying its not apart of the valid character list
        if self.identifierList[0] not in self.validCharUpper:
            #incrememnt line errors
            self.amountOfLineErrors += 1
            print(f"    >First letter of {identifier} must be in <ABCDEFGHIJ>")
            #set the allowedIdentifier bool to false
            self.allowedIdentifier = False
        #if the element is not an allowed digit or lower char error sayig it is not a valid identifier
        for element in self.identifierList[1:]:
            if (element not in self.validIdentifierPadder):
                self.amountOfLineErrors += 1
                print(f"    >{identifier} invalid from second character onwards, must be in <abcd> or <0123456789>")
                self.allowedIdentifier = False
                break
        #if the identifier is allowed, append it to a list of allowed identifiers
        if returnBool == False:
            if self.allowedIdentifier == True:
                self.currentVariables.append(identifier) 
        else:
            return self.allowedIdentifier   
                          
if __name__ == "__main__":
    compiler()
    

