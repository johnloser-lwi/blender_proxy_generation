import bpy
from bpy.types import Operator

class OT_LWI_ApplyDeformOperator(Operator):
    
    bl_idname = "lwi.apply_deform"
    bl_label = "Apply Deform"
    
    def execute(self, context):

        # Get selected object
        proxy_object = bpy.context.active_object
        
        # convert mesh
        bpy.ops.object.convert(target='MESH')
        
        # original name of the object
        original_name = proxy_object.name.replace("_PROXY", "")
        
        # get original object
        original_object = bpy.data.objects[original_name]
        
        # unhide original object
        original_object.hide_viewport = False
        
        # set original object as active object
        bpy.context.view_layer.objects.active = original_object
        
        # apply surface defrom
        bpy.ops.object.modifier_apply(modifier="SurfaceDeform")
        
        # delete proxy object
        bpy.ops.object.delete()
        

        return {'FINISHED'}