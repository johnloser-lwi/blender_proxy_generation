import bpy

class ProxyGenerationPropertyGroup(bpy.types.PropertyGroup):
    falloff : bpy.props.FloatProperty(name="Falloff", default=16, min=0, max=100)
    voxel_size : bpy.props.FloatProperty(name="Voxel Size", default=0.06, min=0, max=1)
    add_subdivision : bpy.props.BoolProperty(name="Add Subdivision", default=True)
    mode : bpy.props.EnumProperty(name="Mode", items=[("MODIFIER", "Modifier", ""), ("QUAD_REMESHER", "Quad Remesher", "")], default="MODIFIER")
    
    state : bpy.props.EnumProperty(name="State", items=[("IDLE", "Idle", ""), ("PROXY", "Proxy", ""), ("PREVIEW", "Preview", "")], default="IDLE")
    
    remove_proxy : bpy.props.BoolProperty(name="Remove Proxy", default=False)
    
    origin_object : bpy.props.PointerProperty(type=bpy.types.Object)
    proxy_object : bpy.props.PointerProperty(type=bpy.types.Object)