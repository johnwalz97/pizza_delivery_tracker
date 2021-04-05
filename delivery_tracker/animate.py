from pathlib import Path

import matplotlib.pyplot as plt

from delivery_tracker import process_moves


_, deliveries, _ = process_moves(moves_file=Path('/home/jwalz/Code/Personal/PizzaDeliverySystem/input.txt'))

fig, ax = plt.subplots()

plt.figure(figsize=(30, 30))
plt.plot(deliveries[:, 0], deliveries[:, 1], '-o')
plt.axis('off')

plt.savefig('animation.png', bbox_inches=0, dpi=100)
