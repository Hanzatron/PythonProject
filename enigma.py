#!/usr/bin/python3
import copy

class pynigma(object):
    """pynigma codering."""
    def __init__(self):
        self.raster_code = [["A","B","C","D","E","F","G","H","I"],["J","K","L","M","N","O","P","Q","R"],["S","T","U","V","W","X","Y","Z","a"],["b","c","d","e","f","g","h","i","j"],["k","l","m","n","o","p","q","r","s"],["t","u","v","w","x","y","z","0","1"],["2","3","4","5","6","7","8","9",","],[".",";","%","€","_","#"," ","?","-"],["+","*","|","&","@",">","<","é","/"]]

    def shift_x_l(self,n,list):
        for lijn in self.raster_code:
            print(lijn)
        print("")
        for lijn in list:
            self.raster_code[lijn] = self.raster_code[n:] + self.raster_code[0:n]

        for lijn in self.raster_code:
            print(lijn)
def main():
    Gen1 = pynigma()
    Gen1.shift_x_l(2,[0,8])

if __name__ == '__main__':
    main()
