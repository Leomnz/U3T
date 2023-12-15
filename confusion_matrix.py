import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

win_array = [[436, 482, 500, 488],
             [14, 0, 73, 459],
             [1, 81, 73, 92],
             [3, 16, 425, 368]]

loss_array = [[372, 7, 0, 2],
              [477, 500, 5, 24],
              [499, 408, 47, 393],
              [484, 468, 67, 278]]

final_array = np.divide(win_array, np.add(win_array, loss_array))
# add a % to each element
print(final_array)

df_cm = pd.DataFrame(final_array, index=["Random", "Alpha-Beta", "MCTS", "Heatmap"],
                     columns=["Random", "Alpha-Beta", "MCTS", "Heatmap"])
plt.figure(figsize=(10, 7))
sn.set(font_scale=1.4)  # for label size
cmap = sn.diverging_palette(10, 200, as_cmap=True)
sn.heatmap(df_cm, annot=True, annot_kws={"size": 20},cmap=cmap)  # font size
plt.title("Win rate for Each Agent", fontsize=20, pad=20)
plt.xlabel("First Player", fontsize=20, labelpad=10, ha='center', rotation=0)
plt.ylabel("Second Player", fontsize=20, labelpad=10, ha='center', rotation=90)
plt.tick_params(axis='x', which='major', labelbottom=False, labeltop=True)
plt.show()
