import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig2 = plt.figure()
ax2 = fig2.add_subplot(111, aspect='equal')
ax2.add_patch(
    patches.Circle(
        (0.5, 0.5),
        0.2,
        fill=False      # remove background
    )
)
plt.show()