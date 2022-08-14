from __future__ import print_function
from collections import namedtuple
import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math

'''
---------INPUT---------
customer_count : number of customers
vehicle_count : number of vehicles
vehicle_capacity : capacity of every vehicle
customers_list : a list of triples (d, x, y) -> where d : customer demand, (x , y) : coordinate / location of that customer

---------OUTPUT--------- (n : float, routes : list)
n : total distance covered by all the vehicles
routes: a list, where each row represents the route taken by corresponding vehicle. The route starts with '0' indicating warehouse. Then the following numbers represents the customers attended by that vehicle.

'''
def vrp_ortools(customer_count,vehicle_count, vehicle_capacity, customers_list):
    def dist(x1,y1,x2,y2):
        return int(math.sqrt((x1-x2)**2+(y1-y2)**2))

    Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])
    

    customers = []
    customers_list = np.array(customers_list)
    for i in range(1, customer_count+1):
        customers.append(Customer(i-1, int(customers_list[i-1, 0]), float(customers_list[i-1, 1]), float(customers_list[i-1, 2])))

    def get_routes(solution, routing, manager):
      """Get vehicle routes from a solution and store them in an array."""
      
      # Get vehicle routes and store them in a two dimensional array whose
      # i,j entry is the jth location visited by vehicle i along its route.
      
      routes = []
      for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
          index = solution.Value(routing.NextVar(index))
          route.append(manager.IndexToNode(index))
        routes.append(route)
      return routes

    customer_demand=[c.demand for c in customers]
    distance_matrix=[[dist(customers[i].x,customers[i].y,customers[j].x,customers[j].y)\
                                    for j in range(customer_count)] for i in range(customer_count)]
    
    #creating_data_for_the_model
    data = {}
    data['distance_matrix']=distance_matrix.copy()
    data['demands'] = [c.demand for c in customers]
    data['vehicle_capacities'] = [vehicle_capacity for i in range(vehicle_count)]
    data['num_vehicles'] = vehicle_count
    data['depot'] = 0


    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)

    search_parameters.local_search_metaheuristic = (
                routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 180

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    obj=solution.ObjectiveValue()
    # Print solution on console.
    final_routes=get_routes(solution,routing,manager)

    return obj,final_routes
