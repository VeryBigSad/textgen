import random	
import argparse
import pickle


def get_text(path):
	text = open(path) # лев толстой, война и мир
	text = text.read()

	text = text[:9999] # i dont need long process time
	# TODO: if i finish pickle, remove this cuz it wont take
	# that much time anymore.

	return text


def get_sentense_list(text):
	# returns something like that: [['word1', 'in', 'sentence', 'one'], ['sentence', 'with', ',', '(comma)'],...] etc

	sentences = []
	tmp = ''

	for i in text:
		if i == '.' or i == '?' or i == '!':
			sentences.append(tmp)
			tmp = ''
		else:
			tmp += i

	for i in range(len(sentences)):
		sentences[i] = get_word_list(sentences[i])

	return sentences


def get_word_list(text):

	# TODO: (maybe not in this func) CHECK IF IT IS SOMEONE SPEAKING TO SOMEONE, NOT JUST TEXT. OR IT WILL BE BROKEN.

	alphabet = 'йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЧЯСМИТЬБЮЁ'
	word_list = [i for i in text.split(' ')]

	result = []

	index_counter = -1
	# so it will start from 0. it works, dont touch it.

	for word in word_list:
		index_counter += 1
		tmp = ''

		flag = False
		for letter in word:
			if letter in alphabet or letter == ',':
				tmp += letter
				if letter == ',':
					tmp = tmp[:-1]
					flag = True

		# counter variable is replacement for word_list.index(i)
		result.append(tmp)
		if flag:
			result.append(',')
		
		# now it adds not only words, but also commas as separate words.

	result = [i for i in result if i != '']
	return result


def get_word_order(sentence_list):
	# returns:
	#
	# {'word': {'second_word1': {'times_repeated': 100, 'next_words': {'third_word': 2, 'third_word2': 1}},
	# 'second_word2': {'times_repeated': 99, 'next_words': {'third_word': 12, 'third_word2': 11}}, ...}

	# TODO: make it use sentense_list, not word_list, so it
	# will be able to cut proper nouns. And use commas?

	order = {}
	counter = 0
	some_constant_which_we_need_to_have = 3
	# todo: add that constant

	for word_list in sentence_list:
		counter_for_capitalize = 0

		for word in word_list:
			if word == word.capitalize() and counter_for_capitalize == 0:
				# if this is capitalised and not first word in sentense, then ignore it,
				# because we don't need proper nouns.
				continue
			counter += 1
			counter_for_capitalize += 1
			try:
				next_word = word_list[counter]
				try:
					tmp = word_list[counter + 1]
					# TODO: use it as a variable
				except IndexError:
					tmp = 'NONE'
					# REALLY TODO: DO IT, CONTINUE IS SOOOO BAD
					continue
			except IndexError:
				continue

			try:
				order[word][next_word]['times_repeated'] += 1
				order[word][next_word]['next_words'][word_list[counter + 1]] += 1
			except KeyError:
				try:
					order[word][next_word]['times_repeated'] += 1
					order[word][next_word]['next_words'].update({word_list[counter + 1]: 1})
				except KeyError:
					try:
						# here and in next "try:" var.update({smthing: {}}) is equal to var[smthing] = {...}
						order[word].update({next_word: {
							'times_repeated': 1, 'next_words': {word_list[counter + 1]: 1}}
							})
					except KeyError:
						order.update({word: {next_word: {
							'times_repeated': 1, 'next_words': {word_list[counter + 1]: 1}}
							}})


	# if word has been mentioned very not often after 
	# some word, we delete it, because maybe it was 1 situation,
	# not an order we can follow.
	for key, val in order.items():
		for key2, val2 in val.items():
			for key3, vall in val2['next_words'].items():
				if vall > some_constant_which_we_need_to_have:
					order[key][key2]['next_words'].pop(keyy)


	return order


def main():
	parser = argparse.ArgumentParser(description='Teach your model.', prog='python train.py')
	parser.add_argument('input_dir',  help='Path to text file.', type=str)
	parser.add_argument('model', help='Path to where to save your model.', type=str)
	args = parser.parse_args()

	# args.path = 'data/text.txt' # temporaly

	text = get_text(args.input_dir)
	sentense_list = get_sentense_list(text)
	order = get_word_order(sentense_list)

	with open(args.model, 'wb') as f:
		pickle.dump(order, f)

main()

