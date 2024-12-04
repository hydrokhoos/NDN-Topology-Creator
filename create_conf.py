import os
import networkx as nx

def generate_router_configs_with_template(graph, output_dir, site_name):
    """
    Generate NLSR configuration files for each router based on the provided graph and template.

    Parameters:
    - graph: NetworkX graph object containing nodes and edges.
    - output_dir: Directory where the configuration files will be saved.
    - site_name: The site name to use in the configuration (e.g., "waseda").
    """
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

    for node in graph.nodes:
        config_file = os.path.join(output_dir, f"nlsr_{node}.conf")
        with open(config_file, "w") as f:
            # General section
            f.write("general\n{\n")
            f.write(f"    network /ndn\n")
            f.write(f"    site {site_name}\n")
            f.write(f"    router /%C1.Router/{node}\n")
            f.write("    lsa-refresh-time 1800\n")
            f.write("    lsa-interest-lifetime 4\n")
            f.write("    sync-protocol psync\n")
            f.write("    sync-interest-lifetime 60000\n")
            f.write("    state-dir /var/lib/nlsr\n")
            f.write("}\n\n")

            # Neighbors section
            f.write("neighbors\n{\n")
            for neighbor in graph.neighbors(node):
                f.write("  neighbor {\n")
                f.write(f"    name /ndn/{site_name}/%C1.Router/{neighbor}\n")
                f.write(f"    face-uri tcp4://{neighbor}\n")  # Face URI for TCP connection
                f.write("    link-cost 10\n")  # Default link cost
                f.write("  }\n")
            f.write("}\n\n")

            # Security section
            f.write("security\n{\n")
            f.write("    validator {\n")
            f.write("        trust-anchor {\n")
            f.write("            type any\n")
            f.write("        }\n")
            f.write("    }\n")
            f.write("    prefix-update-validator {\n")
            f.write("        trust-anchor {\n")
            f.write("            type any\n")
            f.write("        }\n")
            f.write("    }\n")
            f.write("}\n")

    print(f"Configurations have been generated in {output_dir}")

# Main Execution
if __name__ == "__main__":
    # Path to the GML file
    gml_file_path = "Geant2012.gml"

    # Load the GML file
    graph = nx.read_gml(gml_file_path)

    # Output directory for the generated configs
    output_dir = "./configs/"

    # Site name
    site_name = str(gml_file_path.split(".")[0])

    # Generate the configuration files
    generate_router_configs_with_template(graph, output_dir, site_name)
