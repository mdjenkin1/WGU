import re
import pandas as pd
import pprint

test_df = pd.DataFrame()

#def SplitTime(intIn):
#    timeMask = re.compile('(\d{2})(\d{2})')
#    try:
#        timeStr = str(int(intIn)).zfill(4)
#        #print(timeStr)
#        timeParts = timeMask.match(timeStr)
#        #print(timeParts)
#        #print(timeParts[1])
#        #print(timeParts[2])
#        #print(timeParts.groups())
#        print("{} split to {} and {}".format(intIn,timeParts.group(1),timeParts.group(2)))
#        #return timeParts.groups()
#        #return {'hr':int(timeParts.group(1)), 'mn':int(timeParts.group(2))}
#        return [int(timeParts.group(1)), int(timeParts.group(2))]
#    except:
#        return[0,0]
#        #pprint.pprint("This can not be cast as an integer: {}".format(intIn))
#        #return {
#        #    'hr':0,
#        #    'mn':0
#        #}
#        pass
#    else:
#        return[0,0]
#        #return {
#        #    'hr':0,
#        #    'mn':0
#        #}


def SplitTime(intIn):
    timeMask = re.compile('(\d{1,2})(\d{2})')
    try:
        timeParts = timeMask.match(str(int(intIn)))
        return [int(timeParts.group(1)), int(timeParts.group(2))]
    except:
        return [0,0]
    else:
        return [0,0]

#t1 = {
#    'time': [123,2342,235,6532,'NaN'],
#   'Year': [2018,1989,2002,1976,2001],
#    'Month':[1,12,3,5,1],
#    'DayofMonth':[6,5,4,3,2]
#}
#test_df = pd.DataFrame(t1)
#print(test_df)

#test_df[['ti','me']] = pd.DataFrame(test_df.apply(lambda row: SplitTime(row['time']), axis = 1).values.tolist())
#print(test_df.apply(lambda row: SplitTime(row['time']), axis = 1).values.tolist())
#print(test_df)

#test_df['DepartDateTime'] = pd.to_datetime({
#    'year': test_df['Year'],
#    'month': test_df['Month'],
#    'day': test_df['DayofMonth'],
#    'hour': test_df['ti'],
#    'minute': test_df['me']
#})
#print(test_df)

#columnsToValidate = [
#    "DepTime", "CRSDepTime", 
#    "ArrTime", "CRSArrTime",
#    "Year", "Month","DayofMonth"
#]

reloaded_df = pd.read_pickle("./pickles/inprocessDf.pkl")

#working_df = reloaded_df[columnsToValidate].copy()
working_df = reloaded_df[['ArrTime']].copy()
#working_df[['ti','me']] = working_df.apply(lambda row: SplitTime(row["ArrTime"]), axis = 1).values.tolist()
#working_df[['ti','me']] = working_df.apply(lambda row: SplitTime(row["ArrTime"]), axis = 1)
#pprint.pprint(working_df)
#print(working_df.dtypes)

#split_values = pd.DataFrame(working_df.apply(lambda row: SplitTime(row["ArrTime"]), axis = 1).values.tolist())
split_values = working_df.apply(lambda row: SplitTime(row["ArrTime"]), axis = 1).values.tolist()
pprint.pprint(split_values)


#DataFramePickler(working_df, "DtValidation", pklPath=picklePath)



#test_df['DepartDateTimeStrings'] = pd.to_datetime(
#    str(test_df['Year']) + str(test_df['Month']).zfill(2) + str(test_df['DayofMonth']).zfill(2) + str(test_df['time']).zfill(4),
#    format='%Y%m%d%H%M'
#)
#print(test_df)

#print(SplitTime(5432).values()))