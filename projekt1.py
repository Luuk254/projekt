from tkinter import *
from tkinter import messagebox, ttk
from tkintermapview import TkinterMapView
from collections import defaultdict
import requests

# Kolory
COLOR_BG     = "#ecf2f8"
COLOR_FRAME  = "#ffffff"
COLOR_ACCENT = "#2864c7"
COLOR_SHADOW = "#c6d1e1"
COLOR_BTN    = "#3577e6"
COLOR_BTN2   = "#bcc9db"
COLOR_LISTB  = "#f8fafc"
COLOR_FONT   = "#1e2a36"

def get_coordinates(loc):
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": loc, "format": "json", "limit": 1},
            headers={"User-Agent": "MyApp/1.0"}
        )
        js = r.json()
        return float(js[0]["lat"]), float(js[0]["lon"])
    except:
        return None

police_units = []
employees = []
incidents = []

root = Tk()
root.title("System zarządzania jednostkami Policji")
root.geometry("1240x760")
root.configure(bg=COLOR_BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
style.configure("TNotebook.Tab", padding=(15,8), font=('Arial', 11, 'bold'))
style.configure("TLabelframe", background=COLOR_FRAME, borderwidth=0)
style.configure("TLabelframe.Label", background=COLOR_FRAME)
style.configure("TLabel", background=COLOR_FRAME)
style.configure("TButton", font=("Arial", 10, "bold"), borderwidth=0, padding=6)
style.map("TButton", background=[("active", COLOR_BTN2)])

notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True, padx=15, pady=10)

tab_units = Frame(notebook, bg=COLOR_BG)
notebook.add(tab_units, text="Jednostki Policji")
tab_employees = Frame(notebook, bg=COLOR_BG)
notebook.add(tab_employees, text="Wszyscy funkcjonariusze")
tab_incidents = Frame(notebook, bg=COLOR_BG)
notebook.add(tab_incidents, text="Wszystkie incydenty")

# ----------- Panel Jednostki -----------
frame_left = Frame(tab_units, padx=8, pady=8, bg=COLOR_BG)
frame_left.pack(side=LEFT, fill=Y)
frame_map = Frame(tab_units, bg=COLOR_BG)
frame_map.pack(side=RIGHT, fill=BOTH, expand=True)

Label(frame_left, text="Jednostki policji", font=("Arial", 13, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG).pack(anchor="w", pady=(0,6))
frm_add_unit = LabelFrame(frame_left, text="Dodaj/edytuj jednostkę", bg=COLOR_FRAME)
frm_add_unit.pack(fill=X, pady=6, ipadx=2, ipady=2)
Label(frm_add_unit, text="Nazwa:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=0, column=0, sticky=W, pady=3)
entry_unit_name = Entry(frm_add_unit, width=22, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
entry_unit_name.grid(row=0, column=1, padx=5, pady=3)
Label(frm_add_unit, text="Lokalizacja:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=1, column=0, sticky=W, pady=3)
entry_unit_loc = Entry(frm_add_unit, width=22, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
entry_unit_loc.grid(row=1, column=1, padx=5, pady=3)

btn_add_unit = Button(frm_add_unit, text="Dodaj", width=11, bg=COLOR_BTN, fg="white", activebackground=COLOR_ACCENT, font=("Arial",10,"bold"), relief=FLAT, borderwidth=0)
btn_add_unit.grid(row=2, column=0, pady=7)
btn_edit_unit = Button(frm_add_unit, text="Zmień", width=11, bg=COLOR_BTN2, fg=COLOR_FONT, activebackground=COLOR_SHADOW, font=("Arial",10,"bold"), relief=FLAT, borderwidth=0, state=DISABLED)
btn_edit_unit.grid(row=2, column=1, pady=7)
btn_del_unit = Button(frm_add_unit, text="Usuń", width=11, bg=COLOR_BTN2, fg=COLOR_FONT, activebackground=COLOR_SHADOW, font=("Arial",10,"bold"), relief=FLAT, borderwidth=0, state=DISABLED)
btn_del_unit.grid(row=2, column=2, padx=4, pady=7)

Label(frame_left, text="Lista jednostek:", font=("Arial", 11), fg=COLOR_FONT, bg=COLOR_BG).pack(anchor="w", pady=(16,0))
listbox_units = Listbox(frame_left, height=10, bg=COLOR_LISTB, fg=COLOR_FONT, selectbackground=COLOR_ACCENT, borderwidth=0, highlightthickness=1, highlightbackground=COLOR_SHADOW, font=("Arial",10))
listbox_units.pack(fill=X, pady=4)
btn_unit_details = Button(frame_left, text="Szczegóły jednostki", bg=COLOR_BTN, fg="white", font=("Arial",10,"bold"), relief=FLAT, borderwidth=0, activebackground=COLOR_ACCENT)
btn_unit_details.pack(fill=X, pady=(4,8))

# --- Mapa z wszystkimi jednostkami ---
frame_map.config(bg=COLOR_SHADOW)
map_all_units = TkinterMapView(frame_map)
map_all_units.pack(fill=BOTH, expand=True, padx=10, pady=10)
map_all_units.set_position(52.2, 19.2)
map_all_units.set_zoom(6)
markers_units = []

def refresh_units_listbox():
    listbox_units.delete(0, END)
    for u in police_units:
        listbox_units.insert(END, f"{u['name']} ({u['location']})")
    global markers_units
    for m in markers_units: m.delete()
    markers_units = []
    # grupuj po lokalizacji (dla wszystkich jednostek)
    loc_groups = defaultdict(list)
    for u in police_units:
        coords = get_coordinates(u['location'])
        if coords:
            loc_groups[coords].append(u['name'])
    for c, names in loc_groups.items():
        markers_units.append(map_all_units.set_marker(
            *c, text="\n".join(names),
            marker_color_circle="#183463", marker_color_outside="#183463", text_color="#183463"
        ))

refresh_units_listbox()

def add_unit(event=None):
    name = entry_unit_name.get().strip()
    loc = entry_unit_loc.get().strip()
    if not name or not loc:
        messagebox.showwarning("Błąd", "Wypełnij oba pola!")
        return
    police_units.append({"name": name, "location": loc})
    refresh_units_listbox()
    entry_unit_name.delete(0, END)
    entry_unit_loc.delete(0, END)
    after_unit_update()

def select_unit_for_edit(event=None):
    sel = listbox_units.curselection()
    if not sel:
        btn_edit_unit.config(state=DISABLED)
        btn_del_unit.config(state=DISABLED)
        return
    idx = sel[0]
    u = police_units[idx]
    entry_unit_name.delete(0, END)
    entry_unit_loc.delete(0, END)
    entry_unit_name.insert(0, u['name'])
    entry_unit_loc.insert(0, u['location'])
    btn_edit_unit.config(state=NORMAL)
    btn_del_unit.config(state=NORMAL)

def edit_unit():
    sel = listbox_units.curselection()
    if not sel: return
    idx = sel[0]
    name = entry_unit_name.get().strip()
    loc = entry_unit_loc.get().strip()
    if not name or not loc:
        messagebox.showwarning("Błąd", "Wypełnij oba pola!")
        return
    police_units[idx] = {"name": name, "location": loc}
    refresh_units_listbox()
    entry_unit_name.delete(0, END)
    entry_unit_loc.delete(0, END)
    after_unit_update()

def del_unit():
    sel = listbox_units.curselection()
    if not sel: return
    idx = sel[0]
    if messagebox.askyesno("Potwierdź", "Usunąć jednostkę?"):
        police_units.pop(idx)
        refresh_units_listbox()
        entry_unit_name.delete(0, END)
        entry_unit_loc.delete(0, END)
        after_unit_update()

btn_add_unit.config(command=add_unit)
listbox_units.bind("<<ListboxSelect>>", select_unit_for_edit)
btn_edit_unit.config(command=edit_unit)
btn_del_unit.config(command=del_unit)
for widget in [entry_unit_name, entry_unit_loc]:
    widget.bind("<Return>", add_unit)

def show_unit_details():
    sel = listbox_units.curselection()
    if not sel:
        messagebox.showwarning("Błąd", "Wybierz jednostkę.")
        return
    idx = sel[0]
    unit = police_units[idx]
    win = Toplevel(root)
    win.title(f"Szczegóły: {unit['name']}")
    win.geometry("1040x690")
    win.config(bg=COLOR_BG)

    left = Frame(win, padx=10, pady=12, bg=COLOR_BG)
    left.pack(side=LEFT, fill=Y)
    right = Frame(win, bg=COLOR_BG)
    right.pack(side=RIGHT, fill=BOTH, expand=True)

    Label(left, text=f"Jednostka: {unit['name']} ({unit['location']})", font=("Arial", 12, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG).pack(anchor="w")

    Label(left, text="Funkcjonariusze tej jednostki:", font=("Arial", 11, "bold"), fg=COLOR_FONT, bg=COLOR_BG).pack(anchor="w", pady=(12,0))
    lb_emp = Listbox(left, height=7, bg=COLOR_LISTB, fg=COLOR_FONT, selectbackground=COLOR_ACCENT, borderwidth=0, highlightthickness=1, highlightbackground=COLOR_SHADOW, font=("Arial",10))
    lb_emp.pack(fill=X, pady=2)

    Label(left, text="Incydenty jednostki:", font=("Arial", 11, "bold"), fg=COLOR_FONT, bg=COLOR_BG).pack(anchor="w", pady=(12,0))
    lb_inc = Listbox(left, height=7, bg=COLOR_LISTB, fg=COLOR_FONT, selectbackground=COLOR_ACCENT, borderwidth=0, highlightthickness=1, highlightbackground=COLOR_SHADOW, font=("Arial",10))
    lb_inc.pack(fill=X, pady=2)

    map_det = TkinterMapView(right)
    map_det.pack(fill=BOTH, expand=True, padx=12, pady=12)

    def refresh_map_and_lists():
        lb_emp.delete(0, END)
        for e in employees:
            if e['unit'] == unit['name']:
                lb_emp.insert(END, f"{e['rank']} {e['name']} {e['surname']}")
        lb_inc.delete(0, END)
        for inc in incidents:
            if inc['unit'] == unit['name']:
                lb_inc.insert(END, f"{inc['date']} {inc['desc']} ({inc['location']})")
        map_det.delete_all_marker()
        coords = get_coordinates(unit['location'])
        if coords:
            map_det.set_position(*coords)
            map_det.set_zoom(10)
            # NIE dodawaj markera dla jednostki!
            # Grupuj funkcjonariuszy po lokalizacji:
            loc_groups_emp = defaultdict(list)
            for e in employees:
                if e['unit'] == unit['name']:
                    c = get_coordinates(e['location'])
                    if c:
                        loc_groups_emp[c].append(f"{e['rank']} {e['name']} {e['surname']}")
            for c, names in loc_groups_emp.items():
                map_det.set_marker(*c, text="\n".join(names), marker_color_circle="#183463", marker_color_outside="#183463", text_color="#183463")
            # Grupuj incydenty po lokalizacji:
            loc_groups_inc = defaultdict(list)
            for inc in incidents:
                if inc['unit'] == unit['name']:
                    c = get_coordinates(inc['location'])
                    if c:
                        loc_groups_inc[c].append(inc['desc'])
            for c, descs in loc_groups_inc.items():
                map_det.set_marker(*c, text="\n".join([f"Inc: {d}" for d in descs]), marker_color_circle="#15325f", marker_color_outside="#15325f", text_color="#15325f")

    frm_emp = LabelFrame(left, text="Dodaj/edytuj funkcjonariusza", bg=COLOR_FRAME)
    frm_emp.pack(fill=X, pady=8, ipadx=2, ipady=2)
    er1 = Entry(frm_emp, width=16, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
    er2 = Entry(frm_emp, width=16, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
    er3 = Entry(frm_emp, width=16, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
    Label(frm_emp, text="Stopień:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=0, column=0)
    er1.grid(row=0, column=1)
    Label(frm_emp, text="Imię:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=1, column=0)
    er2.grid(row=1, column=1)
    Label(frm_emp, text="Nazwisko:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=2, column=0)
    er3.grid(row=2, column=1)
    def add_emp(event=None):
        rk, nm, sn = er1.get().strip(), er2.get().strip(), er3.get().strip()
        if not rk or not nm or not sn: return
        employees.append({"rank": rk, "name": nm, "surname": sn, "unit": unit['name'], "location": unit['location']})
        er1.delete(0, END); er2.delete(0, END); er3.delete(0, END)
        refresh_map_and_lists(); refresh_all_employees(); refresh_map_employees()
    def edit_emp(event=None):
        idx = lb_emp.curselection()
        if not idx: return
        current = [e for e in employees if e['unit'] == unit['name']][idx[0]]
        current['rank'] = er1.get().strip()
        current['name'] = er2.get().strip()
        current['surname'] = er3.get().strip()
        refresh_map_and_lists(); refresh_all_employees(); refresh_map_employees()
    def del_emp():
        idx = lb_emp.curselection()
        if not idx: return
        all_idx = [i for i,e in enumerate(employees) if e['unit']==unit['name']]
        employees.pop(all_idx[idx[0]])
        refresh_map_and_lists(); refresh_all_employees(); refresh_map_employees()
    Button(frm_emp, text="Dodaj", command=add_emp, width=9, bg=COLOR_BTN, fg="white", relief=FLAT, borderwidth=0).grid(row=3, column=0, pady=4)
    Button(frm_emp, text="Edytuj", command=edit_emp, width=9, bg=COLOR_BTN2, fg=COLOR_FONT, relief=FLAT, borderwidth=0).grid(row=3, column=1, pady=4)
    Button(frm_emp, text="Usuń", command=del_emp, width=9, bg=COLOR_BTN2, fg=COLOR_FONT, relief=FLAT, borderwidth=0).grid(row=3, column=2, padx=3)
    for widget in [er1, er2, er3]: widget.bind("<Return>", add_emp)
    lb_emp.bind("<<ListboxSelect>>", lambda e: (
        er1.delete(0, END), er2.delete(0, END), er3.delete(0, END),
        er1.insert(0, employees[[i for i,e in enumerate(employees) if e['unit']==unit['name']][lb_emp.curselection()[0]]]['rank']) if lb_emp.curselection() else None,
        er2.insert(0, employees[[i for i,e in enumerate(employees) if e['unit']==unit['name']][lb_emp.curselection()[0]]]['name']) if lb_emp.curselection() else None,
        er3.insert(0, employees[[i for i,e in enumerate(employees) if e['unit']==unit['name']][lb_emp.curselection()[0]]]['surname']) if lb_emp.curselection() else None
    ))

    frm_inc = LabelFrame(left, text="Dodaj/edytuj incydent", bg=COLOR_FRAME)
    frm_inc.pack(fill=X, pady=8, ipadx=2, ipady=2)
    ei1 = Entry(frm_inc, width=16, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
    ei2 = Entry(frm_inc, width=16, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
    ei3 = Entry(frm_inc, width=16, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
    Label(frm_inc, text="Opis:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=0, column=0)
    ei1.grid(row=0, column=1)
    Label(frm_inc, text="Lokalizacja:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=1, column=0)
    ei2.grid(row=1, column=1)
    Label(frm_inc, text="Data:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=2, column=0)
    ei3.grid(row=2, column=1)
    def add_inc(event=None):
        desc, loc, date = ei1.get().strip(), ei2.get().strip(), ei3.get().strip()
        if not desc or not loc or not date: return
        incidents.append({"desc": desc, "location": loc, "date": date, "unit": unit['name']})
        ei1.delete(0, END); ei2.delete(0, END); ei3.delete(0, END)
        refresh_map_and_lists(); refresh_all_incidents(); refresh_map_incidents()
    def edit_inc(event=None):
        idx = lb_inc.curselection()
        if not idx: return
        current = [i for i,inc in enumerate(incidents) if inc['unit']==unit['name']][idx[0]]
        inc_obj = incidents[current]
        inc_obj['desc'] = ei1.get().strip()
        inc_obj['location'] = ei2.get().strip()
        inc_obj['date'] = ei3.get().strip()
        refresh_map_and_lists(); refresh_all_incidents(); refresh_map_incidents()
    def del_inc():
        idx = lb_inc.curselection()
        if not idx: return
        all_idx = [i for i,inc in enumerate(incidents) if inc['unit']==unit['name']]
        incidents.pop(all_idx[idx[0]])
        refresh_map_and_lists(); refresh_all_incidents(); refresh_map_incidents()
    Button(frm_inc, text="Dodaj", command=add_inc, width=9, bg=COLOR_BTN, fg="white", relief=FLAT, borderwidth=0).grid(row=3, column=0, pady=4)
    Button(frm_inc, text="Edytuj", command=edit_inc, width=9, bg=COLOR_BTN2, fg=COLOR_FONT, relief=FLAT, borderwidth=0).grid(row=3, column=1, pady=4)
    Button(frm_inc, text="Usuń", command=del_inc, width=9, bg=COLOR_BTN2, fg=COLOR_FONT, relief=FLAT, borderwidth=0).grid(row=3, column=2, padx=3)
    for widget in [ei1, ei2, ei3]: widget.bind("<Return>", add_inc)
    lb_inc.bind("<<ListboxSelect>>", lambda e: (
        ei1.delete(0, END), ei2.delete(0, END), ei3.delete(0, END),
        ei1.insert(0, incidents[[i for i,inc in enumerate(incidents) if inc['unit']==unit['name']][lb_inc.curselection()[0]]]['desc']) if lb_inc.curselection() else None,
        ei2.insert(0, incidents[[i for i,inc in enumerate(incidents) if inc['unit']==unit['name']][lb_inc.curselection()[0]]]['location']) if lb_inc.curselection() else None,
        ei3.insert(0, incidents[[i for i,inc in enumerate(incidents) if inc['unit']==unit['name']][lb_inc.curselection()[0]]]['date']) if lb_inc.curselection() else None
    ))

    refresh_map_and_lists()

btn_unit_details.config(command=show_unit_details)

# ==================== ZAKŁADKA "WSZYSCY FUNKCJONARIUSZE" ====================
frame_left_emp = Frame(tab_employees, padx=8, pady=8, bg=COLOR_BG)
frame_left_emp.pack(side=LEFT, fill=Y)
frame_map_emp = Frame(tab_employees, bg=COLOR_BG)
frame_map_emp.pack(side=RIGHT, fill=BOTH, expand=True)
Label(frame_left_emp, text="Funkcjonariusze", font=("Arial", 13, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG).pack(anchor="w")
lb_all_emp = Listbox(frame_left_emp, height=14, bg=COLOR_LISTB, fg=COLOR_FONT, selectbackground=COLOR_ACCENT, borderwidth=0, highlightthickness=1, highlightbackground=COLOR_SHADOW, font=("Arial",10))
lb_all_emp.pack(fill=X, pady=3)

frm_add_emp = LabelFrame(frame_left_emp, text="Dodaj funkcjonariusza", bg=COLOR_FRAME)
frm_add_emp.pack(fill=X, pady=8, ipadx=2, ipady=2)
emp_unit = StringVar()
Label(frm_add_emp, text="Jednostka:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=0, column=0)
emp_unit_menu = ttk.Combobox(frm_add_emp, textvariable=emp_unit, state="readonly")
emp_unit_menu.grid(row=0, column=1)
emp_unit_menu['values'] = []
erank = Entry(frm_add_emp, width=15, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
ename = Entry(frm_add_emp, width=15, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
esurname = Entry(frm_add_emp, width=15, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
Label(frm_add_emp, text="Stopień:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=1, column=0)
erank.grid(row=1, column=1)
Label(frm_add_emp, text="Imię:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=2, column=0)
ename.grid(row=2, column=1)
Label(frm_add_emp, text="Nazwisko:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=3, column=0)
esurname.grid(row=3, column=1)
def add_emp_all(event=None):
    u = emp_unit.get()
    if not u: return
    rk, nm, sn = erank.get().strip(), ename.get().strip(), esurname.get().strip()
    if not rk or not nm or not sn: return
    loc = next((p['location'] for p in police_units if f"{p['name']} ({p['location']})"==u), "")
    employees.append({"rank": rk, "name": nm, "surname": sn, "unit": u.split(' (')[0], "location": loc})
    erank.delete(0, END); ename.delete(0, END); esurname.delete(0, END)
    refresh_all_employees(); refresh_map_employees()
Button(frm_add_emp, text="Dodaj", command=add_emp_all, bg=COLOR_BTN, fg="white", relief=FLAT, borderwidth=0, width=12).grid(row=4, column=0, columnspan=2, pady=6)
for widget in [erank, ename, esurname]:
    widget.bind("<Return>", add_emp_all)

def refresh_all_employees():
    emp_unit_menu['values'] = [f"{u['name']} ({u['location']})" for u in police_units]
    lb_all_emp.delete(0, END)
    for e in employees:
        lb_all_emp.insert(END, f"{e['rank']} {e['name']} {e['surname']} ({e['unit']})")
refresh_all_employees()

map_emp = TkinterMapView(frame_map_emp)
map_emp.pack(fill=BOTH, expand=True, padx=10, pady=10)
map_emp.set_position(52.2, 19.2)
map_emp.set_zoom(6)
markers_emps = []

def refresh_map_employees():
    global markers_emps
    for m in markers_emps: m.delete()
    markers_emps = []
    loc_groups = defaultdict(list)
    for e in employees:
        coords = get_coordinates(e['location'])
        if coords:
            loc_groups[coords].append(f"{e['rank']} {e['name']} {e['surname']}")
    for c, names in loc_groups.items():
        markers_emps.append(map_emp.set_marker(*c, text="\n".join(names), marker_color_circle="#183463", marker_color_outside="#183463", text_color="#183463"))

refresh_map_employees()

# ==================== ZAKŁADKA "WSZYSTKIE INCYDENTY" ====================
frame_left_inc = Frame(tab_incidents, padx=8, pady=8, bg=COLOR_BG)
frame_left_inc.pack(side=LEFT, fill=Y)
frame_map_inc = Frame(tab_incidents, bg=COLOR_BG)
frame_map_inc.pack(side=RIGHT, fill=BOTH, expand=True)
Label(frame_left_inc, text="Wszystkie incydenty", font=("Arial", 13, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG).pack(anchor="w")
lb_all_inc = Listbox(frame_left_inc, height=14, bg=COLOR_LISTB, fg=COLOR_FONT, selectbackground=COLOR_ACCENT, borderwidth=0, highlightthickness=1, highlightbackground=COLOR_SHADOW, font=("Arial",10))
lb_all_inc.pack(fill=X, pady=3)

frm_add_inc = LabelFrame(frame_left_inc, text="Dodaj incydent", bg=COLOR_FRAME)
frm_add_inc.pack(fill=X, pady=8, ipadx=2, ipady=2)
inc_unit = StringVar()
Label(frm_add_inc, text="Jednostka:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=0, column=0)
inc_unit_menu = ttk.Combobox(frm_add_inc, textvariable=inc_unit, state="readonly")
inc_unit_menu.grid(row=0, column=1)
inc_unit_menu['values'] = []
eidesc = Entry(frm_add_inc, width=15, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
eiloc = Entry(frm_add_inc, width=15, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
eidate = Entry(frm_add_inc, width=15, bg="#f6faff", relief=FLAT, highlightthickness=1, highlightbackground=COLOR_SHADOW)
Label(frm_add_inc, text="Opis:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=1, column=0)
eidesc.grid(row=1, column=1)
Label(frm_add_inc, text="Lokalizacja:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=2, column=0)
eiloc.grid(row=2, column=1)
Label(frm_add_inc, text="Data:", fg=COLOR_FONT, bg=COLOR_FRAME).grid(row=3, column=0)
eidate.grid(row=3, column=1)
def add_inc_all(event=None):
    u = inc_unit.get()
    if not u: return
    desc, loc, date = eidesc.get().strip(), eiloc.get().strip(), eidate.get().strip()
    if not desc or not loc or not date: return
    incidents.append({"desc": desc, "location": loc, "date": date, "unit": u.split(' (')[0]})
    eidesc.delete(0, END); eiloc.delete(0, END); eidate.delete(0, END)
    refresh_all_incidents(); refresh_map_incidents()
Button(frm_add_inc, text="Dodaj", command=add_inc_all, bg=COLOR_BTN, fg="white", relief=FLAT, borderwidth=0, width=12).grid(row=4, column=0, columnspan=2, pady=6)
for widget in [eidesc, eiloc, eidate]:
    widget.bind("<Return>", add_inc_all)

def refresh_all_incidents():
    inc_unit_menu['values'] = [f"{u['name']} ({u['location']})" for u in police_units]
    lb_all_inc.delete(0, END)
    for inc in incidents:
        lb_all_inc.insert(END, f"{inc['date']} {inc['desc']} ({inc['location']}) – {inc['unit']}")
refresh_all_incidents()

map_inc = TkinterMapView(frame_map_inc)
map_inc.pack(fill=BOTH, expand=True, padx=10, pady=10)
map_inc.set_position(52.2, 19.2)
map_inc.set_zoom(6)
markers_inc = []
def refresh_map_incidents():
    global markers_inc
    for m in markers_inc: m.delete()
    markers_inc = []
    loc_groups = defaultdict(list)
    for inc in incidents:
        coords = get_coordinates(inc['location'])
        if coords:
            loc_groups[coords].append(inc['desc'])
    for c, descs in loc_groups.items():
        markers_inc.append(map_inc.set_marker(*c, text="\n".join([f"Inc: {d}" for d in descs]), marker_color_circle="#15325f", marker_color_outside="#15325f", text_color="#15325f"))

refresh_map_incidents()

def after_unit_update():
    refresh_units_listbox()
    refresh_all_employees()
    refresh_all_incidents()
    refresh_map_employees()
    refresh_map_incidents()

btn_add_unit.config(command=lambda: [add_unit(), after_unit_update()])
btn_edit_unit.config(command=lambda: [edit_unit(), after_unit_update()])
btn_del_unit.config(command=lambda: [del_unit(), after_unit_update()])

root.mainloop()
