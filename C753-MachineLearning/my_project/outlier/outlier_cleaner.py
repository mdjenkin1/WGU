#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    
    cleaned_data = []

    ### your code goes here
    import math
    from sklearn import linear_model
    
    reg = linear_model.LinearRegression()
    reg.fit(ages, net_worths)
    #print(ages)

    for i,age in enumerate(ages):
        # determine the error (predicted value minus actual value)
        error = abs(predictions[i] - net_worths[i])
        cleaned_data.append((age, net_worths[i], error))

    cleaned_data = sorted(cleaned_data, key = lambda x: x[2])[:-10]
    #print(len(cleaned_data))
    return cleaned_data


