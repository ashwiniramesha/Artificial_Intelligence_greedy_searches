#!/usr/bin/python
import os,sys

input_file = "input.txt"
path = []
nodes = []
list_of_pathlists = []
index_node_dict={}
node_dict={}
visited_nodes=[]
FIFO = []
DFS_queue = []
universal_children_list = []
parent_child_dict = {} 
path_cost = {}
orig_cost = {}
cost_state_tuples = []
visited_tuples = []
node_list = []
nodes_in_cst = []
visited_nodelist = []

def filter_nodes_from_cst(cost_state_tuple):
    nodes_in_cst = []
    for j in cost_state_tuples:
        nodes_in_cst.append(j[1])
    return nodes_in_cst

def refresh_visited_nodes(visited_tuples):
    visited_nodelist = []
    for j in visited_tuples:
        visited_nodelist.append(j[1])
    return visited_nodelist


def read_parse_input(input_file):
    global source
    global search_type
    global destination
    global node_dict
    global number_of_nodes 

    fd = open(input_file,"r")
    line_list = fd.readlines()

    search_type = int(line_list[0])
    source = line_list[1].strip('\n')
    destination = line_list[2].strip('\n')
    number_of_nodes = int(line_list[3])

    parent_child_dict[source] = None

    for i in range(1,number_of_nodes+1):    
        nodes.append(line_list[3+i].strip('\n'))

    for j in range(1,number_of_nodes+1):
        path.append(line_list[j+number_of_nodes+3])

    for k in range(0,number_of_nodes):
        list_of_pathlists.append(path[k].split())

    for index in range(0,number_of_nodes):
        index_node_dict[nodes[index]] = index


    fd.close()

def get_orig_cost(node):
    orig_cost = 0

    parent=get_parent(node)
    while parent != None:
        node_index =index_node_dict[node]
        parent_index =index_node_dict[parent] 
        orig_cost = orig_cost + int(list_of_pathlists[node_index][parent_index]) 
        node = parent
        parent=get_parent(node)
    return orig_cost 

def get_parent(node):
    if node == source:
        return None

    else:
        return parent_child_dict[node]

def get_depth(node):
    if node == source:
        return 0 

    depth = 0
    while get_parent(node) != None:
        depth=depth+1;
        node = get_parent(node) 
    return depth  


def assign_parent(child,parent):
    parent_child_dict[child] = parent


def BFS_expand_enqueue_children(node,FIFO):
    same_pathcosts = {} 
    sorted_same_pathcosts = {}

    node_index = index_node_dict[node]
    for i in range(0, number_of_nodes):
        i_nodename = nodes[i]
        if list_of_pathlists[node_index][i] != '0' and i_nodename not in universal_children_list and i_nodename not in FIFO and i_nodename not in visited_nodes:

            assign_parent(i_nodename,node)
            path_cost[i_nodename] = get_depth(i_nodename)
            orig_cost[i_nodename] = get_orig_cost(i_nodename)
            universal_children_list.append(i_nodename)
            FIFO.insert(0,i_nodename)

            for index in range(0,len(FIFO)):
                if path_cost[FIFO[index]] == path_cost[i_nodename]:
		    same_pathcosts[FIFO[index]]= index
                else:
                    continue

            sorted_values = sorted(same_pathcosts.values())
            sorted_same_pathcosts = sorted(same_pathcosts)
            sorted_same_pathcosts.reverse()

            ind = 0
            for fifo_index in sorted_values:
                FIFO[fifo_index] = sorted_same_pathcosts[ind]         
                ind = ind+1
    return 


def DFS_expand_enqueue_children(node, DFS_queue):
    same_pathcosts = {}
    sorted_same_pathcosts = {}

    node_index = index_node_dict[node]
    for i in range(0, number_of_nodes):
        i_nodename = nodes[i]
        if list_of_pathlists[node_index][i] != '0' and i_nodename not in universal_children_list and  i_nodename not in DFS_queue and i_nodename not in visited_nodes:
            assign_parent(i_nodename,node)
            path_cost[i_nodename] = get_depth(i_nodename)
            orig_cost[i_nodename] = get_orig_cost(i_nodename)
            universal_children_list.append(i_nodename)
            DFS_queue.insert(0,i_nodename)
 
            for index in range(0,len(DFS_queue)):
                if path_cost[DFS_queue[index]] == path_cost[i_nodename]:
                    same_pathcosts[DFS_queue[index]]= index
                else:
                    continue
 
            sorted_values = sorted(same_pathcosts.values())
            sorted_same_pathcosts = sorted(same_pathcosts)

            ind = 0
            for DFS_index in sorted_values:
                DFS_queue[DFS_index] = sorted_same_pathcosts[ind]
                ind = ind+1

        elif list_of_pathlists[node_index][i] != '0' and i_nodename in universal_children_list and i_nodename in DFS_queue:
            current_path_cost = 1+get_depth(node) 
            if current_path_cost < path_cost[i_nodename]:
                assign_parent(i_nodename,node)
                path_cost[i_nodename] = get_depth(i_nodename)
                orig_cost[i_nodename] = get_orig_cost(i_nodename)
                DFS_queue.insert(0,i_nodename)

                for index in range(0,len(DFS_queue)):
                    if path_cost[DFS_queue[index]] == path_cost[i_nodename]:
                        same_pathcosts[DFS_queue[index]]= index
                    else:
                        continue

                sorted_values = sorted(same_pathcosts.values())
                sorted_same_pathcosts = sorted(same_pathcosts)

                ind = 0
                for DFS_index in sorted_values:
                    DFS_queue[DFS_index] = sorted_same_pathcosts[ind]
                    ind = ind+1


def UCS_expand_enqueue_children(node,cost_state_tuples,nodes_in_cst,visited_nodelist):
    same_pathcosts = {}
    sorted_same_pathcosts = {}

    node_index = index_node_dict[node]
    for i in range(0, number_of_nodes):
        i_nodename = nodes[i]
        if list_of_pathlists[node_index][i] != '0' and i_nodename not in universal_children_list and i_nodename not in nodes_in_cst and i_nodename not in visited_nodelist:

            assign_parent(i_nodename,node)
            orig_cost[i_nodename] = get_orig_cost(i_nodename)
            universal_children_list.append(i_nodename)

            original_costs = orig_cost.values()
            original_costs.sort()

            tuple = (orig_cost[i_nodename],i_nodename)
            cost_state_tuples.append(tuple)   
            nodes_in_cst = filter_nodes_from_cst(cost_state_tuples)

            cost_state_tuples.sort()
            nodes_in_cst = filter_nodes_from_cst(cost_state_tuples)

            for index in range(0,len(cost_state_tuples)):
                if cost_state_tuples[index][0] == orig_cost[i_nodename]:
                    same_pathcosts[cost_state_tuples[index][1]]= index
                else:
                    continue

            sorted_values = sorted(same_pathcosts.values())
            sorted_same_pathcosts = sorted(same_pathcosts)

            ind = 0
            for ucs_index in sorted_values:
                cost_state_tuples[ucs_index] = (orig_cost[sorted_same_pathcosts[ind]], sorted_same_pathcosts[ind])
                ind = ind+1
            
            nodes_in_cst = filter_nodes_from_cst(cost_state_tuples) 

        elif list_of_pathlists[node_index][i] != '0' and i_nodename != source and i_nodename in nodes_in_cst:
            
            index_of_child = nodes_in_cst.index(i_nodename)
            index_of_parent = visited_nodelist.index(node)

            previous_cost = cost_state_tuples[index_of_child][0]
            cur_node_index = index_node_dict[i_nodename] 
            current_cost =    orig_cost[node] +  int(list_of_pathlists[index_of_child][node_index]) 
        
            if current_cost < previous_cost:
                del(cost_state_tuples[index_of_child])
                cost_state_tuples.append((current_cost,i_nodename))
                nodes_in_cst = filter_nodes_from_cst(cost_state_tuples)
                parent_child_dict[i_nodename] = node
                cost_state_tuples.sort()
                nodes_in_cst = filter_nodes_from_cst(cost_state_tuples)

            for index in range(0,len(cost_state_tuples)):
                if cost_state_tuples[index][0] == orig_cost[i_nodename]:
                    same_pathcosts[cost_state_tuples[index][1]]= index
                else:
                    continue

            sorted_values = sorted(same_pathcosts.values())
            sorted_same_pathcosts = sorted(same_pathcosts)

            ind = 0
            for ucs_index in sorted_values:
                cost_state_tuples[ucs_index] = (orig_cost[sorted_same_pathcosts[ind]], sorted_same_pathcosts[ind])
                ind = ind+1
            
            nodes_in_cst = filter_nodes_from_cst(cost_state_tuples) 

    return
 
def print_shortest_path():
    global shortest_path
    shortest_path = [] 
    node = destination 
  
    while node!=None:
        shortest_path.append(node)
        node = get_parent(node)
    shortest_path.reverse()
    return shortest_path

def traverse_BFS(source_index, destination_index):
    FIFO.insert(0,source)
    path_cost[source] = 0

    while True:
        if len(FIFO) == 0:
            output_file = open("output.txt","w")
            print_expansion = '-'.join(visited_nodes)
            output_file.write(print_expansion+"\n")
            output_file.write("NoPathAvailable") 
            output_file.close()
            break
        else:
            visited = FIFO.pop()
            visited_nodes.append(visited)
            if visited == destination:
                output_file = open("output.txt","w")
                print_expansion = '-'.join(visited_nodes)
                print_log = '-'.join(print_shortest_path())
                print_cost = get_orig_cost(destination)

                output_file.write(print_expansion+"\n")
                output_file.write(print_log+"\n")
                output_file.write(str(print_cost)+"\n")

                output_file.close()
                break
            else:
                BFS_expand_enqueue_children(visited,FIFO)
                 
def traverse_DFS(source_index, destination_index):
    DFS_queue.insert(0,source)
    path_cost[source] = 0
    
    while True:
        if len(DFS_queue) == 0:
            output_file = open("output.txt","w")
            print_expansion = '-'.join(visited_nodes)
            output_file.write(print_expansion+"\n") 
            output_file.write("NoPathAvailable")
            output_file.close()
            break    
        else:
            visited = DFS_queue.pop(0)
            visited_nodes.append(visited)
            if visited == destination:
                output_file = open("output.txt","w")
                print_expansion = '-'.join(visited_nodes)
                print_log = '-'.join(print_shortest_path())
                print_cost = get_orig_cost(destination)

                output_file.write(print_expansion+"\n")
                output_file.write(print_log+"\n")
                output_file.write(str(print_cost)+"\n")

                output_file.close()
                break
            else:
                DFS_expand_enqueue_children(visited,DFS_queue)


def traverse_UCS(source_index, destination_index):
    global nodes_in_cst
    path_cost[source] = 0
    cost_state_tuples.insert(0,(0,source))
    nodes_in_cst = filter_nodes_from_cst(cost_state_tuples)

    while True:
        if len(cost_state_tuples) == 0:
            for index in visited_tuples:
                node_list.append(index[1])
            nodes_in_cst = filter_nodes_from_cst(cost_state_tuples)

            output_file = open("output.txt","w")
            print_expansion = '-'.join(node_list)
            output_file.write(print_expansion+"\n") 
            output_file.write("NoPathAvailable")
            output_file.close()
            break
        else:
            visited = cost_state_tuples.pop(0)
            nodes_in_cst = filter_nodes_from_cst(cost_state_tuples)
            visited_tuples.append(visited)
            visited_nodelist = refresh_visited_nodes(visited_tuples)
            if visited[1] == destination:

                for index in visited_tuples:
                    node_list.append(index[1])
                nodes_in_cst = filter_nodes_from_cst(cost_state_tuples)

                output_file = open("output.txt","w")
                print_expansion = '-'.join(node_list)
                print_log = '-'.join(print_shortest_path())
                print_cost = get_orig_cost(destination)

                output_file.write(print_expansion+"\n")
                output_file.write(print_log+"\n")
                output_file.write(str(print_cost)+"\n")

                output_file.close()
                break 

            else:
                UCS_expand_enqueue_children(visited[1],cost_state_tuples, nodes_in_cst,visited_nodelist)

read_parse_input(input_file)

source_index = index_node_dict[source] 
destination_index = index_node_dict[destination]

if search_type == 1:
    traverse_BFS(source_index, destination_index)

elif search_type == 2:
    traverse_DFS(source_index, destination_index)

elif search_type == 3:
    traverse_UCS(source_index, destination_index) 
