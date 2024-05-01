class LimitesMapaVirtual:
    #window= Tk()
    def __init__(self,w_window,h_window):
        self.w_window= int(w_window)
        self.h_window= int(h_window)
        # Considero como cerca del extremo en un 10% de cercanías
        porcentajeExtrmos= 0.1
        self.w_window_extremo= int(int(self.w_window)*porcentajeExtrmos)
        self.h_window_extremo= int(int(self.h_window)*porcentajeExtrmos)

    def getAncho(self):
        return self.w_window

    def getAlto(self):
        return self.h_window

    def estaDentroDelMapaVirtual(self,punto):
        punto= [int(punto[0]), int(punto[1])]
        res= False
        aux= 0
        if((punto[0]>=0) and (punto[0]<=self.w_window)):
            aux= aux +1
        if((punto[1]>=0) and (punto[1]<=self.h_window)):
            aux= aux +1
        if(aux == 2):
            res= True
        return res

    def estaEnLosExtremosDelMapa(self,punto):
        punto= [int(punto[0]), int(punto[1])]
        res= False
        res_estaEnWextremo= self.estaEnWextremo(punto)
        res_estaEnHextremo= self.estaEnHextremo(punto)
        if(res_estaEnWextremo and res_estaEnHextremo):
            res= True
        return res

    def estaEnWextremo(self,punto):
        punto= [int(punto[0]), int(punto[1])]
        res= False
        if(self.estaDentroDelMapaVirtual(punto)):
            if((punto[0]<= self.w_window_extremo) or (punto[0]>=(self.w_window - self.w_window_extremo))):
                res= True
        return res

    def estaEnHextremo(self,punto):
        punto= [int(punto[0]), int(punto[1])]
        res= False
        if(self.estaDentroDelMapaVirtual(punto)):
            if((punto[0]<= self.h_window_extremo) or (punto[0]>=(self.h_window - self.h_window_extremo))):
                res= True
        return res

    def estaEnElCentroDelMapa(self,punto):
        punto= [int(punto[0]), int(punto[1])]
        aux= 0
        res= False
        if((punto[0]>=self.w_window_extremo) and (punto[0]<=(self.w_window-self.w_window_extremo))):
            aux= aux +1
        if((punto[1]>=self.h_window_extremo) and (punto[1]<=(self.h_window-self.h_window_extremo))):
            aux= aux +1
        if(aux == 2):
            res= True
        return res
    
    def areNewEnElExtremoROI(self,personas_new_array):
        areNewEnElExtremoROI_array= []
        for personasXY in personas_new_array:
            res= False
            if(self.estaEnLosExtremosDelMapa(personasXY)):
                res= True
            areNewEnElExtremoROI_array.append(res)
        return areNewEnElExtremoROI_array

    ## Para Listas de Puntos de Personas:
    def areNewEnElCentroROI(self,personas_new_array):
        areNewEnElCentroROI_array= []
        for personasXY in personas_new_array:
            res= False
            if(self.estaEnElCentroDelMapa(personasXY)):
                res= True
            areNewEnElCentroROI_array.append(res)
        return areNewEnElCentroROI_array

if __name__ == '__main__':

    w=247
    h=247
    lmv= LimitesMapaVirtual(w,h)

    p_follow=  ['83', '76']
    obst1= ['246', '86']
    obst2= ['4', '160']
    obst3= ['199', '125']

    res_p__follow_estaDentroDelMapaVirtual= lmv.estaDentroDelMapaVirtual(p_follow)
    print("res_p_follow_estaDentroDelMapaVirtual: ",res_p__follow_estaDentroDelMapaVirtual)
    res_obst1= lmv.estaDentroDelMapaVirtual(obst1)
    print("res_obst1_estaDentroDelMapaVirtual: ",res_obst1)
    res_obst2= lmv.estaDentroDelMapaVirtual(obst2)
    print("res_obst2_estaDentroDelMapaVirtual: ",res_obst2)
    res_obst3= lmv.estaDentroDelMapaVirtual(obst3)
    print("res_obst3_estaDentroDelMapaVirtual: ",res_obst3)

    print("----------------------")

    res_p_follow_estaEnLosExtremosDelMapa= lmv.estaEnLosExtremosDelMapa(p_follow)
    print("res_p_follow_estaEnLosExtremosDelMapa: ",res_p_follow_estaEnLosExtremosDelMapa)
    res_obst1_estaEnLosExtremosDelMapa= lmv.estaEnLosExtremosDelMapa(obst1)
    print("res_obst1_estaEnLosExtremosDelMapa: ",res_obst1_estaEnLosExtremosDelMapa)
    res_obst2_estaEnLosExtremosDelMapa= lmv.estaEnLosExtremosDelMapa(obst2)
    print("res_obst2_estaEnLosExtremosDelMapa: ",res_obst2_estaEnLosExtremosDelMapa)
    res_obst3_estaEnLosExtremosDelMapa= lmv.estaEnLosExtremosDelMapa(obst3)
    print("res_obst3_estaEnLosExtremosDelMapa: ",res_obst3_estaEnLosExtremosDelMapa)

    print("----------------------")

    res_p__follow_estaEnElCentroDelMapa=lmv.estaEnElCentroDelMapa(p_follow)
    print("res_p__follow_estaEnElCentroDelMapa: ",res_p__follow_estaEnElCentroDelMapa)
    res_obst1_estaEnLosExtremosDelMapa= lmv.estaEnElCentroDelMapa(obst1)
    print("res_res_obst1_estaEnElCentroDelMapa: ",res_obst1_estaEnLosExtremosDelMapa)
    res_obst2_estaEnLosExtremosDelMapa= lmv.estaEnElCentroDelMapa(obst2)
    print("res_obst2_estaEnLosExtremosDelMapa: ",res_obst2_estaEnLosExtremosDelMapa)
    res_obst3_estaEnLosExtremosDelMapa= lmv.estaEnElCentroDelMapa(obst3)
    print("res_obst3_estaEnLosExtremosDelMapa: ",res_obst3_estaEnLosExtremosDelMapa)