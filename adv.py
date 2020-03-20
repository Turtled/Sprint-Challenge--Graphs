from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from queue import Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

player = Player(world.starting_room)


# Print an ASCII map
world.print_rooms(player.current_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited_rooms = set()

def get_unvisited_exits(room):
    unvisitedDirections = []
    for direction in room.get_exits():
        if room.get_room_in_direction(direction) not in traversal_path:
            unvisitedDirections.append(direction)

    return unvisitedDirections

def bfs(starting_room):
    """
    Return a list containing the shortest path from
    starting_vertex to destination_vertex in
    breath-first order.
    """
    visited = set()
    queue = Queue(maxsize=0)
    start_path = list()
    start_path.append(starting_room)
    #print(start_path)
    queue.put(start_path)
    while not queue.empty():
        path = queue.get()
        #print("path" + str(path))
        room = path[len(path) - 1]
        if room not in visited:
            visited.add(room)

            if len(get_unvisited_exits(room)) > 0:
                return path

            for v in room.get_exits():
                path_copy = path.copy()
                path_copy.append(room.get_room_in_direction(v) )
                queue.put(path_copy)

while True:
    # print("Steps taken: " + str(len(traversal_path)))
    traversal_path.append(player.current_room)
    # player.current_room.print_room_description(player)
    # world.print_rooms(player.current_room)

    visited_rooms.add(player.current_room)

    if len(visited_rooms) == len(room_graph):
        input("TRAVERSED ALL ROOMS! Took " + str(len(traversal_path)) + " steps.\n\n\n\n\n\n")
        break

    unvisted_directions = get_unvisited_exits(player.current_room)
    # input("Continue?")

    if len(unvisted_directions) > 0:
        player.travel( random.choice(unvisted_directions) )
    else:
        #dead end, backtrack
        backtrackPath = bfs(player.current_room)
        for r in backtrackPath[:len(backtrackPath)]:
            player.travel_to_room( r )
            traversal_path.append(r)

#format traversal_path the way the test wants it (directions not rooms)
new_traversal_path = []
last_room = None
for room in traversal_path:
    if last_room is not None:
        for dir in last_room.get_exits():
            if last_room.get_room_in_direction(dir) is room:
                new_traversal_path.append(dir)

    last_room = room

traversal_path = new_traversal_path

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
