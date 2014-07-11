# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#  Contributors : Saurabh Wankhade
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Bhai's Tools",
    "author": "Saurabh Wankhade",
    "version": (0, 1, 1),
    "blender": (2, 70),
    "description": "Layers UFf",
    "warning": "",
    "category": "3D View"}
import bpy

# Amaranth Code
# XXX Todo how to reuse classes ?
class RiggLayers(bpy.types.Operator):
    '''Riggers layers'''
    bl_idname="layermgr.rigger"
    bl_label = "Save Riggers layer"
    
    def execute(self, context):
        listriglyr = []
        n = -1

        for l in context.scene.layers:
            n += 1
            if l:
                listriglyr.append(n)

        context.scene['chriglyr'] = listriglyr
        self.report({'INFO'}, "Layers for Render Saved")

        return{'FINISHED'}
    
class RiggRestore(bpy.types.Operator):
    '''Riggers Layer Restorer'''
    bl_idname="layermgr.rigreset"
    bl_label = "Reset Rig layers in viewport"
    

    def execute(self, context):    
        scene = bpy.context.scene
        vwly = bpy.context.scene['chriglyr']   
        rl= bpy.context.scene.render.layers.active
        rlname = rl.name

        
        for window in bpy.context.window_manager.windows:
            screen = window.screen

            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    override = {'window': window, 'screen': screen, 'scene': scene, 
                                'area': area, 'region': area.regions[4],
                                'blend_data': context.blend_data}
                    if vwly:
                        bpy.ops.view3d.layers(override, nr=vwly[0]+1, extend=False, toggle=False)
                        
                        for n in  vwly:
                            bpy.context.scene.layers[n] = True
                            bpy.context.scene.render.layers[rlname].layers[n] = True 
                    else:
                        bpy.ops.view3d.layers(override, nr=1, extend=False, toggle=False)
                        self.report({'INFO'}, "No layers set for render")
                            
                    break
                
        return {'FINISHED'}
    
    
class AnimatorsLayers(bpy.types.Operator):
    '''Animators layers'''
    bl_idname="layermgr.anim"
    bl_label = "Save Animators layer"
    
    def execute(self, context):
        listanimlyr = []
        n = -1

        for l in context.scene.layers:
            n += 1
            if l:
                listanimlyr.append(n)

        context.scene['chanimlyr'] = listanimlyr
        self.report({'INFO'}, "Layers for Render Saved")

        return{'FINISHED'}
    
class AnimatorsRestore(bpy.types.Operator):
    '''Animators Layer Restorer'''
    bl_idname="layermgr.animreset"
    bl_label = "Reset Animators layers in viewport"
    def execute(self, context):    
        scene = bpy.context.scene
        vwly = bpy.context.scene['chanimlyr']   
        rl= bpy.context.scene.render.layers.active
        rlname = rl.name
        l = []
        l = bpy.context.scene.render.layers[rlname].layers
        pos = []
        i=0
        for a in l:
            i=i+1
            if  a ==True:
                pos.append(i-1)
        for b in pos:
            print (b)
            

        for ctr in range(0,20):
                            bpy.context.scene.render.layers[rlname].layers[ctr] = False    
                    
        for window in bpy.context.window_manager.windows:
            screen = window.screen

            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    override = {'window': window, 'screen': screen, 'scene': scene, 
                    'area': area, 'region': area.regions[4],
                    'blend_data': context.blend_data}

                    
                        
                    if vwly:
                        bpy.ops.view3d.layers(override, nr=vwly[0]+1, extend=False, toggle=False)
                        for n in  vwly:
                            bpy.context.scene.layers[n] = True
                            bpy.context.scene.render.layers[rlname].layers[n] = True    
                        for n in pos:
                            if(bpy.context.scene.layers[n] == False and bpy.context.scene.render.layers[rlname].layers[n] == True):
                                bpy.context.scene.render.layers[rlname].layers[n] = False
                    
                                
                    else:
                        bpy.ops.view3d.layers(override, nr=1, extend=False, toggle=False)
                    #    bpy.context.scene.render.layers[rlname].layers[n] = False   
                        self.report({'INFO'}, "No layers set for render")
                            
                    break
                
            return {'FINISHED'}    
    
#End Amaranth Code
        
class DrawPanel(bpy.types.Panel):
    bl_label = "Bhai's panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text="Layer Manager")
        split = layout.split()
        col = split.column()
        col.operator("layermgr.rigger",text = "Rig Save", icon='CANCEL')
        col.operator("layermgr.rigreset",text = "Rig Reset", icon = 'RADIO')
        
        row = layout.row()
        row.label(text = "Layer Manager(Animators)")
        split = layout.split()
        col = split.column()
        col.operator("layermgr.anim", text = "Animators Save", icon = 'CANCEL')
        col.operator("layermgr.animreset", text = "Animators Reset", icon = 'RADIO')
        
        

def register():
    bpy.utils.register_class(DrawPanel)
    bpy.utils.register_class(RiggRestore)
    bpy.utils.register_class(RiggLayers)
    bpy.utils.register_class(AnimatorsLayers)
    bpy.utils.register_class(AnimatorsRestore)
    

def unregister():
    bpy.utils.unregister_class(AnimatorsRestore)
    bpy.utils.unregister_class(AnimatorsLayers)
    bpy.utils.unregister_class(RiggRestore)
    bpy.utils.unregister_class(RiggLayers)
    bpy.utils.unregister_class(DrawPanel)



if __name__ == "__main__":
    register()








                         







