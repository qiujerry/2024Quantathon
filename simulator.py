import csv
from simple_bot import SimpleBot

def main():
    print("Hello World")

    bot = SimpleBot(10000)

    with open('DAL_data_1.csv', newline='') as f:
        reader = csv.reader(f)
        delta_data = list(reader)

    print(len(delta_data))
    

    with open('CLF_data_1.csv', newline='') as z:
        reader = csv.reader(z)
        CLF_data = list(reader)
    
    print(len(CLF_data))

    for x in range(1,len(CLF_data)):
        bot.next_day(CLF_data[x],delta_data[x])

    print(bot.cur_val())


if __name__ == "__main__":
    main()