import bpy
bl_info = {
    "name": " Delete/Select by Name",
    "author": "1C0D",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),
    "location": "View3D>ObjectMenu",
    "description": "Delete objects by name",
    "category": "Menu"
}


class DELETE_OT_obj_by_name (bpy.types.Operator):
    bl_idname = "delete.obj_by_name"
    bl_label = "Delete/Select object by name"
    bl_options = {'UNDO'}

    name: bpy.props.StringProperty(default="", maxlen=100)
    sel: bpy.props.EnumProperty(
        items=[("0", "Scene", ""), ("1", "Selected", "")])
    mode: bpy.props.EnumProperty(
        items=[("0", "Delete", ""), ("1", "Select", "")])
    respect_case: bpy.props.BoolProperty(name='case sensitive')

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

            if name in target:
                if self.mode == "0":
                    removed.append(obj.name)
                    objects = bpy.data.objects
                    objects.remove(obj, do_unlink=True)
                else:
                    obj.select_set(True)

        if removed:
            bpy.ops.outliner.orphans_purge()
        self.report({'INFO'}, f'{len(removed)} removed, details in Console')
        print(f'===> removed: {removed}')

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, 'sel', expand=True)
        layout.prop(self, "name", text='pattern')
        row = layout.row()
        row.prop(self, "respect_case")
        if self.mode == '1':
            row.operator("object.select_all",
                         text="deselect all", icon='SELECT_SET').action = 'DESELECT'

        layout.prop(self, 'mode', expand=True)


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
