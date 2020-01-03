import random
import pickle
import argparse

parser = argparse.ArgumentParser(description='Generate text using created model.', prog='python parser.py')
parser.add_argument('model', metavar='m', help='Path where to get your model.', required=True, type=str)
parser.add_argument('length', metavar='l', help='Length in words of your text.', required=True, type=int)
parser.add_argument('seed', metavar='s', help='Seed to generate your model', required=False, type=int)
args = parser.parse_args()


def generate(word_order, length=100):

	key = random.choice(list(word_order)) # seeding
	sequence = [key]

	# right now it works like this: raffle. more times you are beeing met after some word,
	# more chances for you to be after this word here.
	for i in range(length):
		summ = 0
		for keyy, val in word_order[key].items():
			summ += val
		item = random.randint(1, summ)
		for keyy, val in word_order[key].items():
			item -= val
			if item <= 0:
				word = keyy
				break

		sequence.append(word)
		key = word

	str = ''
	for i in sequence:
		str += i + ' '
	str = str[0].upper() + str[1:]
	str = str[:-1] + '.'
	return str


