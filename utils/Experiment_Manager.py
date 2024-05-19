from mlflow import set_tracking_uri, create_experiment, get_experiment_by_name
from Auto_ML_Testing.utils.Experiment import Experiment
from tqdm import tqdm
from uuid import uuid4

# Function to create a colored string
# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
def colored_text(color, text):
    return f"{color}{text}{GREEN}"


class Experiment_Manager:
    def __init__(self, experiment_name: str,
                 experiment_description="No description",
                 experiment_creator="Admin",
                 add_UID=True):

        self.experiment_description = experiment_description

        if add_UID:
            # TODO: Not ideal, should be improved in the future
            self.experiment_name = experiment_name + "_" + str(uuid4())[:8]
            self.experiment_id = create_experiment(self.experiment_name)


        else:
            self.experiment_name = experiment_name

            if get_experiment_by_name(experiment_name) is None:
                self.experiment_id = create_experiment(experiment_name)
            else:
                self.experiment_id = get_experiment_by_name(experiment_name)['experiment_id']

        self.experiment_creator = experiment_creator
        self.experiments = []

    def add_experiments(self, list_of_configs: list):
        for config in list_of_configs:
            self.experiments.append(Experiment(config, self.experiment_id))

    def run_experiments(self):
        print(f"Your {len(self.experiments)} experiments in the {self.experiment_name}-context will now be executed")
        for experiment in tqdm(self.experiments, desc=colored_text(GREEN, "Experimenting in progress")):
            experiment.run_experiment()
        print("All your experiments have been successfully executed. The results can be found in the MLFlow UI")


