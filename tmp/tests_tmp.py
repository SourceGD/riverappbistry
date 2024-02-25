import matplotlib.pyplot as plt
points = [[783, 919], [1510, 963], [1440, 335], [203, 426]]

# plot the points
fig, ax = plt.subplots()
ax.plot(*zip(*points), marker='o', color='r', ls='')
# invert y axis
ax.invert_yaxis()
plt.show()