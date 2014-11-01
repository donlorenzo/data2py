data2py
=======

Embed data files in python modules

Creation of Resource File 
-------------------------
 - reate an instance ResourceFile
   r = data2py.ResourceFile()
 - add resources adding an optional path inside the resource file
   r.add_resource("/filesystem/path/to/resource.png", "/virtual/path/resource.png")
 - save the resource file
   r.save("/filesystem/path/to/resourcemudule.py")

Usage of Resource File
----------------------
 - import the resource file
   import resourcefile as r
 - list content of resource file
   print(r.keys())
 - get the content of a resource
   data = r.get("/virtual/path/resource.png")
 - if you need a file-like object
   filelike = r.open("/virtual/path/resource.png")
  
