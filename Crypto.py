import json, requests, sys


#function to return all the JSON response from the web services
def web_service(coinlist, coin_number):

    urlslist = []
    JSONList = []

    for coinlist in coinlist:
        url = 'https://api.coinmarketcap.com/v1/ticker/' + coinlist
        #append coin url in the list
        urlslist.append(url)

    # JSON request in a loop for all the coins
    for i in range(len(urlslist)):
        r = requests.get(urlslist[i])
        JSON = r.json()
        JSONList.append(JSON)

    return JSONList


def find_worst_coin(JSONList,coinlist):

    #initial definitions
    min_value24h = []
    min_value1h  = []
    max_value24h = []
    min_value1h  = []

    worst_24h = []
    worst_1h  = []
    best_1h   = []
    best_24h  = []

    #four Lists
    worst_hour = [None]*3
    worst_day  = [None]*3
    best_hour  = [None]*3
    best_day   = [None]*3

    #initialise lists
    percent_change_1h  = []
    percent_change_24h = []

    #enter all changes in a list
    for i1 in range(len(coinlist)):
        JSON = JSONList[i1]
        percent_change_1h.append(JSON[0]['percent_change_1h'])
        percent_change_24h.append(JSON[0]['percent_change_24h'])


    #Worst performance last hour and last 24hours
    min_value_1h  = min([float(i) for i in percent_change_1h])
    min_value_24h = min([float(i) for i in percent_change_24h])

    #Best Performance last hour and last 24 hours
    max_value_1h  = max([float(i) for i in percent_change_1h])
    max_value_24h = max([float(i) for i in percent_change_24h])

    #Get index of that element
    index_worst_1h  = percent_change_1h.index(str(min_value_1h))
    index_worst_24h = percent_change_24h.index(str(min_value_24h))
    index_best_1h   = percent_change_1h.index(str(max_value_1h))
    index_best_24h  = percent_change_24h.index(str(max_value_24h))

    #assign worst/best rate
    worst_1h =  coinlist[index_worst_1h];
    worst_24h = coinlist[index_worst_24h]
    best_1h   = coinlist[index_best_1h]
    best_24h  = coinlist[index_best_24h]


    #fill in lists
    worst_hour[0] = worst_1h; worst_hour[1] = min_value_1h; worst_hour[2] = percent_change_24h[index_worst_1h];
    worst_day[0] = worst_24h;  worst_day[1] = min_value_24h; worst_day[2] = percent_change_1h [index_worst_24h];

    best_hour[0] = best_1h; best_hour[1] = max_value_1h; best_hour[2] = percent_change_24h[index_best_1h];
    best_day[0] = best_24h; best_day[1] = max_value_24h; best_day[2] = percent_change_1h[index_best_24h];


    return min_value_1h, min_value_24h, max_value_1h, max_value_24h, worst_1h, worst_24h, \
            best_1h, best_24h , worst_hour, worst_day, best_hour, best_day, percent_change_1h, percent_change_24h


#function to calculate the total amount of money in USD
def total_money(JSONList, coin_number, coinlist):

    dollars_per_coin = []
    dollars = 0
    #Loop over to calculate total amount of money
    for i1 in range(len(coin_number)):
        JSON = JSONList[i1]
        if 'error' in JSON:
            print("The " + coinlist[i1] + " is not a valid currency name or it does not exist in coinmarketcap yet")
            print("We will calculate the rest of the valid currencies you entered")
            if i1+1 == len(coin_number):
                print("You don't have any other currencies to calculate")
                break
            else:
                i1 = i1+1
                #update element in JSONList
                JSON = JSONList[i1]
                dollars += float(coin_number[i1])*float(JSON[0]['price_usd'])
                #dollars_per_coin.append(float(coin_number[i1])*float(JSON[0]['price_usd']))

        else:
            dollars += float(coin_number[i1])*float(JSON[0]["price_usd"])
            dollars_per_coin.append(float(coin_number[i1])*float(JSON[0]['price_usd']))


    return dollars, dollars_per_coin

if __name__ == "__main__":
    #Solution Types
    "if solution is 1 then you enter the values manually"
    "if solution is 0 you predefine the coins and coin numbers you have"
    Solution = 0
    #enter the list of coins you have
    coinlist = ['bitcoin','ethereum', 'expanse', 'gulden','syscoin','digibyte','gamecredits','blackcoin','desire','colossuscoinxt','coinonatx',\
    'electra','grimcoin','litecoin','Verge', 'Potcoin', 'Dogecoin','Dash', 'Clams','Reddcoin']
    coin_number = ['0.00225','0.0228', '1','0', '130.6088','1888.5898','25.8530','0','49.6','5000','2008','99840','5000',\
    '0.237', '1462.2715', '0','12','0','0','0']


    coinomilist = ['bitcoin','ethereum', 'expanse', 'gulden','syscoin','digibyte','gamecredits','blackcoin',\
    'litecoin','Verge', 'Potcoin', 'Dogecoin','Dash', 'Clams','Reddcoin']

    coinomi_number = ['11','0','12','11','0','0','10','2000','0','0','0','0','0','0','0']

    if Solution == 1:
        #check digits initialisation
        check = 1
        checkdigit = 1
        idigit = 1
        #list initialisation
        #This is the list that contains your coins names
        coinlist = []
        # This is the list that contains your number of coins per coin
        coin_number = []

        print("Do you have cryptocurrencies? (Yes/No)")
        answer = raw_input()

        while check == 1:
            if answer == "Yes":
                if idigit == 1:
                    print ("enter the name of the cryptocurrency you have")
                    crypto_name = raw_input()
                    print ('How many coins of '+ crypto_name +' do you have?')
                    try:
                        crypto_number = raw_input()
                        crypto_number = float(crypto_number)
                    except ValueError:
                        print("That's not a  valid number. Please enter a real number!")
                    if isinstance(crypto_number, float):
                        coinlist.append(crypto_name)
                        coin_number.append(crypto_number)
                    print ("Do you have any other cryptocurrencies? (Yes/No)")
                    answer = raw_input()
                if answer == "Yes":
                    print ("enter the name of the other cryptocurrency you have")
                    crypto_name = raw_input()
                    print('How many coins of ' + crypto_name +' do you have?')
                    try:
                        crypto_number = raw_input()
                        crypto_number = float(crypto_number)
                    except ValueError:
                        print("That's not a valid number. Please enter a real number!")
                    if isinstance(crypto_number, float):
                        coinlist.append(crypto_name)
                        coin_number.append(crypto_number)
                    print ("Do you have any other cryptocurrencies? (Yes/No)")
                    answer = raw_input()
                    #check digit for first cryptocurrency becomes null
                    idigit = 0
                    #print out the list of coins and number of coins
                    print(coinlist)
                    print(coin_number)
                elif answer == "No":
                    #check digit for additional cryptocurrencies becomes null
                    check = 0
                    if answer == "No":
                        print("That is unfortunate. Go buy some")
                        JSONList = web_service(coinlist, coin_number)
                        dollars = total_money(JSONList,coin_number,coinlist)
                        sys.stdout.write("Your total amount of  Dollars you have is " + str(dollars) + '\n')
                if answer != "Yes":
                    if answer != "No":
                        print("Please enter Yes or No with a capital first letter")
                    break
            else:
                print("You should buy more cryptocurrencies!")
                print("so far you have the following cryptos")
                break
        for i in range(len(coinlist)):
            print (' You have ' + str(coin_number[i]) + ' coins of ' + str(coinlist[i]))

        # Call the main function for profit calculation  and decision making
        JSONList = web_service(coinlist, coin_number)

        dollars, dollars_per_coin = total_money(JSONList,coin_number,coinlist)

        sys.stdout.write("Your total amount of  Dollars you have is " + str(dollars) + '\n')

        # This runs the lists as they are here
    elif Solution == 0:
        for i in range(len(coinlist)):
            print (' You have ' + str(coin_number[i]) + ' coins of ' + str(coinlist[i]))

        JSONList = web_service(coinlist, coin_number)

        dollars, dollars_per_coin = total_money(JSONList,coin_number,coinlist)

        sys.stdout.write("Your total amount of  Dollars you have is " + str(dollars) + '\n')
        sys.stdout.write("Your total amount of  Dollars per coin is " + str(dollars_per_coin) + '\n')

        sys.stdout.write("calling web service to convert with the latest exchange USD/EUR rate" + '\n')

        #exchange in dollars
        url = 'https://api.fixer.io/latest?base=USD'
        r = requests.get(url)
        JSON = r.json()
        exchange_rate = JSON['rates']['EUR']
        euros_total = exchange_rate*dollars

        sys.stdout.write("Your total amount of Euros you have is " + str(euros_total) + '\n')

        #find worst/best coins
        min_value_1h, min_value_24h, max_value_1h, max_value_24h, worst_1h, worst_24h, \
        best_1h, best_24h , worst_hour, worst_day, best_hour, best_day, \
        percent_change_1h, percent_change_24h = find_worst_coin(JSONList,coinlist)

        # Calculate perfomances in coinomi
        JSONList_coinomi  = web_service(coinomilist, coinomi_number)

        #find worst/best coins in coinomi
        min_value_11h, min_value_244h, max_value_11h, max_value_244h, worst_11h, worst_244h, \
        best_11h, best_244h , worst_hour1, worst_day1, best_hour1, best_day1, \
        percent_change_11h, percent_change_244h = find_worst_coin(JSONList_coinomi,coinomilist)


        #convert unicode to float
        percent_change_1h  = [float(i) for i in percent_change_1h]
        percent_change_24h = [float(i) for i in percent_change_24h]


        #calculate average 1h
        average_1h  = sum((percent_change_1h))/((len(percent_change_1h)))
        average_24h = sum((percent_change_24h))/((len(percent_change_24h)))

        #Percentage % of capital per coin
        percentage_dollar_per_coin = []
        for dollars_coin in dollars_per_coin:
            percentage_dollar_per_coin.append(((dollars_coin)/dollars)*100)
        #control flow

        print("Checking percentages per coin...")
        sys.stdout.write("Total added percentage is " +  str(sum(percentage_dollar_per_coin[0:])) + '\n')

        sys.stdout.write("....." + '\n')
        sys.stdout.write("....." + '\n')
        sys.stdout.write("....." + '\n')
        sys.stdout.write("....." + '\n')
        print("average 1h is  "  + str(average_1h))
        print("average 24h is  " + str(average_24h))
        sys.stdout.write("Total Comparison performance Reporting" + '\n')
        for i1 in range(len(coinlist)):
            print(str(coinlist[i1]) + ',' + str(percent_change_1h[i1]) + '% 1h ' + ',' + str(percent_change_24h[i1]) + '% 24h')


        sys.stdout.write("Coinomi markets exchange comparison performance" + '\n')
        print("The worst coin for the past hour is " + str(worst_hour1[0]) + ' with a % rate of ' + str(worst_hour1[1]) + ' and 24h % of ' + str(worst_hour1[2]))
        print("The worst coin since the past day is " + str(worst_day1[0]) + ' with a % rate of ' + str(worst_day1[1]) + ' and last hour with % ' + str(worst_day1[2]))
        print("The best coin for the past hour is " + str(best_hour1[0]) + ' with a % rate of ' + str(best_hour1[1]) + ' and 24h % of ' + str(best_hour1[2]))
        print("The best coin since the past day is " + str(best_day1[0]) + ' with a % rate of ' + str(best_day1[1]) + ' and last hour with % ' + str(best_day1[2]))



