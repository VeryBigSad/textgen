import random
import pickle
import argparse
import logging
import sys

l = logging.getLogger('Generating')
formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)

l.addHandler(handler)
l.setLevel(logging.DEBUG)

def unpack(path):
	try:
		with open(path, 'rb') as f:
			data = pickle.loads(f.read())
	except FileNotFoundError:
		exit('Error: Wrong path to model.')

	return data


def generate(order, length, seed):
	# order
	#
	# {'word': {'second_word1': {'times_repeated': 100, 'next_words': {'third_word': 2, 'third_word2': 1}},
	# 'second_word2': {'times_repeated': 99, 'next_words': {'third_word': 12, 'third_word2': 11}}, ...}

	if length == None:
		length = 10
	if seed == None:
		random.seed()
		l.info('Generating with random seed.')
	else:
		random.seed(seed)
		l.info('Generating with seed ' + str(seed))
	sequence = [random.choice(list(order))]

	for counter in range(length):
		last_used = sequence[-1:][0]
		# l.debug(order[last_used])
		# l.debug('possible next words: ' + str([order[last_used][next_word]['next_words'] for next_word in order[last_used]]))

		tmp_sum = [order[last_used][next_word]['times_repeated'] for next_word in list(order[last_used])]
		tmp_sum = sum(tmp_sum)
		# tmp_sum - how many times word had been used.

		item = random.randint(0, tmp_sum)
		item_copy = int(item)
		for next_word in [random.choice(list(order[last_used])) for i in range(len(list(order[last_used])))]:
			item -= order[last_used][next_word]['times_repeated']
			if item <= 0:
				key = next_word
				sequence.append(next_word)
				l.debug('We added a word ' + next_word + ', because it had chance ' + 
					str(order[last_used][next_word]['times_repeated'] / tmp_sum))
				if True:
					# TODO: add if; if we need to use next_word2, use it,
					# otherwise - just pick another rando word.
					break
					# for next_word2 in order[last_used][next_word]['next_words']:
					# 	pass

				else:
					break



	# adding big-letter to first word and "." to end.
	string = ''
	for i in sequence:
		string += i + ' '
	string = string[0].upper() + string[1:]
	string = string[:-1] + '.'
	return string


def main():
	# parsing arguments from console
	parser = argparse.ArgumentParser(description='Generate text using created model.')
	parser.add_argument('model', help='Path where to get your model.', type=str)
	parser.add_argument('--length', help='Length of your text in words.', required=False, type=int)
	parser.add_argument('--seed', help='Seed to generate your model.', required=False, type=int)
	args = parser.parse_args()

	order = unpack(args.model)
	result = generate(order, length=args.length, seed=args.seed)

	print('\n\n\n\n\n\n', result)
if sys.argv[0] == 'generate.py':
	try:
		main()
	except KeyboardInterrupt:
		exit('\n\nKeyboard Interrupt')

