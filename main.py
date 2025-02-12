import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import *
import requests
from io import BytesIO
from urllib import request




def dijkstras(graph, start, end):
    # Create a dictionary to store the shortest distance to each node
    distance = {node: float('inf') for node in graph}
    distance[start] = 0  # The distance to the start node is 0
    visited = set()  # Set of visited nodes

    while distance:
        # Find the node with the smallest distance
        current_node, current_distance = min(distance.items(), key=lambda x: x[1])
        
        # Remove the current node from the dictionary
        distance.pop(current_node)
        
        # If we reached the end node, reconstruct the path
        if current_node == end:
            path = []
            while current_node is not None:
                path.insert(0, current_node)
                current_node = previous[current_node]
            return path, current_distance

        # If the current distance is infinity, there is no path to the end
        if current_distance == float('inf'):
            return [], float('inf')

        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            if neighbor not in visited:
                new_distance = current_distance + weight
                if new_distance < distance.get(neighbor, float('inf')):
                    distance[neighbor] = new_distance
                    previous[neighbor] = current_node

    # If we couldn't reach the end node, return an empty path and infinity distance
    return [], float('inf')


def dijkstra(graph, start, end):
    shortest_path = nx.shortest_path(graph, source=start, target=end, weight='weight')
    shortest_distance = nx.shortest_path_length(graph, source=start, target=end, weight='weight')
    return shortest_path, shortest_distance

# Define functions to create graphs for different locations
def create_graphD():
    G = nx.Graph()
    G.add_node("Dubai Mall")
    G.add_node("Burj Khalifa")
    G.add_node("Palm Jumeirah")
    G.add_node("Jumeirah Beach")
    G.add_node("Mall of the Emirates")
    G.add_edge("Dubai Mall", "Burj Khalifa", weight=1.5)
    G.add_edge("Dubai Mall", "Palm Jumeirah", weight=10)
    G.add_edge("Burj Khalifa", "Palm Jumeirah", weight=5)
    G.add_edge("Burj Khalifa", "Jumeirah Beach", weight=3)
    G.add_edge("Palm Jumeirah", "Jumeirah Beach", weight=2)
    G.add_edge("Palm Jumeirah", "Mall of the Emirates", weight=8)
    G.add_edge("Jumeirah Beach", "Mall of the Emirates", weight=7)
    return G

def create_graphI():
    G = nx.Graph()
    G.add_node("Taj Mahal")
    G.add_node("Red Fort")
    G.add_node("Gateway of India")
    G.add_node("Howrah Station")
    G.add_node("Humayun's Tomb")
    G.add_edge("Taj Mahal", "Red Fort", weight=5)
    G.add_edge("Taj Mahal", "Gateway of India", weight=8)
    G.add_edge("Red Fort", "Gateway of India", weight=6)
    G.add_edge("Red Fort", "Howrah Station", weight=3)
    G.add_edge("Gateway of India", "Howrah Station", weight=5)
    G.add_edge("Howrah Station", "Humayun's Tomb", weight=4)
    return G

def create_graphC():
    G = nx.Graph()
    G.add_node("Great Wall of China")
    G.add_node("Forbidden City")
    G.add_node("Terracotta Army")
    G.add_node("Pearl River Cruise")
    G.add_node("Wudang Mountains")
    G.add_edge("Great Wall of China", "Forbidden City", weight=5)
    G.add_edge("Great Wall of China", "Terracotta Army", weight=8)
    G.add_edge("Forbidden City", "Terracotta Army", weight=5)
    G.add_edge("Forbidden City", "Pearl River Cruise", weight=3)
    G.add_edge("Terracotta Army", "Pearl River Cruise", weight=2)
    G.add_edge("Terracotta Army", "Wudang Mountains", weight=8)
    G.add_edge("Pearl River Cruise", "Wudang Mountains", weight=7)
    return G

def create_graphL():
    G = nx.DiGraph()
    G.add_node("Sydney Opera House")
    G.add_node("Uluru")
    G.add_node("The Great Barrier Reef")
    G.add_node("Kakadu National Park")
    G.add_node("Darwin Waterfront")
    G.add_edge("Sydney Opera House", "Uluru", weight=2.5)
    G.add_edge("Sydney Opera House", "The Great Barrier Reef", weight=2)
    G.add_edge("Uluru", "The Great Barrier Reef", weight=1.5)
    G.add_edge("Uluru", "Kakadu National Park", weight=4)
    G.add_edge("The Great Barrier Reef", "Kakadu National Park", weight=2.5)
    G.add_edge("Kakadu National Park", "Darwin Waterfront", weight=1)
    return G

def create_graphM():
    G = nx.DiGraph()
    G.add_node("Statue of Liberty")
    G.add_node("Empire State Building")
    G.add_node("Yellowstone National Park")
    G.add_node("Grand Canyon")
    G.add_node("Las Vegas Strip")
    G.add_edge("Statue of Liberty", "Empire State Building", weight=1.5)
    G.add_edge("Statue of Liberty", "Yellowstone National Park", weight=3)
    G.add_edge("Empire State Building", "Yellowstone National Park", weight=2.5)
    G.add_edge("Empire State Building", "Grand Canyon", weight=3.5)
    G.add_edge("Yellowstone National Park", "Grand Canyon", weight=1.5)
    G.add_edge("Grand Canyon", "Las Vegas Strip", weight=3)
    return G

# Define nearby hotels data
nearby_hotels = {
    "Dubai Mall": ["Hotel A", "Hotel B", "Hotel C"],
    "Burj Khalifa": ["Hotel D", "Hotel E", "Hotel F"],
    "Palm Jumeirah": ["Hotel G", "Hotel H", "Hotel I"],
    "Jumeirah Beach": ["Hotel J", "Hotel K", "Hotel L"],
    "Mall of the Emirates": ["Hotel M", "Hotel N", "Hotel O"],
    "Taj Mahal": ["Hotel X", "Hotel Y", "Hotel Z"],
    "Red Fort": ["Hotel P", "Hotel Q", "Hotel R"],
    "Gateway of India": ["Hotel S", "Hotel T", "Hotel U"],
    "Howrah Station": ["Hotel V", "Hotel W", "Hotel Y"],
    "Sydney Opera House": ["Hotel A1", "Hotel B1", "Hotel C1"],
    "Uluru": ["Hotel D1", "Hotel E1", "Hotel F1"],
    "The Great Barrier Reef": ["Hotel G1", "Hotel H1", "Hotel I1"],
    "Kakadu National Park": ["Hotel J1", "Hotel K1", "Hotel L1"],
    "Statue of Liberty": ["Hotel X1", "Hotel Y1", "Hotel Z1"],
    "Empire State Building": ["Hotel P1", "Hotel Q1", "Hotel R1"],
    "Yellowstone National Park": ["Hotel S1", "Hotel T1", "Hotel U1"],
    "Great Wall of China": ["Hotel China1", "Hotel China2", "Hotel China3"],
    "Forbidden City": ["Hotel China4", "Hotel China5", "Hotel China6"],
    "Terracotta Army": ["Hotel China7", "Hotel China8", "Hotel China9"],
    "Pearl River Cruise": ["Hotel China10", "Hotel China11", "Hotel China12"],
    "Wudang Mountains": ["Hotel China13", "Hotel China14", "Hotel China15"],
    "Sydney Opera House": ["Hotel Australia1", "Hotel Australia2", "Hotel Australia3"],
    "Uluru": ["Hotel Australia4", "Hotel Australia5", "Hotel Australia6"],
    "The Great Barrier Reef": ["Hotel Australia7", "Hotel Australia8", "Hotel Australia9"],
    "Kakadu National Park": ["Hotel Australia10", "Hotel Australia11", "Hotel Australia12"],
    "Darwin Waterfront": ["Hotel Australia13", "Hotel Australia14", "Hotel Australia15"],
    "Statue of Liberty": ["Hotel USA1", "Hotel USA2", "Hotel USA3"],
    "Empire State Building": ["Hotel USA4", "Hotel USA5", "Hotel USA6"],
    "Yellowstone National Park": ["Hotel USA7", "Hotel USA8", "Hotel USA9"],
    "Grand Canyon": ["Hotel USA10", "Hotel USA11", "Hotel USA12"],
    "Las Vegas Strip": ["Hotel USA13", "Hotel USA14", "Hotel USA15"]
}
# Get a list of locations
locations = nearby_hotels.keys()

def find_shortest_path():
    start_location = start_entry.get()
    end_location = end_entry.get()
    if start_location not in locations or end_location not in locations:
        messagebox.showerror("Error", "Invalid locations")
        return
    shortest_path, shortest_distance = dijkstra(graph, start_location, end_location)
    result_label.config(text=f"Shortest Path: {' -> '.join(shortest_path)}\nShortest Distance: {shortest_distance} km")

def plot_graph(graph, canvas):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', width=2)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    canvas.draw()

def create_hotel_graph(location):
    G = nx.Graph()
    G.add_node(location)
    for hotel in nearby_hotels[location]:
        G.add_node(hotel)
        G.add_edge(location, hotel, weight=1)
    return G

def display_hotel_graph(location):
   
    if location not in nearby_hotels:
        messagebox.showerror("Error", "Location not found in nearby hotels")
        return
    hotel_graph = create_hotel_graph(location)
    display_graph_in_window(hotel_graph, "Nearby Hotels for " + location)

def display_graph_in_window(graph, title):
    new_window = tk.Toplevel(root)
    new_window.title(title)

    # Use grid for the canvas in the new window
    canvas = FigureCanvasTkAgg(plt.figure())
    canvas.get_tk_widget().grid(row=0, column=0)
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', width=2)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)


graph = None

def visit_place(place):
    global graph  # Declare the 'graph' as global

    message = f"You chose to visit {place}"

    if place == "DUBAI":
        graph = create_graphD()
    elif place == "INDIA":
        graph = create_graphI()
    elif place == "CHINA":
        graph = create_graphC()
    elif place == "AUSTRALIA":
        graph = create_graphL()
    elif place == "AMERICA":
        graph = create_graphM()

    if graph is not None:
        display_shortest_path_finder(place, graph)
        display_graph_in_window(graph, place)
    else:
        messagebox.showerror("Error", "No graph data for this location.")

    # Now, display nearby hotels
    if place in nearby_hotels:
        display_hotel_graph(place)
    else:
        messagebox.showerror("Error", "No nearby hotels data for this location.")

    print(message)

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = [(key, value)]
        else:
            for i, (existing_key, _) in enumerate(self.table[index]):
                if existing_key == key:
                    self.table[index][i] = (key, value)
                    break
            else:
                self.table[index].append((key, value))

    def search(self, key):
        index = self.hash_function(key)
        if self.table[index] is not None:
            for existing_key, value in self.table[index]:
                if existing_key == key:
                    return value
        return None

class HashTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hash Table App")

        self.hash_table = HashTable(10)

        self.key_label = Label(self.root, text="Key:")
        self.key_label.pack()
        
        self.key_entry = Entry(self.root)
        self.key_entry.pack()

        self.value_label = Label(self.root, text="Value:")
        self.value_label.pack()
        
        self.value_entry = Entry(self.root)
        self.value_entry.pack()

        self.insert_button = Button(self.root, text="Insert", command=self.insert)
        self.insert_button.pack()
        self.search_button = Button(self.root, text="Search", command=self.search)
        self.search_button.pack()
        self.result_label = Label(self.root, text="")
        self.result_label.pack()

    def insert(self):
        key = self.key_entry.get()
        value = self.value_entry.get()
        self.hash_table.insert(key, value)
        self.key_entry.delete(0, 'end')
        self.value_entry.delete(0, 'end')

    def search(self):
        key = self.key_entry.get()
        value = self.hash_table.search(key)
        if value is not None:
            self.result_label.config(text=f"Value: {value}")
        else:
            self.result_label.config(text="Key not found")

def open_new_window():
    new_window = Toplevel(root)
    new_window.title("Search the country")

    app = HashTableApp(new_window)

# ... Your code ...

def display_shortest_path_finder(location, graph):
    global start_entry, end_entry, result_label  # Declare 'start_entry', 'end_entry', and 'result_label' as global

    # Create GUI components for the main graph
    shortest_path_window = tk.Toplevel(root)
    shortest_path_window.title("SHORTEST PATH FINDER")
    shortest_path_window.configure(bg="purple")

    start_label = tk.Label(shortest_path_window, text="Start Location:")
    start_label.pack(pady=10)  # Add vertical space below label1

    start_entry = tk.Entry(shortest_path_window)
    start_entry.pack(pady=10)

    end_label = tk.Label(shortest_path_window, text="End Location:")
    end_label.pack(pady=10)  # Add vertical space below label1

    end_entry = tk.Entry(shortest_path_window)
    end_entry.pack(pady=10)

    find_button = tk.Button(shortest_path_window, text="Find Shortest Path", command=find_shortest_path)
    find_button.pack()

    result_label = tk.Label(shortest_path_window, text="")
    result_label.pack(pady=10)

    graph_frame = tk.Frame(shortest_path_window)
    graph_frame.pack(pady=10)

    canvas = FigureCanvasTkAgg(plt.figure())
    canvas.get_tk_widget().grid(row=0, column=0)  # Use grid for canvas
    plot_graph(graph, canvas)

    # Button to open the location graph window
    location_label = tk.Label(shortest_path_window, text="Enter Location:")
    location_label.pack(pady=10)
    location_entry = tk.Entry(shortest_path_window)
    location_entry.pack(pady=10)
    show_hotel_button = tk.Button(shortest_path_window, text="Show Hotel Graph", command=lambda: display_hotel_graph(location_entry.get()))
    show_hotel_button.pack(pady=10)
    shortest_path_window.mainloop()

# ... Your code ...



# ... (rest of your code)

import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import *
import requests
from io import BytesIO
from urllib import request

# Your functions and data here...

root = tk.Tk()
root.title("Places to Visit")
root.configure(bg="lightblue")

# Create a frame for text content on the left
text_frame = tk.Frame(root, bg="lightblue")
text_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

# Create a frame for the graph on the right
graph_frame = tk.Frame(root)
graph_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ne")

# Your text label
lbl2 = tk.Label(text_frame, text='''Welcome to our webpage
                    Welcome to our webpageTraveling is significant for several reasons,and its importance can vary depending on individual
    perspectivesand goals.
    Here are some of the key reasons why traveling is important:
    Cultural Exposure: Traveling allows you to experience and immerse yourself in different cultures,
    traditions,and lifestyles. This exposure can broaden your horizons and enhance your understanding
    of the world's diversity.Education and Learning: Traveling is an educational experience. It
    provides the opportunity to learn about history,geography, art, architecture, and languages
    firsthand. It can be a powerful teacher that goes beyond what you can learn in a classroom.
    ''', font=("Helvetica", 7), bg="lightblue")
lbl2.pack()

# Define your buttons and labels for the graph frame
places = ["DUBAI", "INDIA", "CHINA", "AUSTRALIA", "AMERICA"]

for i in range(0, len(places), 3):
    row_frame = tk.Frame(graph_frame)
    row_frame.grid(row=i // 3, column=0, columnspan=3, padx=10, pady=10)
    for j in range(3):
        if i + j < len(places):
            label = tk.Label(row_frame, text=places[i + j], bg="pink")
            button = tk.Button(row_frame, text="Visit", command=lambda p=places[i + j]: visit_place(p))
            label.grid(row=0, column=j, padx=10, pady=10)
            button.grid(row=1, column=j, padx=10, pady=10)

btn3 = Button(root, text="Search", width=8, height=2, bd=5, command=open_new_window)
btn3.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()


start_entry = None
end_entry = None



result_label = None



