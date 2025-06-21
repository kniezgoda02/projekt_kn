from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

hotels: list = []
employees: list = []
clients: list = []


class Hotel:
    def __init__(self, name, location, stars):
        self.name = name
        self.location = location
        self.stars = stars
        self.coordinates = self.get_coordinates()
        self.marker = self.create_marker()

    def get_coordinates(self) -> list:
        adres_url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
        response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(',', '.')),
            float(response_html.select('.longitude')[1].text.replace(',', '.')),
        ]

    def create_marker(self):
        return map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"🏨 {self.name}")


class Employee:
    def __init__(self, first_name, last_name, city, role, hotel_name):
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.role = role
        self.hotel_name = hotel_name
        self.coordinates = self.get_coordinates()
        self.marker = self.create_marker()

    def get_coordinates(self):
        url = f'https://pl.wikipedia.org/wiki/{self.city}'
        html = BeautifulSoup(requests.get(url).text, 'html.parser')
        return [
            float(html.select('.latitude')[1].text.replace(',', '.')),
            float(html.select('.longitude')[1].text.replace(',', '.')),
        ]

    def create_marker(self):
        return map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                     text=f"👤 {self.first_name} {self.last_name} ({self.hotel_name})")


class Client:
    def __init__(self, first_name, last_name, city, hotel_name):
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.hotel_name = hotel_name
        self.coordinates = self.get_coordinates()
        self.marker = self.create_marker()

    def get_coordinates(self):
        url = f'https://pl.wikipedia.org/wiki/{self.city}'
        html = BeautifulSoup(requests.get(url).text, 'html.parser')
        return [
            float(html.select('.latitude')[1].text.replace(',', '.')),
            float(html.select('.longitude')[1].text.replace(',', '.')),
        ]

    def create_marker(self):
        return map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                     text=f"🧳 {self.first_name} {self.last_name} ({self.hotel_name})")


# Funkcje hotelu
def add_hotel() -> None:
    name = entry_name.get()
    location = entry_location.get()
    stars = entry_stars.get()
    if name and location and stars:
        hotel = Hotel(name=name, location=location, stars=stars)
        hotels.append(hotel)
        show_hotels()
        update_hotel_dropdown()
        entry_name.delete(0, END)
        entry_location.delete(0, END)
        entry_stars.delete(0, END)


def show_hotels():
    listbox_lista_obiektow.delete(0, END)
    for idx, hotel in enumerate(hotels):
        listbox_lista_obiektow.insert(idx, f"{hotel.name} ({hotel.stars}★, {hotel.location})")


def remove_hotel():
    i = listbox_lista_obiektow.index(ACTIVE)
    if hotels[i].marker:
        hotels[i].marker.delete()
    hotels.pop(i)
    show_hotels()
    update_hotel_dropdown()


def edit_hotel():
    i = listbox_lista_obiektow.index(ACTIVE)
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_stars.delete(0, END)

    hotel = hotels[i]

    entry_name.insert(0, hotel.name)
    entry_location.insert(0, hotel.location)
    entry_stars.insert(0, hotel.stars)
    button_add_hotel.config(text="Zapisz", command=lambda: update_hotel(i))


def update_hotel(i):
    hotel = hotels[i]
    hotel.marker.delete()

    name = entry_name.get()
    location = entry_location.get()
    stars = entry_stars.get()

    if hotels[i].marker:
        hotels[i].marker.delete()

    hotels[i].name = name
    hotels[i].location = location
    hotels[i].stars = stars
    hotels[i].coordinates = hotels[i].get_coordinates()
    hotels[i].marker = hotels[i].create_marker()

    show_hotels()
    button_add_hotel.configure(text='Dodaj hotel', command=add_hotel)

    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_stars.delete(0, END)
    entry_name.focus()


def show_hotel_detail():
    i = listbox_lista_obiektow.index(ACTIVE)
    label_name.config(text=f"Nazwa: {hotels[i].name}")
    label_location.config(text=f"Lokalizacja: {hotels[i].location}")
    label_stars.config(text=f"Gwiazdki: {hotels[i].stars}")

    map_widget.set_zoom(14)
    map_widget.set_position(hotels[i].coordinates[0], hotels[i].coordinates[1])


# Pracownicy
def add_employee():
    fname = entry_fname.get()
    lname = entry_lname.get()
    city = entry_city.get()
    role = entry_role.get()
    hotel = hotel_var.get()
    if fname and lname and city and role and hotel:
        emp = Employee(fname, lname, city, role, hotel)
        employees.append(emp)
        show_employees()
        entry_fname.delete(0, END)
        entry_lname.delete(0, END)
        entry_city.delete(0, END)
        entry_role.delete(0, END)


def show_employees():
    listbox_employees.delete(0, END)
    for idx, e in enumerate(employees):
        listbox_employees.insert(idx, f"{e.first_name} {e.last_name} - {e.role} ({e.hotel_name})")


def remove_employee():
    i = listbox_employees.index(ACTIVE)
    employees[i].marker.delete()
    employees.pop(i)
    show_employees()


def edit_employee():
    i = listbox_employees.index(ACTIVE)
    emp = employees[i]
    entry_fname.delete(0, END)
    entry_lname.delete(0, END)
    entry_city.delete(0, END)
    entry_role.delete(0, END)

    entry_fname.insert(0, emp.first_name)
    entry_lname.insert(0, emp.last_name)
    entry_city.insert(0, emp.city)
    entry_role.insert(0, emp.role)
    hotel_var.set(emp.hotel_name)

    button_add_emp.config(text="Zapisz", command=lambda: update_employee(i))


def update_employee(i):
    emp = employees[i]
    emp.marker.delete()

    emp.first_name = entry_fname.get()
    emp.last_name = entry_lname.get()
    emp.city = entry_city.get()
    emp.role = entry_role.get()
    emp.hotel_name = hotel_var.get()
    emp.coordinates = emp.get_coordinates()
    emp.marker = emp.create_marker()

    show_employees()
    entry_fname.delete(0, END)
    entry_lname.delete(0, END)
    entry_city.delete(0, END)
    entry_role.delete(0, END)
    hotel_var.set(hotels[0].name if hotels else "")
    button_add_emp.config(text="Dodaj pracownika", command=add_employee)


def show_employee_detail():
    i = listbox_employees.index(ACTIVE)
    emp = employees[i]
    label_emp_name.config(text=f"Imię i nazwisko: {emp.first_name} {emp.last_name}")
    label_emp_city.config(text=f"Miasto: {emp.city}")
    label_emp_role.config(text=f"Stanowisko: {emp.role}")
    label_emp_hotel.config(text=f"Hotel: {emp.hotel_name}")

    map_widget.set_zoom(14)
    map_widget.set_position(emp.coordinates[0], emp.coordinates[1])


# --- Funkcje klientów ---
def add_client():
    fname = entry_c_fname.get()
    lname = entry_c_lname.get()
    city = entry_c_city.get()
    hotel = hotel_client_var.get()
    if fname and lname and city and hotel:
        client = Client(fname, lname, city, hotel)
        clients.append(client)
        show_clients()
        entry_c_fname.delete(0, END)
        entry_c_lname.delete(0, END)
        entry_c_city.delete(0, END)


def show_clients():
    listbox_clients.delete(0, END)
    for idx, c in enumerate(clients):
        listbox_clients.insert(idx, f"{c.first_name} {c.last_name} ({c.hotel_name})")


def remove_client():
    i = listbox_clients.index(ACTIVE)
    clients[i].marker.delete()
    clients.pop(i)
    show_clients()


def edit_client():
    i = listbox_clients.index(ACTIVE)
    c = clients[i]
    entry_c_fname.delete(0, END)
    entry_c_lname.delete(0, END)
    entry_c_city.delete(0, END)
    entry_c_fname.insert(0, c.first_name)
    entry_c_lname.insert(0, c.last_name)
    entry_c_city.insert(0, c.city)
    hotel_client_var.set(c.hotel_name)
    button_add_client.config(text="Zapisz", command=lambda: update_client(i))


def update_client(i):
    clients[i].marker.delete()
    clients[i].first_name = entry_c_fname.get()
    clients[i].last_name = entry_c_lname.get()
    clients[i].city = entry_c_city.get()
    clients[i].hotel_name = hotel_client_var.get()
    clients[i].coordinates = clients[i].get_coordinates()
    clients[i].marker = clients[i].create_marker()
    show_clients()
    button_add_client.config(text="Dodaj klienta", command=add_client)


def update_hotel_dropdown():
    hotel_dropdown['menu'].delete(0, 'end')
    hotel_client_dropdown['menu'].delete(0, 'end')
    for h in hotels:
        hotel_dropdown['menu'].add_command(label=h.name, command=lambda value=h.name: hotel_var.set(value))
        hotel_client_dropdown['menu'].add_command(label=h.name,
                                                  command=lambda value=h.name: hotel_client_var.set(value))
    if hotels:
        hotel_var.set(hotels[0].name)
        hotel_client_var.set(hotels[0].name)
    else:
        hotel_var.set("")
        hotel_client_var.set("")


def show_client_details():
    i = listbox_clients.index(ACTIVE)
    c = clients[i]
    label_client_name.config(text=f"Imię i nazwisko: {c.first_name} {c.last_name}")
    label_client_city.config(text=f"Miasto: {c.city}")
    label_client_hotel.config(text=f"Hotel: {c.hotel_name}")
    map_widget.set_zoom(14)
    map_widget.set_position(c.coordinates[0], c.coordinates[1])


# Pokaż
def show_only_hotels():
    # Usuń wszystkie markery
    for e in employees:
        if e.marker:
            e.marker.delete()
            e.marker = None
    for c in clients:
        if c.marker:
            c.marker.delete()
            c.marker = None
    # Stwórz markery dla hoteli jeśli ich nie ma
    for h in hotels:
        if not h.marker:
            h.marker = map_widget.set_marker(h.coordinates[0], h.coordinates[1], text=f"🏨 {h.name}")


def show_only_employees():
    for h in hotels:
        if h.marker:
            h.marker.delete()
            h.marker = None
    for c in clients:
        if c.marker:
            c.marker.delete()
            c.marker = None
    for e in employees:
        if not e.marker:
            e.marker = map_widget.set_marker(e.coordinates[0], e.coordinates[1],
                                             text=f"👤 {e.first_name} {e.last_name} ({e.hotel_name})")


def show_only_clients():
    for h in hotels:
        if h.marker:
            h.marker.delete()
            h.marker = None
    for e in employees:
        if e.marker:
            e.marker.delete()
            e.marker = None
    for c in clients:
        if not c.marker:
            c.marker = map_widget.set_marker(c.coordinates[0], c.coordinates[1],
                                             text=f"🧳 {c.first_name} {c.last_name} ({c.hotel_name})")




#tylko danego hotelu
def show_employees_for_selected_hotel():
    if not hotels:
        return
    try:
        i = listbox_lista_obiektow.index(ACTIVE)
    except:
        return
    selected_hotel = hotels[i].name

    # Usunięcie wszystkich markerów
    for emp in employees:
        if emp.marker:
            emp.marker.delete()
            emp.marker = None
    for c in clients:
        if c.marker:
            c.marker.delete()
            c.marker = None
    for h in hotels:
        if h.marker:
            h.marker.delete()
            h.marker = None

    # Pokazanie tylko pracowników wybranego hotelu
    for emp in employees:
        if emp.hotel_name == selected_hotel:
            emp.marker = map_widget.set_marker(emp.coordinates[0], emp.coordinates[1],
                                               text=f"👤 {emp.first_name} {emp.last_name} ({emp.hotel_name})")


def show_clients_for_selected_hotel():
    if not hotels:
        return
    try:
        i = listbox_lista_obiektow.index(ACTIVE)
    except:
        return
    selected_hotel = hotels[i].name

    # Usunięcie wszystkich markerów
    for emp in employees:
        if emp.marker:
            emp.marker.delete()
            emp.marker = None
    for c in clients:
        if c.marker:
            c.marker.delete()
            c.marker = None
    for h in hotels:
        if h.marker:
            h.marker.delete()
            h.marker = None

    # Pokazanie tylko klientów wybranego hotelu
    for c in clients:
        if c.hotel_name == selected_hotel:
            c.marker = map_widget.set_marker(c.coordinates[0], c.coordinates[1],
                                             text=f"🧳 {c.first_name} {c.last_name} ({c.hotel_name})")




# GUI setup
# Mapa
root = Tk()
root.geometry("1200x800")
root.title('HotelMap')

for i in range(4):
    root.columnconfigure(i, weight=1, uniform="group1")

ramka_wysokosc = 380

frame_hotels = LabelFrame(root, text="Hotele", padx=5, pady=5)
frame_hotels.grid(row=0, column=0, sticky="nsew")
frame_hotels.configure(height=ramka_wysokosc)
frame_hotels.grid_propagate(False)

frame_employees = LabelFrame(root, text="Pracownicy", padx=5, pady=5)
frame_employees.grid(row=0, column=1, sticky="nsew")
frame_employees.configure(height=ramka_wysokosc)
frame_employees.grid_propagate(False)

frame_clients = LabelFrame(root, text="Klienci", padx=5, pady=5)
frame_clients.grid(row=0, column=2, sticky="nsew")
frame_clients.configure(height=ramka_wysokosc)
frame_clients.grid_propagate(False)

frame_details = LabelFrame(root, text="Szczegóły")
frame_details.grid(row=0, column=3)

frame_hotel_details = Frame(frame_details)
frame_hotel_details.grid(row=0, column=0, padx=20, sticky="nw")

frame_employee_details = Frame(frame_details)
frame_employee_details.grid(row=1, column=0, padx=20, sticky="nw")

frame_client_details = Frame(frame_details)
frame_client_details.grid(row=3, column=0, padx=20, sticky="nw")

frame_map = Frame(root)
frame_map.grid(row=2, column=0, columnspan=4, sticky="nsew")

# Hotele
Label(frame_hotels, text="Nazwa hotelu:").grid(row=0, column=0)
entry_name = Entry(frame_hotels)
entry_name.grid(row=0, column=1)
Label(frame_hotels, text="Lokalizacja:").grid(row=1, column=0)
entry_location = Entry(frame_hotels)
entry_location.grid(row=1, column=1)
Label(frame_hotels, text="Liczba gwiazdek:").grid(row=2, column=0)
entry_stars = Entry(frame_hotels)
entry_stars.grid(row=2, column=1)
button_add_hotel = Button(frame_hotels, text="Dodaj hotel", command=add_hotel)
button_add_hotel.grid(row=6, column=0)

listbox_lista_obiektow = Listbox(frame_hotels, width=35)
listbox_lista_obiektow.grid(row=3, column=0, columnspan=2)
Button(frame_hotels, text="Pokaż szczegóły", command=show_hotel_detail).grid(row=7, column=0)
Button(frame_hotels, text="Usuń", command=remove_hotel).grid(row=7, column=1, columnspan=1)
Button(frame_hotels, text="Edytuj", command=edit_hotel).grid(row=6, column=1, columnspan=1)

# Szczegóły hotelu
Label(frame_hotel_details, text="Szczegóły hotelu:").grid(row=0, column=0, sticky="w")
label_name = Label(frame_hotel_details, text="Nazwa: ....")
label_name.grid(row=1, column=0, sticky="w", padx=(10, 30))
label_location = Label(frame_hotel_details, text="Lokalizacja: ....")
label_location.grid(row=2, column=0, sticky="w", padx=(10, 30))
label_stars = Label(frame_hotel_details, text="Gwiazdki: ....")
label_stars.grid(row=3, column=0, sticky="w", padx=(10, 30))

# Pracownicy
Label(frame_employees, text="Imię:").grid(row=0, column=0)
entry_fname = Entry(frame_employees)
entry_fname.grid(row=0, column=1)
Label(frame_employees, text="Nazwisko:").grid(row=1, column=0)
entry_lname = Entry(frame_employees)
entry_lname.grid(row=1, column=1)
Label(frame_employees, text="Miasto zam.:").grid(row=2, column=0)
entry_city = Entry(frame_employees)
entry_city.grid(row=2, column=1)
Label(frame_employees, text="Stanowisko:").grid(row=3, column=0)
entry_role = Entry(frame_employees)
entry_role.grid(row=3, column=1)
Label(frame_employees, text="Hotel:").grid(row=4, column=0)
hotel_var = StringVar()
hotel_dropdown = OptionMenu(frame_employees, hotel_var, "")
hotel_dropdown.grid(row=4, column=1)
button_add_emp = Button(frame_employees, text="Dodaj", command=add_employee)
button_add_emp.grid(row=6, column=0)
listbox_employees = Listbox(frame_employees, width=35)
listbox_employees.grid(row=5, column=0, columnspan=2, pady=(10, 10))
Button(frame_employees, text="Usuń", command=remove_employee).grid(row=7, column=1, columnspan=1, padx=2, pady=(0, 2))
Button(frame_employees, text="Edytuj", command=edit_employee).grid(row=6, column=1, columnspan=1, padx=2, pady=(0, 2))
Button(frame_employees, text="Pokaż szczegóły", command=show_employee_detail).grid(row=7, column=0, padx=2, pady=(0, 2))

# Szczegóły pracownika
Label(frame_employee_details, text="Szczegóły pracownika:").grid(row=4, column=0, sticky="w", padx=(10, 30))
label_emp_name = Label(frame_employee_details, text='Imię i nazwisko: ....')
label_emp_name.grid(row=5, column=0, sticky="w", padx=(10, 30))
label_emp_city = Label(frame_employee_details, text='Miasto: ....')
label_emp_city.grid(row=6, column=0, sticky="w", padx=(10, 30))
label_emp_role = Label(frame_employee_details, text='Stanowisko: ....')
label_emp_role.grid(row=7, column=0, sticky="w", padx=(10, 30))
label_emp_hotel = Label(frame_employee_details, text='Hotel: ....')
label_emp_hotel.grid(row=8, column=0, sticky="w", padx=(10, 30))

# Klienci
Label(frame_clients, text="Imię:").grid(row=0, column=0)
entry_c_fname = Entry(frame_clients)
entry_c_fname.grid(row=0, column=1)
Label(frame_clients, text="Nazwisko:").grid(row=1, column=0)
entry_c_lname = Entry(frame_clients)
entry_c_lname.grid(row=1, column=1)
Label(frame_clients, text="Miasto:").grid(row=2, column=0)
entry_c_city = Entry(frame_clients)
entry_c_city.grid(row=2, column=1)
Label(frame_clients, text="Hotel:").grid(row=3, column=0)
hotel_client_var = StringVar()
hotel_client_dropdown = OptionMenu(frame_clients, hotel_client_var, "")
hotel_client_dropdown.grid(row=3, column=1)
button_add_client = Button(frame_clients, text="Dodaj", command=add_client)
button_add_client.grid(row=5, column=0)
listbox_clients = Listbox(frame_clients, width=35)
listbox_clients.grid(row=4, column=0, columnspan=2, pady=(10, 10))
Button(frame_clients, text="Usuń", command=remove_client).grid(row=6, column=1)
Button(frame_clients, text="Edytuj", command=edit_client).grid(row=5, column=1)
Button(frame_clients, text="Pokaż szczegóły", command=show_client_details).grid(row=6, column=0)

# szczegóły klienta
Label(frame_client_details, text="Szczegóły klienta:").grid(row=9, column=0, columnspan=3, sticky="w", padx=(10, 0))
label_client_name = Label(frame_client_details, text='Imię i nazwisko: ....')
label_client_name.grid(row=10, column=0, sticky="w", padx=(10, 30))
label_client_city = Label(frame_client_details, text='Miasto: ....')
label_client_city.grid(row=11, column=0, sticky="w", padx=(10, 30))
label_client_hotel = Label(frame_client_details, text='Hotel: ....')
label_client_hotel.grid(row=12, column=0, sticky="w", padx=(10, 30))

frame_filters = Frame(root)
frame_filters.grid(row=1, column=0, columnspan=4, pady=10)

Button(frame_filters, text="Pokaż tylko hotele", command=show_only_hotels).grid(row=0, column=0, padx=5)
Button(frame_filters, text="Pokaż tylko pracowników", command=show_only_employees).grid(row=0, column=1, padx=5)
Button(frame_filters, text="Pokaż tylko klientów", command=show_only_clients).grid(row=0, column=2, padx=5)

Button(frame_hotels, text="Mapa pracowników", command=show_employees_for_selected_hotel).grid(row=8, column=0, pady=2)
Button(frame_hotels, text="Mapa klientów", command=show_clients_for_selected_hotel).grid(row=8, column=1, pady=2)




for i in range(4):
    root.columnconfigure(i, weight=1, uniform="group1")

frame_map = Frame(root)
frame_map.grid(row=2, column=0, columnspan=4, sticky="nsew")
frame_map.rowconfigure(0, weight=1)
frame_map.columnconfigure(0, weight=1)

map_widget = tkintermapview.TkinterMapView(frame_map, width=1350, height=400, corner_radius=0)
map_widget.grid(row=0, column=0, sticky="nsew")
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()
