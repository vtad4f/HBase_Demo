

import sys


class Review:
   FIELDS = [
      "product/productId:",
      "review/userId:",
      "review/profileName:",
      "review/helpfulness:",
      "review/score:",
      "review/time:",
      "review/summary:",
      "review/text:"
   ]
   MOVIE_ID, USER_ID, USER_NAME, HELPFUL, SCORE, TIME, SUMMARY, TEXT = range(len(FIELDS))
   
   
def Parse(path, interval, callback, *args, **kwargs):
   """
      BRIEF  Get the reviews from the file
             NOTE - The file this is designed to parse has 71205215 lines
                  - The max printed value of n is 7911 for interval 1000
   """
   reviews = []
   review = ['']*len(Review.FIELDS)
   state = 0
   n = 0
   
   print("Parsing...")
   sys.stdout.flush()
   
   # Iterate over all the lines
   with open(path, 'rb') as f:
      for i, line in enumerate(f):
         
         line = line.strip()
         if line:
            
            # Expect certain content each line
            expected = Review.FIELDS[state]
            if line.startswith(expected):
               review[state] = line[len(expected):].lstrip()
               state += 1
               
               # Cache each complete review
               if (state == len(Review.FIELDS)):
                  reviews.append(review)
                  
                  # Start a new review
                  review = ['']*len(Review.FIELDS)
                  state = 0
                  
                  # Trigger the callback every once in a while
                  if len(reviews) % interval == 0:
                     print(n)
                     sys.stdout.flush()
                     callback(reviews, *args, **kwargs)
                     n += 1
                     
                     # Reset the list after the callback is triggered
                     reviews = []
                     
            elif not ':' in line:
               
               # Else it may be a continuation of the previous field
               review[state - 1] += '\n' + line
               
            else:
               
               # Report the error
               raise Exception("{0:<10} #{1}#".format(i, line))
               
   # Handle whatever is left
   if reviews:
      print(n)
      sys.stdout.flush()
      callback(reviews, *args, **kwargs)
      
   print("Done!")
   sys.stdout.flush()
   
   
if __name__ == '__main__':
   """
      BRIEF  Test parsing the reviews file
   """
   import os
   
   def DoNothing(reviews):
      pass
      
   Parse(os.path.join('..', 'in', 'movies.txt'), 100000, DoNothing)
   
   