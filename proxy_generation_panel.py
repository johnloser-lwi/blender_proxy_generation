import bpy

from bpy.types import Panel

class OBJECT_PT_LWI_ProxyGenerationPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Generate Proxy"
    bl_category = "LWI Util"
    
    falloff : bpy.props.FloatProperty(name="Falloff", default=16, min=0, max=100)
    voxel_size : bpy.props.FloatProperty(name="Voxel Size", default=0.06, min=0, max=1)

    def draw(self, context):
        prop_group = context.scene.lwi_proxy_generation
        
        layout = self.layout    
        
        creation = layout.row()
        title = layout.label(text="Generate Proxy")
        
        if prop_group.origin_object != None:
            og = layout.row()
            og.label(text="Origin Object : " + prop_group.origin_object.name)
        
        px = layout.row()
        if prop_group.state == "IDLE":
            px.prop(prop_group, "proxy_object")
        elif prop_group.proxy_object != None:
            px.label(text="Proxy Object : " + prop_group.proxy_object.name)
        
        
        if prop_group.state == "IDLE":
            md = layout.row()
            md.prop(prop_group, "mode", expand=True)
            
            sub = layout.row()
            sub.prop(prop_group, "add_subdivision")
            
            row0 = layout.row()
            fo = row0.column()
            fo.prop(prop_group, "falloff", slider=True)
            
            if prop_group.mode == "MODIFIER":
                row1 = layout.row()
                vs = row1.column()
                vs.prop(prop_group, "voxel_size", slider=True)
            
            gp = layout.row()
            gp.operator("lwi.generate_proxy", text="Generate Proxy")
        
        if prop_group.state != "IDLE":
            toggle_text = "Disable Preview" if prop_group.state == "PREVIEW" else "Enable Preview"
            pv = layout.row()
            pv.operator("lwi.toggle_proxy", text=toggle_text)
            
            ad = layout.row()
            rm = ad.column()
            rm.prop(prop_group, "remove_proxy")
            bt = ad.column()
            bt.operator("lwi.apply_deform", text="Apply Deform")
        

        
        