import json
import psycopg2
import statistics
import numpy as np
from scipy import stats

def format_float(num):
    return np.format_float_positional(num, trim='-')

def cleanStr4SQL(s):
    return s.replace("'","''").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def insertZip():
    print("Inserting zipcodes... ")

    with open('.//yelp_business.JSON','r') as f:
        line = f.readline()
        zipcode_list = []

        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')

        cur = conn.cursor()

        while line:
            data = json.loads(line)

            if data['postal_code'] not in zipcode_list:
                zipcode_list.append(data['postal_code'])

                sql_str = "INSERT INTO zipcode (num, city_name, state_name)" \
                          "VALUES ('" + cleanStr4SQL(data['postal_code']) + "','" + cleanStr4SQL(data['city']) + "','" + cleanStr4SQL(data['state']) + "');"
            
                try:
                    cur.execute(sql_str)
                except:
                    print("Insert to ZipCode failed!")
                    print(sql_str)

            line = f.readline()

        conn.commit()

def insertBuisness():
    print("Inserting businesses...")
    #read the JSON file
    with open('.//yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        #read each JSON abject and extract data
        while line:
            data = json.loads(line)
            business = data['business_id'] #business id

            sql_str = "INSERT INTO Business (bid,business_name,business_address,state_name,city_name,zip,stars,avgRating,numReviews,checkins) " \
                      "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(data["name"]) + "','" + cleanStr4SQL(data["address"]) + "','" + \
                      cleanStr4SQL(data["state"]) + "','" + cleanStr4SQL(data["city"]) + "','" + cleanStr4SQL(data["postal_code"]) + "'," + str(data["stars"]) + ",0, " + str(data["review_count"]) + ",0);"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to businessTABLE failed!")
                print(sql_str)

            conn.commit()

            # process business categories
            for category in data['categories']:

                category_str = "INSERT INTO Categories (business_id, category) " \
                               "VALUES ('" + business + "','" + cleanStr4SQL(category) + "');"
                
                try:
                    cur.execute(category_str)
                except:
                    print("Insert to categoryTABLE failed!")
                    print(category_str)

            conn.commit()

            line = f.readline()
            count_line +=1

    f.close()

def insertReviews():
    print("Inserting reviews... ")
    errorcount = 0

    with open('.//yelp_review.JSON','r') as f:
        line = f.readline()

        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')

        cur = conn.cursor()

        while line:
            data = json.loads(line)

            sql_str = "INSERT INTO Review (review_id, review_date, stars, review_text, business)" \
                      "VALUES ('" + cleanStr4SQL(data['review_id']) + "','" + data['date'] + "','" + str(data['stars'])\
                       + "','" + cleanStr4SQL(data['text']) + "', (" + "SELECT bid FROM Business WHERE bid = '" + cleanStr4SQL(data['business_id']) + "'));"
            
            try:
                cur.execute(sql_str)

            # track errors to avoid console spam when debugging
            except:
                if (errorcount < 11):
                    print(sql_str)
                    errorcount += 1

            line = f.readline()

        conn.commit()

def updateBusiness():
    print('Updating business avgRating, checkins, numRatings... ')
    open('./emmons_UPDATE.sql', 'w')

    try:
        conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='admin'")
    except:
        print('Unable to connect to the database!')

    cur = conn.cursor()
    cur.execute("SELECT business, stars FROM Review")

    businesses = {}
    ratings = cur.fetchall()

    # create dictionary of business_id:list(review scores)
    for x in ratings:
        if x[0] not in businesses:
            businesses[x[0]] = [x[1]]
        else:
            businesses[x[0]].append(x[1])

    # change value for each business id to avg review score
    with open('./emmons_UPDATE.sql', 'a') as f:
        for x in businesses:
            total = 0

            sql_str = "UPDATE business SET numReviews = " + str(len(businesses[x])) + " WHERE bid = '" + x + "';"

            # update numReviews for each business
            try:
                cur.execute(sql_str)
                f.write(sql_str + '\n')
            except:
                print('Failed to update numReviews in business table.')

            for rating in businesses[x]:
                total += rating

            businesses[x] = float("{:.1f}".format(total/len(businesses[x])))

            # update avgRating for each business
            sql_str = "UPDATE business SET avgRating = " + str(businesses[x]) + " WHERE bid = '" + x + "';"

            try:
                cur.execute(sql_str)
                f.write(sql_str + '\n')
            except:
                print('Failed to update avgRating in business table.')
                print(sql_str)

    # now we update checkins
    with open('./yelp_checkin.JSON', 'r') as y:
        line = y.readline()
        businesses = {}

        while line:
            data = json.loads(line)
            days = list(data['time'].values()) # dictionary of format {time:checkins} 

            total = 0

            for d in days:
                times = list(d.values()) # times = list(checkins)
                total = sum(times)

            businesses[data['business_id']] = total

            line = y.readline()

        with open('./emmons_UPDATE.sql', 'a') as f:
            for x in businesses:
                sql_str = "UPDATE business SET checkins = " + str(businesses[x]) + " WHERE bid = '" + x + "';"

                try:
                    cur.execute(sql_str)
                    f.write(sql_str + '\n')
                except:
                    print('Failed to update checkins in business table.')
                    print(sql_str)

    conn.commit()
    

def getTableSizes():
    try:
        conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='admin'")
    except:
        print('Unable to connect to the database!')

    cur = conn.cursor()
    open('./emmons_TableSizes.txt', 'w')


    with open('./emmons_TableSizes.txt', 'a') as f:
        f.write('YelpDB Table Sizes' + '\n')

        cur.execute("SELECT COUNT(*) FROM ZipCode")
        f.write('ZipCode: ' + str(cur.fetchall()[0][0]) + '\n')

        cur.execute("SELECT COUNT(*) FROM Business")
        f.write('Business: ' + str(cur.fetchall()[0][0]) + '\n')

        cur.execute("SELECT COUNT(*) FROM Review")
        f.write('Review: ' + str(cur.fetchall()[0][0]) + '\n')

        cur.execute("SELECT COUNT(*) FROM Categories")
        f.write('Categories: ' + str(cur.fetchall()[0][0]) + '\n')

def assignPopularity():
    businesses = []

    try:
        conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='admin'")
    except:
        print('Unable to connect to the database!')

    cur = conn.cursor()

    cur.execute("SELECT bid, checkins FROM business")

    try:
        cur.execute("SELECT business.bid, business.checkins, zipdata.population FROM business INNER JOIN zipdata ON business.zip = zipdata.zipcode;")
        businesses = cur.fetchall()

    except:
        print("Calculation/query failed")

    constants = []
    output = []

    #get initial popularity constants
    for x in businesses:
        calc = x[1]/x[2]
        output.append((x[0], calc))
        constants.append(calc)
        
    minConst = min(constants)
    maxConst = max(constants)
    minmax = maxConst-minConst
    avgConst = statistics.mean(constants)

    # normalize
    for x in output:
        calc = (x[1]-avgConst)/minmax
        x = (x[0], calc)

    sixtyPercentile = stats.scoreatpercentile(constants, [60])

    # if popularity constant is positive, the business is above average and therefore popular
    for x in output:
        if x[1] > sixtyPercentile:
            try:
                cur.execute("UPDATE business SET ispopular = TRUE WHERE bid = '" + x[0] + "';")
            except:
                print('Query failed')
        else:
            try:
                cur.execute("UPDATE business SET ispopular = FALSE WHERE bid = '" + x[0] + "';")
            except:
                print('Query failed')

    conn.commit()


def assignSuccess():
    
    try:
        conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='admin'")
    except:
        print('Unable to connect to the database!')

    cur = conn.cursor()
    ratings = []
    businessYears = {}

    try:
        cur.execute("SELECT business, CAST(EXTRACT(YEAR FROM review_date) AS INTEGER), stars FROM review;")
        ratings = cur.fetchall()
    except:
        print("Review query failed")


    for x in ratings:
        if x[0] not in businessYears:
            businessYears[x[0]] = {x[1]:[x[2]]}
        else:
            if x[1] not in businessYears[x[0]]:
                businessYears[x[0]][x[1]] = [x[2]]
            else:
                businessYears[x[0]][x[1]].append(x[2])

    output = {}

    # calculate yearly averages, if average of all years is > 3, business is successful
    for x in businessYears:
        numOfYears = len(list(businessYears[x].values()))
        averageScore = 0
        yearlyAverages = []

        for y in businessYears[x]:
            yearlyAverages.append(sum(businessYears[x][y])/len(businessYears[x][y]))

        averageScore = sum(yearlyAverages)

        output[x] = averageScore/numOfYears


    for x in output:
        if output[x] > 3:
            try:
                cur.execute("UPDATE business SET issuccessful = TRUE WHERE bid = '" + x + "';")
            except:
                print('Query failed')
        else:
            try:
                cur.execute("UPDATE business SET issuccessful = FALSE WHERE bid = '" + x + "';")
            except:
                print('Query failed')

    cur.execute("SELECT bid FROM business WHERE ispopular = FALSE")
    unpopular = cur.fetchall()

    # set all unpopular businesses to FALSE
    for x in unpopular:
        cur.execute("UPDATE business SET issuccessful = FALSE WHERE bid = '" + x[0] + "';")

    conn.commit()

insertZip()
insertBuisness()
insertReviews()
updateBusiness()
getTableSizes()
assignPopularity()
assignSuccess()