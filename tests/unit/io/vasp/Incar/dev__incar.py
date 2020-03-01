import os
from mexm.io.vasp import Incar

incar_path = os.path.join('resources', 'INCAR')

obj = Incar()
obj.read(path=incar_path)
print(obj.to_string())