import matplotlib.pyplot as plt
import pandas as pd

d = pd.read_csv('Data/276城_3source_by_ct_V3.csv')


df = d.groupby('age_feb20').mean()['locked_down']
plt.bar(x=df.index, height= df)

df = d.groupby('age_feb20').mean()['xc_lockdown']
plt.bar(x=df.index, height= df)

plt.show()



import seaborn as sns
sns.set(style="whitegrid")

# penguins = sns.load_dataset("penguins")

# Draw a nested barplot by species and sex
g = sns.catplot(
    data=d, kind="bar",
    x="age_feb20", y="locked_down",alpha=.6, height=6
)
g.despine(left=True)
g.set_axis_labels("", "Body mass (g)")
# g.legend.set_title("")
plt.show()