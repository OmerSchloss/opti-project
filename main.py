from branchandbound import branchandbound
from cuttingplanes import cuttingplanes

timeLimit = 600

print("\n\n\n")
print("time limit: ",timeLimit)
print("\n\n\n")

tcpFile = "ilcities.tsp"

cuttingplanes(tcpFile, timeLimit)
print("\n\n\n")
branchandbound(tcpFile, timeLimit)
