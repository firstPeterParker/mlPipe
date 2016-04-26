import os

dirs = os.listdir('/users/matthew/desktop/')

maFls = []

for dir in dirs:
    if dir.endswith('.ma'):
        maFls.append(dir)

print maFls