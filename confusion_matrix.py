import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

array = [[13, 1, 1, 0],
         [3, 9, 6, 0],
         [0, 0, 16, 2],
         [0, 0, 0, 13]]

df_cm = pd.DataFrame(array, index=["Alpha-Beta", "Random Player", "Heatmap", "MCTS"],
                     columns=["Alpha-Beta", "Random Player", "Heatmap", "MCTS"])
plt.figure(figsize=(10,7))
sn.set(font_scale=1.4)  # for label size

sn.heatmap(df_cm, annot=True, annot_kws={"size": 20})  # font size

plt.show()
