import pickle
import matplotlib.pyplot as plt
import sys

plot1Name = sys.argv[1]
plot2Name = sys.argv[2]


with open("results.pkl", "rb") as f:
	plots = pickle.load(f)

plt.figure(1)
bars = []
labels = []
y_pos = list(range( len(plots[0]) ))
for run in plots[0]:
	bars.append( run[1][0] )
	labels.append( run[2] )
plt.bar( y_pos, bars, align='center')
plt.xticks( y_pos, labels)
plt.title("Computation Time")
plt.ylabel("Running Time per Seq. (sec)")
plt.xlabel("Number of Levels in Sim.")
plt.savefig(plot1Name)

plt.figure(1)
bars = []
labels = []
y_pos = list(range( len(plots[1]) ))
for run in plots[1]:
	bars.append( run[1][0] )
	labels.append( run[2] )
plt.bar( y_pos, bars, align='center')
plt.xticks( y_pos, labels)
plt.title("Compression")
plt.ylabel("Storage per Seq. (compressed)")
plt.xlabel("Number of Levels in Sim.")
plt.savefig(plot2Name)
