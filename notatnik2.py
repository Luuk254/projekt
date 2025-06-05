from tkinter import *

import tkintermapview

users:list = []

root = Tk()
root.title("System do zarządzania jednostkami policji i policjantami przypisanymi do danej jednostki")
root.geometry("1024x768")

ramka_lista_jednostek= Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_jednostki = Frame(root)
ramka_mapa = Frame(root)
ramka_incydenty = Frame(root)
ramka_incydenty_jednostki = Frame(root)
ramka_funkcjonariusze = Frame(root)
ramka_dane_funkcjonariusza = Frame(root)



ramka_lista_jednostek.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_jednostki.grid(row=1, column=0)
ramka_mapa.grid(row=2, column=0, columnspan=2)
ramka_incydenty.grid(row=3, column=0)
ramka_incydenty_jednostki.grid(row=4, column=0)
ramka_funkcjonariusze.grid(row=5, column=0)
ramka_dane_funkcjonariusza.grid(row=6, column=0)

#jednostki
label_lista_jednostek=Label(ramka_lista_jednostek, text="Lista jednostek: ")
label_lista_jednostek.grid(row=0, column=0, columnspan=3)
listbox_lista_jednostek= Listbox(ramka_lista_jednostek)
listbox_lista_jednostek.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly= Button(ramka_lista_jednostek, text="Pokaż szczegóły jednostki", command=user_details)
button_pokaz_szczegoly.grid(row=2, column=0)
button_edytuj_obiekt= Button(ramka_lista_jednostek, text="Edytuj obiekt", command=edit_user)
button_edytuj_obiekt.grid(row=2, column=1)
button_usun_obiekt= Button(ramka_lista_jednostek, text="Usuń obiekt", command=delete_user)
button_usun_obiekt.grid(row=2, column=2)

#incydenty
label_lista_incydentow=Label(ramka_incydenty, text="Lista wszystkich incydentów: ")
label_lista_incydentow.grid(row=0, column=0, columnspan=2)
listbox_lista_incydentow= Listbox(ramka_incydenty)
listbox_lista_incydentow.grid(row=1, column=0, columnspan=2)
button_dodaj_incydent= Button(ramka_incydenty, text="Dodaj incydent", command=add_incident)
button_dodaj_incydent.grid(row=2, column=0)
button_usun_incydent= Button(ramka_incydenty, text="Usuń incydent", command=delete_incident)
button_usun_incydent.grid(row=2, column=1)

#incydenty jednostki
label_lista_incydentow_jednostki= Label(ramka_incydenty_jednostki, text="Lista wszystkich incydentów jednostki: ")
label_lista_incydentow_jednostki.grid(row=0, column=0, columnspan=2)
listbox_lista_incydentow_jednostki= Listbox(ramka_incydenty_jednostki)
listbox_lista_incydentow_jednostki.grid(row=1, column=0, columnspan=2)

#funkcjonariusze
label_lista_funkcjonariuszy= Label(ramka_funkcjonariusze, text="Lista funkcjonariuszy: ")
label_lista_funkcjonariuszy.grid(row=0, column=0, columnspan=4)
listbox_lista_funkcjonariusze= Listbox(ramka_funkcjonariusze)
listbox_lista_funkcjonariusze.grid(row=1, column=0, columnspan=4)
button_dodaj_funkcjonariusza= Button(ramka_funkcjonariusze, text="Dodaj funkcjonariusza", command=add_user)
button_dodaj_funkcjonariusza.grid(row=2, column=0)
button_edytuj_funkcjonariusza= Button(ramka_funkcjonariusze, text="Edytuj dane", command=edit_user)
button_edytuj_funkcjonariusza.grid(row=2, column=1)
button_usun_funkcjonariusza= Button(ramka_funkcjonariusze, text="Usuń funkcjonariusza", command=delete_user)
button_usun_funkcjonariusza.grid(row=2, column=2)
button_pokaz_szczegoly_funkcjonariusza= Button(ramka_funkcjonariusze, text="Pokaż dane", command=user_details)
button_pokaz_szczegoly_funkcjonariusza.grid(row=3, column=0)





label_formularz= Label(ramka_formularz, text="Formularz: ")
label_formularz.grid(row=0, column=0, columnspan=2)
label_rank= Label(ramka_formularz, text="Stopień: ")
label_rank.grid(row=1, column=0, sticky=W)
label_name= Label(ramka_formularz, text="Imię: ")
label_name.grid(row=2, column=0, sticky=W)
label_surname= Label(ramka_formularz, text="Nazwisko: ")
label_surname.grid(row=3, column=0, sticky=W)
label_police_unit= Label(ramka_formularz, text="Jednostka policji: ")
label_police_unit.grid(row=4, column=0, sticky=W)
label_location= Label(ramka_formularz, text="Miejscowość: ")
label_location.grid(row=5, column=0, sticky=W)

entry_rank= Entry(ramka_formularz)
entry_rank.grid(row=1, column=1)
entry_name= Entry(ramka_formularz)
entry_name.grid(row=2, column=1)
entry_surname= Entry(ramka_formularz)
entry_surname.grid(row=3, column=1)
entry_police_unit= Entry(ramka_formularz)
entry_police_unit.grid(row=4, column=1)
entry_location= Entry(ramka_formularz)
entry_location.grid(row=5, column=1)

button_dodaj_obiekt= Button(ramka_formularz, text="Dodaj", command=add_user)
button_dodaj_obiekt.grid(row=5, column=1, columnspan=2)





#szczegóły jednostki
label_szczegoly= Label(ramka_szczegoly_jednostki, text="Szczegóły jednostki: ")
label_szczegoly.grid(row=0, column=0, sticky=W)

label_police_unit= Label(ramka_szczegoly_jednostki, text="Jednostka policji: ")
label_police_unit.grid(row=1, column=0, sticky=W)
label_police_unit_wartosc= Label(ramka_szczegoly_jednostki, text=".....")
label_police_unit_wartosc.grid(row=1, column=1, sticky=W)

label_location= Label(ramka_szczegoly_jednostki, text="Miejscowość: ")
label_location.grid(row=2, column=0, sticky=W)
label_location_wartosc= Label(ramka_szczegoly_jednostki, text=".....")
label_location_wartosc.grid(row=2, column=1, sticky=W)





#dane funkcjonariusza
label_dane_funkcjonariusza= Label(ramka_dane_funkcjonariusza, text="Dane funkcjonariusza: ")
label_dane_funkcjonariusza.grid(row=0, column=0, sticky=W)

label_police_officer_rank= Label(ramka_dane_funkcjonariusza, text="Stopień: ")
label_police_officer_rank.grid(row=1, column=0, sticky=W)
label_police_officer_rank_wartosc= Label(ramka_dane_funkcjonariusza, text=".....")
label_police_officer_rank_wartosc.grid(row=1, column=1, sticky=W)

label_police_officer_name= Label(ramka_dane_funkcjonariusza, text="Imię: ")
label_police_officer_name.grid(row=2, column=0, sticky=W)
label_police_officer_name_wartosc= Label(ramka_dane_funkcjonariusza, text=".....")
label_police_officer_name_wartosc.grid(row=2, column=1, sticky=W)

label_police_officer_surname= Label(ramka_dane_funkcjonariusza, text="Nazwisko: ")
label_police_officer_surname.grid(row=3, column=0, sticky=W)
label_police_officer_surname_wartosc= Label(ramka_dane_funkcjonariusza, text=".....")
label_police_officer_surname_wartosc.grid(row=3, column=1, sticky=W)




map_widget= tkintermapview.TkinterMapView(ramka_mapa, width=1024, height=400)
map_widget.set_position(52.23, 21)
map_widget.set_zoom(5)
map_widget.grid(row=0, column=0, columnspan=8)

root.mainloop()





