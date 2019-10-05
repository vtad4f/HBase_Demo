

import sys


class Reviews:
   """
      BRIEF  
   """
   
   FIELDS = [
      "product/productId:" ,
      "review/userId:"     ,
      "review/profileName:",
      "review/helpfulness:",
      "review/score:"      ,
      "review/time:"       ,
      "review/summary:"    ,
      "review/text:"       ,
   ]
   MOVIE_ID, USER_ID, USER_NAME, HELPFUL, SCORE, TIME, SUMMARY, TEXT = range(len(FIELDS))
   
   @staticmethod
   def Parse(path):
      """
         BRIEF  Get the reviews from the file
                NOTE - the file this is designed to parse has 71205215 lines
      """
      reviews = []
      review = {}
      state = 0
      
      # Iterate over all the lines
      with open(path, 'rb') as f:
         for i, line in enumerate(f):
            
            if i % 1000000 == 0:
               print(i / 1000000)
               sys.stdout.flush()
               
            line = line.strip()
            if line:
               
               # Expect certain content each line
               expected = Reviews.FIELDS[state]
               if line.startswith(expected):
                  review[state] = line[len(expected):].lstrip()
                  state += 1
                  
                  # Cache each complete review
                  if (state == len(Reviews.FIELDS)):
                     reviews.append(review)
                     
                     # Clear since we're ready to start over
                     review = {}
                     state = 0
                     
               elif not ':' in line:
                  
                  # Else it may be a continuation of the previous field
                  review[state - 1] += '\n' + line
                  
               else:
                  # Report the error
                  print("{0:<10} #{1}#".format(i, line))
                  sys.stdout.flush()
                  
                  # Clear to be safe
                  review = {}
                  state = 0
                  
      return reviews
      
      
if __name__ == '__main__':
   """
      BRIEF  Test parsing the reviews file
   """
   import os
   
   path = os.path.join('..', 'in', 'movies.txt')
   
   print("Parsing...")
   sys.stdout.flush()
   
   reviews = Reviews.Parse(path)
   
   print("Done!")
   sys.stdout.flush()
   
   