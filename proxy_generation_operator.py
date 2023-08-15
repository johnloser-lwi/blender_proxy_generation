import bpy
from bpy.types import Operator, PropertyGroup

class OT_LWI_ProxyGenerationOperator(Operator):
    
    bl_idname = "lwi.generate_proxy"
    bl_label = "Generate Proxy"
    
    def execute(self, context):
        prop_group = context.scene.lwi_proxy_generation
        
        
        # Get selected object
        origin_object = bpy.context.active_object

        # copy object
        bpy.ops.object.duplicate()
        
        dup_object = bpy.context.active_object
        
        bpy.ops.object.select_all(action='DESELECT')
        dup_object.select_set(True)
        
        bpy.ops.object.convert(target='MESH')
        
        # rename object
        dup_object.name = origin_object.name + "_PROXY"
        
        # set active object to origin object
        bpy.context.view_layer.objects.active = origin_object
        bpy.ops.object.select_all(action='DESELECT')
        origin_object.select_set(True)

        
        bpy.ops.object.modifier_add(type='SURFACE_DEFORM')
        bpy.context.object.modifiers["SurfaceDeform"].falloff = prop_group.falloff
        bpy.context.object.modifiers["SurfaceDeform"].target = dup_object
        
        # set active object to dup object
        bpy.context.view_layer.objects.active = dup_object
        bpy.ops.object.select_all(action='DESELECT')
        dup_object.select_set(True)
        
        bpy.ops.object.modifier_add(type='REMESH')
        # set voxel size
        bpy.context.object.modifiers["Remesh"].voxel_size = prop_group.voxel_size
        
        # apply modifiers
        bpy.ops.object.modifier_apply(modifier="Remesh")
        
        bpy.context.view_layer.objects.active = origin_object
        bpy.ops.object.select_all(action='DESELECT')
        origin_object.select_set(True)
        
        # bind surface deform
        bpy.ops.object.surfacedeform_bind(modifier="SurfaceDeform")
        
        # hide origin object
        origin_object.hide_viewport = True
        
        bpy.context.view_layer.objects.active = dup_object
        bpy.ops.object.select_all(action='DESELECT')
        dup_object.select_set(True)

        return {'FINISHED'}