import unittest
import importlib
#import logging
import jsonpickle
import json


function = __import__('lambda_function')
handler = function.lambda_handler

class TestFunction(unittest.TestCase):

  def test_function(self):
    file = open('event.json', 'rb')
    try:
      ba = bytearray(file.read())
      event = jsonpickle.decode(ba)
      context = {'requestid' : '1234'}
      result = handler(event, context)
      print(str(result))
      self.assertRegex(str(result), 'FunctionCount', 'Should match')
    finally:
      file.close()
    file.close()

if __name__ == '__main__':
    unittest.main()