import matplotlib.pyplot as plt
# points = [[783, 919], [1510, 963], [1440, 335], [203, 426]]
points = [[494, 465], [1391, 427]]
# plot points on a 1920x1080 grid
# plot the points
fig, ax = plt.subplots()
ax.plot([points[0][0], points[1][0]], [points[0][1], points[1][1]], 'r')
# invert y axis
# set axes ranges to 0 to 1920 and 0 to 1080

ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.invert_yaxis()
plt.show()