import bpy
bl_info = {
    "name": "Delete Select Pattern",
    "author": "1C0D",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),
    "location": "View3D>ObjectMenu",
    "description": "Delete/Select objects by pattern",
    "category": "Menu"
}


class DELETE_OT_obj_by_name (bpy.types.Operator):
    bl_idname = "delete.obj_by_name"
    bl_label = "Delete/Select pattern"
    bl_options = {'UNDO'}

    sel: bpy.props.EnumProperty(
        items=[("0", "Scene", "in Scene Objects"), ("1", "Selected", "in Selected Objects")])
    name: bpy.props.StringProperty(
        default="", maxlen=100, description='enter part or whole name')
    mode: bpy.props.EnumProperty(
        items=[("0", "Delete", ""), ("1", "Select", "")], description='Delete or Select pattern')
    respect_case: bpy.props.BoolProperty(
        name='case sensitive', description='Sensitive to case')
    extend: bpy.props.BoolProperty(
        name='extend', description='Extend the existing selection')

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)

    def execute(self, context):
        sel = []

        sel = context.scene.objects if self.sel == "0" else context.selected_objects
        removed = []
        for obj in sel:
            if not self.respect_case:
                name = self.name if self.respect_case else self.name.lower()
                target = obj.name if self.respect_case else obj.name.lower()

            if self.mode == "0":
                if name in target:
                    removed.append(obj.name)
                    objects = bpy.data.objects
                    objects.remove(obj, do_unlink=True)
            else:
                if self.extend:
                    if name in target:
                        obj.select_set(True)
                else:
                    if name in target:
                        obj.select_set(True)
                    else:
                        obj.select_set(False)

        if removed:
            bpy.ops.outliner.orphans_purge()

        self.report({'INFO'}, f'{len(removed)} removed, details in Console')
        print(f'===> removed: {removed}')

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'mode')
        row = layout.row()
        if self.mode == '0':
            row.prop(self, 'sel', expand=True)
        layout.prop(self, "name", text='pattern')
        row = layout.row()
        row.prop(self, "respect_case")
        if self.mode == '1':
            row.prop(self, "extend")


def draw(self, context):
    layout = self.layout
    layout.operator("delete.obj_by_name", text='Delete/Select pattern')


def register():
    bpy.utils.register_class(DELETE_OT_obj_by_name)
    bpy.types.VIEW3D_MT_object.append(draw)


def unregister():
    bpy.utils.unregister_class(DELETE_OT_obj_by_name)
    bpy.types.VIEW3D_MT_object.remove(draw)


if __name__ == "__main__":
    register()
