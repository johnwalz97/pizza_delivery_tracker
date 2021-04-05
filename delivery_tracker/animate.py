from math import ceil, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from delivery_tracker import process_moves

# agents here are just a list of format strings for matplotlib
agents = ['-ro', '--bo', '-.go']

num_houses, deliveries, grid_diagonal = process_moves(
    moves_file=Path('/home/jwalz/Code/Personal/PizzaDeliverySystem/input.txt'),
    num_agents=len(agents),
)

# calculate size of plot based on length of grid diagonal
(x1, y1), (x2, y2) = grid_diagonal
plot_size = ceil(sqrt((x2 - x1)**2 + (y2 - y1)**2)) / 2
plt.figure(figsize=(plot_size, plot_size), dpi=100)

# add title with info about the deliveries
plt.text(x2, y2, f'{num_houses} Unique Deliveries', fontsize=plot_size/1.5 if plot_size > 12 else 12)

# loop through agents and plot their deliveries
for agent_index, agent_color in enumerate(agents):
    agent_deliveries = deliveries[deliveries[:, 2] == agent_index]
    agent_deliveries = np.insert(agent_deliveries, 0, [0, 0, agent_index], axis=0)

    plt.plot(
        agent_deliveries[:, 0],
        agent_deliveries[:, 1],
        agent_color,
        linewidth=agent_index + 3,
        alpha=0.5,
    )

# plot center so its easier to see where the agents started
plt.plot(0, 0, 's', color='black', markersize=10)

plt.axis('off')
plt.savefig('animation.png', bbox_inches='tight')
