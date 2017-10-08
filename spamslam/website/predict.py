import re
import numpy as np
import pickle

import os

def predict_from_text():
	module_dir = os.path.dirname(__file__)  # get current directory
	file_path = os.path.join(module_dir, 'trained_email_classifier.pickle')
	with open('test.txt') as t:
		raw_message = t.readlines()
	# print(raw_message)
	raw_message[0] = raw_message[0].replace('\n', ' ')
	list_of_words = raw_message[0].split()

	for y in list_of_words:
		y = re.sub(r'\W+', '', y)
		y = y.lower()

	file_path_list = os.path.join(module_dir, 'list.txt')
	with open(file_path_list) as f:
	    content = f.readlines()
	    # print content

	# print content

	words = [x[10:x.find(':')] for x in content]
	# print(words)
	freq = {}
	freq = freq.fromkeys(words, 0)

	for word in list_of_words:
		if word in freq.keys():
			print('YOOO')
			freq[word] += 1

	capital_data = []
	count=0
	for char in raw_message[0]:
		if char.isupper():
			count += 1
		if not char.isupper():
			if count != 0:
				capital_data.append(count)
			count = 0

	# print(freq)
	# print(len(list_of_words))
	new_list = []
	for xyz in words:
		new_list.append(freq[xyz])

	fourty_eight_attributes = 100*np.array(new_list)/float(len(list_of_words))
	six_attributes = np.array([raw_message.count(';'), raw_message.count('('), raw_message.count('['), raw_message.count('!'), raw_message.count('$'), raw_message.count('#')])/len(raw_message[0])
	print "Capital data", capital_data
	if capital_data:
		last_three = np.array([float(sum(capital_data))/float(len(capital_data)), max(capital_data), sum(capital_data)])
	else:
		last_three = np.array([0,0,0])

	predict_X = np.concatenate([fourty_eight_attributes, six_attributes, last_three])

	# print(fourty_eight_attributes)
	# print(predict_X.shape)

	pickle_in = open(file_path,'rb')
	mlp=pickle.load(pickle_in)
	ans = mlp.predict([predict_X])
	# print "answer:", ans
	return ans[0]
	# return 1
