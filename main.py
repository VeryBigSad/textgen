from . import *
import argparse


class TextGenerator:
	def __init__():
		parser = argparse.ArgumentParser(description='Fit and generate some text.', prog='python main.py')
		parser.add_argument('length', metavar='L', type=int, required=True, help='Length of text you\'l make.')
		parser.add_argument

		parser.add_argument('path', metavar='p', type=str, required=False, help='Path to your model.')
		args = parser.parse_args()

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


