bl_info = {
  "name": "BlenderTime",
  "author": "Pacifiky",
  "version": (1, 0),
  "blender": (2, 80, 0),
  "location": "View3D > N",
  "description": "Keep track of your hours in blender!",
  "warning": "",
  "doc_url": "",
  "category": "Scene",
}

import bpy,time,os,atexit,struct

starttime = time.time()
opentime = 0
uptime = 0.0

def commit():
    f = open(r"C:\Users\lucas\Documents\Programming\BlenderTime\timeblender", "wb")
    f.write(struct.pack("f",uptime+(time.time()-starttime)))
    f.write(struct.pack("I",opentime))
    f.close()

atexit.register(commit)

def hms(num):
    return num//3600,(num%3600)//60,(num%3600)%60

try:
    f = open(r"C:\Users\lucas\Documents\Programming\BlenderTime\timeblender","rb")
    uptime = struct.unpack("f",f.read(4))[0]
    opentime = struct.unpack("I",f.read(4))[0]+1
    f.close()
    commit()
except:
    f = open(r"C:\Users\lucas\Documents\Programming\BlenderTime\timeblender", "wb")
    f.write(struct.pack("f",0.0))
    f.write(struct.pack("I",1))
    f.close()

class UPDOperator(bpy.types.Operator):
    """Updates the UI display"""
    bl_idname = "updatebltime.1"
    bl_label = "Update stats"

    def execute(self, context):
        bpy.context.area.tag_redraw()
        return {'FINISHED'}

# Define a Panel to display the clock
class ClockPanel(bpy.types.Panel):
    bl_label = "Blender Clock"
    bl_idname = "OBJECT_PT_ClockPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Clock"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Opens: " + str(opentime))
        uhour,umin,usec = hms(int(uptime+(time.time()-starttime)))
        layout.label(text="Total Time: " + str(uhour) + ":" + str(umin) + ":" + str(usec))
        uhour,umin,usec = hms(int(time.time()-starttime))
        layout.label(text="Uptime: " + str(uhour) + ":" + str(umin) + ":" + str(usec))
        row = layout.row()
        row.operator(UPDOperator.bl_idname,text="Update",icon="TIME")
        

from bpy.utils import register_class, unregister_class

_classes = [ClockPanel,UPDOperator]

def register():
    for i in range(len(_classes)):
        register_class(_classes[i])
        
def unregister():
    for i in range(len(_classes)):
        unregister_class(_classes[i])
        
if __name__ == "__main__":
    register()