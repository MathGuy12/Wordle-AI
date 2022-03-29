from itertools import product
from wordfreq import zipf_frequency

def main():
    """
    Purpose:
    To get user inputs for the createguessfiles function and write the values in a file accessible by the AI.

    Method:
    Uses input and the createguessfiles to create all the guess for a starter word and a threshold.
    """
    firstGuess = input("Enter First Guess: ")
    threshold = input("Enter the threshold value: ")

    #Creates unique file identifier
    file = firstGuess + threshold + "thresh"

    #updates files used by AI
    fout = open("aiInfo.txt", "w")
    fout.write(firstGuess + "\n" + threshold + "\n")
    fout.close()

    #creates file
    createguessfiles(file, firstGuess, float(threshold))

def createguessfiles(file, firstGuess, threshold):
    """
    Inputs:
    file - the name of the file to for data to be stored in
    firstGuess - the very first word guessed
    threshold - the word frequency threshold for the the weight to initiate

    Purpose:
    To create the allWords, allFreq, and allOutcomes dictionaries/list required and then to run the make nthguess function for every 
    guess. This will make all 5 files the AI will use to play wordle along with having a user selected first word. 

    Method:
    Creates allOutcomes using itertools, allWords from the allwords5.txt file, and the allFreq by combining the allWords with the zipf_frequency function. The function
    then loops over the guessNumbers and creates the guess data files using the nthguessdata function. 
    """

    fin = open("allwords5.txt", "r")
    n = int(fin.readline())

    #uses the product function to create the allOutcomes list
    a = [0,1,2]
    allOutcomes = list(list(i) for i in product(a, repeat=5))

    #uses the allwords5 file and the zipf_frequency function to make the allWords and allFreq dictionaries
    allWords = {}
    allFreq = {}
    for i in range(n):
        x = fin.readline().rstrip("\n")
        allFreq[x] = zipf_frequency(x, "en")
        allWords[x] = 0
    
    #uses the nthguessdata to create the files for the 2nd through the 6th guesses. 
    print("working on", firstGuess)
    for i in range(2,7):
        print("working on guess", i, "for", firstGuess, "at", threshold)
        nthguessdata(allWords, allOutcomes, i, file, firstGuess, threshold, allFreq)
        print("finished guess", i, "for", firstGuess)
    print("finished", firstGuess, "at", threshold)
    

def firstguessdata(allWords, threshold, allFreq, file):
    """
    Inputs: 
    allWords - a dictionary of all possible guesses
    threshold - the word frequency threshold for the the weight to initiate
    allFreq - a dictionary of all the guesses with words as keys and frequency of the word as the value
    file - the name of the file to for data to be stored in

    Purpose:
    To create and display data for the first guess of the game

    Method:
    Because no data is given at the beginning of the game, the findbestguess function is run where the reduced word list actually the 
    entire word list. This is a slow function, running through around 1.6e8 iterations. 
    """
    fout = open(file + ".txt", "w")

    #here the wordList parameter in findbestguess is filled with the allWords list
    allWords = findbestguess(allWords, allWords, threshold, allFreq)
    for i in allWords:
        fout.write(i + '\t' + str(allWords[i]) + "\n")
    fout.close()


def nthguessdata(allWords, allOutcomes, guessNumber, file, firstGuess, threshold, allFreq):
    """
    Inputs: 
    allWords - a dictionary of all possible guesses
    allOutcomes - a list of all possible outcomes
    guessNumber - the number of the guess to be made (the third guess is has a guessNumber = 3). guessNumber can be in the range [2,6]
    file - the name of the file to for data to be stored in
    firstGuess - the very first word guessed
    threshold - the word frequency threshold for the the weight to initiate
    allFreq - a dictionary of all the guesses with words as keys and frequency of the word as the value

    Purpose:
    To create a file of data that will be used both for the creation of the file for the next guess and for the AI to sort through and 
    determine the best next guess.

    Method:
    The function begins by opening the proper in and out files and reading the first line to get an initial value for the while loop
    (guessNumbers 2 and 6 have midly different approaches due to slightly different circumstances). The function then begins the while
    loop which will cover every previous outcome and covered guess. guessNumber 2 will only use the while loop once since there is only
    one previous guess and no previous outcomes (note that the outcome for the first guess is considered the current outcome for
    guessNumber 2). Inside the while loop, the function creates a string version of the previous outcomes, an integer list of the
    previous outcomes, a list of the previously guessed words (starting with the first guess), a string for the guessed words (starting
    with the second guess), and sets the initial wordList to be the allWords list. The list of words guessed, string of guessed words, 
    and wordList are then updated based on the guessNumber (no updates for guessNumber 2) and the prior outcomes. Then, the function
    loops over all possible outcomes (skipping the 5 impossible outcomes and the all 2s outcome) and creates a final wordList for 
    every possible current outcome, skipping the outcome if the final wordList is empty. If the guessNumber is 6, the final guess, then
    then function will simply find the word frequency of all the words in the final wordList and writes the most common word for that
    situation. If the guessNumber is not 6 but there are only two options available in the final wordList, the function still writes the
    most common word based on word frequency. And of course if there is only one option then that option is written. If, however, none
    of those criteria are met, the function then uses the findbestguess function to find the best guess (shocking!) and writes that. If
    the guessNumber is not 2, the next outcome in the previous guess file is obtained and the while loop runs again, provided the end of
    the file is not reached. 
    """
    #inital file opening and guessNumber 2 exceptions
    fout = open(file + str(guessNumber) + ".txt", "w")
    if guessNumber == 2:
        outcome = ""
    else:
        fin = open(file + str(guessNumber - 1) + ".txt", "r")
        outcome = fin.readline().rstrip("\n")

    #begin while loop
    while outcome or guessNumber == 2:

        #string version of the outcomes for writing
        strOutcome = outcome

        #integer list outcomes for creating wordLists
        outcome = [int(i) for i in outcome if i in "012"]

        #list of prior guesses
        words = [firstGuess]

        #string of prior guesses for writing
        wordsStr = ""

        #initial wordList
        wordList = allWords

        #updating the 3 previous variables, excludes updates for guessNumber 2
        for i in range(guessNumber - 2):

            #updates list of words guessed
            words.append(fin.readline().rstrip("\n"))

            #creates new wordList using previous wordList and parsed outcome
            wordList = possiblewordlist(wordList, words[i], outcome[5 * i:5 * (i + 1)])

            #updates string of words guessed
            wordsStr += words[-1] + "\n"

        #loops through every possible outcome (all 243)
        for i in allOutcomes:

            #skips the correct answer outcome (all 2s) and the 5 impossible outcomes (4 2s and a 1)
            if i in [[1, 2, 2, 2, 2],[2, 1, 2, 2, 2],[2, 2, 1, 2, 2],[2, 2, 2, 1, 2],[2, 2, 2, 2, 1],[2, 2, 2, 2, 2]]:
                continue

            #creates the final wordList using the current supposed projected outcome and gets length
            wordListLast = possiblewordlist(wordList, words[-1], i)
            length = len (wordListLast)

            #skips if the final wordList is empty
            if length == 0:
                continue

            #performs different chosing method for final guesss
            elif guessNumber == 6:

                #creates list of words in the final wordList coupled with their frequencies
                freq = []
                for j in wordListLast:
                    freq.append([j, zipf_frequency(j, "en")])

                #sorts word list to have most frequent word first
                freq.sort(key=myFunc, reverse=True)

                #writes most frequent word in proper format
                fout.write(strOutcome + str(i) + "\n" + wordsStr + freq[0][0] + "\n")
            
            #performs selection between final two options based on word frequency
            elif length == 2:
                
                #gets word frequency of last two options
                freq = []
                for j in wordListLast:
                    freq.append(zipf_frequency(j, "en"))

                #ensures the first word in the final wordList has the highest frequency
                if freq[1] > freq[0]:
                    ind = 1
                else:
                    ind = 0
                
                #writes most frequent word in proper format
                fout.write(strOutcome + str(i) + "\n" + wordsStr + wordListLast[ind] + "\n")
            
            #writes out only option if there is only one word in the final wordList
            elif length == 1:
                fout.write(strOutcome + str(i) + "\n" + wordsStr + wordListLast[0] + "\n")
            
            #if none of the previous criteria apply, the best word is calculated using the findbestguess function
            else:
                allWords = findbestguess(allWords, wordListLast, threshold, allFreq)

                #allowing the first word in the dictionary to be accesssed
                keyList = list(allWords.keys())

                #writes most optimal word choice in proper format
                fout.write(strOutcome + str(i) + "\n" + wordsStr + keyList[0] + "\n")
        
        #ending the while loop if guessNumber is 2
        if guessNumber == 2:
            break
        
        #obtaining the string of outcomes used for the next iteration in the while loop
        outcome = fin.readline().rstrip("\n")

    fout.close()


def myFunc(e):
    """
    Sorting function
    """
    return e[1]


def findbestguess(allWords, wordList, threshold, allFreq):
    """
    Inputs: 
    allWords - a dictionary of all possible guesses
    wordList - a list/dictionary of the current possible correct words
    threshold - the word frequency threshold for the the weight to initiate
    allFreq - a dictionary of all the guesses with words as keys and frequency of the word as the value

    Purpose:
    To find the word in allWords that will, on average, minimize the number of words left after weighting based on word frequency.

    Method:
    For every word in allWords, the function will create a dictionary of possible outcomes (outcomeDict) and a total outcome counter
    (maxi) then the function loops over every word in the word list and records the outcome (e.i if I guessed word a and the correct 
    word was b, what outcome would the game show). Here the function weights based on frequency, giving infrequent words a poor wieght.
    After total all of the outcomes, the function then computes an expected value by summing the probability an outcome will occur
    (number of occurances/maxi) times the number of times an outcome occured. The function then sorts the expected value of all of the
    guess and returns the sorted dictionary.
    """

    #i is the potential guess
    for i in allWords:
        outcomeDict = {}
        maxi = 0

        #j is the potential correct answer
        for j in wordList:
            outcome = str(determineoutcome(i,j))

            #frequency weighting
            if allFreq[j] < threshold:
                add = .0001
            else:
                add = 1

            #adding outcome to dictionary and maxi    
            if outcome in outcomeDict:
                outcomeDict[outcome] += add
            else:
                outcomeDict[outcome] = add
            maxi += add

        #computing expected value    
        total = 0
        for k in outcomeDict:

            #probability calculation
            p = outcomeDict[k]/maxi
            total += p * outcomeDict[k]

        allWords[i] = total
    
    #returning dictionary sorted based on value
    return {k: v for k, v in sorted(allWords.items(), key = lambda item: item[1])}

def possiblewordlist(wordList, wordGuessed, outcome):
    """
    Inputs:
    wordList - a list/dictionary of the current possible correct words
    wordGuessed - the word that was guessed
    outcome - the outcome given for the word guessed

    Purpose:
    To create an updated list of possible correct words based on the outcome of a guess

    Method:
    The function loops over the current possible correct words and checks the outcomes that would occur if the word being checked was
    the correct word. If the outcome found matches the outcome provided, then the word is added to a new list of possible correct words.
    """
    possibles = []

    #i is the potential correct answer
    for i in wordList:
        if determineoutcome(wordGuessed, i) == outcome:
            possibles.append(i)
    return possibles

def determineoutcome(wordGuessed, possibleCorrect):
    """
    Inputs:
    wordGuessed - the word that was guessed
    possibleCorrect - the proposed correct word

    Purpose:
    To determine the outcome that would be displayed if the wordGuessed was guessed and the possibleCorrect was the correct answer.

    Method:
    Using a series of ifs, elifs, elses, and indexing logic, the function accounts for every POSSIBlE scenario (note, a word containing
    4 of the same letter is not possible with the given all words list). A large portion of the function is dedicated to handling when
    the guessed word has 3 of the same letter while the correct word has 2 of the that letter. 
    """
    outcome = []
    for i in range(5):
        l1 = wordGuessed[i]
        l2 = possibleCorrect[i]

        #handling obvious 0s
        if l1 not in possibleCorrect:
            outcome.append(0)

        #handling all 2s
        elif l1 == l2:
            outcome.append(2)
        
        #handling most 1s
        elif wordGuessed.count(l1) <= possibleCorrect.count(l1):
            outcome.append(1)
        
        #handles all guesses which have a reocurring letter (2 or 3 times) and the correct only contains one of such letter 
        elif possibleCorrect.count(l1) == 1:
            if wordGuessed[possibleCorrect.index(l1)] == l1:
                outcome.append(0)
            elif wordGuessed.index(l1) == i:
                outcome.append(1)
            else:
                outcome.append(0)
        
        #handles the nightmare that is 3 of the same letter in the guessed and 2 of that letter in the correct
        else:
            ind1 = possibleCorrect.index(l1)
            ind2 = possibleCorrect.index(l1,ind1+1)

            #handles the 0 in the 022 scenario
            if wordGuessed[ind1] == l1 and wordGuessed[ind2] == l1:
                outcome.append(0)
            
            #handles the first way 012 can appear (based on ind1 being the 2)
            elif wordGuessed[ind1] == l1:
                if i < ind1 and wordGuessed.index(l1) == i:
                    outcome.append(1)
                elif wordGuessed.index(l1) == ind1 and wordGuessed.index(l1, ind1 + 1) == i:
                    outcome.append(1)
                else:
                    outcome.append(0)

            #handles the second way 012 can appear (based on ind2 being the 2)
            elif wordGuessed[ind2] == l1:
                if i < ind2 and wordGuessed.index(l1) == i:
                    outcome.append(1)
                elif wordGuessed.index(l1) == ind2 and wordGuessed.index(l1, ind2 + 1) == i:
                    outcome.append(1)
                else:
                    outcome.append(0)
            
            #handles the 1s in 011
            elif wordGuessed.index(l1) == i or wordGuessed.index(l1, wordGuessed.index(l1)  + 1) == i:
                outcome.append(1)
            
            #handles the 0 in 011
            else:
                outcome.append(0)
    return outcome

if __name__ == "__main__":
    main()
