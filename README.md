# beagle-gnome-search
A search tool for GNOME, written in Python3 and Gtk3.
Two search screens currently available: base and simple

#Base search
Just type and search. It will search for all file types without size limitation and ignoring the case of the typed name.
![base_search](https://cloud.githubusercontent.com/assets/5099266/20641238/1d4390ec-b3f4-11e6-9332-fb7ae71da235.png)

#Simple search
In this section you can configure some search parameters, as shown in the screenshot.
![simple_search](https://cloud.githubusercontent.com/assets/5099266/21052736/b90db476-be26-11e6-8276-42de853cb83f.png)

Getting beogle-gnome-search:
```bash
git clone https://github.com/vinsce/beagle-gnome-search.git
cd beagle-gnome-search/
python3 source/app.py
```
ebuild for Gentoo Linux (thanks to mrbitt): https://github.com/mrbitt/mrbit-overlay/blob/master/gnome-extra/beagle-gnome-search/beagle-gnome-search-0.1.1.ebuild
