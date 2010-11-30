
#y=ax+b, for sys
#   y=sys_real
#   x=sys_actual
#j=ek+g

class Ls():
    def __init__(self):
        self.x=0
        self.y=0
        self.sys_list=[]
        self.dias_list=[]
        self.a_sys=1
        self.b_sys=0
        self.a_dias=1
        self.b_dias=0

        
    def add(self,sys_real,sys_actual,dias_real,dias_actual):
        self.sys_list.append((sys_real,sys_actual))
        self.dias_list.append((dias_real,dias_actual))

    def get_coeffecients(self):
        #formula in the form y=ax+b
        self.a_sys,self.b_sys=self.compute(self.sys_list)
        self.a_dias,self.b_dias=self.compute(self.dias_list)
        print "For Systolic: Y=%sX+(%s)"%(self.a_sys,self.b_sys)
        print "For Diastolic: Y=%sX+(%s)"%(self.a_dias,self.b_dias)
        return self.a_sys,self.b_sys,self.a_dias,self.b_dias
        self.sys_list=[]
        self.dias_list=[]

    def compute(self,data):
        count=len(data)
        sum_x,sum_y,sum_x2,sum_xy=0,0,0,0
        for i in range(count):
            sum_x=sum_x+data[i][1]
            sum_y=sum_y+data[i][0]
            sum_x2=sum_x2+data[i][1]**2
            sum_xy=sum_xy+(data[i][1]*data[i][0])
        print sum_x,sum_y,sum_x2,sum_xy
        coef_b_num= (1.0*sum_y*sum_x2)-(1.0*sum_x*sum_xy)
        coef_b_denum= (count*sum_x2)-sum_x**2
        coef_b=1.0*coef_b_num/coef_b_denum
        print coef_b
        coef_a_num=(count*sum_xy)-(sum_x*sum_y)
        coef_a_denum=(count*sum_x2)-(sum_x)**2
        coef_a=1.0*coef_a_num/coef_a_denum
        print coef_a
        return coef_a,coef_b
    
if __name__ == "__main__":
    a=Ls()
    a.add(120,114,80,78)
    a.add(115,113,78,76)
    a.add(117,109,77,74)
    a.get_coeffecients()

