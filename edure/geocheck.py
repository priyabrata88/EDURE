import geocoder
a = raw_input('')
g = geocoder.google(a)
print g.latlng[0]
print g.latlng[1]

