import random	
import argparse
import pickle
import logging
import sys

# TODO: i know it's bad, will have to make this
# into class and give it self.l variable.

l = logging.getLogger('Training')
formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)

l.addHandler(handler)
l.setLevel(logging.DEBUG)


def get_text(path):
	l.info('getting text from "' + str(path) + '".')
	try:
		text = open(path, encoding='utf8').read() # лев толстой, война и мир
	except FileNotFoundError:
		l.critical('text file not found')
		exit()

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


def dump(model_path, order):
	with open(model_path, 'wb') as f:
		pickle.dump(order, f)
	l.info('writing down to "' + str(model_path) + '" done.')


def get_regular_case(word):

	# TODO: make it work, otherwise it is kinda useless.

	return word


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
	# todo: add that constant properly and etc

	for word_list in sentence_list:
		for word_id in range(len(word_list)-1):
			word = word_list[word_id]
			word = get_regular_case(word)

			if word == word.capitalize() and word_id != 0 and word != ',':
				# if this is capitalised and not first word in sentense, then ignore it,
				# because we don't need proper nouns.
				continue
			word = word.lower()

			counter += 1
			try:
				next_word = word_list[word_id + 1]
				next_next_word = word_list[word_id + 2]
				if word_list[word_id + 2] == word_list[word_id + 2].capitalize():
					next_next_word = ''
				if word_list[word_id + 1] == word_list[word_id + 1].capitalize():
					next_word = ''


			except IndexError:

				# TODO: remove continue and replace it with something
				# else, because this cuts some words.
				continue
			try:
				order[word][next_word]['times_repeated'] += 1
				order[word][next_word]['next_words'][next_next_word] += 1
			except KeyError as e3:
				# l.debug(str(e3) + ' e3')
				try:
					order[word][next_word]['times_repeated'] += 1
					order[word][next_word]['next_words'].update({next_next_word: 1})
				except KeyError as e2:
					# l.debug(str(e2) + ' e2')
					try:
						# here and in next "try:" var.update({smthing: {}}) is equal to var[smthing] = {...}
						order[word].update({next_word: {
							'times_repeated': 1, 'next_words': {next_next_word: 1}}
							})
					except KeyError as e:
						# l.debug(str(e) + ' e')
						order.update({word: {next_word: {
							'times_repeated': 1, 'next_words': {next_next_word: 1}}
							}})

	# if word has been mentioned very not often after 
	# some word, we delete it, because maybe it was 1 situation,
	# not an order we can follow.
	tmporder = order.copy()

	# {'word': {'second_word1': {'times_repeated': 100, 'next_words': {'third_word': 2, 'third_word2': 1}},
	# 'second_word2': {'times_repeated': 99, 'next_words': {'third_word': 12, 'third_word2': 11}}, ...}
	for word, word_val in order.items():
		if word_val == {}:
			tmporder.pop(word)
			continue
		if word == '' or word == ',':
			tmporder.pop(word)
			continue
		for nxt_word in list(word_val):
			nxt_word_val = word_val[nxt_word]
			if nxt_word_val == {}:
				tmporder[word].pop(nxt_word)
				continue
			if nxt_word == '' or nxt_word == ',':
				tmporder[word].pop(nxt_word)
				continue
			for nxt2_word in list(nxt_word_val['next_words']):
				nxt2_word_val = nxt_word_val['next_words'][nxt2_word]
				if nxt2_word_val == {}:
					tmporder[word][nxt_word]['next_words'].pop(nxt2_word)
				if nxt2_word == '' or nxt2_word == ',':
					tmporder[word][nxt_word]['next_words'].pop(nxt2_word)
				elif nxt2_word_val < some_constant_which_we_need_to_have:
					tmporder[word][nxt_word]['next_words'].pop(nxt2_word)
	order = tmporder.copy()
	for word, word_val in order.items():
		if word_val == {}:
			tmporder.pop(word)
			continue
		if word == '' or word == ',':
			tmporder.pop(word)
			continue
		for nxt_word in list(word_val):
			nxt_word_val = word_val[nxt_word]
			if nxt_word_val == {}:
				tmporder[word].pop(nxt_word)
				continue
			if nxt_word == '' or nxt_word == ',':
				tmporder[word].pop(nxt_word)
				continue
			for nxt2_word in list(nxt_word_val['next_words']):
				nxt2_word_val = nxt_word_val['next_words'][nxt2_word]
				if nxt2_word_val == {}:
					tmporder[word][nxt_word]['next_words'].pop(nxt2_word)
				if nxt2_word == '' or nxt2_word == ',':
					tmporder[word][nxt_word]['next_words'].pop(nxt2_word)
				elif nxt2_word_val < some_constant_which_we_need_to_have:
					tmporder[word][nxt_word]['next_words'].pop(nxt2_word)
	order = tmporder.copy()


	return order


def main():
	# parsing arguments
	parser = argparse.ArgumentParser(description='Teach your model.', prog='python train.py')
	parser.add_argument('input_dir',  help='Path to text file.', type=str)
	parser.add_argument('model', help='Path to where to save your model.', type=str)
	args = parser.parse_args()

	text = get_text(args.input_dir)
	sentense_list = get_sentense_list(text)
	order = get_word_order(sentense_list)
	l.debug('order len - ' + str(len(list(order))))

	l.info('training done')
	dump(args.model, order)


if sys.argv[0] == 'train.py' or sys.argv[0] == 'D:/Programming/textgen/train.py':
	try:
		main()
	except KeyboardInterrupt:
		exit('\n\nKeyboard Interrupt')

