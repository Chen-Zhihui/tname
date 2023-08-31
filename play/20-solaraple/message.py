import solara
import reacton.ipyvuetify as rv
import requests
# from IPython.display import JSON
import pandas as pd
import json
import pathlib
from tname.fix.datatable import DataFrame

example_file_path = pathlib.Path(__file__).parent / "data" / "event_example.csv"

example_df = pd.read_csv(f"{example_file_path}")

def split(msg):
    url = "http://172.80.0.1:8900"

    # req = {   
    #     "prompt" : f"""{input["prompt"]}<{input["c"]}>""",
    #     "history" : [],
    #     "max_length" : int(input['max_length']),
    #     "top_p" : float(input['top_p']),
    #     "temperature" : float(input['temperature'])
    # }


    
    req = {
    "prompt" : '''从原文中提取信息并输出，原文由尖括号<>包围，输出为JSON格式。要提取的信息包括一个或多个"侦获事件", 在输出中用数组表示。每个"侦获事件"包含多个字段，这些字段是："日期"、"时间"、"卫星"、"地点"、"被侦获装备的数量"、"被侦获装备的名称"、"被侦获装备的行为"。如果上述字段没有出现在原文中，对应的字段值置为空。原文如下：<2023年6月8日3时5分31秒,吉林一号高分03D星侦获两艘康定级护卫舰驶离基隆军港.>''',
        "history" : [],
        "max_length" : 1024,
        "top_p" : 0.7,
        "temperature" : 0.01
    }
    

    res = requests.post(url, json=req)
    j = res.json()
    # print(j)
    r = j["response"] #["侦获事件"]
    print(r)
    return json.loads(r)

@solara.component
def MsgSplitter():
    # df = pd.DataFrame()
    query, set_query = solara.use_state("") 
    res, set_res = solara.use_state("")
    info, set_info = solara.use_state("")
    evs, set_evs = solara.use_state([])
    def on_query(v):
        if v == "":
            set_res({})
        else:
            try: 
                res = split(v)
                print(f"type(res)={type(res)}")
                set_evs(res["侦获事件"])
            except Exception as e:
                print(e)
                res = "ERROR"
            finally:
                set_res(res)
                set_info(str(res))
    with solara.Row(justify="center") as main:
        with solara.Card() :
            def on_action_cell(column, row_index):
                # row_index = int(row_index)
                # print(f"========  on_action_cell  {row_index}")                
                item = example_df.iloc[row_index]
                # print(item)
                set_query(item["描述"])
                on_query(item["描述"])
            cas = [
                solara.CellAction(
                    icon="mdi-white-balance-sunny", 
                    name="提取信息", 
                    on_click=on_action_cell
                ),
                ]
            DataFrame(example_df, items_per_page=10, column_actions=[], cell_actions=cas)
        with solara.Card() :
            with solara.Row():
                solara.InputText(
                    label="输入侦获事件文本",
                    value=query,
                    on_value=on_query,
                    )
            if res == "ERROR":
                solara.Markdown(info)
            else:
                try:
                    # print(evs)
                    for e in evs:
                        print(e)
                        for k, v in dict(e).items():
                            with solara.Row() :
                                solara.Text(text=f"{k} : ")
                                solara.Text(text=v)

                except Exception as ee:
                    print(ee)
    return main