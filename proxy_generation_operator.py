import typing
import bpy
from bpy.types import Context, Event, Operator, PropertyGroup

class OT_LWI_ProxyGenerationOperator(Operator):
    
    bl_idname = "lwi.generate_proxy"
    bl_label = "Generate Proxy"
    
    def execute(self, context):
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        prop_group = context.scene.lwi_proxy_generation
        
        if prop_group.state != "IDLE":
            return {'FINISHED'}
        
        # Get selected object
        self.origin_object = bpy.context.active_object

        # copy object
        bpy.ops.object.duplicate()
        
        self.dup_object = bpy.context.active_object
        
        bpy.ops.object.select_all(action='DESELECT')
        self.dup_object.select_set(True)
        
        bpy.ops.object.convert(target='MESH')
        
        # rename object
        self.dup_object.name = self.origin_object.name + "_PROXY"
        
        # set active object to origin object
        bpy.context.view_layer.objects.active = self.origin_object
        bpy.ops.object.select_all(action='DESELECT')
        self.origin_object.select_set(True)
        
        # set active object to dup object
        bpy.context.view_layer.objects.active = self.dup_object
        bpy.ops.object.select_all(action='DESELECT')
        self.dup_object.select_set(True)
        
        ###### START REMESH ######
        
        if prop_group.mode == "QUAD_REMESHER":
            self.proxy_name = self.dup_object.name
            self.dup_object = self.dup_object
            bpy.ops.qremesher.remesh()  
            wm = context.window_manager  
            # add timer
            self.timer = wm.event_timer_add(0.3, window=context.window)  
            wm.modal_handler_add(self)  
            
            return {'RUNNING_MODAL'}
            
            
        elif prop_group.mode == "MODIFIER":
            
            bpy.ops.object.modifier_add(type='REMESH')
            # set voxel size
            bpy.context.object.modifiers["Remesh"].voxel_size = prop_group.voxel_size
            
            # apply modifiers
            bpy.ops.object.modifier_apply(modifier="Remesh")
        
        
        ##### END MODIFIER #####
        
        self.apply_deform(context)

        return {'FINISHED'}
    

    def modal(self, context, event):
        if event.type == 'TIMER':
            retopo_name = "Retopo_" + self.proxy_name
            if retopo_name in bpy.data.objects:
                return self.on_qremesh_finished(context)
            
        return {'RUNNING_MODAL'}
        #return {'PASS_THROUGH'}
        
    
    def apply_deform(self, context):
        prop_group = context.scene.lwi_proxy_generation
        
        if prop_group.add_subdivision:
            bpy.context.view_layer.objects.active = self.dup_object
            bpy.ops.object.select_all(action='DESELECT')
            self.dup_object.select_set(True)
            # add subdivision modifier
            bpy.ops.object.modifier_add(type='SUBSURF')
        
        bpy.context.view_layer.objects.active = self.origin_object
        bpy.ops.object.select_all(action='DESELECT')
        self.origin_object.select_set(True)
        
        bpy.ops.object.modifier_add(type='SURFACE_DEFORM')
        bpy.context.object.modifiers["SurfaceDeform"].falloff = prop_group.falloff
        bpy.context.object.modifiers["SurfaceDeform"].target = self.dup_object
        
        # bind surface deform
        result = bpy.ops.object.surfacedeform_bind(modifier="SurfaceDeform")
        
        # if binding failed, delete proxy object and cancel
        if result != {'FINISHED'}:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.context.objects.remove(self.dup_object, do_unlink=True)
            # remove surface deform modifier
            bpy.ops.object.modifier_remove(modifier="SurfaceDeform")
            return {'CANCELLED'}
        
        # hide origin object
        self.origin_object.hide_set(True)
        
        bpy.context.view_layer.objects.active = self.dup_object
        bpy.ops.object.select_all(action='DESELECT')
        self.dup_object.select_set(True)
        
        # disable subdivision modifier
        if prop_group.add_subdivision:
            bpy.context.object.modifiers["Subdivision"].show_viewport = False
            
        prop_group.proxy_object = self.dup_object
        prop_group.origin_object = self.origin_object
            
        prop_group.state = "PROXY";
    
    def on_qremesh_finished(self, context):
        wm = context.window_manager  
        if self.timer != None:
            wm.event_timer_remove(self.timer)  
            self.timer = None
        
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        new_proxy = bpy.data.objects["Retopo_" + self.proxy_name]
        
        self.dup_object.hide_viewport = False
        bpy.context.view_layer.objects.active = self.dup_object
        bpy.ops.object.select_all(action='DESELECT')
        self.dup_object.select_set(True)
        # delete old proxy
        bpy.data.objects.remove(self.dup_object, do_unlink=True)
        
        self.dup_object = new_proxy
        
        bpy.context.view_layer.objects.active = self.dup_object
        bpy.ops.object.select_all(action='DESELECT')
        self.dup_object.select_set(True)
        
        self.dup_object.name = self.proxy_name

        return self.apply_deform(context)
    
class OT_LWI_ApplyDeformOperator(Operator):
    
    bl_idname = "lwi.apply_deform"
    bl_label = "Apply Deform"
    
    def execute(self, context):
        prop_group = context.scene.lwi_proxy_generation
        
        # Get selected object
        proxy_object = prop_group.proxy_object
        
        proxy_object.hide_set(False)
        
        bpy.context.view_layer.objects.active = proxy_object
        bpy.ops.object.select_all(action='DESELECT')
        proxy_object.select_set(True)
        
        # if object is in edit mode, switch to object mode
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        # if object has subdivision modifier, enable it
        if "Subdivision" in bpy.context.object.modifiers:
            bpy.context.object.modifiers["Subdivision"].show_viewport = True
        
        # convert mesh
        bpy.ops.object.convert(target='MESH')
        
        # get original object
        original_object = prop_group.origin_object
        
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
        
        prop_group.state = "IDLE";
        
        return {'FINISHED'}
    
class OT_LWI_TogglePreviewOperator(Operator):
    bl_idname = "lwi.toggle_proxy"
    bl_label = "Toggle Preview"
    
    def execute(self, context):
        prop_group = context.scene.lwi_proxy_generation
        
        if prop_group.state == "IDLE":
            return {'FINISHED'}
        
        is_in_preview = prop_group.state == "PREVIEW"
        
        prop_group.origin_object.hide_set(is_in_preview)
        prop_group.proxy_object.hide_set(not is_in_preview)
        
        current_target = prop_group.proxy_object if is_in_preview else prop_group.origin_object
        
        if "Subdivision" in prop_group.proxy_object.modifiers:
            prop_group.proxy_object.modifiers["Subdivision"].show_viewport = not is_in_preview
        
        # select current target
        bpy.context.view_layer.objects.active = current_target
        bpy.ops.object.select_all(action='DESELECT')
        current_target.select_set(True)
        
        if is_in_preview:
            prop_group.state = "PROXY"
        else:
            prop_group.state = "PREVIEW"
            
        return {'FINISHED'}