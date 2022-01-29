from mesa.visualization.ModularVisualization import ModularServer

from evoenv.model import Environment
from evoenv.SimpleContinuousModule import SimpleCanvas
from evoenv.network_chart import InputChart, OutputChart
# from mesa.visualization.modules import ChartModule
from matplotlib import colors


# Green
RICH_COLOR = "#46FF33"
# Red
POOR_COLOR = "#FF3C33"
# Blue
MID_COLOR = "#3349FF"
# colors.to_hex('green')},

input_chart = InputChart(
    [{"Label": "Energy", "Color": colors.to_hex("red")},
     {"Label": "Fdist", "Color": colors.to_hex("green")},
     {"Label": "Frad", "Color": colors.to_hex("yellow")}]
)

output_chart = OutputChart(
    [{"Label": "Forward", "Color": colors.to_hex("red")},
     {"Label": "Rotation", "Color": colors.to_hex("green")}])

# info = PrintInfo()
size = (1000, 1000)

evo_canvas = SimpleCanvas(*size)
from collections import namedtuple, deque
from evoenv.utils import *
epochs = deque(
    [Epoch(0, [0.8]*100),
     Epoch(3000, [0.8]*20),
     Epoch(4000, [0.8]*200 + [-0.8]*50),
     Epoch(5000, [0.8]*20 + [-0.8]*10),
     Epoch(6000, [0.8] * 200 + [-0.8] * 50),
     Epoch(10000, [0.8] * 200 + [-0.8] * 50)
     ])


# evo_info = SelectedAgentInfo()
model_params = {
    "initial_population": 50,
    "epochs": epochs,
    "space_width": size[0],
    "space_height": size[1],
}
# from datetime import datetime
#
# today = datetime.now()
#         # date = today.strftime("%H%M%S_%d%m%y")
#         date = 'sim'
#         self.data_folder = f'./data/{date}'
#         import shutil
#         shutil.rmtree(self.data_folder) if os.path.exist(self.data_folder) else None
#         pathlib.Path(self.data_folder).mkdir(parents=True, exist_ok=True)


server = ModularServer(Environment, [input_chart, output_chart, evo_canvas], "EvoAgent", model_params)
