def makeguess(wordlist, guesses=[], feedback=[]):
    """
    Inputs:
    wordlist - A list of the valid word choices. The output must come from this list.
    guesses - A list of the previously guessed words, in the order they were made, e.g. guesses[0] = first guess, guesses[1] = second 
                guess. The length of the list equals the number of guesses made so far. An empty list (default) implies no guesses have 
                been made.
    feedback - A list comprising one list per word guess and one integer per letter in that word, to indicate if the letter is correct 
                (2), almost correct (1), or incorrect (0). An empty list (default) implies no guesses have been made.

    Purpose:
    To make an optimal guess in a game of wordle based on the given information.

    Method:
    If it is the first guess, return a set first guess. Otherwise, search through the proper guess txt file to find matching outcomes 
    and return the predetermined and (hopefully) optimal guess. 
    """

    fin = open("aiInfo.txt", "r")

    #updates firstGuess and threshold values from file
    firstGuess = fin.readline().rstrip("\n")
    threshold = fin.readline().rstrip("\n")

    #creates file name
    file = firstGuess + threshold + "thresh"

    length = len(guesses)

    #makes first guess
    if not length:
        return firstGuess.upper()
    
    #uses proper guess file to search of the matching string of outcomes
    else:

        #makes the string of outcomes
        outcome = ""
        for i in feedback:
            outcome += str(i)

        #opens the correct guess file
        fin = open(file + str(length + 1) + ".txt", "r")
        count = 0

        #begins searching the file for the matching string of outcomes
        for line in fin:

            #incrementing the count while passing over the prior guess that lead to this point.
            if count:
                count += 1
            
            #once the count reaches the proper value the guesss is returned
            if count == length + 1:
                return line.rstrip("\n").upper()
            
            #once the string is found, the count to get the next guess and not the previous guesses begins
            elif line.rstrip("\n") == outcome:
                count += 1
        
#The count system is only in place because it was way easier to make the (n + 1)th file if the nth file had all the previous guesses. 

if __name__ == "__main__":
    print(makeguess([],['lares'],[[0,0,0,0,1]]))


