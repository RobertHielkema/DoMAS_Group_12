from graph import Graph
import configparser
from plot_initial_graph import plot_graph

if __name__ == "__main__":

    # Read configuration parameters
    config = configparser.ConfigParser()
    config.read('config.ini')   
    num_neighbourhoods = config.getint('Parameters', 'number_of_neighbourhoods', fallback=3)
    residents_per_neighbourhood = config.getint('Parameters', 'residents_per_neighbourhood', fallback=10)
    num_connection = config.getint('Parameters', 'number_of_connections', fallback=4)
    rewire_prob = config.getfloat('Parameters', 'rewire_probability', fallback=0)
    percentage_neighbourhood_contacts = config.getfloat('Parameters', 'percentage_neighbourhood_contacts', fallback=1)
    include_quarantining = config.getboolean('Parameters', 'include_quarantining', fallback=True)



    history_I, history_E, history_S, history_R = [], [], [], []

    for i in range(100):
        print(f"Simulation run {i+1}/100")
        # initialize graph
        graph = Graph(number_neighbourhoods=num_neighbourhoods, 
                    number_residents=residents_per_neighbourhood,
                    num_connections=num_connection,
                    careless_prob=0.05,
                    rewire_prob=rewire_prob,
                    include_quarantining=include_quarantining)
        
        edge_graphs = []
        pos, x_max, y_max = graph._fix_node_positions()

        for i in range(210):
            #print(f"\nTimestep {i+1}\n")

            graph.make_neighbourhood_contacts(percentage=percentage_neighbourhood_contacts)

            
            if i % 5 == 0:
                edge_graph = graph.A.copy()
                infected_ids = graph._get_infected_ids()
                edge_graphs.append((edge_graph, infected_ids))
                

            graph.timestep(i=i)
            
            graph.delete_neighbourhood_contacts()

        # uncomment to plot graphs at each 6th timestep
        #for idx, g in enumerate(edge_graphs):
        #    plot_graph(*g, (idx*5) + 1, pos)
        history_I.append(graph.history_I)
        history_E.append(graph.history_E)
        history_S.append(graph.history_S)
        history_R.append(graph.history_R)

    graph.plot_history(history_E, history_I, history_S, history_R)



        