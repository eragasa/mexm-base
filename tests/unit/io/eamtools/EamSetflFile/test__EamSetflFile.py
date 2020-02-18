import os
from mexm.io.eamtools import SetflFile

setfl_path =  os.path.join(
    os.path.dirname(__file__),
    'Mishin-Ni-Al-2009.eam.alloy'
)
setfl = SetflFile()
setfl.read(path=setfl_path)
