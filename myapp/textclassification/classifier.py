import os
import pickle
import numpy as np
import re
from itertools import product

class TextClassifier():
  def __init__(self):
    print('I have been initiated')
    self.labels = ['English','Japanese']

  def load_model(self):
    print(os.getcwd())
    self.sc = pickle.load(open(os.path.join('textclassification','pickle_objs','sc_trained.pkl'),'rb'))
    self.pca = pickle.load(open(os.path.join('textclassification','pickle_objs','pca_trained.pkl'),'rb'))
    self.logreg = pickle.load(open(os.path.join('textclassification','pickle_objs','logreg_trained.pkl'),'rb'))

  def classify(self, text):
    X = self.__get_features(text)
    X = self.sc.transform(X)
    X = self.pca.transform(X)
    y = self.logreg.predict(X)[0]
    proba = round(self.logreg.predict_proba(X).max()*100, 2)
    return self.labels[y], proba

  def __get_features(self, text):
    letter_list = 'abcdefghijklmnopqrstuvwxyz '
    comb_list = [''.join(p) for p in product(letter_list, repeat=2)]
    letter_density_list = np.empty(len(letter_list))
    comb_density_list = np.empty(len(comb_list))


    text = text.lower()
    text = re.sub('[^\w\s]','',text)
    text = re.sub('[\d+]','',text)
    text = text.strip()
    if text == "":
      letter_density_list = np.zeros(len(letter_list))
      comb_density_list = np.zeros(len(comb_list))
      return np.concatenate((letter_density_list, comb_density_list), axis=0).reshape(1,-1)
    else:
      for i_letter in range(len(letter_list)):
        letter_density_list[i_letter] = self.__char_density(text, letter_list[i_letter])
      for i_comb in range(len(comb_list)):
        comb_density_list[i_comb] = self.__comb_densities(text, comb_list[i_comb])
      return np.concatenate((letter_density_list, comb_density_list), axis=0).reshape(1,-1)

  def __comb_densities(self, text, comb):
    return text.count(comb)/len(text)

  def __char_density(self, text, letter):
    return len([a for a in text if a.casefold() == letter])/sum([len(b) for b in text.split()])