import csv
import matplotlib.pyplot as plt
import numpy as np
from simple_bot import SimpleBot

def main():

    bot = SimpleBot(10000)

    with open('DAL_data_1.csv', newline='') as f:
        reader = csv.reader(f)
        delta_data = list(reader)

    

    with open('CLF_data_1.csv', newline='') as z:
        reader = csv.reader(z)
        CLF_data = list(reader)
    

    for x in range(1,len(CLF_data)):
        bot.next_day(CLF_data[x],delta_data[x])

    print(bot.cur_val())
    y = bot.val_history
    x = [x for x in range(len(y))]
    plt.plot(x,y)
    plt.show()

if __name__ == "__main__":
    main()