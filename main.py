from taipy.gui import Gui, notify
from taipy import Core, Config
import taipy as tp
from pages.root import root_md
from pages.district.district import district_md
from pages.dataset.dataset import dataset_md
from pages.nepal.nepal import nepal_md
from pages.collect_data.collect_data import collect_data_md

from data.data import data as dataset

district_list = dataset['District'].unique().tolist()
district_one = district_list[0]
district_two = district_list[1]


def save(state):
    state.scenario.first_district_name.write(state.district_one)
    state.scenario.second_district_name.write(state.district_two)
    state.refresh('scenario')
    tp.gui.notify(state, 's', "Saved! Ready to Submit")


def compareStats(first_district: str, second_district: str) -> str:
    print(first_district, second_district)
    return first_district+second_district


first_district_name_data_node_cfg = Config.configure_data_node(
    "first_district_name")
second_district_name_data_node_cfg = Config.configure_data_node(
    "second_district_name")
comparision_output_data_node_cfg = Config.configure_data_node(
    "comparision_output_data_node")
compare_stat_task_cfg = Config.configure_task(
    "compare_stat",
    compareStats,
    input=[
        first_district_name_data_node_cfg, second_district_name_data_node_cfg
    ],
    output=comparision_output_data_node_cfg
)

scenario_cfg = Config.configure_scenario(
    id="scenario", task_configs=[compare_stat_task_cfg]
)

Config.export('config.toml')

compare_stats_md = """
# Create your scenario:
<|{scenario}|scenario_selector|>

# Select the District to Compare

<|layout|columns=1 1|gap=30px|class_name=card|

<|container|
### District One
<|{district_one}|selector|lov={district_list}|on_change=save|dropdown|active={scenario}|>
|>

<|container|
### District Two
<|{district_two}|selector|lov={district_list}|on_change=save|dropdown|active={scenario}|>
|>

|>


# Run the **scenario**{:.color-primary}

<|layout|columns=1 1|

<|{scenario}|scenario|>

<|{scenario}|scenario_dag|>
|>

# **Comparision Stats**{:.color-primary}
<|{scenario.comparision_output_data_node}|data_node|>
"""

pages = {
    "/": root_md,
    "district": district_md,
    "nepal": nepal_md,
    "map": "Map",
    "dataset": dataset_md,
    "collect_data": collect_data_md,
    "compare_stats": compare_stats_md
}
if __name__ == "__main__":
    tp.Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    scenario.first_district_name.write(district_one)
    scenario.second_district_name.write(district_two)
    tp.submit(scenario)

    print("Value at the end of task is",
          scenario.comparision_output_data_node.read())

    tp.Gui(pages=pages).run(
        title="From Taipy Quine Quest-007", use_reloader=True)
