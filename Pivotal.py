bl_info = {
    "name": "Set Pivot Points",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Set the pivot point of an object to predefined locations with an organized interface",
    "author": "Gero Doll",
    "version": (1, 2),
    "location": "View3D > Sidebar > Pivot Set",
}

import bpy
from mathutils import Vector

def set_origin_to_bbox(obj, location='CENTER'):
    """
    Snap the 3D cursor to a specified bounding box location and set the object's origin to the cursor.
    
    Args:
        obj: The target Blender object
        location: The desired pivot point location. Can be one of:
            - Basic: CENTER
            - Axis Extremes: MIN_X, MAX_X, MIN_Y, MAX_Y, MIN_Z, MAX_Z
            - Axis Centers: CENTER_X, CENTER_Y, CENTER_Z (centers along specific axis only)
            - Face Centers: CENTER_XY_BOTTOM, CENTER_XY_TOP, CENTER_XZ_FRONT,
                          CENTER_XZ_BACK, CENTER_YZ_LEFT, CENTER_YZ_RIGHT
    """
    try:
        assert location in ('CENTER', 'MIN_X', 'MAX_X', 'MIN_Y', 'MAX_Y', 'MIN_Z', 'MAX_Z',
                          'CENTER_X', 'CENTER_Y', 'CENTER_Z', 'CENTER_XY_BOTTOM', 'CENTER_XY_TOP',
                          'CENTER_XZ_FRONT', 'CENTER_XZ_BACK', 'CENTER_YZ_LEFT', 'CENTER_YZ_RIGHT'), "Invalid location specified."

        # Calculate the bounding box corners in world space
        bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        center = sum(bbox_corners, Vector()) / 8

        # Get current pivot location (origin)
        current_pivot = obj.matrix_world.translation.copy()

        # Determine pivot point based on the specified location
        if location == 'CENTER':
            pivot_point = center
        elif location == 'CENTER_XY_BOTTOM':
            min_z = min([corner.z for corner in bbox_corners])
            pivot_point = Vector((center.x, center.y, min_z))
        elif location == 'CENTER_XY_TOP':
            max_z = max([corner.z for corner in bbox_corners])
            pivot_point = Vector((center.x, center.y, max_z))
        elif location == 'CENTER_XZ_FRONT':
            max_y = max([corner.y for corner in bbox_corners])
            pivot_point = Vector((center.x, max_y, center.z))
        elif location == 'CENTER_XZ_BACK':
            min_y = min([corner.y for corner in bbox_corners])
            pivot_point = Vector((center.x, min_y, center.z))
        elif location == 'CENTER_YZ_LEFT':
            max_x = max([corner.x for corner in bbox_corners])
            pivot_point = Vector((max_x, center.y, center.z))
        elif location == 'CENTER_YZ_RIGHT':
            min_x = min([corner.x for corner in bbox_corners])
            pivot_point = Vector((min_x, center.y, center.z))
        elif location.startswith('MIN') or location.startswith('MAX'):
            # Get the axis (X, Y, or Z)
            axis = location.split('_')[1]
            axis_index = {'X': 0, 'Y': 1, 'Z': 2}[axis]
            
            # Create a new vector starting from the center
            pivot_point = center.copy()
            
            # Get all values for the specified axis
            axis_values = [corner[axis_index] for corner in bbox_corners]
            
            # Set the extreme value for the specified axis only
            if location.startswith('MIN'):
                pivot_point[axis_index] = min(axis_values)
            else:  # MAX
                pivot_point[axis_index] = max(axis_values)
        else:  # CENTER_X, CENTER_Y, CENTER_Z
            # Get the axis (X, Y, or Z)
            axis = location.split('_')[1]
            axis_index = {'X': 0, 'Y': 1, 'Z': 2}[axis]
            
            # Start with current pivot location
            pivot_point = current_pivot.copy()
            
            # Only center the specified axis
            pivot_point[axis_index] = center[axis_index]

        # Move the 3D cursor to the calculated pivot point
        bpy.context.scene.cursor.location = pivot_point

        # Set the origin of the object to the location of the 3D cursor
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
    except Exception as e:
        self.report({'ERROR'}, f"Error setting pivot point: {str(e)}")
        return {'CANCELLED'}

def update_pivot(self, context):
    obj = context.active_object
    if obj:
        set_origin_to_bbox(obj, self.pivot_type)

class OBJECT_OT_SetPivot(bpy.types.Operator):
    """Set the pivot point of the selected object to a specified location"""
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
            ('CENTER_X', "Center X", "Set origin to the center of the X axis only"),
            ('CENTER_Y', "Center Y", "Set origin to the center of the Y axis only"),
            ('CENTER_Z', "Center Z", "Set origin to the center of the Z axis only"),
            ('CENTER_XY_BOTTOM', "Center XY Bottom", "Set origin to the center of the XY plane at the bottom"),
            ('CENTER_XY_TOP', "Center XY Top", "Set origin to the center of the XY plane at the top"),
            ('CENTER_XZ_FRONT', "Center XZ Front", "Set origin to the center of the XZ plane at the front"),
            ('CENTER_XZ_BACK', "Center XZ Back", "Set origin to the center of the XZ plane at the back"),
            ('CENTER_YZ_LEFT', "Center YZ Left", "Set origin to the center of the YZ plane on the left"),
            ('CENTER_YZ_RIGHT', "Center YZ Right", "Set origin to the center of the YZ plane on the right"),
        ],
        default='CENTER',
        name="Pivot Type"
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        try:
            update_pivot(self, context)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}

class VIEW3D_PT_SetPivotPanel(bpy.types.Panel):
    """Panel for setting object pivot points to various predefined locations"""
    bl_label = "Set Pivot"
    bl_idname = "VIEW3D_PT_set_pivot"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pivot Set'

    def draw(self, context):
        layout = self.layout
        
        # Basic Center Option
        box = layout.box()
        box.label(text="Basic", icon='DOT')
        box.operator("object.set_pivot", text="Center").pivot_type = 'CENTER'
        
        # Axis Extremes
        box = layout.box()
        box.label(text="Axis Extremes", icon='EMPTY_AXIS')
        row = box.row()
        col = row.column()
        col.operator("object.set_pivot", text="Min X").pivot_type = 'MIN_X'
        col.operator("object.set_pivot", text="Min Y").pivot_type = 'MIN_Y'
        col.operator("object.set_pivot", text="Min Z").pivot_type = 'MIN_Z'
        col = row.column()
        col.operator("object.set_pivot", text="Max X").pivot_type = 'MAX_X'
        col.operator("object.set_pivot", text="Max Y").pivot_type = 'MAX_Y'
        col.operator("object.set_pivot", text="Max Z").pivot_type = 'MAX_Z'
        
        # Axis Centers
        box = layout.box()
        box.label(text="Axis Centers", icon='ORIENTATION_GIMBAL')
        row = box.row(align=True)
        row.operator("object.set_pivot", text="X").pivot_type = 'CENTER_X'
        row.operator("object.set_pivot", text="Y").pivot_type = 'CENTER_Y'
        row.operator("object.set_pivot", text="Z").pivot_type = 'CENTER_Z'
        
        # Face Centers
        box = layout.box()
        box.label(text="Face Centers", icon='FACESEL')
        col = box.column(align=True)
        row = col.row(align=True)
        row.operator("object.set_pivot", text="Top").pivot_type = 'CENTER_XY_TOP'
        row.operator("object.set_pivot", text="Bottom").pivot_type = 'CENTER_XY_BOTTOM'
        row = col.row(align=True)
        row.operator("object.set_pivot", text="Front").pivot_type = 'CENTER_XZ_FRONT'
        row.operator("object.set_pivot", text="Back").pivot_type = 'CENTER_XZ_BACK'
        row = col.row(align=True)
        row.operator("object.set_pivot", text="Left").pivot_type = 'CENTER_YZ_LEFT'
        row.operator("object.set_pivot", text="Right").pivot_type = 'CENTER_YZ_RIGHT'

def register():
    bpy.utils.register_class(OBJECT_OT_SetPivot)
    bpy.utils.register_class(VIEW3D_PT_SetPivotPanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_SetPivot)
    bpy.utils.unregister_class(VIEW3D_PT_SetPivotPanel)

if __name__ == "__main__":
    register()
