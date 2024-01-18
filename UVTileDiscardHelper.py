import bpy

# 頂点を選択するオペレーター
class SelectMovedVertsOperator(bpy.types.Operator):
    bl_idname = "mesh.select_moved_verts"
    bl_label = "Select Moved Vertices"
    bl_description = "Select vertices moved by the active shape key"

    def execute(self, context):
        obj = context.object
        if obj.data.shape_keys:
            key_blocks = obj.data.shape_keys.key_blocks
            base_key = key_blocks[0]
            active_key = obj.active_shape_key

            if active_key:
                bpy.ops.object.mode_set(mode='OBJECT')
                for i, vert in enumerate(obj.data.vertices):
                    if (base_key.data[i].co - active_key.data[i].co).length > 0.0001:
                        vert.select = True
                bpy.ops.object.mode_set(mode='EDIT')
            else:
                self.report({'WARNING'}, "No active shape key found")
        else:
            self.report({'WARNING'}, "No shape keys on the object")
        return {'FINISHED'}

# 選択した頂点のUVを移動するオペレーター
class MoveSelectedVertsUVOperator(bpy.types.Operator):
    bl_idname = "mesh.move_selected_verts_uv"
    bl_label = "Move Selected Vertices UV"
    
    x_offset: bpy.props.IntProperty()
    y_offset: bpy.props.IntProperty()

    def execute(self, context):
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        
        # 元のエリアタイプを保持
        original_area = context.area.type

        # UVエディターに切り替え
        context.area.ui_type = 'UV'

        # UVの同期選択を有効にする
        context.scene.tool_settings.use_uv_select_sync = True

        # 選択されたUVを指定されたオフセットで移動
        bpy.ops.transform.translate(value=(self.x_offset, self.y_offset, 0), constraint_axis=(True, True, False))
        print(self.x_offset)
        print(self.y_offset)

        # 元のエリアタイプに戻す
        context.area.type = original_area

        return {'FINISHED'}

# カスタムパネルを定義
class CustomPanel(bpy.types.Panel):
    bl_label = "UVTileDiscardHelper"
    bl_idname = "OBJECT_PT_custom_vertex_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Edit'

    def draw(self, context):
        layout = self.layout
        layout.operator(SelectMovedVertsOperator.bl_idname)
        # 4x4 マトリクスのボタンを生成
        for y in range(3, -1, -1):
            row = layout.row()
            for x in range(0, 4):
                op = row.operator(MoveSelectedVertsUVOperator.bl_idname, text=f"X+{x},Y+{y}")
                op.x_offset, op.y_offset = x, y
                
        # 追加の2x1マトリクスボタン
        row = layout.row()
        op = row.operator(MoveSelectedVertsUVOperator.bl_idname, text="X-1")
        op.x_offset, op.y_offset = -1, 0
        op = row.operator(MoveSelectedVertsUVOperator.bl_idname, text="Y-1")
        op.x_offset, op.y_offset = 0, -1

# オペレーターとパネルを登録
def register():
    bpy.utils.register_class(SelectMovedVertsOperator)
    bpy.utils.register_class(MoveSelectedVertsUVOperator)
    bpy.utils.register_class(CustomPanel)

# オペレーターとパネルを登録解除
def unregister():
    bpy.utils.unregister_class(SelectMovedVertsOperator)
    bpy.utils.unregister_class(MoveSelectedVertsUVOperator)
    bpy.utils.unregister_class(CustomPanel)

# スクリプトが直接実行された場合に登録する
if __name__ == "__main__":
    register()