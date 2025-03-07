##############################################################
# Blender Addon
#   Blender Version: 4.3.2
#   Target: VIEW_3D > Tool
#   Functions:
#     - Scatter selected objects in random distance and rotation.
#   Author: Shunsuke Ohira
#   License: GPLv2
#   Addon Version:
#     0.1.0: 2025/03/07
#          - Scatter with distane of X, Y, Z
#          - Scatter with rotation by X, Y, Z-axis
##############################################################
import bpy
from bpy.props import (
    FloatProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    BoolProperty,
)

from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

import random, math

# Addon information
bl_info = {
    "name": "Objects Scatter",
    "author": "Shunsuke Ohira",
    "version": (0, 1, 0),
    "blender": (4, 3, 2),
    "location": "3Dビューポート > サイドバー > ツール",
    "description": "Objects Random scattering",
    "warning": "",
    "support": "COMMUNITY",
    "doc_utl": "",
    "tracker_url": "",
    "category": "Object",
}

# Addon class
class OBJSCATTER_OT_ObjectsRandomScatter(bpy.types.Operator):
    bl_idname = "objects.random_scattering"
    bl_label = "Scattering"
    bl_description = "Objects Random Scattering"
    bl_options = {"REGISTER", "UNDO"}
    
    # Class properties
    scatter_xm: bpy.props.FloatProperty(
        name = "Scatter -X",
        description = "Maximum scattering to -X",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )
    
    scatter_xp: bpy.props.FloatProperty(
        name = "Scatter +X",
        description = "Maximum scattering to +X",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )
    
    scatter_rxm: bpy.props.FloatProperty(
        name = "Rotation -X",
        description = "Maximum rotation angle -X",
        default = 0.0,
        min = 0.0,
        max = 180.0
    )
    
    scatter_rxp: bpy.props.FloatProperty(
        name = "Rotation +X",
        description = "Maximum rotation angle +X",
        default = 0.0,
        min = 0.0,
        max = 180.0
    )
    
    scatter_ym: bpy.props.FloatProperty(
        name = "Scatter -Y",
        description = "Maximum scattering to -Y",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )
    
    scatter_yp: bpy.props.FloatProperty(
        name = "Scatter +Y",
        description = "Maximum scattering to +Y",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )
    
    scatter_rym: bpy.props.FloatProperty(
        name = "Rotation -Y",
        description = "Maximum rotation angle -Y",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )
    
    scatter_ryp: bpy.props.FloatProperty(
        name = "Rotation +Y",
        description = "Maximum rotation angle +Y",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )
    
    scatter_zm: bpy.props.FloatProperty(
        name = "Scatter -Z",
        description = "Maximum scattering to -Z",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )
    
    scatter_zp: bpy.props.FloatProperty(
        name = "Scatter +Z",
        description = "Maximum scattering to +Z",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )

    scatter_rzm: bpy.props.FloatProperty(
        name = "Rotation -Z",
        description = "Maximum rotation angle -Z",
        default = 0.0,
        min = 0.0,
        max = 180.0
    )
    
    scatter_rzp: bpy.props.FloatProperty(
        name = "Rotation +Z",
        description = "Maximum rotation angle +Z",
        default = 0.0,
        min = 0.0,
        max = 180.0
    )

    def replace_all_objects_random(self, obj_types):
        to_radian = math.pi / 180
        for obj in bpy.context.selected_objects:
            if obj.type in obj_types:
                # Move X, Y, Z
                scatter_m = -self.scatter_xm
                scatter_p = self.scatter_xp
                if scatter_m < scatter_p:
                    mov = random.random() * (scatter_p - scatter_m) + scatter_m
                    obj.location.x += mov

                scatter_m = -self.scatter_ym
                scatter_p = self.scatter_yp
                if scatter_m < scatter_p:
                    mov = random.random() * (scatter_p - scatter_m) + scatter_m
                    obj.location.y += mov
                    
                scatter_m = -self.scatter_zm
                scatter_p = self.scatter_zp
                if scatter_m < scatter_p:
                    mov = random.random() * (scatter_p - scatter_m) + scatter_m
                    obj.location.z += mov

                # Rotate X, Y, Z axis
                scatter_m = -self.scatter_rxm
                scatter_p = self.scatter_rxp
                if scatter_m < scatter_p:
                    rot = random.random() * (scatter_p - scatter_m) + scatter_m
                    obj.rotation_euler.x += (rot * to_radian)

                scatter_m = -self.scatter_rym
                scatter_p = self.scatter_ryp
                if scatter_m < scatter_p:
                    rot = random.random() * (scatter_p - scatter_m) + scatter_m
                    obj.rotation_euler.y += (rot * to_radian)

                scatter_m = -self.scatter_rzm
                scatter_p = self.scatter_rzp
                if scatter_m < scatter_p:
                    rot = random.random() * (scatter_p - scatter_m) + scatter_m
                    obj.rotation_euler.z += (rot * to_radian)
    
    # Run this addon
    def execute(self, context):
        self.replace_all_objects_random(['MESH', 'CURVE'])
        return {'FINISHED'}

# Addon panel class
class OBJSCATTER_PT_ObjectsRandomScatter(bpy.types.Panel):
    bl_idname = "OBJSCATTER_PT_Tool"
    bl_label = "Scattering"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    
    # Draw addon panel header
    def draw_header(self, context):
        layout = self.layout
        layout.label(text = "", icon="PLUGIN")
    
    # Draw addon panel contents
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        op = row.operator(OBJSCATTER_OT_ObjectsRandomScatter.bl_idname, text = "SCATTER")

        op.scatter_xm = scene.scatter_xm
        op.scatter_xp = scene.scatter_xp
        op.scatter_rxm = scene.scatter_rxm
        op.scatter_rxp = scene.scatter_rxp
        
        op.scatter_ym = scene.scatter_ym
        op.scatter_xp = scene.scatter_yp
        op.scatter_rym = scene.scatter_rym
        op.scatter_ryp = scene.scatter_ryp
        
        op.scatter_zm = scene.scatter_zm
        op.scatter_xp = scene.scatter_zp
        op.scatter_rzm = scene.scatter_rzm
        op.scatter_rzp = scene.scatter_rzp

        row = layout.row()
        row.prop(scene, "scatter_xm", text = "-X")
        row.prop(scene, "scatter_xp", text = "+X")

        row = layout.row()
        row.prop(scene, "scatter_ym", text = "-Y")
        row.prop(scene, "scatter_yp", text = "+Y")

        row = layout.row()
        row.prop(scene, "scatter_zm", text = "-Z")
        row.prop(scene, "scatter_zp", text = "+Z")

        row = layout.row()
        row.prop(scene, "scatter_rxm", text = "-Xdeg")
        row.prop(scene, "scatter_rxp", text = "+Xdeg")
        
        row = layout.row()
        row.prop(scene, "scatter_rym", text = "-Ydeg")
        row.prop(scene, "scatter_ryp", text = "+Ydeg")
        
        row = layout.row()
        row.prop(scene, "scatter_rzm", text = "-Zdeg")
        row.prop(scene, "scatter_rzp", text = "+Zdeg")

        # Set initial value to the operator
        op.scatter_xm  = scene.scatter_xm
        op.scatter_xp  = scene.scatter_xp
        op.scatter_rxm = scene.scatter_rxm
        op.scatter_rxp = scene.scatter_rxp
        
        op.scatter_ym  = scene.scatter_ym
        op.scatter_yp  = scene.scatter_yp
        op.scatter_rym = scene.scatter_rym
        op.scatter_ryp = scene.scatter_ryp
        
        op.scatter_zm  = scene.scatter_zm
        op.scatter_zp  = scene.scatter_zp
        op.scatter_rzm = scene.scatter_rzm
        op.scatter_rzp = scene.scatter_rzp

def register_properties():
    scene = bpy.types.Scene

    scene.scatter_xm = bpy.props.FloatProperty(
        name = "Scatter -X",
        description = "Maximum scattering to -X",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )

    scene.scatter_xp = bpy.props.FloatProperty(
        name = "Scatter +X",
        description = "Maximum scattering to +X",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )

    scene.scatter_rxm = bpy.props.FloatProperty(
        name = "Rotation -X",
        description = "Maximum rotation angle -X",
        default = 0.0,
        min = 0.0,
        max = 180.0
    )

    scene.scatter_rxp = bpy.props.FloatProperty(
        name = "Rotation +X",
        description = "Maximum rotation angle +X",
        default = 0.0,
        min = 0.0,
        max = 180.0
    )

    scene.scatter_ym = bpy.props.FloatProperty(
        name = "Scatter -Y",
        description = "Maximum scattering to -Y",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )

    scene.scatter_yp = bpy.props.FloatProperty(
        name = "Scatter +Y",
        description = "Maximum scattering to +Y",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )

    scene.scatter_rym = bpy.props.FloatProperty(
        name = "Rotation -Y",
        description = "Maximum rotation angle -Y",
        default = 0.0,
        min = 0.0,
        max = 180.0
    )

    scene.scatter_ryp = bpy.props.FloatProperty(
        name = "Rotation +Y",
        description = "Maximum rotation angle +Y",
        default = 0.0,
        min = 0.0,
        max = 180.0
    )

    scene.scatter_zm = bpy.props.FloatProperty(
        name = "Scatter -Z",
        description = "Maximum scattering to -Z",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )

    scene.scatter_zp = bpy.props.FloatProperty(
        name = "Scatter +Z",
        description = "Maximum scattering to +Z",
        default = 0.0,
        min = 0.0,
        max = 10000.0
    )

    scene.scatter_rzm = bpy.props.FloatProperty(
        name = "Rotation -Z",
        description = "Maximum rotation angle -Z",
        default = 0.0,
        min = 0.0,
        max = 180.0
    )

    scene.scatter_rzp = bpy.props.FloatProperty(
        name = "Rotation +Z",
        description = "Maximum rotation angle +Z",
        default = 0.0,
        min = 0.0,
        max = 180.0
    )

def unregister_properties():
    scene = bpy.types.Scene
    del scene.scatter_xm
    del scene.scatter_xp
    del scene.scatter_rxm
    del scene.scatter_rxp
    del scene.scatter_ym
    del scene.scatter_yp
    del scene.scatter_rym
    del scene.scatter_ryp
    del scene.scatter_zm
    del scene.scatter_zp
    del scene.scatter_rzm
    del scene.scatter_rzp

def menu_register_func(cls, context):
    cls.layout.separator()
    cls.layout.operator(OBJSCATTER_OT_ObjectsRandomScatter.bl_idname, icon = "PLUGIN")

classes = [
    OBJSCATTER_OT_ObjectsRandomScatter,
    OBJSCATTER_PT_ObjectsRandomScatter,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.VIEW3D_MT_transform_object.append(menu_register_func)
    register_properties()
    print(f"Addon {bl_info['name']} is available.")

def unregister():
    unregister_properties()
    bpy.types.VIEW3D_MT_transform_object.remove(menu_register_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    print(f"Addon {bl_info['name']} is disabled.")
