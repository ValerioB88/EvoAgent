from mesa.visualization.ModularVisualization import VisualizationElement
from .model import Environment, FoodToken
from .evoagent import EvoAgent
from .visualize import draw_net

def object_draw(pop_idx, type="agent", obj : EvoAgent=None, is_selected=False):
    if type == "agent":
        return {"type": "agent",
                "NAME": f'{obj.name} {obj.surname}',
                "pop_idx": pop_idx,
                "r": EvoAgent.radius,
                "generation": obj.generation,
                "parent_id": obj.parent_id,
                "children_id": obj.children_id,
                "color": f"hsl({obj.color_hsl}, 100%, 50%)",
                "fov": EvoAgent.fov,
                "mvisd": EvoAgent.max_vision_dist,
                "energy": f'{obj.energy:.3f}',
                "unique_id": obj.unique_id,
                "dir": obj.direction,
                "age": obj.age,
                "max_age": obj.max_age,
                "fertile_age_start": obj.fertile_age_start,
                "time_between_children": obj.time_between_children,
                "countdown_offspring": round(obj.countdown_offspring.counter) if obj.fertile else 'inf',
                "num_children": obj.num_children,
                "skin_c": str(obj.color_hsl),
                "name_sim": obj.name_run

                }
    if type == "food":
        return {"type": "good_food", "r": FoodToken.radius, "color": "Green" if obj.energy > 0 else "Red", "selected": is_selected}
    # if type == "bad_food":
    #     return {"type": "bad_food", "r": FoodToken.radius, "color": "Red"}


class SimpleCanvas(VisualizationElement):
    local_includes = ["src/evoagent/simple_continuous_canvas.js"]
    portrayal_method = None

    def __init__(self, canvas_height=500, canvas_width=500, name_sim='', additional_info=''):
        """
        Instantiate a new SimpleCanvas
        """
        self.portrayal_method = object_draw
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = f"new Simple_Continuous_Module({self.canvas_width}, {self.canvas_height}, '{name_sim}', '{additional_info}')"
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model: Environment):
        space_state = []
        food_aimed = -1
        agents = model.schedule.agents
        for idx, obj in enumerate(agents):
            sel = False


            portrayal = self.portrayal_method(idx, "agent", obj, is_selected=sel)
            portrayal["x"], portrayal["y"] = obj.pos

            if model.selected_agent_unique_id == obj.unique_id:
                food_aimed = obj.target_food
                if not obj.network_drawn:
                    draw_net(model.config, obj.genome, view=False, filename=model.net_svg_folder + f'id{obj.unique_id}')
                    obj.network_drawn = True
                portrayal['selected'] = True
                # Add here all those info that it's computationally expensive to add for all agents
                portrayal['children_pos'] = [list(model.schedule._agents[i].pos) for i in obj.children_id if i in model.schedule._agents]
                portrayal['pos'] = str(obj.pos.astype(int))
                portrayal['print_info'] = ['NAME', 'pop_idx', 'generation', 'unique_id',  'age', 'parent_id', 'num_children', 'children_id', 'energy', 'countdown_offspring', 'pos', 'skin_c', 'name_sim']


            space_state.append(portrayal)

        for idx, obj in enumerate(model.all_food):
            portrayal = self.portrayal_method(idx, "food", obj, is_selected=True if food_aimed == idx else False)
            portrayal["x"], portrayal["y"] = obj.pos
            portrayal["print_info"], portrayal["y"] = obj.pos

            space_state.append(portrayal)

        info = {}
        info["popcount"] = len(model.schedule.agents)
        info["entities"] = space_state
        info["message"] = model.message
        info["step"] = model.step_count
        info["global_commands"] = model.socket_message

        return info
