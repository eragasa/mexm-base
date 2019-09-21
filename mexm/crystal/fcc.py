from mexm.crystal import SimulationCell

class FaceCenteredCubic(SimulationCell):

    def get_nearest_neighbor_information(a):
        n_NN = [12,6,24,12,24,8]
        d_NN = [a/np.sqrt(2.),a,a*np.sqrt(1.5),a*np.sqrt(2.0),a*np.sqrt(2.5),a*np.sqrt(3.0)]
        return n_NN, d_NN
