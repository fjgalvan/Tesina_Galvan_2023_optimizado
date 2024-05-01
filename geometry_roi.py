## (0,0)      A-------B   
##           |         |     
##          |    ROI    |     
##         |             |
##        D---------------C
import math
import numpy as np

class Geometry_Roi:
    #C= (Cx,Cy) son las coordenadas de la persona dentro de la recta
    def __init__(self, puntos): #puntos es array de 4 arrays de R2
        self.puntos= puntos
        self.A = puntos[0]
        self.B = puntos[1]
        self.D = puntos[2]
        self.C = puntos[3]
        '''print("A: ", self.A)
        print("B: ", self.B)
        print("C: ", self.C)
        print("D: ", self.D)
        '''

    def isHorizontal_AB(self):
        #todas las rectas horizontales representan a una función. Y= X0 (cte)
        res= False
        if(self.A[1] == self.B[1]):
            res= True
        return res
    
    def isHorizontal_DC(self):
        #todas las rectas horizontales representan a una función. Y= X0 (cte)
        res= False
        if(self.D[1] == self.C[1]):
            res= True
        return res

    def isVertical_AD(self):
        #una recta vertical no puede representar una función.
        res= False
        if(self.A[0] == self.D[0]):
            res= True
        return res
    
    def isVertical_BC(self):
        #una recta vertical no puede representar una función.
        res= False
        if(self.B[0] == self.C[0]):
            res= True
        return res

    def getPendiente_AB(self):
        m=0.0
        if(self.isHorizontal_AB()):
            m=0.0
        else:
            m= float((self.B[1]-self.A[1])/(self.B[0]-self.A[0]))
        return m

    def getPendiente_DC(self):
        m=0.0
        if(self.isHorizontal_DC()):
            m=0.0
        else:
            m= float((self.C[1]-self.D[1])/(self.C[0]-self.D[0]))
        return m
    
    def getPendiente_AD(self):
        m=0.0
        if(self.isVertical_AD()):
            m=None
        else:
            m= float((self.A[1]-self.D[1])/(self.A[0]-self.D[0]))
        return m
    
    def getPendiente_BC(self):
        m=0.0
        if(self.isVertical_BC()):
            m=None
        else:
            m= float((self.C[1]-self.B[1])/(self.C[0]-self.B[0]))
        return m

    def get_ordenadaOrigen_AB(self):
        b= None
        if(self.isHorizontal_AB() == True):
            b= self.A[1]
        else:
            b= self.A[1] - self.getPendiente_AB()*self.A[0]
        return b
    
    def get_ordenadaOrigen_DC(self):
        b= None
        if(self.isHorizontal_DC() == True):
            b= self.D[1]
        else:
            b= self.D[1] - self.getPendiente_DC()*self.D[0]
        return b
    
    def get_ordenadaOrigen_AD(self):
        b= None
        if(self.isVertical_AD() == True):
            b= None
        else:
            b= self.A[1] - self.getPendiente_AD()*self.A[0]
        return b
    
    def get_ordenadaOrigen_BC(self):
        b= None
        if(self.isVertical_BC() == True):
            b= None
        else:
            b= self.B[1] - self.getPendiente_BC()*self.B[0]
        return b

    def is_in_a1(self,x,y):
        res= False
        m_AD= self.getPendiente_AD()
        #print("m_AD: ",m_AD)
        b_AD= self.get_ordenadaOrigen_AD()
        #print("b_AD: ",b_AD)

        m_DC= self.getPendiente_DC()
        #print("m_DC: ",m_DC)
        b_DC= self.get_ordenadaOrigen_DC()
        #print("b_DC: ",b_DC)

        if((x >= int(self.puntos[2][0])) and (x <= int(self.puntos[0][0]))):
            valor_2= m_AD*x + b_AD
            valor_1= m_DC*x + b_DC
            if valor_2 <= y <= valor_1:
                #print("El punto ({},{}) se halla en el area A1 de las rectas.".format(x,y))
                res= True
        '''     else: 
                print("El punto ({},{}) no se halla en el area A1 de las tres rectas.".format(x,y))
        else:
            print("El punto ({},{}) no se halla en el area A1 de las tres rectas.".format(x,y))
        ''' 
        return res

    def is_in_a2(self,x,y):
        res= False
        m_AB= self.getPendiente_AB()
        #print("m_AB: ",m_AB)
        b_AB= self.get_ordenadaOrigen_AB()
        #print("b_AB: ",b_AB)

        m_DC= self.getPendiente_DC()
        #print("m_DC: ",m_DC)
        b_DC= self.get_ordenadaOrigen_DC()
        #print("b_DC: ",b_DC)

        if((x >= int(self.puntos[0][0])) and (x <= int(self.puntos[1][0]))):
            valor_2= m_AB*x + b_AB
            valor_1= m_DC*x + b_DC
            if valor_2 <= y <= valor_1:
                res= True
                #print("El punto ({},{}) se halla en el area A2 de las rectas.".format(x,y))
        '''     else: 
                print("El punto ({},{}) no se halla en el area A2 de las tres rectas.".format(x,y))
        else:
            print("El punto ({},{}) no se halla en el area A2 de las tres rectas.".format(x,y))
        ''' 
        return res
    
    def is_in_a3(self,x,y):
        res= False
        m_BC= self.getPendiente_BC()
        #print("m_BC: ",m_BC)
        b_BC= self.get_ordenadaOrigen_BC()
        #print("b_BC: ",b_BC)

        m_DC= self.getPendiente_DC()
        #print("m_DC: ",m_DC)
        b_DC= self.get_ordenadaOrigen_DC()
        #print("b_DC: ",b_DC)

        if((x >= int(self.puntos[1][0])) and (x <= int(self.puntos[3][0]))):
            valor_2= m_BC*x + b_BC
            valor_1= m_DC*x + b_DC
            if valor_2 <= y <= valor_1:
                res= True
        '''        print("El punto ({},{}) se halla en el area A3 de las rectas.".format(x,y))
            else: 
                print("El punto ({},{}) no se halla en el area A3 de las tres rectas.".format(x,y))
        else:
            print("El punto ({},{}) no se halla en el area A3 de las tres rectas.".format(x,y))
        ''' 
        return res

    def is_in_Area_ROI(self,x,y):
        #print("(x,y)= (",x,",",y,")")
        res= False
        if( (self.is_in_a1(x,y)) or (self.is_in_a2(x,y)) or (self.is_in_a3(x,y)) ):
            res= True
        
        return res


if __name__ == '__main__':
    puntos= [[190,300],[280,300],[60,635],[415,635]]
    #puntos= [[190,300],[280,300],[190,635],[415,635]]

    geo_roi= Geometry_Roi(puntos)

    x= 392
    y= 300
    res= geo_roi.is_in_Area_ROI(x,y)
    if(res):
        print("El punto ({},{}) se halla en el area Area_ROI.".format(x,y))
    else: 
        print("El punto ({},{}) no se halla en el area Area_ROI.".format(x,y))