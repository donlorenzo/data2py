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
  

Copyright
---------
data2py is released under the zlib License:

Copyright (c) 2014 Lorenz Quack

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

    1. The origin of this software must not be misrepresented; you
    must not claim that you wrote the original software. If you use
    this software in a product, an acknowledgment in the product
    documentation would be appreciated but is not required.

    2. Altered source versions must be plainly marked as such, and
    must not be misrepresented as being the original software.

    3. This notice may not be removed or altered from any source
    distribution.
