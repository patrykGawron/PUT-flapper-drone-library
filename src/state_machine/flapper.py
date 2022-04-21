import sys
import yaml
import networkx as nx
import matplotlib.pyplot as plt

from console import console_interface, testing
from generator import Gen, setTransition, generate_states
from statemachine import StateMachine, State, Transition

def test(self):
    # send_command(1)
    pass

drone_graph = nx.MultiDiGraph()

from_tos_filename = "from_tos.yaml" # sys.argv[1]
options_filename = "options.yaml" # sys.argv[2]
with open(options_filename, "r") as file:
    loaded = yaml.load(file, Loader=yaml.FullLoader)

drone_options = loaded["drone_options"]
drone_states = generate_states(drone_options)

clbck = {"callable_0_1": test}


with open(from_tos_filename, 'r') as file:
    from_to = yaml.load(file, Loader=yaml.FullLoader)

drone_from_to = from_to["drone_from_to"]
drone_states, drone_transitions = setTransition(drone_from_to, drone_states, clbck)


def create_and_show_graph(graph, states, edges, ax, color, current=""):
    plt.cla()
    # nodes are int ids, since from_to is defined in terms of 0 -> 1 etc.
    i = 0
    for dict in states:
        initial, name, value = dict.values()
        # name is node's attribute
        if name == current:
            graph.add_node(i, name=value, color="red")
        else:
            graph.add_node(i, name=value, color=color)
        i += 1

    # get all labels for drawing
    labels = nx.get_node_attributes(graph, 'name')
    # get colors of all the nodes
    colors = nx.get_node_attributes(graph, 'color').values()
    # add edges from list such as: [from_node, [to_node1, to_node2, ..., to_nodeN]]
    for edge in edges:
        from_node = edge[0]
        for to_node in edge[1]:
            graph.add_edge(from_node, to_node)

    pos = nx.shell_layout(graph)
    nx.draw(graph, pos, with_labels=False, ax=ax, connectionstyle='arc3, rad = 0.1', node_color=colors, alpha=0.75)

    # offset labels along y axis so they are above nodes
    pos_higher = {}
    y_off = 0.15
    for k, v in pos.items():
        pos_higher[k] = (v[0], v[1] + y_off)
    nx.draw_networkx_labels(graph, pos_higher, labels, ax=ax)

    # interactive mode so plt.show() is non-blocking
    plt.ion()
    plt.show()

fig, axs = plt.subplots(1, 2)
colors = ["green", "blue"]
print(axs)

def redraw(curr_drone=""):
    create_and_show_graph(drone_graph, drone_options, drone_from_to, axs[0], colors[0], curr_drone)

for i in range(2):
    create_and_show_graph(drone_graph, drone_options, drone_from_to, axs[0], colors[i%2])
    plt.pause(0.1)

def main():
    drone = Gen.create_object(drone_states, drone_transitions, drone_from_to, clbck)
    # testing(drone, drone_transitions, drone_from_to, redraw)
    console_interface(drone, drone_transitions, drone_from_to, redraw)
if __name__ == '__main__':
    main()