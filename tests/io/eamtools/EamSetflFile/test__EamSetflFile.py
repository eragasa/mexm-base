import os
from mexm.io.eamtools import EamSetflFile

setfl_path =  os.path.join(
    os.path.dirname(__file__),
    'Mishin-Ni-Al-2009.eam.alloy'
)
setfl = EamSetflFile()
setfl.read(path=setfl_path)
