## CS 458/558
## Fall 2015
## hw0.R

# This is a warmup exercise that really has little to do with decision making.
# Rather, it is an opportunity to begin to learn R and Python.
# You will implement the same functions in both languages.

## Function 1: palindrom
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

## Use the following function signature. 
palindrome <- function(filename = "/usr/share/dict/words", letter = "all"){
    words <- read.table(filename, sep="\n",quote="",stringsAsFactors = FALSE)
    words <- words[1]
    if (letter != "all"){
        # Check uppercase and lowercase letters
        letters <- c(tolower(letter),toupper(letter))
        # Limit list to those starting with these letters (exclude alpha numeric)
        words <- subset(words,substring((gsub("[^[:alnum:]]", "", V1)),1,1) %in% letters)
        }
    checkPalindrome <- function(string){
        # Normalize string by setting it to lowercase
        string <- tolower(string)
        string <- gsub("[^[:alnum:]]", "", string)
        invertedString <- paste(rev(strsplit(string, NULL)[[1]]),collapse='')
        return(invertedString == string)
        }
    palindrome_list = c()
    for(i in 1:length(words$V1)){
        if (checkPalindrome(words$V1[i])) {
            palindrome_list <- c(palindrome_list, toString(words$V1[i]))
            print(toString(words$V1[i]),quote=FALSE)
            }
        }
    #return
    }

## Function 2: anagram
##
# write a function anagram which reads an ascii file comprising one word
# per line and returns all the largest set of words which are anagrams.  
# The default file is the standard UNIX online dictionary: /usr/share/dict/words
# (During development, you might want to use a smaller dictionary.)
# 
# There is another optional argument which is a single word.  
# In that case, the function returns all anagrams for that word 

# Example output
# > anagram()
# [1] "alerts" "alters" "artels" "estral" "laster" "lastre" "rastle" "ratels" "relast" "resalt"
# [11] "salter" "slater" "staler" "stelar" "talers"
# 
# > anagram(target = 'male')
# [1] "alem" "alme" "amel" "lame" "leam" "meal" "mela"

## Use the following function signature. 
anagram <- function(filename = "/usr/share/dict/words", target = "FALSE"){
  words <- read.table(filename, sep="\n",quote="",stringsAsFactors = FALSE)
  anagram_list <- list()
  # Provide some counter variables
  current_length <- 0
  check_length <- 0
  longest_anagram_list <- c()
  # Iterate over list 
  for(i in 1:length(words$V1)){
    # Create string with sorted word
    word <- toString(words[i,1])
    word_sorted <- paste(sort(unlist(strsplit(gsub("[^[:alnum:]]", "", tolower(word)),""))), collapse = "") 
    # Use sorted word as key in hash table
    if (word_sorted %in% names(anagram_list)){
      anagram_list[[word_sorted]] <- c(anagram_list[[word_sorted]],word)
      check_length <- length(anagram_list[[word_sorted]])
      if (check_length > current_length) {
        current_length <- check_length
        longest_anagram_list <- anagram_list[[word_sorted]]
        }
    } else {
      anagram_list[[word_sorted]] <- c(word)
    }
  }
  if(target != FALSE){
    targetKey <- paste(sort(unlist(strsplit(tolower(target),""))), collapse = "") 
    longest_anagram_list <- anagram_list[[targetKey]]
  }
  for(i in 1:length(longest_anagram_list)){
    print(longest_anagram_list[i],quote=FALSE)
  }
  #return
}

## Bonus question (no credit)
## An auto-antonym is a word that has two meanings that are opposites.
## For example, "dust" can mean to remove dust (I am dusting under the bed)
## and also "dust" can mean to add dust (I am dusting the cake with powdered sugar)
##
## How would you use a computer to come up with a list of auto-antonyms?
## Hint: there is more than one answer.
