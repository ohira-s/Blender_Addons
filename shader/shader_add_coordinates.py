##############################################################
# Blender Addon
#   Blender Version: 4.3.2
#   Target: Shader Editor > Tool
#   Functions:
#     - Create nodes for calculating cylindrical coordinates.
#   Author: Shunsuke Ohira
#   License: GPLv2
#   Addon Version:
#     0.1.0: 2025/03/05
#          - Cylindrical coordinates
#          - Polar coordinates
##############################################################
import bpy
from bpy.props import (
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    BoolProperty,
)

# Addon information
bl_info = {
    "name": "Add Coordinates Nodes",
    "author": "Shunsuke Ohira",
    "version": (0, 1, 0),
    "blender": (4, 3, 2),
    "location": "シェーダーエディター",
    "description": "Add Coordinates Nodes",
    "warning": "",
    "support": "COMMUNITY",
    "doc_utl": "",
    "tracker_url": "",
    "category": "Shader",
}

# Panel class
class NodeCoordinatesNoePanel(bpy.types.Panel):
    # Panel information
    bl_idname = "NODE_PT_CoordinatesNodes"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Add Corrdinates Nodes"
    bl_region_type = "UI"
    bl_category = "Tool"

    # Drawing panel
    def draw(self, context):
        # Draw on the Shader Editor Node Tree
        material = context.material
        if hasattr(material, 'node_tree'):
            node_tree = material.node_tree
            layout = self.layout
            scene = context.scene

            # Place a label on this panel
            layout.label(text="Coordinates Type:")

            # Place a property (Dropdown list with an enum)
            layout.prop(scene, "NodeCoordinates_type_prop_enum", text="Type")

            # Place a button to execute an operator
            op = layout.operator(NODE_OT_CoordinatesNodes.bl_idname, text = "Create Nodes")
            
            # Set initial value of the dropdown list to the operator
            op.NodeCoordinates_type_prop_enum = scene.NodeCoordinates_type_prop_enum

# Operator class
class NODE_OT_CoordinatesNodes(bpy.types.Operator):
    # Operator information
    bl_idname = "nodetree.coordinatesnode"
    bl_label = "Add corrdinates nodes"
    bl_desicription = "Add corrdinates nodes"
    bl_options = {"REGISTER", "UNDO"}

    # Dropdown list to choose a coordinates to create nodes
    NodeCoordinates_type_prop_enum : EnumProperty(
        name="Types",
        description="Enum Property",
        items=[
            ('ITEM_1', "Cylindrical", "Cylindrical Coordinates"),
            ('ITEM_2', "Polar", "Polar Coordinates"),
        ],
        default='ITEM_1'
    )

    ### CYLINDRICAL COORDINATES NODES DEFINITIONS ###
    # Nodes list for the Cylindrical Coordinates
    node_list_cylindrical = [
        {"ID": "TexCoord",                     "Node": "ShaderNodeTexCoord",    "Location": ( 0, 0)},
        {"ID": "MappingIn",                    "Node": "ShaderNodeMapping",     "Location": ( 1, 0)},
        {"ID": "SeparateXYZ",                  "Node": "ShaderNodeSeparateXYZ", "Location": ( 2, 0)},
        {"ID": "X^2",                          "Node": "ShaderNodeMath",        "Location": ( 3, 2), "Operation": "POWER",      "Inputs": [None, 2.0]},
        {"ID": "Y^2",                          "Node": "ShaderNodeMath",        "Location": ( 3, 1), "Operation": "POWER",      "Inputs": [None, 2.0]},
        {"ID": "X^2+Y^2",                      "Node": "ShaderNodeMath",        "Location": ( 4, 1), "Operation": "ADD",        "Inputs": []},
        {"ID": "SQRT(X^2+Y^2)",                "Node": "ShaderNodeMath",        "Location": ( 5, 1), "Operation": "SQRT",       "Inputs": []},
        {"ID": "X/SQRT(X^2+Y^2)",              "Node": "ShaderNodeMath",        "Location": ( 6,-1), "Operation": "DIVIDE",     "Inputs": []},
        {"ID": "ACOS(X/SQRT(X^2+Y^2))",        "Node": "ShaderNodeMath",        "Location": ( 7, 0), "Operation": "ARCCOSINE",  "Inputs": []},
        {"ID": "SGN(Y)",                       "Node": "ShaderNodeMath",        "Location": ( 8, 1), "Operation": "SIGN",       "Inputs": []},
        {"ID": "SGN(Y)*ACOS(X/SQRT(X^2+Y^2))", "Node": "ShaderNodeMath",        "Location": ( 9, 1), "Operation": "MULTIPLY",   "Inputs": []},
        {"ID": "CombineXYZ",                   "Node": "ShaderNodeCombineXYZ",  "Location": (10, 0)},
        {"ID": "MappingOut",                   "Node": "ShaderNodeMapping",     "Location": (11, 0)},
    ]
    
    # Link list for the Cylindrical Coordinates
    link_list_cylindrical = [
        {"From": ["TexCoord", 3],                     "To": ["MappingIn", 0]},
        {"From": ["MappingIn", 0],                    "To": ["SeparateXYZ", 0]},
        {"From": ["SeparateXYZ", 0],                  "To": ["X^2", 0]},
        {"From": ["SeparateXYZ", 1],                  "To": ["Y^2", 0]},
        {"From": ["X^2", 0],                          "To": ["X^2+Y^2", 0]},
        {"From": ["Y^2", 0],                          "To": ["X^2+Y^2", 1]},
        {"From": ["X^2+Y^2", 0],                      "To": ["X^2+Y^2+Z^2", 0]},
        {"From": ["X^2+Y^2", 0],                      "To": ["SQRT(X^2+Y^2)", 0]},
        {"From": ["SeparateXYZ", 0],                  "To": ["X/SQRT(X^2+Y^2)", 0]},
        {"From": ["SQRT(X^2+Y^2)", 0],                "To": ["X/SQRT(X^2+Y^2)", 1]},
        {"From": ["X/SQRT(X^2+Y^2)", 0],              "To": ["ACOS(X/SQRT(X^2+Y^2))", 0]},
        {"From": ["SeparateXYZ", 1],                  "To": ["SGN(Y)", 0]},
        {"From": ["SGN(Y)", 0],                       "To": ["SGN(Y)*ACOS(X/SQRT(X^2+Y^2))", 0]},
        {"From": ["ACOS(X/SQRT(X^2+Y^2))", 0],        "To": ["SGN(Y)*ACOS(X/SQRT(X^2+Y^2))", 1]},
        {"From": ["SGN(Y)*ACOS(X/SQRT(X^2+Y^2))", 0], "To": ["CombineXYZ", 0]},
        {"From": ["SQRT(X^2+Y^2)", 0],                "To": ["CombineXYZ", 1]},
        {"From": ["SeparateXYZ", 2],                  "To": ["CombineXYZ", 2]},
        {"From": ["CombineXYZ", 0],                   "To": ["MappingOut", 0]},
    ]

    ### POLAR COORDINATES NODES DEFINITIONS ###
    # Nodes list for the Polar Coordinates
    node_list_polar = [
        {"ID": "TexCoord",                     "Node": "ShaderNodeTexCoord",    "Location": ( 0, 0)},
        {"ID": "MappingIn",                    "Node": "ShaderNodeMapping",     "Location": ( 1, 0)},
        {"ID": "SeparateXYZ",                  "Node": "ShaderNodeSeparateXYZ", "Location": ( 2, 0)},
        {"ID": "X^2",                          "Node": "ShaderNodeMath",        "Location": ( 3, 2), "Operation": "POWER",      "Inputs": [None, 2.0]},
        {"ID": "Y^2",                          "Node": "ShaderNodeMath",        "Location": ( 3, 1), "Operation": "POWER",      "Inputs": [None, 2.0]},
        {"ID": "Z^2",                          "Node": "ShaderNodeMath",        "Location": ( 3, 0), "Operation": "POWER",      "Inputs": [None, 2.0]},
        {"ID": "X^2+Y^2",                      "Node": "ShaderNodeMath",        "Location": ( 4, 1), "Operation": "ADD",        "Inputs": []},
        {"ID": "X^2+Y^2+Z^2",                  "Node": "ShaderNodeMath",        "Location": ( 5, 1), "Operation": "ADD",        "Inputs": []},
        {"ID": "SQRT(X^2+Y^2)",                "Node": "ShaderNodeMath",        "Location": ( 6, 1), "Operation": "SQRT",       "Inputs": []},
        {"ID": "SQRT(X^2+Y^2+Z^2)",            "Node": "ShaderNodeMath",        "Location": ( 7, 1), "Operation": "SQRT",       "Inputs": []},
        {"ID": "X/SQRT(X^2+Y^2)",              "Node": "ShaderNodeMath",        "Location": ( 8, 0), "Operation": "DIVIDE",     "Inputs": []},
        {"ID": "Z/SQRT(X^2+Y^2+Z^2)",          "Node": "ShaderNodeMath",        "Location": ( 8,-1), "Operation": "DIVIDE",     "Inputs": []},
        {"ID": "ACOS(X/SQRT(X^2+Y^2))",        "Node": "ShaderNodeMath",        "Location": ( 9,-2), "Operation": "ARCCOSINE",  "Inputs": []},
        {"ID": "ACOS(Z/SQRT(X^2+Y^2+Z^2))",    "Node": "ShaderNodeMath",        "Location": ( 9, 0), "Operation": "ARCCOSINE",  "Inputs": []},
        {"ID": "SGN(Y)",                       "Node": "ShaderNodeMath",        "Location": ( 9,-1), "Operation": "SIGN",       "Inputs": []},
        {"ID": "SGN(Y)*ACOS(X/SQRT(X^2+Y^2))", "Node": "ShaderNodeMath",        "Location": (10,-1), "Operation": "MULTIPLY",   "Inputs": []},
        {"ID": "CombineXYZ",                   "Node": "ShaderNodeCombineXYZ",  "Location": (11, 1)},
        {"ID": "MappingOut",                   "Node": "ShaderNodeMapping",     "Location": (12, 0)},
    ]
    
    # Link list for the Polar Coordinates
    link_list_polar = [
        {"From": ["TexCoord", 3],                     "To": ["MappingIn", 0]},
        {"From": ["MappingIn", 0],                    "To": ["SeparateXYZ", 0]},
        {"From": ["SeparateXYZ", 0],                  "To": ["X^2", 0]},
        {"From": ["SeparateXYZ", 1],                  "To": ["Y^2", 0]},
        {"From": ["SeparateXYZ", 2],                  "To": ["Z^2", 0]},
        {"From": ["X^2", 0],                          "To": ["X^2+Y^2", 0]},
        {"From": ["Y^2", 0],                          "To": ["X^2+Y^2", 1]},
        {"From": ["X^2+Y^2", 0],                      "To": ["X^2+Y^2+Z^2", 0]},
        {"From": ["Z^2", 0],                          "To": ["X^2+Y^2+Z^2", 1]},
        {"From": ["X^2+Y^2", 0],                      "To": ["SQRT(X^2+Y^2)", 0]},
        {"From": ["X^2+Y^2+Z^2", 0],                  "To": ["SQRT(X^2+Y^2+Z^2)", 0]},
        {"From": ["SeparateXYZ", 0],                  "To": ["X/SQRT(X^2+Y^2)", 0]},
        {"From": ["SQRT(X^2+Y^2)", 0],                "To": ["X/SQRT(X^2+Y^2)", 1]},
        {"From": ["SeparateXYZ", 2],                  "To": ["Z/SQRT(X^2+Y^2+Z^2)", 0]},
        {"From": ["SQRT(X^2+Y^2+Z^2)", 0],            "To": ["Z/SQRT(X^2+Y^2+Z^2)", 1]},
        {"From": ["X/SQRT(X^2+Y^2)", 0],              "To": ["ACOS(X/SQRT(X^2+Y^2))", 0]},
        {"From": ["Z/SQRT(X^2+Y^2+Z^2)", 0],          "To": ["ACOS(Z/SQRT(X^2+Y^2+Z^2))", 0]},
        {"From": ["SeparateXYZ", 1],                  "To": ["SGN(Y)", 0]},
        {"From": ["SGN(Y)", 0],                       "To": ["SGN(Y)*ACOS(X/SQRT(X^2+Y^2))", 0]},
        {"From": ["ACOS(X/SQRT(X^2+Y^2))", 0],        "To": ["SGN(Y)*ACOS(X/SQRT(X^2+Y^2))", 1]},
        {"From": ["SGN(Y)*ACOS(X/SQRT(X^2+Y^2))", 0], "To": ["CombineXYZ", 0]},
        {"From": ["ACOS(Z/SQRT(X^2+Y^2+Z^2))", 0],    "To": ["CombineXYZ", 1]},
        {"From": ["SQRT(X^2+Y^2+Z^2)", 0],            "To": ["CombineXYZ", 2]},
        {"From": ["CombineXYZ", 0],                   "To": ["MappingOut", 0]},
    ]

    # Add nodes 
    def add_nodes(self, node_tree, node_list, link_list):
        # Create new nodes
        nodes = {}
        org = (0, 0)
        scale = (200, 200)
        for node_data in node_list:
            new_node = node_tree.nodes.new(node_data["Node"])
            nodes[node_data["ID"]] = new_node
            
            if "Location" in node_data:
                loc = node_data["Location"]
                new_node.location = (loc[0] * scale[0] + org[0], loc[1] * scale[1] + org[1])
 
            # Set data to each node
            node_name = node_data["Node"]                            
            if   node_name == "ShaderNodeTexCoord":
                pass
                        
            elif node_name == "ShaderNodeSeparateXYZ":
                pass
                        
            elif node_name == "ShaderNodeCombineXYZ":
                pass
            
            elif node_name == "ShaderNodeMath":
                new_node.operation = node_data["Operation"]
            
            # Set default values
            if "Inputs" in node_data:
                if len(node_data["Inputs"]) > 0:
                    for idx in list(range(len(node_data["Inputs"]))):
                        inp = node_data["Inputs"][idx]
                        if inp is not None:
                            new_node.inputs[idx].default_value = inp

        # Create new links
        links = node_tree.links
        for linker in link_list:
            from_id = linker["From"][0]
            to_id = linker["To"][0]
            if from_id in nodes and to_id in nodes:
                from_node = nodes[from_id]
                to_node = nodes[to_id]
                links.new(from_node.outputs[linker["From"][1]], to_node.inputs[linker["To"][1]])

    # Execute class function
    def execute(self, context):
        # Get an active material object
        obj = bpy.context.active_object
        if obj and obj.active_material:

            # Get a current node tree of a current material on the current shader editor
            node_tree = obj.active_material.node_tree
            
            # Add nodes to the node tree
            scene = context.scene
            
            # Cylindrical coordinates
            if scene.NodeCoordinates_type_prop_enum == 'CYLINDRICAL':
                self.add_nodes(node_tree, self.node_list_cylindrical, self.link_list_cylindrical)

            # Polar coordinates
            elif scene.NodeCoordinates_type_prop_enum == 'POLAR':
                self.add_nodes(node_tree, self.node_list_polar, self.link_list_polar)

        return {'FINISHED'}

# Addon classes
classes = (
    NodeCoordinatesNoePanel,
    NODE_OT_CoordinatesNodes,
)

# Create properties
def create_props():
    scene = bpy.types.Scene

    # Dropdown list items definition for coordinates type
    scene.NodeCoordinates_type_prop_enum = EnumProperty(
        name =" Types",
        description = "Enum Property",
        items = [
            # 'Get value', 'Show value', 'Description value'
            ('CYLINDRICAL', "Cylindrical", "Cylindrical Coordinates"),
            ('POLAR', "Polar", "Polar Coordinates"),
        ],
        default = 'CYLINDRICAL'
    )

# Delete properties
def delete_props():
    scene = bpy.types.Scene
    del scene.NodeCoordinates_type_prop_enum

# Register the addon classes to Blender
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    create_props()

# Unregister the addon classes from Blender
def unregister():
    delete_props()
    for cls in classes:
        bpy.utils.unregister_class(cls)

#if __name__ == "__main__":
#    register()