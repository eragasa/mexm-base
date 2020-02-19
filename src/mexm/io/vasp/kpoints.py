class Kpoints(object):
    """ KPOINTS file

    Args:
        filename(str): the filename to either read from or to write to.  Default is KPOINTS
        comment(str): a comment to use for the KPOINTS file.  Default is 'Automatic Mesh'
        n_kpoints(int): number of kpoints for automatic mesh.  Default is 0.
        mesh_type(str): mesh type to create.  Default is 'Monkhorst-Pack'
        mesh_size(:obj:`list` of :obj:`int`): defines the density of the sampling in the
            Brillouin zone of the reciprocal lattice.
        mesh_shift(:obj:`list` of :obj:`int`): defines the shift of the k-kpoint mesh

    Attributes:
        filename(str): the filename to either read from or to write to.  Default is KPOINTS
        comment(str): a comment to use for the KPOINTS file.  Default is 'Automatic Mesh'
        n_kpoints(int): number of kpoints for automatic mesh.  Default is 0.
        mesh_type(str): mesh type to create.  Default is 'Monkhorst-Pack'
        mesh_size(:obj:`list` of :obj:`int`): defines the density of the sampling in the
            Brillouin zone of the reciprocal lattice.
        mesh_shift(:obj:`list` of :obj:`int`): defines the shift of the k-kpoint mesh
    """
    def __init__(self,
                 filename="KPOINTS",
                 comment="Automatic Mesh",
                 n_kpoints = 0,
                 mesh_type = "Monkhorst-Pack",
                 mesh_size = [4,4,4],
                 mesh_shift = [0,0,0]):

        self.filename = filename
        self.comment = comment
        self.n_kpoints = n_kpoints
        self.mesh_type = mesh_type
        self.mesh_size = [i for i in mesh_size]
        self.mesh_shift = [i for i in mesh_shift]


    def to_string(self):
        str_out = "{}\n".format(self.comment)
        str_out += "{}\n".format(self.n_kpoints)
        str_out += "{}\n".format(self.mesh_type)

        str_out += "{:3d} {:3d} {:3d}\n".format(self.mesh_size[0],
                                                self.mesh_size[1],
                                                self.mesh_size[2])
        str_out += "{:3d} {:3d} {:3d}\n".format(self.mesh_shift[0],
                                               self.mesh_shift[1],
                                               self.mesh_shift[2])
        return str_out

    def write(self,filename = None):
        if filename is not None:
            self.filename = filename
        f = open(self.filename, 'w')
        f.write(self.to_string())
        f.close()

    def read(self,filename = None):
        if filename is not None:
            self.filename = filename
