

# Factorial: n! = n*(n-1)!
def factorial(n):
    if n != 0:
        return n*factorial(n-1)
    else:
        return 1  # 0! = 1


print(factorial(4))  # 24


'''
Problem 1:
Write a recursive function which takes an integer and computes the cumulative sum of 0 to that integer.
For example, if n=4 , return 4+3+2+1+0, which is 10.
'''


def rec_sum(n):
    if n != 0:
        return n + rec_sum(n-1)
    else:
        return 0


print(rec_sum(4))  # 10


'''
Problem 2:
Given an integer, create a function which returns the sum of all the individual digits in that integer.
For example: if n = 4321, return 4+3+2+1
'''


def sum_func(n):
    if len(str(n)) == 1:
        return n
    else:
        return (n % 10) + sum_func(int(n/10))


print(sum_func(4321))  # 10

'''
Problem 3:
Create a function called word_split() which takes in a string phrase and a set list_of_words.
The function will then determine if it is possible to split the string in a way in which words can be made from the list of words.
The phrase will only contain words found in the dictionary list if it is completely splittable.
'''


def word_split(phrase, list_of_words, output=None):

    if output is None:
        output = []

    for word in list_of_words:

        # If the current phrase begins with the word, we have a split point
        if phrase.startswith(word):
            # Add the word to the output
            output.append(word)

            # Recursively call the split function on the remaining portion of the phrase--- phrase[len(word):]
            return word_split(phrase[len(word):], list_of_words, output)

    # Return output if no phrase.startswith(word) returns True
    return output


# Run Tests
print(word_split('themanran', ['the', 'ran', 'man']))  # ['the', 'man', 'ran']
print(word_split('ilovedogsJohn', ['i', 'am', 'a', 'dogs', 'lover', 'love', 'John']))  # ['i', 'love', 'dogs', 'John']
print(word_split('themanran', ['clown', 'ran', 'man']))  # []
