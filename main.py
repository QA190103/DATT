import random
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import messagebox


class Graph:
    def __init__(self, root):
        self.graph_drawn = False
        self.max_edges = None
        self.max_nodes = None
        self.canvas_widget = None
        self.canvas = None
        self.right_sub_frame = None
        self.left_sub_frame = None
        self.root = root
        self.G = nx.DiGraph()
        self.root.title("Graph management application")
        self.root.state('zoomed')
        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        self.button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "white",
            "fg": "#4A90E2",
            "activebackground": "white",
            "activeforeground": "#4A90E2",
            "bd": 1,
            "relief": "raised",
            "width": 20,
            "height": 2
        }
        self.button_style_min = {
            "font": ("Arial", 12, "bold"),
            "bg": "white",
            "fg": "#4A90E2",
            "activebackground": "white",
            "activeforeground": "#4A90E2",
            "bd": 1,
            "relief": "raised",
            "height": 2
        }
        self.right_frame = None
        self.left_frame = None
        self.buttons = None
        self.current_page = None
        self.current_input = ""
        self.pages = {}
        self.page_frames = {}
        self.left_layout()
        self.right_layout()
        self.create_pages()
        self.show_page("Shortest Path")
        self.is_directed = False
        self.is_weighted = False
        self.pos = None

    def left_layout(self):
        self.left_frame = tk.Frame(self.root, width=self.screen_width * 0.15,
                                   height=self.screen_height, bg="lightblue")
        self.left_frame.pack(side="left", fill=tk.BOTH, expand=True)
        self.left_frame.pack_propagate(False)
        self.create_menu()

    def right_layout(self):
        self.right_frame = tk.Frame(self.root, width=self.screen_width * 0.85,
                                    height=self.screen_height)
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side="right", fill=tk.BOTH, expand=True)

    def create_menu(self):
        label = tk.Label(self.left_frame, text="Menu", bg="lightblue",
                         font=("Arial", 16, "bold"))
        label.pack(pady=10)

        button1 = tk.Button(self.left_frame, text="Shortest Path",
                            **self.button_style,
                            command=lambda: self.show_page("Shortest Path"))
        button1.pack(pady=5)

        button2 = tk.Button(self.left_frame, text="Minimum Spanning Tree",
                            **self.button_style,
                            command=lambda: self.show_page("Minimum Spanning Tree"))
        button2.pack(pady=5)

        button3 = tk.Button(self.left_frame, text="Import", **self.button_style,
                            command=lambda: self.import_graph)
        button3.pack(pady=5)

        button4 = tk.Button(self.left_frame, text="Export", **self.button_style,
                            command=lambda: self.import_graph)
        button4.pack(pady=5)

        self.buttons = [button1, button2, button3, button4]

    def create_pages(self):
        for page in ["Shortest Path", "Minimum Spanning Tree"]:
            frame = tk.Frame(self.right_frame)
            page_content = self.layout_right_frame(frame, page)
            self.page_frames[page] = frame
            self.pages[page] = page_content

    def layout_right_frame(self, frame, page):
        header_frame = tk.Frame(frame, height=50)
        header_frame.pack(side="top", fill=tk.X)

        header_label = tk.Label(header_frame, text=f"{page}", font=("Arial", 18, "bold"))
        header_label.pack(pady=10)

        bottom_frame = tk.Frame(frame)
        bottom_frame.pack(side="bottom", fill=tk.BOTH)

        button_frame = tk.Frame(bottom_frame)
        button_frame.pack(side="left", fill=tk.BOTH, expand=True)

        empty_frame = tk.Frame(bottom_frame)
        empty_frame.pack(side="right", fill=tk.BOTH, expand=True)

        button1 = tk.Button(button_frame, text="Vẽ đồ thị", **self.button_style_min,
                            command=lambda: self.draw_graph(page))
        button1.pack(side="left", padx=5)

        button2 = tk.Button(button_frame, text="Random đồ thị", **self.button_style_min,
                            command=lambda: self.random_graph(page))
        button2.pack(side="left", padx=5)

        button3_text = page if page in ["Shortest Path", "Minimum Spanning Tree"] else "Default"
        if button3_text == "Shortest Path":
            button3 = tk.Button(button_frame, text=button3_text, **self.button_style_min,
                                command=lambda: self.model_shortest_path())
        else:
            button3 = tk.Button(button_frame, text=button3_text, **self.button_style_min,
                                command=lambda: self.minimum_spanning_tree())
        button3.pack(side="left", padx=5)

        content_frame = tk.Frame(frame)
        content_frame.pack(side="top", fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(content_frame, width=self.screen_width * 0.8 * 0.2)
        input_frame.pack_propagate(False)
        input_frame.pack(side="left", fill=tk.BOTH, padx=2, pady=2)

        left_sub_frame = tk.Frame(content_frame, width=self.screen_width * 0.8 * 0.3, bg="white")
        left_sub_frame.pack_propagate(False)
        left_sub_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=2, pady=2)

        right_sub_frame = tk.Frame(content_frame, width=self.screen_width * 0.8 * 0.3, bg="white")
        right_sub_frame.pack_propagate(False)
        right_sub_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=2, pady=2)

        input_entry = tk.Text(input_frame, font=("Arial", 12))
        input_entry.pack(side="left", fill=tk.BOTH, expand=True)
        if self.current_input:
            input_entry.insert("1.0", self.current_input)

        return {
            'frame': frame,
            'input': input_entry,
            'left_frame': left_sub_frame,
            'right_frame': right_sub_frame
        }
    def show_page(self, page_name):
        if self.current_page:
            self.current_input = self.pages[self.current_page]['input'].get("1.0", tk.END).strip()

        for frame in self.page_frames.values():
            frame.pack_forget()

        self.page_frames[page_name].pack(fill=tk.BOTH, expand=True)
        self.page_frames[page_name].pack_propagate(False)

        input_widget = self.pages[page_name]['input']
        input_widget.delete("1.0", tk.END)
        if self.current_input:
            input_widget.insert("1.0", self.current_input)

        # Vẽ lại đồ thị mỗi khi chuyển trang
        if self.current_input:
            self.redraw_graph(page_name)

        for button in self.buttons:
            button.config(bg="white", fg="#4A90E2")

        active_button = self.buttons[["Shortest Path", "Minimum Spanning Tree"].index(page_name)]
        active_button.config(bg="#4A90E2", fg="white")

        self.current_page = page_name

    def redraw_graph(self, page_name):
        for widget in self.pages[page_name]['left_frame'].winfo_children():
            widget.destroy()

        fig, ax = plt.subplots()
        nx.draw_networkx_nodes(self.G, pos=self.pos, node_color="blue", ax=ax)
        nx.draw_networkx_edges(self.G, pos=self.pos, edge_color="black", arrows=self.is_directed, ax=ax)
        if self.is_weighted:
            edge_labels = nx.get_edge_attributes(self.G, 'weight')
            nx.draw_networkx_edge_labels(self.G, pos=self.pos, edge_labels=edge_labels, ax=ax)
        nx.draw_networkx_labels(self.G, pos=self.pos, ax=ax, font_color="white")

        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.pages[page_name]['left_frame'])
        self.canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas_widget.draw()
    def parse_input(self, value):
        lines = value.split("\n")
        arrayVertices = []
        arrayEdges = []
        arrayWeights = []
        for line in lines:
            items = line.split(",")
            if len(items) == 2:
                if items[0] not in arrayVertices:
                    arrayVertices.append(int(items[0]))
                if items[1] not in arrayVertices:
                    arrayVertices.append(int(items[1]))
                arrayEdges.append((int(items[0]), int(items[1])))
                arrayWeights.append((int(items[0]), int(items[1]), 1))
            elif len(items) == 3:
                if items[0] not in arrayVertices:
                    arrayVertices.append(int(items[0]))
                if items[1] not in arrayVertices:
                    arrayVertices.append(int(items[1]))
                arrayEdges.append((int(items[0]), int(items[1])))
                arrayWeights.append((int(items[0]), int(items[1]), int(items[2])))
            else:
                self.show_error_modal("Dữ liệu đầu vào không đúng format")
                return False
        self.G.add_nodes_from(arrayVertices)
        self.G.add_edges_from(arrayEdges)
        self.G.add_weighted_edges_from(arrayWeights)
        return True

    def show_error_modal(self, message):
        modal = tk.Toplevel(self.root)
        modal.title("Lỗi")
        modal_width = 400
        modal_height = 150

        # Tính toán vị trí giữa màn hình
        x_position = (self.root.winfo_screenwidth() // 2) - (modal_width // 2)
        y_position = (self.root.winfo_screenheight() // 2) - (modal_height // 2)
        modal.geometry(f"{modal_width}x{modal_height}+{x_position}+{y_position}")

        modal.transient(self.root)
        modal.grab_set()

        label = tk.Label(modal, text=message, font=("Arial", 14), fg="red")
        label.pack(pady=10)

        close_button = tk.Button(modal, text="Đóng", command=modal.destroy, **self.button_style_min)
        close_button.pack(pady=10)

        modal.wait_window()

    def model_choice_draw_graph(self, page):
        modal = tk.Toplevel(self.root)
        modal.title("Chọn loại đồ thị")
        modal_width = 300
        modal_height = 200

        x_position = (self.root.winfo_screenwidth() // 2) - (modal_width // 2)
        y_position = (self.root.winfo_screenheight() // 2) - (modal_height // 2)
        modal.geometry(f"{modal_width}x{modal_height}+{x_position}+{y_position}")

        modal.transient(self.root)
        modal.grab_set()

        label = tk.Label(modal, text="Chọn loại đồ thị để vẽ:", font=("Arial", 14))
        label.pack(pady=10)

        is_directed = tk.BooleanVar()
        is_weighted = tk.BooleanVar()

        checkbox_directed = tk.Checkbutton(modal, text="Đồ thị có hướng", variable=is_directed, font=("Arial", 12))
        checkbox_directed.pack(pady=5)

        checkbox_weighted = tk.Checkbutton(modal, text="Đồ thị có trọng số", variable=is_weighted, font=("Arial", 12))
        checkbox_weighted.pack(pady=5)

        draw_button = tk.Button(
            modal,
            text="Vẽ đồ thị",
            **self.button_style_min,
            command=lambda: self.set_graph_type(
                modal, is_directed.get(), is_weighted.get(),
            )
        )
        draw_button.pack(pady=10)

        modal.wait_window()

    def set_graph_type(self, modal, directed, weighted):
        self.is_directed = directed
        self.is_weighted = weighted

        nodes = list(self.G.nodes)
        edges = list(self.G.edges(data=True))

        self.G.clear()
        self.G = nx.DiGraph() if self.is_directed else nx.Graph()

        # Thêm lại các đỉnh và cạnh vào đồ thị mới
        self.G.add_nodes_from(nodes)
        self.G.add_edges_from(edges)

        modal.destroy()

    def draw_graph(self, page):
        # Nếu đã có canvas_widget, chỉ cần hiển thị lại
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True, side="left")
            return

        input_value = self.pages[page]['input'].get("1.0", tk.END).strip()
        if self.parse_input(input_value):
            fig, ax = plt.subplots()

            # Chỉ tính toán bố cục một lần
            if not self.pos:
                self.pos = nx.spring_layout(self.G)

            nx.draw_networkx_nodes(self.G, pos=self.pos, node_color="blue", ax=ax)
            nx.draw_networkx_edges(self.G, pos=self.pos, edge_color="black", arrows=self.is_directed, ax=ax)

            if self.is_weighted:
                edge_labels = nx.get_edge_attributes(self.G, 'weight')
                nx.draw_networkx_edge_labels(self.G, pos=self.pos, edge_labels=edge_labels, ax=ax)

            nx.draw_networkx_labels(self.G, pos=self.pos, ax=ax, font_color="white")

            # Tạo lại canvas và hiển thị
            self.canvas = FigureCanvasTkAgg(fig, master=self.pages[page]['left_frame'])
            self.canvas_widget = self.canvas
            self.canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.canvas.draw()

    def set_graph_type_for_random(self, modal, directed, weighted, max_nodes, max_edges):
        self.is_directed = directed
        self.is_weighted = weighted

        if max_nodes < 0:
            self.show_error_modal(f"Số đỉnh tối đa phải lớn hơn 0")
            return
        if max_edges < 0:
            self.show_error_modal(f"Số cạnh tối đa phải lớn hơn 0")
            return
        if max_nodes * (max_nodes - 1) < max_edges * 2:
            self.show_error_modal(f"Số cạnh tối đa phải nằm trong khoảng 0 đến {int(max_nodes * (max_nodes - 1) / 2)}")
            return
        self.max_nodes = max_nodes
        self.max_edges = max_edges

        nodes = list(self.G.nodes)
        edges = list(self.G.edges(data=True))

        self.G.clear()
        self.G = nx.DiGraph() if self.is_directed else nx.Graph()

        # Thêm lại các đỉnh và cạnh vào đồ thị mới
        self.G.add_nodes_from(nodes)
        self.G.add_edges_from(edges)

        modal.destroy()

    def model_choice_random_graph(self):
        modal = tk.Toplevel(self.root)
        modal.title("Chọn loại đồ thị")
        modal_width = 300
        modal_height = 400

        x_position = (self.root.winfo_screenwidth() // 2) - (modal_width // 2)
        y_position = (self.root.winfo_screenheight() // 2) - (modal_height // 2)
        modal.geometry(f"{modal_width}x{modal_height}+{x_position}+{y_position}")

        modal.transient(self.root)
        modal.grab_set()

        label = tk.Label(modal, text="Chọn loại đồ thị để vẽ:", font=("Arial", 14))
        label.pack(pady=10)

        # Thêm trường nhập số đỉnh tối đa
        label_vertices = tk.Label(modal, text="Số đỉnh tối đa:", font=("Arial", 12))
        label_vertices.pack(pady=5)
        entry_vertices = tk.Entry(modal, font=("Arial", 12))
        entry_vertices.pack(pady=5)

        # Thêm trường nhập số cạnh tối đa
        label_edges = tk.Label(modal, text="Số cạnh tối đa của mỗi đỉnh:", font=("Arial", 12))
        label_edges.pack(pady=5)
        entry_edges = tk.Entry(modal, font=("Arial", 12))
        entry_edges.pack(pady=5)

        is_directed = tk.BooleanVar()
        is_weighted = tk.BooleanVar()

        checkbox_directed = tk.Checkbutton(modal, text="Đồ thị có hướng", variable=is_directed, font=("Arial", 12))
        checkbox_directed.pack(pady=5)

        checkbox_weighted = tk.Checkbutton(modal, text="Đồ thị có trọng số", variable=is_weighted, font=("Arial", 12))
        checkbox_weighted.pack(pady=5)

        draw_button = tk.Button(
            modal,
            text="Vẽ đồ thị",
            **self.button_style_min,
            command=lambda: self.set_graph_type_for_random(
                modal, is_directed.get(), is_weighted.get(),
                int(entry_vertices.get()), int(entry_edges.get())
            )
        )
        draw_button.pack(pady=10)

        modal.wait_window()

    def random_input(self):
        currentNode = self.max_nodes
        arrayVertices = []
        arrayEdges = []
        arrayWeights = []

        for i in range(1, currentNode+1):
            arrayVertices.append(i)

        for node in arrayVertices:
            currentEdge = random.randint(0, len(arrayVertices) - 1)
            currentArrayNodes = arrayVertices.copy()
            currentArrayNodes.remove(node)
            if len(currentArrayNodes) > 0:
                for i in range(currentEdge):
                    current_choice_node = random.choice(currentArrayNodes)
                    if self.is_weighted:
                        current_weight = random.randint(1, 10)
                        arrayEdges.append((node, current_choice_node))
                        arrayWeights.append((node, current_choice_node, current_weight))
                    else:
                        arrayEdges.append((node, current_choice_node))
                        arrayWeights.append((node, current_choice_node, "1"))
                    currentArrayNodes.remove(current_choice_node)
        self.pages[self.current_page]['input'].delete("1.0", tk.END)
        self.pages[self.current_page]['input'].insert("1.0", "\n".join(f"{u},{v},{w}" for (u, v, w) in arrayWeights))
        self.G.add_nodes_from(arrayVertices)
        self.G.add_edges_from(arrayEdges)
        self.G.add_weighted_edges_from(arrayWeights)

    def random_graph(self, page):
        # Xóa đồ thị cũ và khởi tạo đồ thị mới
        self.G.clear()
        self.G = nx.DiGraph() if self.is_directed else nx.Graph()
        self.graph_drawn = False

        # Thiết lập thông số random của đồ thị
        self.model_choice_random_graph()
        self.random_input()

        # Xóa `canvas_widget` cũ nếu tồn tại
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().pack_forget()
            self.canvas_widget = None

        # Xóa các widget trong khung bên trái trước khi vẽ đồ thị mới
        for widget in self.pages[page]['left_frame'].winfo_children():
            widget.destroy()

        # Tạo đồ thị mới và hiển thị
        fig, ax = plt.subplots()
        self.pos = nx.spring_layout(self.G)

        nx.draw_networkx_nodes(self.G, pos=self.pos, node_color="blue", ax=ax)
        nx.draw_networkx_edges(self.G, pos=self.pos, edge_color="black", arrows=self.is_directed, ax=ax)

        if self.is_weighted:
            edge_labels = nx.get_edge_attributes(self.G, 'weight')
            nx.draw_networkx_edge_labels(self.G, pos=self.pos, edge_labels=edge_labels, ax=ax)

        nx.draw_networkx_labels(self.G, pos=self.pos, ax=ax, font_color="white")

        # Tạo lại `canvas_widget` với đồ thị mới
        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.pages[page]['left_frame'])
        self.canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas_widget.draw()

    def model_shortest_path(self):
        modal = tk.Toplevel(self.root)
        modal.title("Chọn các đỉnh để tìm đường đi ngắn nhất")
        modal_width = 300
        modal_height = 400

        x_position = (self.root.winfo_screenwidth() // 2) - (modal_width // 2)
        y_position = (self.root.winfo_screenheight() // 2) - (modal_height // 2)
        modal.geometry(f"{modal_width}x{modal_height}+{x_position}+{y_position}")

        modal.transient(self.root)
        modal.grab_set()

        label = tk.Label(modal, text="Chọn các đỉnh để tìm đường đi ngắn nhất", font=("Arial", 14))
        label.pack(pady=10)

        # Thêm trường nhập số đỉnh tối đa
        label_vertices = tk.Label(modal, text="Chọn đỉnh 1:", font=("Arial", 12))
        label_vertices.pack(pady=5)
        entry_vertices = tk.Entry(modal, font=("Arial", 12))
        entry_vertices.pack(pady=5)

        # Thêm trường nhập số cạnh tối đa
        label_edges = tk.Label(modal, text="Chọn đỉnh 2:", font=("Arial", 12))
        label_edges.pack(pady=5)
        entry_edges = tk.Entry(modal, font=("Arial", 12))
        entry_edges.pack(pady=5)

        draw_button = tk.Button(
            modal,
            text="Tìm",
            **self.button_style_min,
            command=lambda: self.shortest_path(
                modal,int(entry_vertices.get()), int(entry_edges.get())
            )
        )
        draw_button.pack(pady=10)

        modal.wait_window()

    def shortest_path(self, modal, vertex_1, vertex_2):
        try:
            # Tìm đường đi ngắn nhất
            path = nx.shortest_path(self.G, source=vertex_1, target=vertex_2)

            # Tạo danh sách các cạnh trong đường đi ngắn nhất
            path_edges = list(zip(path[:-1], path[1:]))

            # Xóa các widget trong right frame
            for widget in self.pages[self.current_page]['right_frame'].winfo_children():
                widget.destroy()

            # Vẽ đồ thị mới với đường đi ngắn nhất
            fig_shortest, ax_shortest = plt.subplots()
            nx.draw_networkx_nodes(self.G, self.pos, node_color='lightblue', node_size=500, ax=ax_shortest)
            nx.draw_networkx_labels(self.G, self.pos, ax=ax_shortest)

            if self.is_weighted:
                edge_labels = nx.get_edge_attributes(self.G, 'weight')
                nx.draw_networkx_edge_labels(self.G, pos=self.pos, edge_labels=edge_labels, ax=ax_shortest)

            # Thêm tiêu đề
            path_length = len(path) - 1
            total_weight = sum(float(self.G[path[i]][path[i + 1]]['weight']) for i in range(len(path) - 1))
            ax_shortest.set_title(f'Shortest Path: {" -> ".join(map(str, path))}\n'
                                  f'Length: {path_length} edges, Total weight: {total_weight}')

            # Tạo canvas và hiển thị
            canvas_shortest = FigureCanvasTkAgg(fig_shortest, master=self.pages[self.current_page]['right_frame'])
            canvas_shortest_widget = canvas_shortest.get_tk_widget()
            canvas_shortest_widget.pack(fill=tk.BOTH, expand=True)

            # Hàm cập nhật cho animation
            def update(num):
                ax_shortest.clear()  # Xóa nội dung của biểu đồ ở mỗi khung hình
                nx.draw_networkx_nodes(self.G, self.pos, node_color='lightblue', node_size=500, ax=ax_shortest)
                nx.draw_networkx_labels(self.G, self.pos, ax=ax_shortest)

                # Vẽ các cạnh đến bước hiện tại
                nx.draw_networkx_edges(self.G, self.pos, edgelist=path_edges[:num + 1], edge_color='red', width=2,
                                       ax=ax_shortest)

                # Hiển thị trọng số nếu có
                if self.is_weighted:
                    edge_labels = nx.get_edge_attributes(self.G, 'weight')
                    nx.draw_networkx_edge_labels(self.G, pos=self.pos, edge_labels=edge_labels, ax=ax_shortest)

                # Cập nhật tiêu đề với phần đường đi hiện tại
                current_path = " -> ".join(map(str, path[:num + 2]))  # Cập nhật chuỗi đường đi từ đầu đến bước hiện tại
                ax_shortest.set_title(f'Shortest Path Animation: {current_path}')

            # Tạo animation
            ani = animation.FuncAnimation(fig_shortest, update, frames=len(path_edges), interval=1000, repeat=True)

            canvas_shortest.draw()
            modal.destroy()

        except nx.NetworkXNoPath:
            self.show_error_modal(f"Không tìm thấy đường đi giữa đỉnh {vertex_1} và đỉnh {vertex_2}")
            modal.destroy()
        except Exception as e:
            self.show_error_modal(f"Lỗi: {str(e)}")
            modal.destroy()

    def minimum_spanning_tree(self):
        # Kiểm tra đồ thị có hướng hay không
        if self.is_directed:
            self.show_error_modal("Minimum Spanning Tree chỉ áp dụng cho đồ thị vô hướng.")
            return

        # Kiểm tra đồ thị có trọng số không
        if not self.is_weighted:
            self.show_error_modal("Minimum Spanning Tree chỉ áp dụng cho đồ thị có trọng số.")
            return

        # Tính toán MST
        mst = nx.minimum_spanning_tree(self.G)

        # Xóa các widget trong khung bên phải để hiển thị MST
        for widget in self.pages[self.current_page]['right_frame'].winfo_children():
            widget.destroy()

        # Vẽ đồ thị MST
        fig_mst, ax_mst = plt.subplots()

        # Vẽ các nút
        nx.draw_networkx_nodes(self.G, self.pos, ax=ax_mst, node_color='lightblue', node_size=500)
        nx.draw_networkx_labels(self.G, self.pos, ax=ax_mst)

        # Vẽ các cạnh của MST màu xanh lá cây
        nx.draw_networkx_edges(mst, self.pos, ax=ax_mst, edge_color='green', width=2)

        # Vẽ trọng số cạnh nếu là đồ thị có trọng số
        if self.is_weighted:
            edge_labels = nx.get_edge_attributes(mst, 'weight')
            nx.draw_networkx_edge_labels(mst, self.pos, edge_labels=edge_labels, ax=ax_mst)

        # Hiển thị MST bên phải
        canvas_mst = FigureCanvasTkAgg(fig_mst, master=self.pages[self.current_page]['right_frame'])
        canvas_mst_widget = canvas_mst.get_tk_widget()
        canvas_mst_widget.pack(fill=tk.BOTH, expand=True)
        canvas_mst.draw()


if __name__ == "__main__":
    root_tk = tk.Tk()
    app = Graph(root_tk)
    root_tk.mainloop()