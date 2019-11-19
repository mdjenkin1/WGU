import re
import pandas as pd

test_df = pd.DataFrame()

def SplitTime(intIn):
    timeMask = re.compile('(\d{2})(\d{2})')
    try:
        timeStr = str(int(intIn)).zfill(4)
        #print(timeStr)
        timeParts = timeMask.match(timeStr)
        #print(timeParts)
        #print(timeParts[1])
        #print(timeParts[2])
        #print(timeParts.groups())
        return timeParts.groups()
    except:
        #pprint.pprint("This can not be cast as an integer: {}".format(intIn))
        return [0,0]
        pass
    else:
        return [0,0]

t1 = {
    'time': [123,2342,235,6532,'NaN'],
    'Year': [2018,1989,2002,1976,2001],
    'Month':[1,12,3,5,1],
    'DayofMonth':[6,5,4,3,2]
}
test_df = pd.DataFrame(t1)
print(test_df)

test_df[['ti','me']] = pd.DataFrame(test_df.apply(lambda row: SplitTime(row['time']), axis = 1).values.tolist())
#print(test_df.apply(lambda row: SplitTime(row['time']), axis = 1).values.tolist())
print(test_df)

test_df['DepartDateTime'] = pd.to_datetime({
    'year': test_df['Year'],
    'month': test_df['Month'],
    'day': test_df['DayofMonth'],
    'hour': test_df['ti'],
    'minute': test_df['me']
})
print(test_df)

#test_df['DepartDateTimeStrings'] = pd.to_datetime(
#    str(test_df['Year']) + str(test_df['Month']).zfill(2) + str(test_df['DayofMonth']).zfill(2) + str(test_df['time']).zfill(4),
#    format='%Y%m%d%H%M'
#)
#print(test_df)

#print(SplitTime(5432).values()))