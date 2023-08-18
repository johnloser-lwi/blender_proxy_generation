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
        
        row2 = layout.row()
        gp = row2.column()
        operator_props = gp.operator("lwi.generate_proxy", text="Generate Proxy")
        
        row3 = layout.row()
        ad = row3.column()
        ad.operator("lwi.apply_deform", text="Apply Deform")
        

        
        