import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

def main():
    # コマンドライン引数の確認
    if len(sys.argv) != 2:
        print("Usage: python3 gml_show.py <path_to_gml_file>")
        sys.exit(1)

    gml_file = sys.argv[1]

    # ファイルの存在確認
    if not os.path.exists(gml_file):
        print(f"Error: File '{gml_file}' does not exist.")
        sys.exit(1)

    try:
        # GMLファイルの読み込み
        print(f"Loading GML file: {gml_file}")
        graph = nx.read_gml(gml_file)
    except Exception as e:
        print(f"Error: Failed to load GML file. {e}")
        sys.exit(1)

    # グラフ情報の表示
    print(f"Graph loaded successfully!")
    print(f"Number of nodes: {graph.number_of_nodes()}")
    print(f"Number of edges: {graph.number_of_edges()}")

    # 可視化
    try:
        print("Visualizing the graph...")
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(graph, seed=42)  # 安定したレイアウト
        nx.draw(
            graph,
            pos,
            with_labels=True,
            node_size=500,
            node_color="lightblue",
            font_size=10,
            font_color="black",
            edge_color="gray",
        )
        plt.title("Network Topology Visualization")
        plt.show()

        # ファイルとして保存する場合
        save_option = input("Do you want to save the visualization? (y/n): ").strip().lower()
        if save_option == "y":
            output_file = "graph_visualization.png"
            plt.savefig(output_file, format="png", dpi=300)
            print(f"Graph visualization saved as '{output_file}'.")

    except Exception as e:
        print(f"Error: Failed to visualize the graph. {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
