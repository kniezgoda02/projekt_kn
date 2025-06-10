from tkinter import *
import tkintermapview

hotels: list = []


class Hotel:
    def __init__(self, name, location, stars):
        self.name = name
        self.location = location
        self.stars = stars
        self.coordinates = self.get_coordinates()
        self.marker = self.create_marker()

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        adres_url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
        response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(',', '.')),
            float(response_html.select('.longitude')[1].text.replace(',', '.')),
        ]

    def create_marker(self):
        return map_widget.set_marker(
            self.coordinates[0],
            self.coordinates[1],
            text=f"{self.name}"
        )


def add_hotel() -> None:
    name = entry_name.get()
    location = entry_location.get()
    stars = entry_stars.get()

    hotel = Hotel(name=name, location=location, stars=stars)
    hotels.append(hotel)

    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_stars.delete(0, END)

    entry_name.focus()
    show_hotels()


def show_hotels():
    listbox_lista_obiektow.delete(0, END)
    for idx, hotel in enumerate(hotels):
        listbox_lista_obiektow.insert(idx, f'{idx + 1}. {hotel.name}')


def remove_hotel():
    i = listbox_lista_obiektow.index(ACTIVE)
    if hotels[i].marker:
        hotels[i].marker.delete()
    hotels.pop(i)
    show_hotels()


def edit_hotel():
    i = listbox_lista_obiektow.index(ACTIVE)
    entry_name.insert(0, hotels[i].name)
    entry_location.insert(0, hotels[i].location)
    entry_stars.insert(0, hotels[i].stars)

    button_dodaj_obiekt.configure(text='Zapisz', command=lambda: update_hotel(i))


def update_hotel(i):
    name = entry_name.get()
    location = entry_location.get()
    stars = entry_stars.get()

    # Usuń stary marker
    if hotels[i].marker:
        hotels[i].marker.delete()

    # Zaktualizuj dane hotelu
    hotels[i].name = name
    hotels[i].location = location
    hotels[i].stars = stars
    hotels[i].coordinates = hotels[i].get_coordinates()
    hotels[i].marker = hotels[i].create_marker()

    show_hotels()
    button_dodaj_obiekt.configure(text='Dodaj', command=add_hotel)

    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_stars.delete(0, END)
    entry_name.focus()


def show_hotel_detail():
    i = listbox_lista_obiektow.index(ACTIVE)
    label_szczegoly_obiektow_name_wartosc.config(text=hotels[i].name)
    label_szczegoly_obiektow_location_wartosc.config(text=hotels[i].location)
    label_szczegoly_obiektow_stars_wartosc.config(text=hotels[i].stars)

    map_widget.set_zoom(15)
    map_widget.set_position(hotels[i].coordinates[0], hotels[i].coordinates[1])


# GUI setup
root = Tk()
root.geometry("1200x700")
root.title('HotelMap')

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# Lista hoteli
Label(ramka_lista_obiektow, text='Lista hoteli:').grid(row=0, column=0)

listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=50, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)

Button(ramka_lista_obiektow, text='Pokaż szczegóły:', command=show_hotel_detail).grid(row=2, column=0)
Button(ramka_lista_obiektow, text='Usuń', command=remove_hotel).grid(row=2, column=1)
Button(ramka_lista_obiektow, text='Edytuj', command=edit_hotel).grid(row=2, column=2)

# Formularz
Label(ramka_formularz, text='Formularz:').grid(row=0, column=0, sticky=W)
Label(ramka_formularz, text='Nazwa hotelu:').grid(row=1, column=0, sticky=W)
Label(ramka_formularz, text='Lokalizacja:').grid(row=2, column=0, sticky=W)
Label(ramka_formularz, text='Liczba gwiazdek:').grid(row=3, column=0, sticky=W)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1)
entry_location = Entry(ramka_formularz)
entry_location.grid(row=2, column=1)
entry_stars = Entry(ramka_formularz)
entry_stars.grid(row=3, column=1)

button_dodaj_obiekt = Button(ramka_formularz, text='Dodaj', command=add_hotel)
button_dodaj_obiekt.grid(row=4, column=0, columnspan=2)

# Szczegóły hotelu
Label(ramka_szczegoly_obiektow, text='Szczegóły hotelu:').grid(row=0, column=0)

Label(ramka_szczegoly_obiektow, text='Nazwa:').grid(row=1, column=0)
label_szczegoly_obiektow_name_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektow_name_wartosc.grid(row=1, column=1)

Label(ramka_szczegoly_obiektow, text='Lokalizacja:').grid(row=1, column=2)
label_szczegoly_obiektow_location_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektow_location_wartosc.grid(row=1, column=3)

Label(ramka_szczegoly_obiektow, text='Gwiazdek:').grid(row=1, column=4)
label_szczegoly_obiektow_stars_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektow_stars_wartosc.grid(row=1, column=5)

# Mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=400, corner_radius=0)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()
