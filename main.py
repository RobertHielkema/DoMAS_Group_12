from graph import Graph
import configparser
from plot_initial_graph import plot_graph
import numpy as np
from datetime import datetime

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
    include_self_test = config.getboolean('Parameters', 'include_self_test', fallback=True)

    pos_app_usage_rate = [0.5,0.6,0.7,0.8,0.9,1]
    pos_quar_prob_rate = [0.5,0.6,0.7,0.8,0.9,1]
    # app_usage_rate = config.getfloat('Parameters', 'app_usage_rate', fallback=1.0)
    # quarantine_probability = config.getfloat('Parameters', 'quarantine_probability', fallback=0.5)

    for app_usage_rate in pos_app_usage_rate:
        for quar_prob_rate in pos_quar_prob_rate:
            history_I, history_E, history_S, history_R, history_quarantaine = [], [], [], [], []

            T = 1
            for i in range(T):
                print(f"Simulation run {i+1}/{T}")
                # initialize graph
                graph = Graph(number_neighbourhoods=num_neighbourhoods, 
                            number_residents=residents_per_neighbourhood,
                            num_connections=num_connection,
                            careless_prob=0.05,
                            rewire_prob=rewire_prob,
                            include_quarantining=include_quarantining,
                            app_usage_rate=app_usage_rate,
                            quarantine_probability=quar_prob_rate,
                            include_self_test=include_self_test
                            )
                
                edge_graphs = []
                #pos, x_max, y_max = graph._fix_node_positions()

                for i in range(210):
                    #print(f"\nTimestep {i+1}\n")

                    graph.make_neighbourhood_contacts(percentage=percentage_neighbourhood_contacts)

                    
                    if i % 5 == 0:
                        edge_graph = graph.A.copy()
                        infected_ids = graph._get_infected_ids()
                        edge_graphs.append((edge_graph, infected_ids))
                        

                    graph.timestep(i=i)
                    
                    graph.delete_neighbourhood_contacts()

                    if graph.history_E[-1] == 0 and graph.history_I[-1] == 0:
                        print(f"Simulation ended early at day {i+1} as there are no more Exposed or Infected individuals.")
                        for _ in range(i+1, 210):
                            graph.history_E.append(0)
                            graph.history_I.append(0)
                            graph.history_S.append(graph.history_S[-1])
                            graph.history_R.append(graph.history_R[-1])
                            if len(graph.history_quarantined) > 0:
                                graph.history_quarantined.append(graph.history_quarantined[-1])
                        break

                # uncomment to plot graphs at each 6th timestep
                #for idx, g in enumerate(edge_graphs):
                #    plot_graph(*g, (idx*5) + 1, pos)
                history_I.append(graph.history_I)
                history_E.append(graph.history_E)
                history_S.append(graph.history_S)
                history_R.append(graph.history_R)

                history_quarantaine.append(graph.history_quarantined)

            # Determine number of simulated days
            num_days = len(graph.history_I)
            print(num_days)
            filename = f"simulation_results_Q={quar_prob_rate}A={app_usage_rate}_selftest={include_self_test}{datetime.now():%Y%m%d_%H%M%S}.npz"

            # pad history_quarantaine to have same length arrays
            history_quarantaine = np.array([x + [-1]*(max(map(len, history_quarantaine)) - len(x)) 
                                            for x in history_quarantaine])
            
            # Save all results to file
            np.savez(
                filename,
                history_E=history_E,
                history_I=history_I,
                history_S=history_S,
                history_R=history_R,
                history_quarantaine=history_quarantaine,
                num_days=num_days,
                n_total=len(graph.nodes)
            )

            graph.plot_history(history_E, history_I, history_S, history_R)
            graph.plot_quarantained(history_quarantaine)




        