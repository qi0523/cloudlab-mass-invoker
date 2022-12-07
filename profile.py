""" Ubuntu 20.04 Optional Kubernetes Cluster w/ OpenWhisk optionally deployed with a parameterized
number of nodes.
"""

import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as rspec

IMAGE = "urn:publicid:IDN+cloudlab.umass.edu+image+containernetwork-PG0:ow-v0"

pc = portal.Context()

pc.defineParameter("cores",
                   "Invoker cpu cores",
                   portal.ParameterType.INTEGER,
                   1,
                   longDescription="Invoker cpu cores.")

pc.defineParameter("memory",
                   "Invoker memory",
                   portal.ParameterType.INTEGER,
                   5120,
                   longDescription="Invoker memory.")

pc.defineParameter("bandwidth",
                   "Invoker bandwidth",
                   portal.ParameterType.INTEGER,
                   512000,
                   longDescription="Invoker bandwidth.")

pc.defineParameter("nodeCount", 
                   "Number of nodes in the experiment. It is recommended that at least 3 be used.",
                   portal.ParameterType.INTEGER, 
                   3)

pc.defineParameter("masterIP", 
                   "Master ip address",
                   portal.ParameterType.STRING, 
                   "172.17.1.1")

pc.defineParameter("tempFileSystemSize", 
                   "Temporary Filesystem Size",
                   portal.ParameterType.INTEGER, 
                   0,
                   advanced=True,
                   longDescription="The size in GB of a temporary file system to mount on each of your " +
                   "nodes. Temporary means that they are deleted when your experiment is terminated. " +
                   "The images provided by the system have small root partitions, so use this option " +
                   "if you expect you will need more space to build your software packages or store " +
                   "temporary files. 0 GB indicates maximum size.")

params = pc.bindParameters()

pc.verifyParameters()
request = pc.makeRequestRSpec()

def create_node(name, nodes):
  # Create node
  node = request.XenVM(name)

  node.exclusive = True
  
  node.cores = params.cores
  # Ask for 2GB of ram
  node.ram   = params.memory

  node.disk_image = IMAGE
  
  # Add extra storage space
  if (params.tempFileSystemSize > 0):
    bs = node.Blockstore(name + "-bs", "/mydata")
    bs.size = str(params.tempFileSystemSize) + "GB"
    bs.placement = "any"
  
  # Add to node list
  nodes.append(node)

nodes = []

for i in range(params.nodeCount):
    name = "ow"+str(i+1)
    create_node(name, nodes)

for i, node in enumerate(nodes[0:]):
    node.addService(rspec.Execute(shell="bash", command="/local/repository/start.sh {} {} > /home/cloudlab-openwhisk/start.log 2>&1 &".format(params.masterIP, params.bandwidth)))
# ./start.sh masterip > /home/cloudlab-openwhisk/start.log 2>&1
# bash ./st.sh 172.17.103.1 > /home/cloudlab-openwhisk/start.log 2>&1
pc.printRequestRSpec()