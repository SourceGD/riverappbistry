from matplotlib import pyplot as plt

P1_v1 = [852, 971]
P2_v1 = [1510, 963]
P3_v1 = [1449, 340]
P4_v1 = [216, 400]

P1_v2 = [1523, 117]
P2_v2 = [1455, 748]
P3_v2 = [203, 650]
P4_v2 = [768, 155]

# plotting the points and linking them in the order of the points
plt.plot([P1_v1[0], P2_v1[0], P3_v1[0], P4_v1[0], P1_v1[0]], [P1_v1[1], P2_v1[1], P3_v1[1], P4_v1[1], P1_v1[1]], 'r')
# subplot the second plot
plt.plot([P1_v2[0], P2_v2[0], P3_v2[0], P4_v2[0], P1_v2[0]], [P1_v2[1], P2_v2[1], P3_v2[1], P4_v2[1], P1_v2[1]], 'b')
plt.gca().invert_yaxis()

plt.text(P1_v1[0], P1_v1[1], 'P1', fontsize=12, color='red')
plt.text(P2_v1[0], P2_v1[1], 'P2', fontsize=12, color='red')
plt.text(P3_v1[0], P3_v1[1], 'P3', fontsize=12, color='red')
plt.text(P4_v1[0], P4_v1[1], 'P4', fontsize=12, color='red')

plt.text(P1_v2[0], P1_v2[1], 'P1', fontsize=12, color='blue')
plt.text(P2_v2[0], P2_v2[1], 'P2', fontsize=12, color='blue')
plt.text(P3_v2[0], P3_v2[1], 'P3', fontsize=12, color='blue')
plt.text(P4_v2[0], P4_v2[1], 'P4', fontsize=12, color='blue')
# legend for the plot
plt.legend(["Version d'Arnaud", "RiverApp V2"])
plt.savefig('transect.png')

plt.show()
# plot to png

