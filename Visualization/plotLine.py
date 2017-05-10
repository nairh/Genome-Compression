import pickle
import matplotlib.pyplot as plt
import sys

plot1Name = sys.argv[1]
plot2Name = sys.argv[2]

with open("results.pkl", "rb") as f:
	plots = pickle.load(f)

plt.figure(1)
for line in plots[0]:
	plt.plot( line[0], line[1], label = line[2] )
plt.legend(loc=2)
plt.title("Computation Time")
plt.ylabel("Running Time per Seq. (sec)")
plt.xlabel("Number of Levels in Sim.")
plt.savefig(plot1Name)

plt.figure(2)
for line in plots[1]:
	plt.plot( line[0], line[1], label = line[2] )
plt.legend(loc=2)
plt.title("Compression")
plt.ylabel("Storage per Seq. (compressed)")
plt.xlabel("Number of Levels in Sim.")
plt.savefig(plot2Name)

