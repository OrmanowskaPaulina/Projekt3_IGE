from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty #polaczenie kv z aplikacja
from kivy.garden.mapview import MapMarker, MarkerMapLayer
import funkcja as f
import matplotlib
matplotlib.use("module://kivy.garden.matplotlib.backend_kivy")
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg # lub FigureCanvas
import matplotlib.pyplot as plt



class AddLocationForm(BoxLayout):
    my_map = ObjectProperty()
    plot = ObjectProperty()
    stat = ObjectProperty()


    def __init__(self, **kwargs):
        super(AddLocationForm, self).__init__(**kwargs)
        self.my_map.map_source = "osm-fr"
        self.fig = plt.figure()
            
    def analizuj_plik(self):
        filename = 'krk1.gpx'
        f.wczytaj_dane(filename)
        lat, lon = f.wczytaj_dane(filename)
        self.draw_route(lat, lon)

        
    def statystyka(self): #statystyki
        filename = 'krk1.gpx'
        f.wczytaj_dane(filename)
        el, dates, DH, suma_odl, odl, czas_ost, czas, v, staty = f.statystyki(filename)
        self.stat.text = "{}".format(staty) #wyswietlanie w aplikacji
        
    def draw_route(self, lat, lon): #rysowanie trasy
        data_lay = MarkerMapLayer()
        self.my_map.add_layer(data_lay) # my_map jest obiektem klasy MapView
        for point in zip(lat, lon):
            self.draw_marker(*point, layer = data_lay)
        
        
    def draw_marker(self, lat, lon, layer=None, markerSource='dot.png'):
        if lat != None and lon != None:
            marker = MapMarker(lat = lat, lon = lon, source=markerSource)
            self.my_map.add_marker(marker, layer=layer)
            
    def rysuj_wykres(self):
        filename = 'krk1.gpx'
        f.wczytaj_dane(filename)
        el, dates, DH, suma_odl, odl, czas_ost, czas, v, staty = f.statystyki(filename)
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.scatter(czas, odl)
        self.ax1.set_xlabel('czas')
        self.ax1.set_ylabel('odl')
        self.ax1.set_title('Odleglosc do czasu')
        self.cnv = FigureCanvasKivyAgg(self.fig)
        self.plot.add_widget(self.cnv)
        self.cnv.draw()
        
        
class MapViewApp(App):
    def build(self):
            return AddLocationForm()
    #pass

if __name__ == '__main__':
    MapViewApp().run()