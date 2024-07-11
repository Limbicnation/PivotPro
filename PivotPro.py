bl_info = {
    "name": "Set Pivot Points",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Set the pivot of an object to predefined locations",
    "author": "Gero Doll",
    "version": (1, 0),
    "location": "View3D > Sidebar > Pivot Set",
}

import bpy
from mathutils import Vector

def set_origin_to_bbox(obj, location='CENTER'):
    """
    Snap the 3D cursor to a specified bounding box location and set the object's origin to the cursor.
    Location can be 'CENTER', 'MIN_X', 'MAX_X', 'MIN_Y', 'MAX_Y', 'MIN_Z', 'MAX_Z',
    'CENTER_X', 'CENTER_Y', 'CENTER_Z', 'CENTER_XY_BOTTOM', 'CENTER_XY_TOP', 'CENTER_XZ_FRONT', 'CENTER_XZ_BACK', 'CENTER_YZ_LEFT', 'CENTER_YZ_RIGHT'.
    """
    assert location in ('CENTER', 'MIN_X', 'MAX_X', 'MIN_Y', 'MAX_Y', 'MIN_Z', 'MAX_Z',
                        'CENTER_X', 'CENTER_Y', 'CENTER_Z', 'CENTER_XY_BOTTOM', 'CENTER_XY_TOP', 'CENTER_XZ_FRONT', 'CENTER_XZ_BACK', 'CENTER_YZ_LEFT', 'CENTER_YZ_RIGHT'), "Invalid location specified."

    # Calculate the bounding box corners in world space
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    # Determine pivot point based on the specified location
    if location == 'CENTER':
        pivot_point = sum(bbox_corners, Vector()) / 8
    elif location == 'CENTER_XY_BOTTOM':
        center_xy = sum(bbox_corners, Vector()) / 8
        min_z = min([corner.z for corner in bbox_corners])
        pivot_point = Vector((center_xy.x, center_xy.y, min_z))
    elif location == 'CENTER_XY_TOP':
        center_xy = sum(bbox_corners, Vector()) / 8
        max_z = max([corner.z for corner in bbox_corners])
        pivot_point = Vector((center_xy.x, center_xy.y, max_z))
    elif location == 'CENTER_XZ_FRONT':
        center_xz = sum(bbox_corners, Vector()) / 8
        max_y = max([corner.y for corner in bbox_corners])
        pivot_point = Vector((center_xz.x, max_y, center_xz.z))
    elif location == 'CENTER_XZ_BACK':
        center_xz = sum(bbox_corners, Vector()) / 8
        min_y = min([corner.y for corner in bbox_corners])
        pivot_point = Vector((center_xz.x, min_y, center_xz.z))
    elif location == 'CENTER_YZ_LEFT':
        center_yz = sum(bbox_corners, Vector()) / 8
        max_x = max([corner.x for corner in bbox_corners])
        pivot_point = Vector((max_x, center_yz.y, center_yz.z))
    elif location == 'CENTER_YZ_RIGHT':
        center_yz = sum(bbox_corners, Vector()) / 8
        min_x = min([corner.x for corner in bbox_corners])
        pivot_point = Vector((min_x, center_yz.y, center_yz.z))
    else:
        axis_index = {'X': 0, 'Y': 1, 'Z': 2}[location.split('_')[-1]]
        if location.startswith('CENTER'):
            pivot_point = Vector((0, 0, 0))
            count = 0
            for i in range(8):
                if i & (1 << axis_index):
                    pivot_point += bbox_corners[i]
                    count += 1
            pivot_point /= count
        else:
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
            ('CENTER_X', "Center X", "Set origin to the center of the bounding box on the X axis"),
            ('CENTER_Y', "Center Y", "Set origin to the center of the bounding box on the Y axis"),
            ('CENTER_Z', "Center Z", "Set origin to the center of the bounding box on the Z axis"),
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
        update_pivot(self, context)
        return {'FINISHED'}

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
        layout.operator("object.set_pivot", text="Center X").pivot_type = 'CENTER_X'
        layout.operator("object.set_pivot", text="Center Y").pivot_type = 'CENTER_Y'
        layout.operator("object.set_pivot", text="Center Z").pivot_type = 'CENTER_Z'
        layout.operator("object.set_pivot", text="Center XY Bottom").pivot_type = 'CENTER_XY_BOTTOM'
        layout.operator("object.set_pivot", text="Center XY Top").pivot_type = 'CENTER_XY_TOP'
        layout.operator("object.set_pivot", text="Center XZ Front").pivot_type = 'CENTER_XZ_FRONT'
        layout.operator("object.set_pivot", text="Center XZ Back").pivot_type = 'CENTER_XZ_BACK'
        layout.operator("object.set_pivot", text="Center YZ Left").pivot_type = 'CENTER_YZ_LEFT'
        layout.operator("object.set_pivot", text="Center YZ Right").pivot_type = 'CENTER_YZ_RIGHT'

def register():
    bpy.utils.register_class(OBJECT_OT_SetPivot)
    bpy.utils.register_class(VIEW3D_PT_SetPivotPanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_SetPivot)
    bpy.utils.unregister_class(VIEW3D_PT_SetPivotPanel)

if __name__ == "__main__":
    register()
