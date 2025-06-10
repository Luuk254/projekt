from tkinter import *
from tkinter import messagebox
from tkintermapview import TkinterMapView
import requests

root = Tk()
root.title("System Policji")
root.geometry("1150x700")

police_units = []
users = []
incidents = []
editing_index = None
editing_incident_index = None
current_marker = None
selected_unit = None
user_markers = []

def get_coordinates(location_name):
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": location_name,
                "format": "json",
                "limit": 1
            },
            headers={
                "User-Agent": "MyPoliceApp/1.0 (your@email.com)"
            }
        )
        data = response.json()
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon
        else:
            return None
    except Exception as e:
        print("Błąd pobierania współrzędnych:", e)
        return None

def update_user_map():
    global user_markers
    for marker in user_markers:
        marker.delete()
    user_markers = []
    for user in users:
        coords = get_coordinates(user["location"])
        if coords:
            lat, lon = coords
            marker = map_widget.set_marker(lat, lon, text=f"{user['rank']} {user['name']} {user['surname']}")
            user_markers.append(marker)

def update_units_listbox():
    listbox_units.delete(0, END)
    for unit in police_units:
        listbox_units.insert(END, f"{unit['name']} ({unit['location']})")

def add_unit():
    global selected_unit
    name = entry_unit_name.get()
    location = entry_unit_location.get()
    if not name or not location:
        messagebox.showwarning("Błąd", "Podaj nazwę i lokalizację jednostki.")
        return
    unit = {"name": name, "location": location}
    police_units.append(unit)
    update_units_listbox()
    entry_unit_name.delete(0, END)
    entry_unit_location.delete(0, END)

def show_unit_details():
    global current_marker, selected_unit
    selected = listbox_units.curselection()
    if not selected:
        messagebox.showwarning("Błąd", "Wybierz jednostkę.")
        return

    frame_user_form.grid()
    frame_incident_form.grid()
    frame_users_list.grid_remove()
    frame_incidents.grid_remove()

    index = selected[0]
    selected_unit = police_units[index]

    coords = get_coordinates(selected_unit["location"])
    if coords is None:
        messagebox.showerror("Błąd", f"Nie można znaleźć lokalizacji: {selected_unit['location']}")
        return
    lat, lon = coords

    map_widget.set_position(lat, lon)

    if current_marker:
        current_marker.delete()
    current_marker = map_widget.set_marker(lat, lon, text=selected_unit["name"])

    frame_map.grid()

def update_users_listbox():
    listbox_users.delete(0, END)
    for user in users:
        listbox_users.insert(END, f"{user['rank']} {user['name']} {user['surname']}")

def add_user():
    global editing_index, selected_unit
    new_user = {
        "rank": entry_rank.get(),
        "name": entry_name.get(),
        "surname": entry_surname.get(),
        "unit": selected_unit["name"],
        "location": selected_unit["location"]
    }

    if not all([new_user["rank"], new_user["name"], new_user["surname"]]):
        messagebox.showwarning("Błąd", "Wypełnij wszystkie pola funkcjonariusza.")
        return

    if editing_index is not None:
        users[editing_index] = new_user
        editing_index = None
    else:
        users.append(new_user)

    update_users_listbox()

    entry_rank.delete(0, END)
    entry_name.delete(0, END)
    entry_surname.delete(0, END)

    frame_user_form.grid_remove()
    frame_incident_form.grid_remove()
    frame_users_list.grid()
    frame_user_details.grid_remove()
    update_user_map()

def show_user_details():
    selected = listbox_users.curselection()
    if not selected:
        messagebox.showinfo("Info", "Wybierz funkcjonariusza z listy.")
        return
    index = selected[0]
    user = users[index]

    label_detail_rank.config(text=f"Stopień: {user['rank']}")
    label_detail_name.config(text=f"Imię: {user['name']}")
    label_detail_surname.config(text=f"Nazwisko: {user['surname']}")
    label_detail_unit.config(text=f"Jednostka: {user['unit']}")
    label_detail_location.config(text=f"Miejscowość: {user['location']}")

    frame_user_details.grid()

def edit_user():
    global editing_index
    selected = listbox_users.curselection()
    if not selected:
        messagebox.showinfo("Info", "Wybierz funkcjonariusza do edycji.")
        return
    index = selected[0]
    user = users[index]
    editing_index = index

    entry_rank.delete(0, END)
    entry_rank.insert(0, user['rank'])

    entry_name.delete(0, END)
    entry_name.insert(0, user['name'])

    entry_surname.delete(0, END)
    entry_surname.insert(0, user['surname'])

    frame_user_form.grid()
    frame_users_list.grid_remove()
    frame_user_details.grid_remove()
    frame_map.grid()

def delete_user():
    selected = listbox_users.curselection()
    if not selected:
        messagebox.showinfo("Info", "Wybierz funkcjonariusza do usunięcia.")
        return
    index = selected[0]
    confirm = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tego funkcjonariusza?")
    if confirm:
        users.pop(index)
        update_users_listbox()
        frame_user_details.grid_remove()
        update_user_map()

def update_incidents_listbox():
    listbox_incidents.delete(0, END)
    for incident in incidents:
        listbox_incidents.insert(END, f"{incident['date']} - {incident['location']} - {incident['desc']}")

def add_incident():
    global editing_incident_index
    desc = entry_inc_desc.get()
    location = entry_inc_location.get()
    date = entry_inc_date.get()
    if not desc or not location or not date:
        messagebox.showwarning("Błąd", "Wypełnij wszystkie pola incydentu.")
        return
    new_incident = {"desc": desc, "location": location, "date": date}
    if editing_incident_index is not None:
        incidents[editing_incident_index] = new_incident
        editing_incident_index = None
    else:
        incidents.append(new_incident)
    update_incidents_listbox()
    entry_inc_desc.delete(0, END)
    entry_inc_location.delete(0, END)
    entry_inc_date.delete(0, END)
    frame_incidents.grid()
    frame_incident_form.grid_remove()

def edit_incident():
    global editing_incident_index
    selected = listbox_incidents.curselection()
    if not selected:
        messagebox.showinfo("Info", "Wybierz incydent do edycji.")
        return
    index = selected[0]
    incident = incidents[index]
    editing_incident_index = index
    entry_inc_desc.delete(0, END)
    entry_inc_desc.insert(0, incident['desc'])
    entry_inc_location.delete(0, END)
    entry_inc_location.insert(0, incident['location'])
    entry_inc_date.delete(0, END)
    entry_inc_date.insert(0, incident['date'])
    frame_incident_form.grid()
    frame_incidents.grid_remove()

def delete_incident():
    selected = listbox_incidents.curselection()
    if not selected:
        messagebox.showinfo("Info", "Wybierz incydent do usunięcia.")
        return
    index = selected[0]
    confirm = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć ten incydent?")
    if confirm:
        incidents.pop(index)
        update_incidents_listbox()
        if not incidents:
            frame_incidents.grid_remove()

def show_incident_on_map():
    global current_marker
    selected = listbox_incidents.curselection()
    if not selected:
        messagebox.showinfo("Info", "Wybierz incydent z listy.")
        return
    index = selected[0]
    inc = incidents[index]

    coords = get_coordinates(inc["location"])
    if coords is None:
        messagebox.showerror("Błąd", f"Nie można znaleźć lokalizacji: {inc['location']}")
        return
    lat, lon = coords

    map_widget.set_position(lat, lon)
    if current_marker:
        current_marker.delete()
    current_marker = map_widget.set_marker(lat, lon, text=inc["desc"])
    map_widget.set_zoom(14)
    frame_map.grid()

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

def focus_prev_widget(event):
    event.widget.tk_focusPrev().focus()
    return "break"

# --- UI ---
frame_unit = LabelFrame(root, text="Dodaj jednostkę policji")
frame_unit.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

Label(frame_unit, text="Nazwa:").grid(row=0, column=0, sticky=W)
entry_unit_name = Entry(frame_unit, width=30)
entry_unit_name.grid(row=0, column=1, padx=5, pady=2)

Label(frame_unit, text="Lokalizacja:").grid(row=1, column=0, sticky=W)
entry_unit_location = Entry(frame_unit, width=30)
entry_unit_location.grid(row=1, column=1, padx=5, pady=2)

Button(frame_unit, text="Dodaj jednostkę", command=add_unit).grid(row=2, column=0, columnspan=2, pady=5)

frame_unit_list = LabelFrame(root, text="Lista jednostek")
frame_unit_list.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

listbox_units = Listbox(frame_unit_list, height=6, width=45)
listbox_units.pack(padx=5, pady=5)

Button(frame_unit_list, text="Pokaż szczegóły", command=show_unit_details).pack(pady=5)

frame_map = LabelFrame(root, text="Mapa")
frame_map.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="ne")
map_widget = TkinterMapView(frame_map, width=700, height=500)
map_widget.set_position(52.23, 20.01)
map_widget.set_zoom(5.5)
map_widget.pack()

frame_user_form = LabelFrame(root, text="Dodaj funkcjonariusza")
frame_user_form.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
frame_user_form.grid_remove()

Label(frame_user_form, text="Stopień:").grid(row=0, column=0, sticky=W)
entry_rank = Entry(frame_user_form, width=30)
entry_rank.grid(row=0, column=1, padx=5, pady=2)

Label(frame_user_form, text="Imię:").grid(row=1, column=0, sticky=W)
entry_name = Entry(frame_user_form, width=30)
entry_name.grid(row=1, column=1, padx=5, pady=2)

Label(frame_user_form, text="Nazwisko:").grid(row=2, column=0, sticky=W)
entry_surname = Entry(frame_user_form, width=30)
entry_surname.grid(row=2, column=1, padx=5, pady=2)

Button(frame_user_form, text="Zapisz funkcjonariusza", command=add_user).grid(row=3, column=0, columnspan=2, pady=5)

frame_users_list = LabelFrame(root, text="Lista funkcjonariuszy")
frame_users_list.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
frame_users_list.grid_remove()

listbox_users = Listbox(frame_users_list, height=6, width=45)
listbox_users.pack(padx=5, pady=5)

frame_user_buttons = Frame(frame_users_list)
frame_user_buttons.pack()

Button(frame_user_buttons, text="Szczegóły", command=show_user_details).grid(row=0, column=0, padx=2)
Button(frame_user_buttons, text="Edytuj", command=edit_user).grid(row=0, column=1, padx=2)
Button(frame_user_buttons, text="Usuń", command=delete_user).grid(row=0, column=2, padx=2)

frame_user_details = LabelFrame(root, text="Szczegóły funkcjonariusza")
frame_user_details.grid(row=4, column=0, padx=10, pady=10, sticky="nw")
frame_user_details.grid_remove()

label_detail_rank = Label(frame_user_details, text="")
label_detail_rank.grid(row=0, column=0, sticky=W)
label_detail_name = Label(frame_user_details, text="")
label_detail_name.grid(row=1, column=0, sticky=W)
label_detail_surname = Label(frame_user_details, text="")
label_detail_surname.grid(row=2, column=0, sticky=W)
label_detail_unit = Label(frame_user_details, text="")
label_detail_unit.grid(row=3, column=0, sticky=W)
label_detail_location = Label(frame_user_details, text="")
label_detail_location.grid(row=4, column=0, sticky=W)

frame_incident_form = LabelFrame(root, text="Dodaj incydent")
frame_incident_form.grid(row=5, column=0, padx=10, pady=10, sticky="nw")
frame_incident_form.grid_remove()

Label(frame_incident_form, text="Opis:").grid(row=0, column=0, sticky=W)
entry_inc_desc = Entry(frame_incident_form, width=30)
entry_inc_desc.grid(row=0, column=1, padx=5, pady=2)

Label(frame_incident_form, text="Lokalizacja:").grid(row=1, column=0, sticky=W)
entry_inc_location = Entry(frame_incident_form, width=30)
entry_inc_location.grid(row=1, column=1, padx=5, pady=2)

Label(frame_incident_form, text="Data:").grid(row=2, column=0, sticky=W)
entry_inc_date = Entry(frame_incident_form, width=30)
entry_inc_date.grid(row=2, column=1, padx=5, pady=2)

Button(frame_incident_form, text="Zapisz incydent", command=add_incident).grid(row=3, column=0, columnspan=2, pady=5)

frame_incidents = LabelFrame(root, text="Lista incydentów")
frame_incidents.grid(row=6, column=0, padx=10, pady=10, sticky="nw")
frame_incidents.grid_remove()

listbox_incidents = Listbox(frame_incidents, height=6, width=45)
listbox_incidents.pack(padx=5, pady=5)

frame_incident_buttons = Frame(frame_incidents)
frame_incident_buttons.pack()

Button(frame_incident_buttons, text="Pokaż na mapie", command=show_incident_on_map).grid(row=0, column=0, padx=2)
Button(frame_incident_buttons, text="Edytuj", command=edit_incident).grid(row=0, column=1, padx=2)
Button(frame_incident_buttons, text="Usuń", command=delete_incident).grid(row=0, column=2, padx=2)

root.mainloop()
