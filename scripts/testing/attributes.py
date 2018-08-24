
def log(text):
	"""Log the given text in a file."""
	print(text, file=open('test.log', 'w+'))

print(log.__doc__)