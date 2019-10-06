

class Reviews:
   """
      BRIEF  Just a 
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
   def Parse(path, callback, interval):
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
                     
                     # Start a new review
                     review = {}
                     state = 0
                     
                     # Trigger the callback every once in a while
                     if len(reviews) % interval == 0:
                        callback(reviews)
                        
                        # Reset the list after the callback is triggered
                        reviews = []
                        
               elif not ':' in line:
                  
                  # Else it may be a continuation of the previous field
                  review[state - 1] += '\n' + line
                  
               else:
                  
                  # Report the error
                  raise Exception("{0:<10} #{1}#".format(i, line))
                  
                  
if __name__ == '__main__':
   """
      BRIEF  Test parsing the reviews file
   """
   import os
   import sys
   
   path = os.path.join('..', 'in', 'movies.txt')
   
   i = 0
   def HandleReviews(reviews):
      global i
      print(i)
      sys.stdout.flush()
      i += 1
      
   print("Parsing...")
   sys.stdout.flush()
   
   reviews = Reviews.Parse(path, HandleReviews, 100000)
   
   print("Done!")
   sys.stdout.flush()
   
   