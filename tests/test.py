# -*- coding: utf-8 -*-
from prediction import nlp


import unittest

class PredictionTest(unittest.TestCase):

    def test_positive(self):
        comment = "J'aime ça"
        prediction = nlp(comment)[0]['label'].capitalize()
        self.assertEqual(prediction, 'Positive')

    def test_negative(self):
        comment = "c'est triste de voir ça"
        prediction = nlp(comment)[0]['label'].capitalize()
        self.assertEqual(prediction, 'Negative')


if __name__ == '__main__':
    unittest.main()