import unittest
import json


function = __import__('lambda_function')
handler = function.lambda_handler

class TestFunction(unittest.TestCase):
  def test_function(self):
    file = open('event.json', 'rb')
    try:
      event = (json.loads(file.read()))
      print('event',event)
      context = {'requestid' : '1234'}
      result = handler(event, context)
      print(str(result))
    finally:
      file.close()
    #file.close()

if __name__ == '__main__':
    unittest.main()