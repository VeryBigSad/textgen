from train import get_sentense_list, get_text, get_word_order, dump
from generate import generate as gen


class TextGenerator:
	def __init__(self, text_path='data/text.txt', store_path='data/model.mdl', seed=None, length=70):
		self.text_path = text_path
		self.store_path = store_path
		self.seed = seed
		self.length = length
		self.order = None

	def set_store_path(store_path):
		self.store_path = store_path

	def set_text_path(text_path):
		self.text_path = text_path

	def set_seed(seed):
		self.seed = seed

	def set_length(length):
		self.length = length

	def fit(self):
		self.order = get_word_order(get_sentense_list(get_text(text_path)))
		return self.order

	def generate(self):
		return gen(self.order, self.length, self.seed)

	def store(self):
		# save model to file
		dump(self.store_path, self.order)

