from django.views import View
from django.http import JsonResponse
import json

from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

SEPARATORS = ['-', '#', '_', '\n', ' ']

class Receipts(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request, format=None):
        data = request.FILES['receipt'].read().decode('UTF-8')
        response = JsonResponse(getBlocks(data), status=200)
        response["Access-Control-Allow-Origin"] = "*"
        return response

def getBlocks(text):
  blocks = []
  current_row = 1
  currentBlock = []
  currentLine = ""
  for character in text:
    if (character == '\n'):
      if (isValidLine(currentLine)):
        currentBlock.append(currentLine)
      elif len(currentBlock) !=0:
        blocks.append({
          "begin_row": current_row - len(currentBlock),
          "begin_col": 1,
          "end_row": current_row - 1,
          "end_col": len(currentBlock[-1])
        })
        currentBlock = []
      currentLine = ""
      current_row += 1
    else:
      currentLine += character
  return {
    "blocks": blocks
  }



def isValidLine(line):
  for c in line:
    if c not in SEPARATORS:
      return True  
  return False