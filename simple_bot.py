class SimpleBot:
    def __init__(self,cash):
        self.cash = cash
        self.days = 0
        self.d_stock=0
        self.oil=0
        self.d_short = []
        self.c_short = []
        #Date,Open,High,Low,Close,Adj Close,Volume
        self.d_history = []
        self.c_history = []
        #trading sentiment range -10 - 10
        self.c_sent = 0
        self.d_sent = 0
        #trading strategy instructions
        self.instrucs = []
        self.val_history = []
    
    def next_day(self, coil,dstock):
        if self.days == 0:
            #first day 75% delta, 25% crude oil
            self.d_stock = (self.cash*.75) / float(dstock[1])
            self.oil = (self.cash*.25) / float(coil[1])
            self.cash=0
        else:
            self.execute(coil,dstock)
            
        
        self.days = self.days+1
        # if(self.days%365==0):
        #     self.cash = self.cash + (self.cash*.0527)
        
        self.d_history.append(dstock)
        self.c_history.append(coil)
        self.det_sent()
        self.val_history.append(self.cur_val())


    def cur_val(self):
        total = self.cash + self.d_stock*float(self.d_history[-1][4]) + self.oil*float(self.c_history[-1][4])
        return total

    def csent(self):
        ocd = float(self.c_history[-1][1]) - float(self.c_history[-1][4])
        p_change = ocd / float(self.c_history[-1][1])

        if p_change < 0.0:
            if p_change > -0.0055:
                self.c_sent = -1
            elif p_change > -0.01:
                self.c_sent = -2
            elif p_change > -0.02:
                self.c_sent = -3
            elif p_change > -0.03:
                self.c_sent = -3
            elif p_change > -0.04:
                self.c_sent = -5
            elif p_change > -0.05:
                self.c_sent = -5
            else:
                self.c_sent = -7
        elif p_change>0:
            if p_change < 0.005:
                self.c_sent = 1
            elif p_change < 0.01:
                self.c_sent = 2
            elif p_change < 0.02:
                self.c_sent = 3
            elif p_change < 0.03:
                self.c_sent = 3
            elif p_change < 0.04:
                self.c_sent = 5
            elif p_change < 0.05:
                self.c_sent = 5
            else:
                self.c_sent = 7
    

    def dsent(self):
        ocd = float(self.d_history[-1][1]) - float(self.d_history[-1][4])
        p_change = ocd / float(self.d_history[-1][1])

        if p_change < 0.0:
            if p_change > -0.005:
                self.d_sent = -1
            elif p_change > -0.01:
                self.d_sent = -2
            elif p_change > -0.02:
                self.d_sent = -3
            elif p_change > -0.03:
                self.d_sent = -3
            elif p_change > -0.04:
                self.d_sent = -5
            elif p_change > -0.05:
                self.d_sent = -5
            else:
                self.d_sent = -7
        elif p_change>0:
            if p_change < 0.005:
                self.d_sent = 1
            elif p_change < 0.01:
                self.d_sent = 2
            elif p_change < 0.02:
                self.d_sent = 3
            elif p_change < 0.03:
                self.d_sent = 3
            elif p_change < 0.04:
                self.d_sent = 5
            elif p_change < 0.05:
                self.d_sent = 5
            else:
                self.d_sent = 7

    def det_sent(self):
        self.csent()
        self.dsent()
        self.det_strat()
        # print("sent")
        # print(self.c_sent)
        # print(self.d_sent)

    def det_strat(self):
        if self.d_sent > 0 and self.c_sent>0:
            if self.cash >0:
                if self.d_sent > self.c_sent:
                    self.instrucs.append(["B","D",100,"O"])
                else:
                    self.instrucs.append(["B","C",100,"O"])

        elif self.d_sent > 0:
            sent_diff = (abs(self.d_sent - self.c_sent)) %10
            self.instrucs.append(["S","C",sent_diff*10,"H"])
            self.instrucs.append(["B","D",100,"L"])
        elif self.c_sent > 0:
            sent_diff = (abs(self.c_sent - self.d_sent)) %10
            self.instrucs.append(["S","D",sent_diff*10,"H"])
            self.instrucs.append(["B","C",100,"L"])
        else:
            self.instrucs.append(["S","D",abs(self.d_sent)*10,"H"])
            self.instrucs.append(["S","C",abs(self.c_sent)*10,"H"])
            
    def execute(self, coil,dstock):
        inst = {
            "D" : {"O":float(dstock[1]),"H":float(dstock[2]),"L":float(dstock[3]),"C":float(dstock[4])},
            "C" : {"O":float(coil[1]),"H":float(coil[2]),"L":float(coil[3]),"C":float(coil[4])}
        }
        while(len(self.instrucs)>0):
            instr = self.instrucs.pop(0)

            if(instr[0]=="B"):
                spend = self.cash * (instr[2]/100.0)
                self.cash = self.cash - spend

                if(instr[1]=="D"):
                    self.d_stock = self.d_stock + (float(spend)/inst[instr[1]][instr[3]])
                else:
                    self.oil = self.oil+ (float(spend)/inst[instr[1]][instr[3]])
            else:
                num_sell = (instr[2]/100.0)
                
                if(instr[1]=="D"):
                    num_sell = self.d_stock * num_sell
                    
                    self.cash = self.cash + (num_sell*inst[instr[1]][instr[3]])
                    self.d_stock = self.d_stock - num_sell
                else:
                    num_sell = self.oil * num_sell
                    self.cash = self.cash + (num_sell*inst[instr[1]][instr[3]])
                    self.oil = self.oil - num_sell
        #print(self.cur_val())