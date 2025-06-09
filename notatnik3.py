from tkinter import *
from tkinter import messagebox
from tkintermapview import TkinterMapView

users = []
incidents = []
editing_index = None
current_marker = None


def add_user():
    global editing_index
    new_user = {
        "rank": entry_rank.get(),
        "name": entry_name.get(),
        "surname": entry_surname.get(),
        "unit": entry_police_unit.get(),
        "location": entry_location.get()
    }

    if not new_user["rank"] or not new_user["name"] or not new_user["surname"]:
        messagebox.showwarning("Uwaga", "Stopień, imię i nazwisko są wymagane.")
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
    entry_police_unit.delete(0, END)
    entry_location.delete(0, END)

    # Po dodaniu funkcjonariusza chowamy mapę (zgodnie z Twoim życzeniem)
    frame_mapa.grid_remove()
    # Pokaż listę funkcjonariuszy
    frame_users.grid(row=1, column=0, padx=10, pady=10, sticky="n")


def update_users_listbox():
    listbox_funkcjonariusze.delete(0, END)
    for user in users:
        listbox_funkcjonariusze.insert(END, f"{user['rank']} {user['name']} {user['surname']}")


def delete_user():
    selected = listbox_funkcjonariusze.curselection()
    if not selected:
        messagebox.showinfo("Info", "Nie wybrano funkcjonariusza do usunięcia.")
        return
    index = selected[0]
    users.pop(index)
    update_users_listbox()
    if not users:
        frame_users.grid_remove()
        frame_mapa.grid()


def edit_user():
    global editing_index
    selected = listbox_funkcjonariusze.curselection()
    if not selected:
        messagebox.showinfo("Info", "Nie wybrano funkcjonariusza do edycji.")
        return
    index = selected[0]
    editing_index = index
    user = users[index]

    entry_rank.delete(0, END)
    entry_rank.insert(0, user["rank"])
    entry_name.delete(0, END)
    entry_name.insert(0, user["name"])
    entry_surname.delete(0, END)
    entry_surname.insert(0, user["surname"])
    entry_police_unit.delete(0, END)
    entry_police_unit.insert(0, user["unit"])
    entry_location.delete(0, END)
    entry_location.insert(0, user["location"])


def show_user_details():
    selected_index = listbox_funkcjonariusze.curselection()
    if not selected_index:
        messagebox.showinfo("Info", "Nie wybrano funkcjonariusza do wyświetlenia danych.")
        return
    index = selected_index[0]
    user = users[index]

    label_police_officer_rank_wartosc.config(text=user["rank"])
    label_police_officer_name_wartosc.config(text=user["name"])
    label_police_officer_surname_wartosc.config(text=user["surname"])
    label_police_officer_unit_wartosc.config(text=user["unit"])
    label_police_officer_location_wartosc.config(text=user["location"])


def add_incident():
    desc = entry_inc_desc.get().strip()
    place = entry_inc_place.get().strip()
    date = entry_inc_date.get().strip()

    if not desc or not place or not date:
        messagebox.showwarning("Uwaga", "Wszystkie pola incydentu muszą być wypełnione.")
        return

    # Prosty regex na datę YYYY-MM-DD (można rozszerzyć)
    import re
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        messagebox.showwarning("Uwaga", "Data musi być w formacie RRRR-MM-DD.")
        return

    incident = {"desc": desc, "place": place, "date": date}
    incidents.append(incident)

    listbox_incydenty.insert(END, f"{date} - {place} - {desc}")

    entry_inc_desc.delete(0, END)
    entry_inc_place.delete(0, END)
    entry_inc_date.delete(0, END)

    # Po dodaniu incydentu pokazujemy listę incydentów i mapę
    frame_incidents.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="n")
    frame_mapa.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


def delete_incident():
    selected = listbox_incydenty.curselection()
    if not selected:
        messagebox.showinfo("Info", "Nie wybrano incydentu do usunięcia.")
        return
    index = selected[0]
    incidents.pop(index)
    listbox_incydenty.delete(index)
    global current_marker
    if current_marker:
        current_marker.delete()
        current_marker = None


def show_incident_on_map():
    global current_marker
    selected = listbox_incydenty.curselection()
    if not selected:
        messagebox.showinfo("Info", "Nie wybrano incydentu.")
        return
    index = selected[0]
    incident = incidents[index]
    place = incident["place"]

    # Usuń poprzedni marker
    if current_marker:
        current_marker.delete()

    # Dodaj nowy marker i zoomuj
    current_marker = map_widget.set_address(place, marker=True)
    if current_marker:
        map_widget.set_zoom(15)


root = Tk()
root.title("System Policji")
root.geometry("1000x700")

# --- Formularz funkcjonariusza ---
frame_form_user = LabelFrame(root, text="Dodaj funkcjonariusza")
frame_form_user.grid(row=0, column=0, padx=10, pady=10, sticky="n")

Label(frame_form_user, text="Stopień:").grid(row=0, column=0, sticky=W)
entry_rank = Entry(frame_form_user)
entry_rank.grid(row=0, column=1)

Label(frame_form_user, text="Imię:").grid(row=1, column=0, sticky=W)
entry_name = Entry(frame_form_user)
entry_name.grid(row=1, column=1)

Label(frame_form_user, text="Nazwisko:").grid(row=2, column=0, sticky=W)
entry_surname = Entry(frame_form_user)
entry_surname.grid(row=2, column=1)

Label(frame_form_user, text="Jednostka:").grid(row=3, column=0, sticky=W)
entry_police_unit = Entry(frame_form_user)
entry_police_unit.grid(row=3, column=1)

Label(frame_form_user, text="Miejscowość:").grid(row=4, column=0, sticky=W)
entry_location = Entry(frame_form_user)
entry_location.grid(row=4, column=1)

Button(frame_form_user, text="Dodaj / Zapisz", command=add_user).grid(row=5, column=0, columnspan=2, pady=5)

# --- Formularz incydentu ---
frame_form_incident = LabelFrame(root, text="Dodaj incydent")
frame_form_incident.grid(row=0, column=1, padx=10, pady=10, sticky="n")

Label(frame_form_incident, text="Opis incydentu:").grid(row=0, column=0, sticky=W)
entry_inc_desc = Entry(frame_form_incident, width=30)
entry_inc_desc.grid(row=0, column=1)

Label(frame_form_incident, text="Miejsce:").grid(row=1, column=0, sticky=W)
entry_inc_place = Entry(frame_form_incident, width=30)
entry_inc_place.grid(row=1, column=1)

Label(frame_form_incident, text="Data (RRRR-MM-DD):").grid(row=2, column=0, sticky=W)
entry_inc_date = Entry(frame_form_incident, width=30)
entry_inc_date.grid(row=2, column=1)

Button(frame_form_incident, text="Dodaj incydent", command=add_incident).grid(row=3, column=0, columnspan=2, pady=5)

# --- Lista funkcjonariuszy ---
frame_users = LabelFrame(root, text="Lista funkcjonariuszy")
# Nie pokazujemy na starcie
frame_users.grid_remove()

listbox_funkcjonariusze = Listbox(frame_users, width=40, height=10)
listbox_funkcjonariusze.pack(padx=5, pady=5)

frame_user_btns = Frame(frame_users)
frame_user_btns.pack()
Button(frame_user_btns, text="Edytuj", command=edit_user).pack(side=LEFT, padx=5)
Button(frame_user_btns, text="Usuń", command=delete_user).pack(side=LEFT, padx=5)
Button(frame_user_btns, text="Pokaż dane", command=show_user_details).pack(side=LEFT, padx=5)

# --- Szczegóły funkcjonariusza ---
frame_user_details = LabelFrame(root, text="Dane funkcjonariusza")
frame_user_details.grid(row=1, column=1, padx=10, pady=10, sticky="n")

Label(frame_user_details, text="Stopień:").grid(row=0, column=0, sticky=W)
label_police_officer_rank_wartosc = Label(frame_user_details, text="")
label_police_officer_rank_wartosc.grid(row=0, column=1, sticky=W)

Label(frame_user_details, text="Imię:").grid(row=1, column=0, sticky=W)
label_police_officer_name_wartosc = Label(frame_user_details, text="")
label_police_officer_name_wartosc.grid(row=1, column=1, sticky=W)

Label(frame_user_details, text="Nazwisko:").grid(row=2, column=0, sticky=W)
label_police_officer_surname_wartosc = Label(frame_user_details, text="")
label_police_officer_surname_wartosc.grid(row=2, column=1, sticky=W)

Label(frame_user_details, text="Jednostka:").grid(row=3, column=0, sticky=W)
label_police_officer_unit_wartosc = Label(frame_user_details, text="")
label_police_officer_unit_wartosc.grid(row=3, column=1, sticky=W)

Label(frame_user_details, text="Miejscowość:").grid(row=4, column=0, sticky=W)
label_police_officer_location_wartosc = Label(frame_user_details, text="")
label_police_officer_location_wartosc.grid(row=4, column=1, sticky=W)

# --- Lista incydentów ---
frame_incidents = LabelFrame(root, text="Lista incydentów")
frame_incidents.grid_remove()  # na start ukryta

listbox_incydenty = Listbox(frame_incidents, width=80, height=6)
listbox_incydenty.pack(padx=5, pady=5)

frame_inc_btns = Frame(frame_incidents)
frame_inc_btns.pack()
Button(frame_inc_btns, text="Usuń", command=delete_incident).pack(side=LEFT, padx=5)
Button(frame_inc_btns, text="Dane incydentu", command=show_incident_on_map).pack(side=LEFT, padx=5)

# --- Mapa ---
frame_mapa = LabelFrame(root, text="Mapa")
frame_mapa.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

map_widget = TkinterMapView(frame_mapa, width=950, height=300)
map_widget.set_position(52.23, 21.01)  # Warszawa
map_widget.set_zoom(5)
map_widget.pack()

root.mainloop()
