#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from nltk.corpus import names
import random

def gender_features(word):
	return {'last_letter': word[-1]}

print(gender_features('Shrek'))



labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
print(random.shuffle(labeled_names))

featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print("Nombres extraños: ")
print( classifier.classify(gender_features('Neo')) )

print( classifier.classify(gender_features('Trinity')) )
print("-------------")


print("Acuracy: ")
print(nltk.classify.accuracy(classifier, test_set))
print("------------------")
print("")
print( classifier.show_most_informative_features(5) )

print(".-.-.-.-.-.-")

from nltk.classify import apply_features
train_set = apply_features(gender_features, labeled_names[500:])
test_set = apply_features(gender_features, labeled_names[:500])

def gender_features2(name):
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    return features
 	
print("Aplicando gender_features2 con Jhon:")
print( gender_features2('John') )

print("..........................")


featuresets = [(gender_features2(n), gender) for (n, gender) in labeled_names]
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))

train_names = labeled_names[1500:]
devtest_names = labeled_names[500:1500]
test_names = labeled_names[:500]

train_set = [(gender_features(n), gender) for (n, gender) in train_names]
devtest_set = [(gender_features(n), gender) for (n, gender) in devtest_names]
test_set = [(gender_features(n), gender) for (n, gender) in test_names]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, devtest_set))

print("Seccion tag, guess, name:")

errors = []
for (name, tag) in devtest_names:
	guess = classifier.classify(gender_features(name))
	if guess != tag:
		errors.append( (tag, guess, name) )

for (tag, guess, name) in sorted(errors):
	print('correct={:<8} guess={:<8s} name={:<30}'.format(tag, guess, name))

def gender_features(word):
	return {'suffix1': word[-1:],'suffix2': word[-2:]}

train_set = [(gender_features(n), gender) for (n, gender) in train_names]
devtest_set = [(gender_features(n), gender) for (n, gender) in devtest_names]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, devtest_set))