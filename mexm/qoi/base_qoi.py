from copy import deepcopy

class Qoi(object):
    qoi_type = 'base_qoi'
    is_abstract_class = True

    """ Abstract Quantity of Interest

    Args:
        qoi_name(str)
        qoi_type(str)
        structure_names(list of str)

    Attributes:
        qoi_name(str): this is a unique identifier
        qoi_type(str): this should be set by the implementing class
        structure_names
        reference_values(dict): these are the reference values of quantities
            of interest which we want to calculate.
        task_definitions(dict):
             task_definition[task_name]
             task_definition[task_name][task_type]
             task_definition[task_name][structure]
        task_dependencies(dict):
             task_dependencies[task_name]
        results(dict): these are the results after aggregating the values
            from the different simulations and making some calculations.
    """
    def __init__(self, qoi_name, structures):
        assert isinstance(qoi_name,str)
        assert isinstance(qoi_type,str)
        assert any([
            isinstance(structures,dict),
            isinstance(structures,list),
            isinstance(structures,str),
            ])
        #assert all([isinstance(k,str) for k,v in structures.items()])
        #assert all([isinstance(v,str) for k,v in structures.items()])

        self.qoi_name = qoi_name
        self.structures = deepcopy(structures)
        self.tasks = None

    def determine_tasks(self):
        raise NotImplementedError

    def calculate_qoi(self):
        raise NotImplementedError

    @property
    def reference_value(self):
        return self._ref_value

    @reference_value.setter
    def reference_value(self, value):
        assert type(value), float
        self._ref_value = value

    @property
    def predicted_value(self):
        return self._predicted_value

    @predicted_value.setter
    def predicted_value(self, qhat):
        self._predicted_value = qhat

    def add_task(self,task_type,task_name,task_structure,bulk_structure_name=None):
        if self.tasks is None:
            self.tasks = OrderedDict()

        self.tasks[task_name] = OrderedDict()
        self.tasks[task_name]['task_type'] = task_type
        self.tasks[task_name]['task_structure'] = task_structure
        if bulk_structure_name is not None:
            self.tasks[task_name]['bulk_structure'] = bulk_structure_name

    def process_task_results(self,task_results):
        assert isinstance(task_results,dict)

        if self.task_results is None:
            self.task_results = OrderedDict()

    def add_required_simulation(self,structure,simulation_type):
        simulation_name = '{}.{}'.format(structure,simulation_type)
        self.required_simulations[simulation_name] = {}
        self.required_simulations[simulation_name]['structure'] = structure
        self.required_simulations[simulation_name]['simulation_type'] = simulation_type
        self.required_simulations[simulation_name]['precedent_tasks'] = None
        return simulation_name

    def add_precedent_task(self,
            task_name,precedent_task_name,precedent_variables):
        """add a precedent task

        Args:
            task_name(str):
            precedent_task_name(str):
            precedent_variables(str):

        Raises:
            ValueError

        """

        if task_name not in self.required_simulations.keys():
            s = ( 'Tried to add precedent_task_name to task_name.  task_name '
                  'does not exist in required_simulations.\n'
                  '\ttask_name: {}\n'
                  '\tpredecessor_task_name: {}\n' ).format(
                          task_name,
                          precedent_task_name)
            raise ValueError(s)

        if precedent_task_name not in self.required_simulations.keys():
            s = ( 'Tried to add predecessor_task_name to task_name.  '
                  'predecessor_task_name task_name does not exist in '
                  'required_simulations.\n'
                  '\ttask_name: {}\n'
                  '\tpredecessor_task_name: {}\n' ).format(
                          task_name,
                          precedent_task_name)
            raise ValueError(s)

        if self.required_simulations[task_name]['precedent_tasks'] is None:
            self.required_simulations[task_name]['precedent_tasks'] = {}

        self.required_simulations[task_name]['precedent_tasks'][precedent_task_name] ={}
        for v in required_variables:
            self.required_simulations[task_name]['precedent_tasks'][precedent_task_name] = {
                    'variable_name':v,
                    'variable_value':None}

    def determine_required_simulations(self):
        raise NotImplementedError

    def calculate_qoi(self):
        s_type = str(type(self))
        raise NotImplementedError(s_type)

    def get_required_simulations(self):
        if self.required_simulations is None:
            self.determine_required_simulations()
        return copy.deepcopy(self.required_simulations)
