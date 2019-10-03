//enter into hbase environment
hbase shell


##### Table 'emp' #####

//create a table
create 'emp', 'personal', 'professional'

//see what tables are there
list

//see table structure
describe 'emp'

//see all table data
scan 'emp' 

//put the datas
put 'emp', 'e1', 'personal:name', 'A'
put 'emp', 'e1', 'personal:age', '50'
put 'emp', 'e1', 'professional:designation', 'head'
put 'emp', 'e2', 'personal:name', 'B'
put 'emp', 'e2', 'personal:age', '25'

//get data
get 'emp', 'e1'
get 'emp', 'e2', 'personal:name'

//delete data
deleteall 'emp', 'e1'
delete 'emp', 'e2', 'personal:name'

//drop the table
disable 'emp'
drop 'emp'


##### Table Twitter ######

//see a limited number of data
scan 'Twitter', {'COLUMNS'=>'DateTime:Time', 'LIMIT'=>4, 'REVERSED'=>true}

//read limited number of data from specific row
scan 'Twitter', { 'COLUMNS' => ['DateTime:Date', 'DateTime:Time'], 'LIMIT'=>5, 'STARTROW'=>' https://twitter.com/realDonaldTrump/status/795845126744604673'}

//read data with a specific substring
scan 'Twitter', { 'COLUMNS' => 'Tweets:Tweet_Text', 'FILTER' => "ValueFilter(=, 'substring:beautiful')"}

//read data with specific column value
scan 'Twitter', {'COLUMNS'=>'Tweets:Type', 'LIMIT'=>3, 'FILTER'=>"ValueFilter(=,'binary:link')"}

//see all column value while filtering in one value
scan 'Twitter', {'COLUMNS'=>'Info:Retweets', 'LIMIT'=>2}
//decimal 1738 = hexadecimal 6CA
scan 'Twitter', {'FILTER'=>"SingleColumnValueFilter('Info','Retweets',=,'binary:\x00\x00\x06\xCA')"}


//Setting the version property to a column family
alter 'Twitter', {'NAME'=>'Tweets', 'VERSIONS'=>3}

//Putting data (adding two additional versioned data with the actual data)
put 'Twitter', 'https://twitter.com/realDonaldTrump/status/797034721075228672', 'Tweets:Type', 'type1'
put 'Twitter', 'https://twitter.com/realDonaldTrump/status/797034721075228672', 'Tweets:Type', 'type2'

//getting data (If you want to see latest 2 Versions of that data
get 'Twitter', 'https://twitter.com/realDonaldTrump/status/797034721075228672', {'COLUMNS'=>'Tweets:Type', 'VERSIONS'=>2}

