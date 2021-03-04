"""Graph Util Class."""
from hdash.validator.categories import Categories


class GraphUtil:
    """Graph Utilities Class."""

    def __init__(self, node_map, edge_list):
        """Construct a new Graph Utility Class."""
        self.node_map = node_map
        self.edge_list = edge_list
        categories = Categories()
        abbrev_map = categories.abbrev_category_map

        self.data_list = []
        for node_id in node_map:
            node = node_map[node_id]
            dict = {}
            dict["id"] = node.id
            dict["label"] = abbrev_map[node.category] + "_" + node.label
            dict["category"] = node.category
            node_dict = {}
            node_dict["data"] = dict
            self.data_list.append(node_dict)

        edge_id = 0
        for edge in edge_list:
            dict = {}
            dict["id"] = "e" + str(edge_id)
            dict["source"] = edge.source_id
            dict["target"] = edge.target_id
            node_dict = {}
            node_dict["data"] = dict
            self.data_list.append(node_dict)
            edge_id += 1
            self.data_list.append(node_dict)
