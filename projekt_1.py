# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 20:13:28 2019

@author: Ewa
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:11:02 2019

@author: Ewa
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QColorDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class AppWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title='matplotlib przyklad'
        self.initInterface()
        self.initWidgets()
        
    def initInterface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100,100,500,400,)
        self.show()
        
    def initWidgets(self):
        btn=QPushButton("Wyznacz punkt przecięcia",self)                        #zdefiniowanie przycisków
        btnColor=QPushButton("Zmień kolor wykresu",self)
        btnZapisz=QPushButton("Zapisz współrzędne",self)
        btnClear=QPushButton("Wyczyć dane",self)
        btnKoniec=QPushButton("Zakończ",self)
        
        xaLabel=QLabel("Xa",self)                                               # zdefiniowanie pól edycji oraz pól tytułowych
        yaLabel=QLabel("Ya",self)
        self.xaEdit=QLineEdit()
        self.yaEdit=QLineEdit()
        xbLabel=QLabel("Xb",self)
        ybLabel=QLabel("Yb",self)
        self.xbEdit=QLineEdit()
        self.ybEdit=QLineEdit()
        xcLabel=QLabel("Xc",self)
        ycLabel=QLabel("Yc",self)
        self.xcEdit=QLineEdit()
        self.ycEdit=QLineEdit()
        xdLabel=QLabel("Xd",self)
        ydLabel=QLabel("Yd",self)
        self.xdEdit=QLineEdit()
        self.ydEdit=QLineEdit()
        xpLabel=QLabel("Xp:",self)
        ypLabel=QLabel("Yp",self)
        self.xp=QLineEdit()
        self.yp=QLineEdit()
        
        self.polozenie=QLineEdit()
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
        
        grid=QGridLayout()                                                      #rozmieszczenie widgetów
        grid.addWidget(xaLabel, 1,0)
        grid.addWidget(self.xaEdit ,1,1)
        grid.addWidget(yaLabel,2,0)
        grid.addWidget(self.yaEdit,2,1)
        
        grid.addWidget(xbLabel, 3, 0)
        grid.addWidget(self.xbEdit ,3,1)
        grid.addWidget(ybLabel,4,0)
        grid.addWidget(self.ybEdit,4,1)
        
        grid.addWidget(xcLabel, 5, 0)
        grid.addWidget(self.xcEdit ,5,1)
        grid.addWidget(ycLabel,6,0)
        grid.addWidget(self.ycEdit,6,1)
        
        grid.addWidget(xdLabel, 7, 0)
        grid.addWidget(self.xdEdit ,7,1)
        grid.addWidget(ydLabel,8,0)
        grid.addWidget(self.ydEdit,8,1)
        
        grid.addWidget(btn,9,0)
        
        grid.addWidget(xpLabel, 10, 0)
        grid.addWidget(self.xp ,10,1)
        grid.addWidget(ypLabel,11,0)
        grid.addWidget(self.yp,11,1)
        
        grid.addWidget(self.polozenie,12,0)
        
        grid.addWidget(btnColor,13,0)
        
        grid.addWidget(btnZapisz,14,0)
        
        grid.addWidget(btnClear,15,0)
        
        grid.addWidget(btnKoniec,16,0)
        
        grid.addWidget(self.canvas,1,2,-1,-1)
        
        self.setLayout(grid)
        
        btn.clicked.connect(self.liczWsp)                                       #powiązanie przycisków z funkcjami
        btnColor.clicked.connect(self.zmienKolor)
        btnZapisz.clicked.connect(self.zapisz)
        btnClear.clicked.connect(self.clear)
        btnKoniec.clicked.connect(self.koniec)
        
        
    def liczWsp(self):                                                          #funkcja wyznaczająca wspórzędne pp oraz okrelająca jego położenie
        self.rysuj()
        xa=self.sprawdzWartosc(self.xaEdit)
        ya=self.sprawdzWartosc(self.yaEdit)
        xb=self.sprawdzWartosc(self.xbEdit)
        yb=self.sprawdzWartosc(self.ybEdit)
        xc=self.sprawdzWartosc(self.xcEdit)
        yc=self.sprawdzWartosc(self.ycEdit)
        xd=self.sprawdzWartosc(self.xdEdit)
        yd=self.sprawdzWartosc(self.ydEdit)
        lista=[xa,ya,xb,yb,xc,yc,xd,yd]
        if None not in lista:
            dXac=xc-xa
            dYac=yc-ya
            dXcd=xd-xc
            dYcd=yd-yc
            dXab=xb-xa
            dYab=yb-ya
            
            if (dXab*dYcd-dYab*dXcd)==0:
                self.polozenie.setText('Odcinki są równoległe-nie ma rozwiązania lub jest ich nieskończenie wiele')
            else:
                t1=(dXac*dYcd-dYac*dXcd)/(dXab*dYcd-dYab*dXcd)
                t2=(dXac*dYab-dYac*dXab)/(dXab*dYcd-dYab*dXcd)
                xp=xa+t1*dXab
                yp=ya+t1*dYab
                xpz='%.3f' % xp
                ypz='%.3f' % yp
                self.xp.setText(str(xpz))
                self.yp.setText(str(ypz))
                if 0<=t1<=1 and 0<=t2<=1:
                    self.polozenie.setText('Punkt ten leży na przecięciu obu odcinków') 
                elif ((t1<0 or t1>0) and 0<=t2<=1) or ((t2<0 or t2>0) and 0<=t1<=1):
                    self.polozenie.setText('Punkt ten leży na przecięciu jednego odcinka i przedłużeniu drugiego') 
                else:
                    self.polozenie.setText('Punkt ten leży na przecięciu przedłużeń obu odcinków') 
        
    def rysuj(self, col='red'):                                                 #funkcja rysująca wykres
        xa=self.sprawdzWartosc(self.xaEdit)
        ya=self.sprawdzWartosc(self.yaEdit)
        xb=self.sprawdzWartosc(self.xbEdit)
        yb=self.sprawdzWartosc(self.ybEdit)
        xc=self.sprawdzWartosc(self.xcEdit)
        yc=self.sprawdzWartosc(self.ycEdit)
        xd=self.sprawdzWartosc(self.xdEdit)
        yd=self.sprawdzWartosc(self.ydEdit)
        dXac=xc-xa
        dYac=yc-ya
        dXcd=xd-xc
        dYcd=yd-yc
        dXab=xb-xa
        dYab=yb-ya
        lista=[xa,ya,xb,yb,xc,yc,xd,yd]
        if None not in lista:
            self.figure.clear()
            AX=self.figure.add_subplot(111)
            if (dXab*dYcd-dYab*dXcd)==0:
                Xw=[xa,xb]
                Yw=[ya,yb]
                AX.plot(Xw,Yw,color=col,marker='o')
            else:
                t1=(dXac*dYcd-dYac*dXcd)/(dXab*dYcd-dYab*dXcd)
                global xp
                xp=xa+t1*dXab
                global yp
                yp=ya+t1*dYab
                Xw1=[xa,yb]
                Yw1=[ya,yb]
                Xw2=[xc,xd]
                Yw2=[yc,yd]
                AX.plot(Xw1,Yw1, color=col)
                AX.plot(Xw2,Yw2, color=col)
                AX.scatter(xa,ya,  color=col, marker='o')
                AX.scatter(xb,yb,  color=col, marker='o')
                AX.scatter(xc,yc,  color=col, marker='o')
                AX.scatter(xd,yd,  color=col, marker='o')
                AX.scatter(xp,yp,  color=col,marker='p')
            self.canvas.draw()
            
    def sprawdzWartosc(self, element):                                          #funkcja sprwdzająca czy format podanych wpólrzędnych jest odpowiedni
        if element.text().lstrip('-').replace('.','',1). isdigit():
            return float(element.text())
        else:
            element.setFocus()              #element staje się widoczny
            return None                     #nic nie zwraca 
        
    def zmienKolor(self):                                                       #funkcja umożliwiająca zmienę koloru wykresu
        color=QColorDialog.getColor()
        if color.isValid():                    
            self.rysuj(col=color.name())
            
    def zapisz(self):                                                           #funkcja umożliwiająca zapis współrzędnych pp do pliku TXT
        plik=open('punkt_przecięcia.txt','w')
        plik.write("Współrzędne punktu przecięcia [m] ")
        plik.write('\nX ')
        plik.write('{0:.3f}'.format(xp))
        plik.write("| Y ")
        plik.write('{0:.3f}'.format(yp))
        plik.close()
        
    def clear(self):                                                            #funkcja umożliwiająca wyczyszczenie danych
        self.xaEdit.clear()
        self.yaEdit.clear()
        self.xbEdit.clear()
        self.ybEdit.clear()
        self.xcEdit.clear()
        self.ycEdit.clear()
        self.xdEdit.clear()
        self.ydEdit.clear()
        self.xpEdit.clear()
        self.ypEdit.clear()
        self.polozenie.clear()
        
    def koniec(self):                                                           #funkcja zamykająca program
        self.close()
        
            
def main():
    app=QApplication(sys.argv)
    window=AppWindow()
    app.exec_()
    
if __name__=='__main__':
    main()