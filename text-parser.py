import random	

text = open('text.txt') # лев толстой, война и мир
text = text.read().lower()[:99999]


def get_sentense_list(text):
	alphabet = 'йцукенгшщзхъфывапролджэячсмитьбюё'
	sentences = []
	tmp = ''
	for i in text:
		if i == '.' or i == '?' or i == '!':
			sentences.append(tmp)
			tmp = ''
		else:
			tmp += i
	return sentences


def get_word_list(text):
	alphabet = 'йцукенгшщзхъфывапролджэячсмитьбюё'
	word_list = [i for i in text.split(' ')]
	
	for i in word_list:
		tmp = ''  
		for j in i:
			if j in alphabet:
				tmp += j
		word_list[word_list.index(i)] = tmp

	word_list = [i for i in word_list if i != '']
	return word_list

def get_word_order(word_list):
	order = {} # {'word': {'second_word1': 100, 'second_word2': 99}, 'another_word': {}...}
	counter = 0

	for word in word_list:
		counter += 1
		try:
			next_word = word_list[counter]
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


def generate(word_order, length=100):

	key = random.choice(list(word_order)) # seeding
	sequence = [key]
	print('key:', key)
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

word_list = get_word_list(text)
word_order = get_word_order(word_list)
# result = generate(word_order, length = 30)
sentense_list = get_sentense_list(text)
print (sentense_list[:100])
# print(result)
