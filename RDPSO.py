import random
import networkx as nx
import matplotlib.pyplot as plt
import os

class Task:
    def __init__(self, id, execution_time, data_size, dependencies=[]):
        self.id = id
        self.execution_time = execution_time
        self.data_size = data_size
        self.dependencies = dependencies

    def __repr__(self):
        return f"Task(id={self.id}, exec_time={self.execution_time}, data_size={self.data_size})"

class ServiceInstance:
    def __init__(self, id, cost_per_hour, data_transfer_rate):
        self.id = id
        self.cost_per_hour = cost_per_hour
        self.data_transfer_rate = data_transfer_rate

    def __repr__(self):
        return f"Service(id={self.id}, cost/hr={self.cost_per_hour}, data_rate={self.data_transfer_rate})"

class Particle:
    def __init__(self, tasks, services):
        self.position = {task: random.choice(services) for task in tasks}
        self.velocity = {task: {service: random.random() for service in services} for task in tasks}
        self.best_position = self.position.copy()
        self.best_cost = float('inf')

    def update_velocity(self, global_best, w=0.5, c1=1.0, c2=1.0):
        for task in self.velocity:
            for service in self.velocity[task]:
                r1, r2 = random.random(), random.random()
                cognitive_component = c1 * r1 * (self.best_position[task].id - service.id)
                social_component = c2 * r2 * (global_best[task].id - service.id)
                self.velocity[task][service] = w * self.velocity[task][service] + cognitive_component + social_component

    def update_position(self):
        for task in self.position:
            self.position[task] = max(self.velocity[task], key=self.velocity[task].get, default=self.position[task])

def calculate_cost(particle, tasks):
    total_cost = 0
    for task in tasks:
        service = particle.position[task]
        execution_cost = task.execution_time * service.cost_per_hour
        data_transfer_cost = sum(tasks[dep].data_size * service.data_transfer_rate for dep in task.dependencies if particle.position[tasks[dep]] != service)
        total_cost += execution_cost + data_transfer_cost
    return total_cost


def visualize_solution(tasks, services, best_solution, best_cost, folder_path):
    G = nx.DiGraph()
    pos = {}
    labels = {}
    node_colors = []

    # Create a layout that extends the width
    fig, ax = plt.subplots(figsize=(12, 8))  # Increase the width of the figure

    # Add task nodes with a specific position
    for i, task in enumerate(tasks):
        task_node = f"Task {task.id}"
        G.add_node(task_node)
        pos[task_node] = (1, -i)  # Line up on the left
        labels[task_node] = f"{task_node}\n(Exec Time: {task.execution_time}, Data: {task.data_size} MB)"
        node_colors.append('skyblue')

    # Add service nodes with a specific position
    for i, service in enumerate(services):
        service_node = f"Service {service.id}"
        G.add_node(service_node)
        pos[service_node] = (2, -i)  # Line up on the right
        labels[
            service_node] = f"{service_node}\n(Cost/hr: {service.cost_per_hour}, Data Rate: {service.data_transfer_rate})"
        node_colors.append('lightgreen')

    # Add edges between tasks and their assigned services
    for task in tasks:
        service = best_solution[task]
        G.add_edge(f"Task {task.id}", f"Service {service.id}")

    # Draw the network graph with adjusted positions and labels
    nx.draw(G, pos, labels=labels, node_color=node_colors, with_labels=True, node_size=2500, edge_color='gray', width=2,
            font_size=10, font_color='black', font_weight='bold', arrowstyle='-|>', arrowsize=15)
    plt.title('Task to Service Assignment', size=15)

    # Display the best cost in the plot
    plt.annotate(f"Best Cost: {best_cost}", xy=(0.5, -0.1), xycoords="axes fraction", ha='center', va='center', fontsize=12, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="black", lw=1))

    # Adjust the plot margins and space specifically for the left and right
    plt.margins(0.2)  # Add 20% more space on the left and right sides

    # Save the figure with extra space for the labels
    plt.savefig(f"{folder_path}/task_service_mapping.png", bbox_inches="tight")
    plt.show()

def rd_pso(tasks, services, num_particles=10, max_iters=100, output_folder='output'):
    particles = [Particle(tasks, services) for _ in range(num_particles)]
    global_best = particles[0].position
    global_best_cost = calculate_cost(particles[0], tasks)

    for _ in range(max_iters):
        for particle in particles:
            particle.update_velocity(global_best)
            particle.update_position()
            current_cost = calculate_cost(particle, tasks)
            if current_cost < particle.best_cost:
                particle.best_cost = current_cost
                particle.best_position = particle.position.copy()
            if current_cost < global_best_cost:
                global_best = particle.position.copy()
                global_best_cost = current_cost

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

        # Now that we have the best solution and cost, call visualize_solution
    visualize_solution(tasks, services, global_best, global_best_cost, output_folder)

    # Return the best solution and cost from the RDPSO function
    return global_best, global_best_cost

# Sample tasks and services for demonstration
tasks = [
    Task(1, 3, 100),
    Task(2, 2, 150, [1]),
    Task(3, 1, 200, [1, 2]),
    Task(4, 4, 100, [2]),
    Task(5, 2, 300, [3, 4])
]
services = [
    ServiceInstance(1, 0.20, 0.05),
    ServiceInstance(2, 0.15, 0.03),
    ServiceInstance(3, 0.25, 0.02)
]

best_solution, best_cost = rd_pso(tasks, services)
print("Best Solution:")
for task, service in best_solution.items():
    print(f"Task {task.id} -> Service {service.id}")
print("Best Cost:", best_cost)