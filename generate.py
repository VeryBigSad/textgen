import random
import pickle
import argparse

def unpack(path):
	try:
		with open(path, 'rb') as f:
			data = pickle.loads(f.read())
	except FileNotFoundError:
		exit('Error: Wrong path to model.')

	return data


def generate(word_order, length, seed):
	# word_order
	#
	# {'word': {'second_word1': {'times_repeated': 100, 'next_words': {'third_word': 2, 'third_word2': 1}},
	# 'second_word2': {'times_repeated': 99, 'next_words': {'third_word': 12, 'third_word2': 11}}, ...}

	if length == None:
		length = 50
	if seed == None:
		seed = random.randint(0, len(list(word_order))-1)
	seed = seed % (len(list(word_order)) - 1)

	word = list(word_order)[seed]
	sequence = [word]

	# right now it works like this: raffle. more times you are beeing met after some word,
	# more chances for you to be after this word here.
	for i in range(length):
		word = word.lower()
		summ = 0

		# all uses of words summary
		for tmp, val in word_order[word].items():
			summ += val['times_repeated']

		# picking random item and choosing the winner

		# TODO: maybe replace this inefficient for() with
		# something in 1st cycle. like, list of flags? idk, think about it
		item = random.randint(0, summ)
		for key in list(word_order[word]):

			val = word_order[word][key]
			item -= val['times_repeated']

			if item <= 0 and key != ',':
				word = key
				sequence.append(key)
				summ2 = 0

				for key2 in list(word_order[word][key]):
					for tmp, val in word_order[word].items():
						summ += val['times_repeated']					


		word = word

	# adding big-letter to first word and "." to end.
	str = ''
	for i in sequence:
		str += i + ' '
	str = str[0].upper() + str[1:]
	str = str[:-1] + '.'
	return str


def main():
	# parsing arguments form console
	parser = argparse.ArgumentParser(description='Generate text using created model.')
	parser.add_argument('model', help='Path where to get your model.', type=str)
	parser.add_argument('--length', help='Length of your text in words.', required=False, type=int)
	parser.add_argument('--seed', help='Seed to generate your model.', required=False, type=int)
	args = parser.parse_args()

	order = unpack(args.model)
	result = generate(order, length=args.length, seed=args.seed)

	print(result)

main()

