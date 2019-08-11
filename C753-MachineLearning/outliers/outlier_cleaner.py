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
    from sklearn import linear_model
    import math
    reg = linear_model.LinearRegression()
    reg.fit(ages, net_worths)
    #print(ages)

    for i,age in enumerate(ages):
        # determine the error (predicted value minus actual value)
        error = abs(predictions[i] - net_worths[i])
        cleaned_data.append((age, net_worths[i], error))

    cleaned_data = sorted(cleaned_data, key = lambda x: x[2])[:-10] # 10 points <> 10%
    #print(len(cleaned_data))
    return cleaned_data

    ######
    # Below here is work that does not provide correct output
    ######
    #point_errors = []
    #outliers = []
    #print("Number of ages: {}".format(len(ages)))
    #print("Number of predictions: {}".format(len(predictions)))
    #for index,age in enumerate(ages):
        #print(age)
        #print(predictions)
        # determine the square of the error for the specific point: y = mx + b; p - y = error
        # Ages is a list of lists. The nested lists have 1 value (the age)
        #diff = (predictions[index] - (reg.coef_ * age[0] + reg.intercept_))^2

        # Determine if the error is greater than the existing known errors
        #point_errors.append(diff)
        #point_errors.sort(reverse=True)
        #point_errors = point_errors[10:]

        #if diff in point_errors:
        #    outliers.append(index)

    #cleaned_data = copy(ages)
    #for i in outliers: cleaned_data.remove(i)

