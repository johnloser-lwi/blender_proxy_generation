import bpy

class ProxyGenerationPropertyGroup(bpy.types.PropertyGroup):
    falloff : bpy.props.FloatProperty(name="Falloff", default=16, min=0, max=100)
    voxel_size : bpy.props.FloatProperty(name="Voxel Size", default=0.06, min=0, max=1)
    mode : bpy.props.EnumProperty(name="Mode", items=[("MODIFIER", "Modifier", ""), ("QUAD_REMESHER", "Quad Remesher", "")], default="MODIFIER")