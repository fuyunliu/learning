# -*- coding: utf-8 -*-
"""understanding python decorator"""


# example 1
def makebold(f):
    def wrapped():
        return '<b>' + f() + '</b>'
    return wrapped


def makeitalic(f):
    def wrapped():
        return '<i>' + f() + '</i>'
    return wrapped


@makebold
@makeitalic
def hello():
    return 'hello, world!'

print(hello())


# now, let's see a long explanations
# Python’s functions are objects
def shout(word="yes"):
    return word.capitalize() + "!"

print(shout())
# outputs : 'Yes!'

# As an object, you can assign the function to a variable like any other object
scream = shout

# Notice we don't use parentheses: we are not calling the function,
# we are putting the function "shout" into the variable "scream".
# It means you can then call "shout" from "scream":

print(scream())
# outputs : 'Yes!'

# More than that, it means you can remove the old name 'shout',
# and the function will still be accessible from 'scream'

del shout
try:
    print(shout())
except NameError as e:
    print(e)
    # outputs: "name 'shout' is not defined"

print(scream())
# outputs: 'Yes!'


# Another interesting property of Python functions is they can be defined
# inside another function!
def talk():

    # You can define a function on the fly in "talk" ...
    def whisper(word="yes"):
        return word.lower() + "..."

    # ... and use it right away!
    print(whisper())

# You call "talk", that defines "whisper" EVERY TIME you call it, then
# "whisper" is called in "talk".
talk()
# outputs:
# "yes..."

# But "whisper" DOES NOT EXIST outside "talk":

try:
    print(whisper())
except NameError as e:
    print(e)
    # outputs : "name 'whisper' is not defined"
    # Python's functions are objects


# You’ve seen that functions are objects. Therefore, functions:
# can be assigned to a variable
# can be defined in another function
# That means that a function can return another function.
def getTalk(kind="shout"):

    # We define functions on the fly
    def shout(word="yes"):
        return word.capitalize() + "!"

    def whisper(word="yes"):
        return word.lower() + "..."

    # Then we return one of them
    if kind == "shout":
        # We don't use "()", we are not calling the function,
        # we are returning the function object
        return shout
    else:
        return whisper

# Get the function and assign it to a variable
talk = getTalk()

# You can see that "talk" is here a function object:
print(talk)
# outputs : <function shout at 0xb7ea817c>

# The object is the one returned by the function:
print(talk())
# outputs : Yes!

# And you can even use it directly if you feel wild:
print(getTalk("whisper")())
# outputs : yes...
