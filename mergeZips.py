# I am usuing it pasted in jupyter

import zipfile as z

zips = ['z1.zip', 'z2.zip', 'z3.zip']

"""
Open the first zip file as append and then read all
subsequent zip files and append to the first one
"""
with z.ZipFile(zips[0], 'a') as z1:
    for fname in zips[1:]:
        zf = z.ZipFile(fname, 'r')
        for n in zf.namelist():
            z1.writestr(n, zf.open(n).read())
