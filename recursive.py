import unidecode

def factorial(x):
  """recursive function to find the factorial of an integer"""

  if x == 1:
    return 1
  else:
    return (x * factorial(x-1))

num = 3
text = "flávio"
print(text)
print(unidecode.unidecode(text))
#print(f"Factorial of {num}, is {factorial(num)}")
