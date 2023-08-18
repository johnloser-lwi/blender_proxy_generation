import bpy
from bpy.types import Operator

class OT_LWI_ApplyDeformOperator(Operator):
    
    bl_idname = "lwi.apply_deform"
    bl_label = "Apply Deform"
    
    def execute(self, context):

        # Get selected object
        proxy_object = bpy.context.active_object
        bpy.ops.object.select_all(action='DESELECT')
        proxy_object.select_set(True)
        
        # if object is in edit mode, switch to object mode
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        # find all modifier and apply them
        for modifier in proxy_object.modifiers:
            bpy.ops.object.modifier_apply(modifier=modifier.name)
        
        # original name of the object
        original_name = proxy_object.name.replace("_PROXY", "")
        
        # get original object
        original_object = bpy.data.objects[original_name]
        
        # unhide original object
        original_object.hide_set(False)
        
        # set original object as active object
        bpy.context.view_layer.objects.active = original_object
        bpy.ops.object.select_all(action='DESELECT')
        original_object.select_set(True)
        
        # apply surface defrom
        bpy.ops.object.modifier_apply(modifier="SurfaceDeform")
        
        
        bpy.ops.object.select_all(action='DESELECT')
        proxy_object.select_set(True)
        
        # delete proxy object
        bpy.ops.object.delete()
        
        bpy.context.view_layer.objects.active = original_object
        bpy.ops.object.select_all(action='DESELECT')
        original_object.select_set(True)
        

        return {'FINISHED'}