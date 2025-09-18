from person import Person
from neighbourhood import Neighourhood
from graph import Graph
import configparser

if __name__ == "__main__":

    # Read configuration parameters
    config = configparser.ConfigParser()
    config.read('config.ini')   
    num_neighbourhoods = config.getint('Parameters', 'number_of_neighbourhoods', fallback=3)
    residents_per_neighbourhood = config.getint('Parameters', 'residents_per_neighbourhood', fallback=10)
    num_connection = config.getint('Parameters', 'number_of_connections', fallback=4)
    rewire_prob = config.getfloat('Parameters', 'rewire_probability', fallback=0)
    percentage_neighbourhood_contacts = config.getfloat('Parameters', 'percentage_neighbourhood_contacts', fallback=1)

    # initialize graph
    graph = Graph(number_neighbourhoods=num_neighbourhoods, 
                  number_residents=residents_per_neighbourhood)


    graph.make_ring_lattice(k = num_connection)
    graph.initialize_mask()
    graph.make_careless(p=0.05)

    
    # make small world model
    graph.rewire_edges(rewire_prob)
    print("\nAfter rewiring:\n")
    #graph.print_edges()    

    for i in range(210):
        print(f"\nTimestep {i+1}\n")
        graph.make_neighbourhood_contacts(percentage=percentage_neighbourhood_contacts)

        graph.timestep()
        
        graph.delete_neighbourhood_contacts()


    graph.plot_history()



    