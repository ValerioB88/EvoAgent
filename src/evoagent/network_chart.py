"""
Chart Module
============

Module for drawing live-updating line charts using Charts.js

"""
import json
from mesa.visualization.ModularVisualization import VisualizationElement


class Chart(VisualizationElement):
    """Each chart can visualize one or more model-level series as lines
     with the data value on the Y axis and the step number as the X axis.

    At the moment, each call to the render method returns a list of the most
    recent values of each series.

    Attributes:
        series: A list of dictionaries containing information on series to
                plot. Each dictionary must contain (at least) the "Label" and
                "Color" keys. The "Label" value must correspond to a
                model-level series collected by the model's DataCollector, and
                "Color" must have a valid HTML color.
        canvas_height, canvas_width: The width and height to draw the chart on
                                     the page, in pixels. Default to 200 x 500
        data_collector_name: Name of the DataCollector object in the model to
                             retrieve data from.
        template: "chart_module.html" stores the HTML template for the module.


    Example:
        schelling_chart = ChartModule([{"Label": "happy", "Color": "Black"}],
                                      data_collector_name="datacollector")

    TODO:
        Have it be able to handle agent-level variables as well.

        More Pythonic customization; in particular, have both series-level and
        chart-level options settable in Python, and passed to the front-end
        the same way that "Color" is currently.

    """

    package_includes = ["Chart.min.js"]
    local_includes = ["src/evoagent/network_chart.js"]


    def __init__(
        self,
        series,
        canvas_height=200,
        canvas_width=500,
        render_with_canvas=True,
        plot_every=1
    ):
        """
        Create a new line chart visualization.

        Args:
            series: A list of dictionaries containing series names and
                    HTML colors to chart them in, e.g.
                    [{"Label": "happy", "Color": "Black"},]
            canvas_height, canvas_width: Size in pixels of the chart to draw.
            data_collector_name: Name of the DataCollector to use.
        """
        self.plot_every = plot_every
        self.series = series
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width

        series_json = json.dumps(self.series)
        new_element = f"new SelectedAgentInfo({series_json}, {canvas_width}, {canvas_height}, {'true' if render_with_canvas else 'false'})"

        self.js_code = "elements.push(" + new_element + ");"


class InputChart(Chart):
    def render(self, model):
        # space_state = {}
        if model.step_count % self.plot_every == 0:
            if len(model.schedule.agents) > 0:
                # idx = find_pop_idx_from_id(model.schedule.agents, model.selected_agent_unique_id)
                current_values = model.schedule._agents[model.selected_agent_unique_id].inputs
                return current_values


class OutputChart(Chart):
    def render(self, model):
        # space_state = {}
        if model.step_count % self.plot_every == 0:
            if len(model.schedule.agents) > 0:
                # idx = find_pop_idx_from_id(model.schedule.agents, model.selected_agent_unique_id)
                current_values = model.schedule._agents[model.selected_agent_unique_id].outputs
                return current_values

from matplotlib import colors

cols = ["red", "green", "yellow", "blue", "cyan"]
class PopChart(Chart):
    def __init__(self, name_runs, **kwargs):
        self.name_runs = name_runs
        super().__init__([{"Label": f"Num {n}", "Color": colors.to_hex(cols[idx])} for idx, n in enumerate(self.name_runs)], **kwargs)

    def render(self, model):
        if model.step_count % self.plot_every == 0:
            if len(model.schedule.agents) > 0:
                current_values = [len([j for j in model.schedule.agents if j.name_run == i]) for i in self.name_runs]
                return current_values



