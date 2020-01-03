from . import *

class TextGenerator:
	def fit():
		# process text
		pass

	def generate():
		# generate text
		pass

	def store():
		# save model to file
		pass

word_list = get_word_list(text)
word_order = get_word_order(word_list)
# result = generate(word_order, length = 30)
sentense_list = get_sentense_list(text)
print (sentense_list[:10])
# print(result)


