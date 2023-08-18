# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "ProxyGeneration",
    "author" : "John Yang",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from . proxy_generation_operator import *
from . proxy_generation_panel import *
from . proxy_generation_property_group import *

classes = {
        OT_LWI_ProxyGenerationOperator, 
        OT_LWI_ApplyDeformOperator, 
        OT_LWI_TogglePreviewOperator,
        OBJECT_PT_LWI_ProxyGenerationPanel, 
        ProxyGenerationPropertyGroup
    }

def register():
    for c in classes:
        bpy.utils.register_class(c)
        
    bpy.types.Scene.lwi_proxy_generation = bpy.props.PointerProperty(type=ProxyGenerationPropertyGroup)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
        
    del bpy.types.Scene.lwi_proxy_generation
