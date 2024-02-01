import pickle
from navigator_class import navigator
import asyncio

dest = input("Enter the house you wish to visit: ")

async def some_async_function():
    navigator(dest)


async def load():
    await some_async_function()

# Load the objects from the pickle file
    with open('navigator_state.pkl', 'rb') as file:
        data = pickle.load(file)



if __name__ == "__main__":
    asyncio.run(load())




# # Check if the entered destination house is in the graph
# if dest_house not in G_loaded.nodes:
#     print(f"The house '{dest_house}' is not a valid destination.")
# else:
#     shortest_path = nx.shortest_path(G_loaded, source=main_road_loaded.start, target=dest_house)
#     print(f"Shortest path from Main Gate to {dest_house}: {shortest_path}")
