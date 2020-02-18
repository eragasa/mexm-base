import ase.build
from mexm.structure import SimulationCell, Lattice, convert_coordinates
import numpy as np

def test__initialize_from_ase():
    structure_ase = ase.build.bulk('Cu', 'fcc', cubic=True)
    structure_mexm = SimulationCell.initialize_from_ase(obj=structure_ase)

    assert isinstance(structure_mexm, SimulationCell)
    assert isinstance(structure_mexm.a0, float)
    assert isinstance(structure_mexm.H, np.ndarray)
    assert len(structure_ase) == len(structure_mexm.atomic_basis)
    for i,a in enumerate(structure_ase):
        assert structure_mexm.atomic_basis[i].symbol == a.symbol

        ase_position = convert_coordinates(
            position = a.position,
            lattice = Lattice(a0=1.0, H=structure_ase.cell),
            src_type='cartesian',
            dst_type='direct'
        )
        mexm_position = structure_mexm.atomic_basis[i].position

        assert np.array_equal(ase_position, mexm_position)

def dev__initialize_from_ase():
    structure_ase = ase.build.bulk('Cu', 'fcc', cubic=True)
    structure_mexm = SimulationCell.initialize_from_ase(obj=structure_ase)

if __name__ == "__main__":
    dev__initialize_from_ase()
