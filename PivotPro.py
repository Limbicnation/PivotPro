bl_info = {
    "name": "Set Pivot Points",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Set the pivot of an object to predefined locations",
    "author": "Your Name",
    "version": (1, 0),
    "location": "View3D > Sidebar > Pivot Set",
}

import bpy
from mathutils import Vector

# Create Functions to Set Pivot Points
def set_origin_to_bbox(obj, location='CENTER'):
    """
    Snap the 3D cursor to a specified bounding box location and set the object's origin to the cursor.
    Location can be 'CENTER', 'MIN_X', 'MAX_X', 'MIN_Y', 'MAX_Y', 'MIN_Z', 'MAX_Z'.
    """
    assert location in ('CENTER', 'MIN_X', 'MAX_X', 'MIN_Y', 'MAX_Y', 'MIN_Z', 'MAX_Z'), "Invalid location specified."

    # Calculate the bounding box corners in world space
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    # Determine pivot point based on the specified location
    if location == 'CENTER':
        pivot_point = sum(bbox_corners, Vector()) / 8
    else:
        axis_index = {'X': 0, 'Y': 1, 'Z': 2}[location.split('_')[1]]
        pivot_points = [corner[axis_index] for corner in bbox_corners]
        if 'MIN' in location:
            pivot_value = min(pivot_points)
        else:  # 'MAX' in location
            pivot_value = max(pivot_points)
        pivot_point = bbox_corners[pivot_points.index(pivot_value)]

    # Move the 3D cursor to the calculated pivot point
    bpy.context.scene.cursor.location = pivot_point

    # Set the origin of the object to the location of the 3D cursor
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

def update_pivot(self, context):
    obj = context.active_object
    if obj:
        set_origin_to_bbox(obj, self.pivot_type)

# Define the Operator Classes
class OBJECT_OT_SetPivot(bpy.types.Operator):
    """Set Pivot Point"""
    bl_idname = "object.set_pivot"
    bl_label = "Set Pivot"
    bl_options = {'REGISTER', 'UNDO'}

    pivot_type: bpy.props.EnumProperty(
        items=[
            ('CENTER', "Center", "Set origin to the center of the bounding box"),
            ('MIN_X', "Min X", "Set origin to the minimum X of the bounding box"),
            ('MAX_X', "Max X", "Set origin to the maximum X of the bounding box"),
            ('MIN_Y', "Min Y", "Set origin to the minimum Y of the bounding box"),
            ('MAX_Y', "Max Y", "Set origin to the maximum Y of the bounding box"),
            ('MIN_Z', "Min Z", "Set origin to the minimum Z of the bounding box"),
            ('MAX_Z', "Max Z", "Set origin to the maximum Z of the bounding box"),
        ],
        default='CENTER',
        name="Pivot Type"
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        update_pivot(self, context)
        return {'FINISHED'}

# Create the UI Panel
class VIEW3D_PT_SetPivotPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Set Pivot"
    bl_idname = "VIEW3D_PT_set_pivot"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pivot Set'

    def draw(self, context):
        layout = self.layout

        layout.operator("object.set_pivot", text="Center").pivot_type = 'CENTER'
        layout.operator("object.set_pivot", text="Min X").pivot_type = 'MIN_X'
        layout.operator("object.set_pivot", text="Max X").pivot_type = 'MAX_X'
        layout.operator("object.set_pivot", text="Min Y").pivot_type = 'MIN_Y'
        layout.operator("object.set_pivot", text="Max Y").pivot_type = 'MAX_Y'
        layout.operator("object.set_pivot", text="Min Z").pivot_type = 'MIN_Z'
        layout.operator("object.set_pivot", text="Max Z").pivot_type = 'MAX_Z'

# Register Classes and Addon Functionality
def register():
    bpy.utils.register_class(OBJECT_OT_SetPivot)
    bpy.utils.register_class(VIEW3D_PT_SetPivotPanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_SetPivot)
    bpy.utils.unregister_class(VIEW3D_PT_SetPivotPanel)

if __name__ == "__main__":
    register()
