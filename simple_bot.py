class SimpleBot:
    def __init__(self,cash):
        self.cash = cash
        self.days = 0
        self.d_stock=0
        self.oil=0
        self.d_history = []
        self.c_history = []
    
    def next_day(self, coil,dstock):
        if self.days == 0:
            #first day 75% delta, 25% crude oil
            self.d_stock = (self.cash*.75) / float(dstock[1])
            self.oil = (self.cash*.25) / float(coil[1])
            self.cash=0
        
            
        
        self.days = self.days+1
        # if(self.days%365==0):
        #     self.cash = self.cash + (self.cash*.0527)
        
        self.d_history.append(dstock)
        self.c_history.append(coil)

    def cur_val(self):
        total = self.cash + self.d_stock*float(self.d_history[-1][4]) + self.oil*float(self.c_history[-1][4])
        return total