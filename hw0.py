## CS 458/558
## Fall 2015
## hw0.py

# This is a warmup exercise that really has little to do with decision making.
# Rather, it is an opportunity to begin to learn R and Python.
# You will implement the same functions in both languages.

## Function 1: palindrome
# a palindrome is a string or word or number or phrase that is the same backward
# as forward.  Examples:

# radar
# Bob
# 10101
# A man, a plan, a canal: Panama!
# Madam, I'm Adam

# write a function palindrome which reads an ascii file comprising one word
# per line and returns all the palindromes.  
# The default file is the standard UNIX online dictionary: /usr/share/dict/words
# There is another optional argument of a single letter, in which case the
# program returns only palindromes which start with that letter.

## Use the following function signature.  Replace "pass" with your code.
def palindrome(filename = "/usr/share/dict/words", letter = "all"):
    # Read in dictionary list delimited by newlines
    words = open(filename,'r').readlines()
    # Strip \n from strings
    words = [words[i].rstrip() for i in range(len(words))]
    # Limit dictionary if specified letter is given
    if letter != "all":
        # Check uppercase and lowercase letters
        letters = (letter.lower(),letter.upper())
        # Limit list to those starting with these letters
        words = [words[i] for i in range(len(words)) if (''.join(ch for ch in words[i] if ch.isalnum())).startswith(letters)]
    def checkPalindrome(string):
        # Compares string to inverted string
        string = string.lower()
        # Strip non alphanumeric 
        string = ''.join(ch for ch in string if ch.isalnum())
        return string == string[::-1]
    # Create list of palindromes considering specified letter
    palindromes = [words[i] for i in range(len(words)) if checkPalindrome(words[i])]
    # Print the list in the specified format
    for i in range(len(palindromes)):
        print(palindromes[i])
    return 

    
# >>> palindrome(letter = "b")
# B
# b
# Bab
# bab
# B/B
# BB
# bb
# BBB
# Beeb
# Bib
# bib
# Bob
# bob
# boob
# Bub
# bub



## Function 2: anagram
#
# write a function anagram which reads an ascii file comprising one word
# per line and returns all the largest set of words which are anagrams.  
# The default file is the standard UNIX online dictionary: /usr/share/dict/words
# 
# There is another optional argument which is a single word.  
# In that case, the function returns all anagrams for that word 

# Example output
# >>> anagram()
# ['alerts', 'alters', 'artels', 'estral', 'laster', 'lastre', 'rastle', 'ratels', 'relast', 'resalt', 'salter', 'slater', 'staler', 'stelar', 'talers']
# 
# >>> anagram(target = 'male')
# ['alem', 'alme', 'amel', 'lame', 'leam', 'male', 'meal', 'mela']

## Use the following function signature.  Replace "pass" with your code.

def anagram(filename = "/usr/share/dict/words", target = False):
    # Read in dictionary list delimited by newlines
    words = open(filename,'r').readlines()
    # Initialize dictionary and check length counter
    anagrams = dict()
    check_length = 0
    # Iterate through list once
    for i in range(len(words)):
        # Created the sorted string stripped of \n and sent to 
        # lower case.
        words[i] = words[i].rstrip()
        words[i] = ''.join(ch for ch in words[i] if ch.isalnum())
        wordSorted = ''.join(sorted(words[i].lower()))
        # Logic below adds entries to dictionary if their hash
        # already exists, otherwise creates new entries.
        if wordSorted in anagrams:
            anagrams[wordSorted].append(words[i])
        else:
            anagrams[wordSorted] = [words[i]]
        # This logic updates the hash with the greatest number
        # of entries.
        if len(anagrams[wordSorted]) > check_length:
            check_length = len(anagrams[wordSorted])
            longest_hash = wordSorted    
    # If a target is specified print that target's entry,
    # otherwise print the longest
    if target:  
        final_list = anagrams[''.join(sorted(target.lower()))]
    else:
        final_list = anagrams[longest_hash] 
    for i in range(len(final_list)):
        print final_list[i]
    return               

    
## Bonus question (no credit)
## An auto-antonym is a word that has two meanings that are opposites.
## For example, "dust" can mean to remove dust (I am dusting under the bed)
## and also "dust" can mean to add dust (I am dusting the cake with powdered sugar)
##
## How would you use a computer to come up with a list of auto-antonyms?
## Hint: there is more than one answer.
