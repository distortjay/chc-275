word = input("Enter a word: ")

i = 0
reverse = ""

for char in word:
    reverse = char + reverse 
if word == reverse:
    print("That is a palindrome!")
else:
    print("That is not a palindrome.")

