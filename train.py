import random	
import argrapse

parser = argparse.ArgumentParser(description='Teach your model.', prog='python train.py')
parser.add_argument('input-dir', metavar='i', help='Path to text file.', required=True, type=str)
parser.add_argument('model', metavar='m', help='Path to where to save your model.', required=True, type=str)
args = parser.parse_args()

def unpack():
	text = open('data/text.txt') # лев толстой, война и мир
	text = text.read()[:99999]

	return text


def get_sentense_list(text):
	# returns something like that: [['word1', 'in', 'sentence', 'one'], ['second', 'sentence'],...] etc

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
	alphabet = 'йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЧЯСМИТЬБЮЁ'
	word_list = [i for i in text.split(' ')]
	
	counter = -1
	# so it will start from 0

	for i in word_list:
		counter += 1
		tmp = ''
		for j in i:
			if j in alphabet:
				tmp += j


		# counter variable is replacement for word_list.index(i)
		word_list[counter] = tmp


	word_list = [i for i in word_list if i != '']
	return word_list


def get_word_order(sentence_list):
	# returns:
	# {'word': {'second_word1': 100, 'second_word2': 99}, 'another_word': {}...}

	# TODO: make it use sentense_list, not word_list, so it
	# will be able to cut proper nouns.

	order = {} 
	counter = 0

	for word_list in sentence_list:
		for word in word_list:
			counter += 1
			try:
				next_word = word_list[counter]
				if next_word == next_word.capitalize() and counter != 0:
					continue
					# if this is capitalised and not first word in sentense, then ignore it,
					# because we don't need proper nouns.
			except IndexError:
				continue

			try:
				order[word][next_word] += 1
			except KeyError:
				try:
					order[word].update({next_word: 1})
				except KeyError:
					order.update({word: {next_word: 1}})

	return order


