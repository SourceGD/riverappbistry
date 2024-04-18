from matplotlib import pyplot as plt

#
# P1_v1 = [852, 971]
# P2_v1 = [1510, 963]
# P3_v1 = [1449, 340]
# P4_v1 = [216, 400]
#
# P1_v2 = [1523, 117]
# P2_v2 = [1455, 748]
# P3_v2 = [203, 650]
# P4_v2 = [768, 155]
#
# # plotting the points and linking them in the order of the points
# plt.plot([P1_v1[0], P2_v1[0], P3_v1[0], P4_v1[0], P1_v1[0]], [P1_v1[1], P2_v1[1], P3_v1[1], P4_v1[1], P1_v1[1]], 'r')
# # subplot the second plot
# plt.plot([P1_v2[0], P2_v2[0], P3_v2[0], P4_v2[0], P1_v2[0]], [P1_v2[1], P2_v2[1], P3_v2[1], P4_v2[1], P1_v2[1]], 'b')
# plt.gca().invert_yaxis()
#
# plt.text(P1_v1[0], P1_v1[1], 'P1', fontsize=12, color='red')
# plt.text(P2_v1[0], P2_v1[1], 'P2', fontsize=12, color='red')
# plt.text(P3_v1[0], P3_v1[1], 'P3', fontsize=12, color='red')
# plt.text(P4_v1[0], P4_v1[1], 'P4', fontsize=12, color='red')
#
# plt.text(P1_v2[0], P1_v2[1], 'P1', fontsize=12, color='blue')
# plt.text(P2_v2[0], P2_v2[1], 'P2', fontsize=12, color='blue')
# plt.text(P3_v2[0], P3_v2[1], 'P3', fontsize=12, color='blue')
# plt.text(P4_v2[0], P4_v2[1], 'P4', fontsize=12, color='blue')
# # legend for the plot
# plt.legend(["Version d'Arnaud", "RiverApp V2"])
# plt.savefig('transect.png')
#
# plt.show()
# plot to png


# points = [[494, 465], [1391, 427]]
# # plot points on a 1920x1080 grid
# plt.plot([points[0][0], points[1][0]], [points[0][1], points[1][1]], 'r')
# # set x range from 0 to 1920 and y range from 0 to 1080
# # INVERT Y AXIS
# plt.gca().invert_yaxis()
# plt.xlim(0, 1920)
# plt.ylim(0, 1080)
# plt.show()


# points = [(6.707273355354496, 5.954018841911765),
#           (6.743281099358046, -0.34245804028132865),
#           (1.203125, -0.34375),
#           (1.203125, 6.132187500000001)]
# lens_position = [7, -2]
#
# # plot points on a grid
# plt.plot([points[0][0], points[1][0], points[2][0], points[3][0], points[0][0]],
#          [points[0][1], points[1][1], points[2][1], points[3][1], points[0][1]], 'r')
# # add lens position
# plt.plot(lens_position[0], lens_position[1], 'bo')
# # invert grid
# plt.gca().invert_yaxis()
# plt.show()
#
transect_points = [[-0.17580663, 1.0084325],
                   [1.5961611, 1.3885338]]

points2 = [[1.6349489777122168, 2.5629166666666667], [1.4892907950698857, 0.17892156862745123], [0, 0],
           [0, 2.55]]  # get center of 4 points
x = (points2[0][0] + points2[1][0] + points2[2][0] + points2[3][0]) / 4
y = (points2[0][1] + points2[1][1] + points2[2][1] + points2[3][1]) / 4
lens_position = [2.5, 0.5]
print(x, " ", y)
# plot points on a grid
plt.plot([points2[0][0], points2[1][0], points2[2][0], points2[3][0], points2[0][0]],
         [points2[0][1], points2[1][1], points2[2][1], points2[3][1], points2[0][1]], 'r')
# add lens position
#plt.plot(lens_position[0], lens_position[1], 'bo')
# plot transect as a line
plt.plot([transect_points[0][0], transect_points[1][0]], [transect_points[0][1], transect_points[1][1]], 'g')
# invert grid
plt.show()

## AVEC LES COORDONNEES INVERSEES
# points = [(3.1776889712456136, 1.250833333333333), (3.0739153303931377, -0.44763527728688035), (2.0128755364806867, -0.5751072961373391), (2.0128755364806867, 1.2416309012875533)]
# lens_position = [2.5, 0.5]
#
# # plot points on a grid
# plt.plot([points[0][0], points[1][0], points[2][0], points[3][0], points[0][0]],
#          [points[0][1], points[1][1], points[2][1], points[3][1], points[0][1]], 'r')
# # add lens position
# plt.plot(lens_position[0], lens_position[1], 'bo')
# # invert grid
# plt.show()


transect_points = [[0.1569639, 2.2067773],
                   [6.1345754, 2.1755385]]

points2 = [[6.646518768729957, 7.60485294117647], [6.689999818092734, 0.0015601023017917583], [0, 0], [0, 7.82]]
# get center of 4 points
x = (points2[0][0] + points2[1][0] + points2[2][0] + points2[3][0]) / 4
y = (points2[0][1] + points2[1][1] + points2[2][1] + points2[3][1]) / 4
lens_position = [7, -2]

# print distance between P2 and P4
p2top4 = ((points2[1][0] - points2[3][0]) ** 2 + (points2[1][1] - points2[3][1]) ** 2) ** 0.5
# label distance between P2 and P4
plt.text(x, y, f'{p2top4:.2f}', fontsize=12, color='black')
print(x, " ", y)
# plot points on a grid
plt.plot([points2[0][0], points2[1][0], points2[2][0], points2[3][0], points2[0][0]],
         [points2[0][1], points2[1][1], points2[2][1], points2[3][1], points2[0][1]], 'r')
# add lens position
plt.plot(lens_position[0], lens_position[1], 'bo')
# plot transect as a line
plt.plot([transect_points[0][0], transect_points[1][0]], [transect_points[0][1], transect_points[1][1]], 'g')
# invert grid
plt.savefig('setup_vgc.png')
plt.show()

## WITHOUT INVERTED COORDINATES
points = [[2.453425244255791, 1.3493348623853203], [2.549920423954833, -0.02014525993883787], [0, 0], [0, 1.635]]
lens_position = [1.25, 0.75]
transect = [[-0.17838277, 0.53786594], [2.387818, 0.7043685]]
# plot points on a grid
plt.plot([points[0][0], points[1][0], points[2][0], points[3][0], points[0][0]],
         [points[0][1], points[1][1], points[2][1], points[3][1], points[0][1]], 'r')
# add lens position
plt.plot(lens_position[0], lens_position[1], 'bo')
# plot transect as a line
plt.plot([transect[0][0], transect[1][0]], [transect[0][1], transect[1][1]], 'g')
plt.show()


## WITH POINT OF VIEW FIEW METERS AWAY FROM CENTER AND 45 DEGREES
points = [[2.453425244255791, 1.3493348623853203], [2.549920423954833, -0.02014525993883787], [0, 0], [0, 1.635]]
lens_position = [1.25, -2]
transect = [[-0.17838277, 0.53786594], [2.387818, 0.7043685]]
# plot points on a grid
plt.plot([points[0][0], points[1][0], points[2][0], points[3][0], points[0][0]],
         [points[0][1], points[1][1], points[2][1], points[3][1], points[0][1]], 'r')
# add lens position
plt.plot(lens_position[0], lens_position[1], 'bo')
# plot transect as a line
plt.plot([transect[0][0], transect[1][0]], [transect[0][1], transect[1][1]], 'g')
plt.show()

