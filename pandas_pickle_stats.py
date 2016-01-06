import sys
import Quandl as qd
import pickle as pkl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')



api_key = 'aaaaaaaaaaaaaaaaaaaaaaaaaa'

def get_states():
    us_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return us_states[0][0][1:]


def grab_data():
    states = get_states()
    main_df = pd.DataFrame()

    for abbv in states:
        query = 'FMAC/HPI_'+str(abbv)
        df = qd.get(query, authtoken=api_key)
        print(df[abbv])

##Here we define the column of our dataframe as percentage change.
##To get that we do ((new - old) / old) * 100.
##Note, that we only specify one dimension in the list for the new as
##we want it to convert every value in that dimension

        
        df[abbv] = ((df[abbv] - df[abbv][0]) / df[abbv][0]) * 100

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    print(main_df.head())

    with open('us_states.pickle','wb') as pickle_out:
        pkl.dump(main_df, pickle_out)


def HPI_Benchmark():
    df = qd.get("FMAC/HPI_USA", authtoken=api_key)
    title = list(df.columns.values)
    df[title[0]] = ((df[title[0]] - df[title[0]][0]) / df[title[0]][0]) * 100
    return df

def open_and_plot():    
    with open('us_states.pickle', 'rb') as pickle_in:
        HPI_data = pkl.load(pickle_in)

    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1),(0,0))

    benchmark = HPI_Benchmark();
    
    HPI_data.plot(ax = ax1)
    benchmark.plot(ax = ax1, color='k', linewidth = 10)
    
    plt.legend().remove()
    plt.show()


##Cleaning up our execution script so thats its modular and tidy 

##Wrapper for our sys.exit() call 
def ex():
    print('exiting...')
    sys.exit()

##Omg fucntion objects as values in a dictionary are the best thing ever 

def main():
    func_dict = {'plot': open_and_plot,
           'grab': grab_data,
           'exit': ex
           }
    
    while(1):
        x = input("Enter >> ")
        if not x:
            print('Error\n')
        elif x not in func_dict:
            print('Error\n')
        else:
            func_dict[x]()

main()
