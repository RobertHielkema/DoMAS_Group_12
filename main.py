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

    # initialize graph
    graph = Graph(number_neighbourhoods=num_neighbourhoods, 
                  number_residents=residents_per_neighbourhood,
                  num_connections=num_connection,
                  careless_prob=0.05,
                  rewire_prob=rewire_prob)


    for i in range(210):
        print(f"\nTimestep {i+1}\n")
        # if include_quarantining:
        #     graph.remove_quarantined()

        graph.make_neighbourhood_contacts(percentage=percentage_neighbourhood_contacts)
        if not intial_one:
            initial_edges = graph.A.copy()
            intial_one = True

        graph.timestep(i=i)
        
        graph.delete_neighbourhood_contacts()

    plot_graph(initial_edges, graph.first_infected_index)
    
    quit()

    graph.plot_history()



    