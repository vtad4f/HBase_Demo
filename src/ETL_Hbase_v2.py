# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 21:38:19 2019

@author: Ed
"""

from starbase import Connection

c = Connection("127.0.0.1", "8000")

#Create a table instance - no table is created at this point, just instantiated.
ratings = c.table('ratings')

#if table exists, drop
if (ratings.exists()):
    print('Drop existing ratings table \n')
    ratings.drop()
    
#Now create a table(ratings) with column family/ies - rating in this example
#This is the point when the table is created
ratings.create('rating')
#Check if table exists - confirm - this cmd should print True if table exists
ratings.exists()
#Show table columns - explore
ratings.columns()
'''
#This is how you add & drop columns if needed
ratings.add_columns('col1','col2','col3')
ratings.drop_columns('col1','col2','col3')
'''
print('Parsing the ml-100k ratings data.....\n')
ratingFile = open('PATH to local dir on local PC', 'r')

batch = ratings.batch()

for line in ratingFile:
    (userID, movieID, rating, timestamp) = line.plit()
    batch.ipdate(userID, {'rating': {movieID: rating}})
    
ratingFile.close()

print('Committing ratings data to HBase via REST serice\n')
batch.commit(finalize = True)


print('Get back ratings for some users.....\n')
print('Ratings for user ID 1: \n')
print(ratings.fetch('1'))
print('Ratings for user ID 33: \n')
print(ratings.fetch('33'))