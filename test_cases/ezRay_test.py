## Dependencies
from ezRay import MultiCoreExecutionTool
from pprint import pprint

# configure ezRay
instance_metadata:dict = {
    'num_cpus': 4,              # number of cpus to use
    'num_gpus': 0,              # number of gpus to use
    'address': None,            # remote cluster address. None for local.
    }

# setup ezRay
MultiCore = MultiCoreExecutionTool(instance_metadata = instance_metadata, task_metadata = {'num_returns' : None})

# define a task
def do_something(foo:int, bar:int) -> int:
    return foo + bar

# prepare your data in a dictionary. They keys work as identifiers, while the values should be dictionaries matching the function signature.
data = {1:{'foo' : 0, 'bar': 1},
        2:{'foo': 1, 'bar': 2},
        3:{'foo': 2, 'bar': 3}}

# pass the data to ezRay
MultiCore.update_data(data)

# run the task
MultiCore.run(do_something)

# get the results
results = MultiCore.get_results()
pprint(results)