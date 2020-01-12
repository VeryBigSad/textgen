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
l.setLevel(logging.INFO)


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

    if length is None:
        length = 10
    if seed is None:
        random.seed()
        l.info('Generating with random seed.')
    else:
        random.seed(seed)
        l.info('Generating with seed ' + str(seed))
    sequence = [random.choice(list(order))]

    for counter in range(length):
        try:
            last_used = sequence[-1:][0]
            l.debug('last_used: ' + last_used)

            tmp_sum = [order[last_used][next_word]['times_repeated'] for next_word in list(order[last_used])]
            tmp_sum = sum(tmp_sum)
            # tmp_sum - how many times word had been used.

            item = random.randint(0, tmp_sum)
            l.debug(order[last_used])
            l.debug([random.choice(list(order[last_used])) for i in range(len(list(order[last_used])))])
            for next_word in [random.choice(list(order[last_used])) for i in range(len(list(order[last_used])))]:
                item -= order[last_used][next_word]['times_repeated']
                if item <= 0:
                    sequence.append(next_word)
                    l.debug('We added a word ' + next_word + ', because it had chance ' +
                            str(order[last_used][next_word]['times_repeated'] / tmp_sum))
                    break
                    # TODO: train method adds next_word to next_words, so it is sequence by length of 3. We HAVE to
                    #  use it.
        except KeyError as e:
            l.error(str(e) + '; Probably some word had been used in description of other words (like, {"word": {'
                             '"bad_word"}}), and not mentioned in main order dictionary. Now length is one less.')
            l.info('Getting another "seed" word.')
            sequence.append(random.choice(list(order)))
    l.info('generation done, length - ' + str(len(sequence)) + '. Might not be one you typed in.')

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

    # generation itself
    order = unpack(args.model)
    result = generate(order, length=args.length, seed=args.seed)

    # printing result
    print('\n', result)


# my local path for pycharm and path from console
# TODO: use not absolute path
if sys.argv[0] == 'generate.py' or sys.argv[0] == 'D:/Programming/textgen/generate.py':
    try:
        main()
    except KeyboardInterrupt:
        exit('\n\nKeyboard Interrupt')
