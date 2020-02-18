import pytest
from mexm.structure import SimulationCell

def dev__SimulationCell():
    o = SimulationCell()
    print(o.lattice)

def dev__MgO():
    o = SimulationCell()
    o.a0 = 4.21
    o.h1 = [1,0,0]
    o.h2 = [0,1,0]
    o.h3 = [0,0,1]

    o.add_atom(symbol='Mg', position = [0.0, 0.0, 0.0])
    o.add_atom(symbol='Mg', position = [0.5, 0.5, 0.0])
    o.add_atom(symbol='Mg', position = [0.0, 0.5, 0.5])
    o.add_atom(symbol='Mg', position = [0.5, 0.0, 0.5])
    o.add_atom(symbol='O', position = [0.5, 0.0, 0.0])
    o.add_atom(symbol='O', position = [0.0, 0.5, 0.0])
    o.add_atom(symbol='O', position = [0.5, 0.5, 0.5])
    o.add_atom(symbol='O', position = [0.0, 0.0, 0.5])

    print(o)

if __name__ == "__main__":
    dev__SimulationCell()
    dev__MgO()
