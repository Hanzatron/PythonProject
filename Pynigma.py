class pynigma(object):
    """pynigma codering."""
    def __init__(self, key):
        self.key = key
        self.raster_ori = [["A","B","C","D","E","F","G","H","I"],["J","K","L","M","N","O","P","Q","R"],["S","T","U","V","W","X","Y","Z","a"],["b","c","d","e","f","g","h","i","j"],["k","l","m","n","o","p","q","r","s"],["t","u","v","w","x","y","z","0","1"],["2","3","4","5","6","7","8","9",","],[".",";","%","€","_","#"," ","?","-"],["+","*","|","&","@",">","<","é","/"]]
        #self.raster_code = [["A","B","C","D","E","F","G","H","I"],["J","K","L","M","N","O","P","Q","R"],["S","T","U","V","W","X","Y","Z","a"],["b","c","d","e","f","g","h","i","j"],["k","l","m","n","o","p","q","r","s"],["t","u","v","w","x","y","z","0","1"],["2","3","4","5","6","7","8","9",","],[".",";","%","€","_","#"," ","?","-"],["+","*","|","&","@",">","<","é","/"]]
        self.raster_code = self.raster_ori.copy()
    def trace(self,raster,karakter):
        coor=[]
        for lijn in range(len(raster)):
            if karakter in raster[lijn]:
                coor=[lijn,raster[lijn].index(karakter)]
        return coor

    def lees_raster(self,raster, coor):
        return raster[coor[0]][coor[1]]

    def codeer(self, tekst):
        tekst_code = ""
        tekst_coor = []
        for karakter in tekst:
            tekst_coor.append(self.trace(self.raster_ori,karakter))
        for coor in tekst_coor:
            tekst_code = tekst_code + self.lees_raster(self.raster_code,coor)
        return tekst_code

    def decodeer(self, tekst):
        tekst_code = ""
        tekst_coor = []
        for karakter in tekst:
            tekst_coor.append(self.trace(self.raster_code,karakter))
        for coor in tekst_coor:
            tekst_code = tekst_code + self.lees_raster(self.raster_ori,coor)
        return tekst_code

    def shift_x_l(self,n):
        for lijn in range(len(self.raster_code)):
            self.raster_code[lijn] = self.raster_code[lijn][n:] + self.raster_code[lijn][0:n]
    def shift_x_r(self,n):
        for lijn in range(len(self.raster_code)):
            self.raster_code[lijn] = self.raster_code[lijn][-n:] + self.raster_code[lijn][:-n]

    def shift_y_b(self,n):
        self.raster_code = self.raster_code[n:] + self.raster_code[0:n]

    def shift_y_o(self,n):
        self.raster_code = [self.raster_code[-n:]] + self.raster_code[:-n]

    def print_raster(self,raster):
        for lijn in raster:
            print(lijn)

def main():
    Gen1 = pynigma(123)
    print("###GECODEERDE TEKST###")
    Gen1.shift_y_b(1)
    Gen1.shift_x_l(2)
    Gen1.shift_y_b(1)
    Gen1.shift_x_r(3)
    Gen1.shift_y_b(2)
    print(Gen1.codeer("ABC"))
    print("###GEDECODEERDE TEKST###")
    print(Gen1.decodeer(Gen1.codeer("ABC")))
if __name__ == '__main__':
    main()
