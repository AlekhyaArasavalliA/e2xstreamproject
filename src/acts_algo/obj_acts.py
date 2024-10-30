import os
import sys

from e2xostream.src.scenario_generator.basescenario import BaseScenario
from e2xostream.stk.scenariogeneration import xosc, prettyprint, ScenarioGenerator
from e2xostream.stk.vehicledynamics.VehicleControl import VehicleControlMovements as vehiclecontrol
from e2xostream.stk.vehicledynamics.DataControl import DataControls as datacontrol
from e2xostream.stk.vehicledynamics.VehicleScenarioSetup import VehicleScenario
from e2xostream.src.vehiclestream.ebtb_stream import EBTBAnalyzer, EBTB_API_data
from e2xostream.config import default_properties, global_parameters, settings
from e2xostream.config.api_constants import (api_methods_constants as ApiMethods,
                                             ego_api_constants as EgoAPI,
                                             obj_api_constants as ObjAPI,
                                             other_api_constants as OtherAPI)
from e2xostream.src.scenario_generator import basescenario as BS

MAIN_PATH = os.path.abspath(os.path.join(__file__, "..", "..", "..", ".."))
CURRENT_WORKING_FILE_DIRECTORY = os.path.abspath(os.path.join(__file__))
CURRENT_WORKING_DIRECTORY = os.path.abspath(os.path.join(__file__, ".."))

if MAIN_PATH not in sys.path:
    sys.path.append(MAIN_PATH)

dir_path = os.path.dirname(os.path.realpath(__file__))
for root, dirs, files in os.walk(dir_path):
    sys.path.append(root)


class Obj_Acts:
    def __init__(self, egoname, states_analysis, paramlist_analysis, state_events, param_events, esmini_path):
        self.states_analysis = states_analysis
        self.paramlist_analysis = paramlist_analysis
        self.state_events = state_events
        self.param_events = param_events
        self.esmini_path = esmini_path
        self.target_name = None


        self.egoname = egoname
        self.open_scenario_version = 0
        self.obj_speed, self.obj_transition_time = EBTB_API_data.get_obj_speed_transition_time(target_name=self.target_name, states_analysis=self.states_analysis)



        self.VehicleControls = vehiclecontrol()
        self.Data_Controls = datacontrol()
        self.VehicleDefines = VehicleScenario()
        self.basescenario = BaseScenario()

        self.processed_flags = {}  # Define it as an instance attribute
        self.lane = 0

        # for state_id, state_info in self.states_analysis():
        #     for kv in state_info.items() :
        # target_name = "Obj1"
        # for k, v in self.states_analysis.items():
        #     for kv, vv in v["ObjectActions"].items():
        #         if "Obj_Set_Longitudinal_Speed" == vv[0]["Action"]:
        #             if vv[0]["Parameters"][0]["ObjectId"] == "target_name":
        #                 print("qwe")
        #         # Process for Obj1 if it hasn't been processed yet
            #     if 'Obj1' in state_info['ObjectActions']:
            #         obj1_actions = state_info['ObjectActions']['Obj1']
            #         print("qwe1",obj1_actions)
            #         # for action in obj1_actions:
                    #     if action['Action'] == 'Obj_SetLongitudinalSpeed':
                    #         # for param in action['Parameters']:

        # for k, v in self.states_analysis.items():
        #     for kv, vv in v["ObjectActions"].items():
        #         if vv[0]['Action'] == "Obj_SetLongitudinalSpeed":
        #             obj_id = vv[0]['Parameters'][0]['ObjectId']
        #             print(obj_id)


    # def obj_set_longitudinal_speed(self, all_target_events,target_name):
    #     print("exit")
    #     start_trig = self.VehicleDefines.create_target_event(value=15)
    #     #start_action = self.basescenario.Target_initialize(init=None,step_time=None,states_analysis=self.states_analysis,overlap_data=None)
    #     start_action = self.VehicleDefines.obj_acceleration_actions(self.obj_speed,
    #                                                                 self.obj_transition_time,
    #                                                                 self.extract_info,
    #                                                                 target_name=target_name,
    #                                                                 state_data=self.states_analysis,
    #                                                                 param_data=self.paramlist_analysis)
    #
    #     target_next_event = self.VehicleDefines.define_target_action_event(start_trig=start_trig,
    #                                                                        start_action=start_action)
    #     all_target_events.append(target_next_event)
    def Obj_Accelration_act(self, all_target_events,target_name):
        pass

        # print("enter acc loop")
        #
        # # pass
        # obj_speed = 0
        # start_trig = self.VehicleDefines.create_target_event(value=15)
        # start_action = self.VehicleDefines.create_target_action(obj_speed)
        #
        # target_next_event = self.VehicleDefines.define_target_action_event(start_trig=start_trig,
        #                                                                    start_action=start_action)
        # all_target_events.append(target_next_event)

    # def obj_set_longitudinal_speed(self, all_target_events,target_name):
    #     start_trig = self.VehicleDefines.create_target_event(value=15)
    #     obj_id = []
    #     for k, v in self.states_analysis.items():
    #         for kv, vv in v["ObjectActions"].items():
    #             if vv[0]['Action'] == "Obj_SetLongitudinalSpeed":
    #                 obj_id.append(vv[0]['Parameters'][0]['ObjectId'])
    #                 # obj_id = vv[0]['Parameters'][0]['ObjectId']
    #
    #     for obj in obj_id:
    #         if target_name == obj:
    #             start_action = self.VehicleDefines.obj_acceleration_actions(self.obj_speed,
    #                                                                     self.obj_transition_time,
    #                                                                     self.extract_info,
    #                                                                     target_name,
    #                                                                     state_data=self.states_analysis,
    #                                                                     param_data=self.paramlist_analysis)
    #
    #             target_next_event = self.VehicleDefines.define_target_action_event(start_trig=start_trig,
    #                                                                            start_action=start_action)
    #             all_target_events.append(target_next_event)
    # def Obj_Accelration_act(self, all_target_events,target_name):
    #     all_target_events = []  # Create a new list for each call
    #
    #     obj_speed = 0
    #     start_trig = self.VehicleDefines.create_target_event(value=15)
    #     start_action = self.VehicleDefines.create_target_action(obj_speed)
    #
    #     target_next_event = self.VehicleDefines.define_target_action_event(
    #         start_trig=start_trig,
    #         start_action=start_action
    #     )
    #
    #     all_target_events.append(target_next_event)
    #     print("asd", all_target_events)

    def obj_changelane(self, all_target_events,target_name):
        try:

            start_trig = self.VehicleDefines.create_target_event(value=15)

            for state_id, state_info in self.states_analysis.items():
                if 'ObjectActions' in state_info and state_info['ObjectActions']:
                    if target_name in state_info['ObjectActions']:
                        obj1_actions = state_info['ObjectActions'][target_name]
                        for action in obj1_actions:
                            if action['Action'] == 'Obj_ChangeLane':
                                direction = action['Parameters'][0]['Direction']

            for k, v in self.states_analysis.items():
                for obj_id, actions in v.get('ObjectActions', {}).items():
                    for action in actions:
                        if action.get('Action') == ObjAPI.Obj_Initialize:
                            for param in action.get('Parameters', []):
                                present_lane = param.get('LaneSelection')

            start_action = self.VehicleDefines.create_obj_lanechange_action(obj_id=target_name, direction = direction, present_lane=present_lane,
                                                                            state_data=self.states_analysis,
                                                                            param_data=self.paramlist_analysis)
            target_next_event = self.VehicleDefines.define_target_action_event(start_trig=start_trig,
                                                                               start_action=start_action)

            all_target_events.append(target_next_event)
        except Exception as e:
            print(f"Error: {e}")

    def obj_setlateraldisplacement(self, all_target_events,target_name):
        for k, v in self.states_analysis.items():
            for kv, vv in v["ObjectActions"].items():
                if vv[0]['Action'] == "Obj_SetLateralDisplacement":
                    dispvalue = vv[0]['Parameters'][0]['TargetDisplacement']

        start_trig = self.VehicleDefines.create_target_event(value=5)
        start_action = self.VehicleDefines.create_obj_lateral_distance_action(value=dispvalue,
                                                                              entity=target_name,
                                                                              state_data=self.states_analysis)
        target_next_event = self.VehicleDefines.define_target_action_event(start_trig=start_trig,
                                                                           start_action=start_action)
        all_target_events.append(target_next_event)

    # def obj_set_longitudinal_speed(self, all_target_events, target_name):
    #     print("enter obj_set_longspeed")
    #     start_trig = self.VehicleDefines.create_target_event(value=15)
    #     start_action = self.VehicleDefines.obj_acceleration_actions(target_name,
    #                                                                 transition_time=self.obj_transition_time,
    #                                                                 state_data=self.states_analysis,
    #                                                                 param_data=self.paramlist_analysis)
    #
    #     target_next_event = self.VehicleDefines.define_target_action_event(start_trig=start_trig,
    #                                                                        start_action=start_action)
    #     all_target_events.append(target_next_event)

    def obj_set_longitudinal_speed(self, all_target_events, target_name):
        start_trig = self.VehicleDefines.create_target_event(value=15)

        for state_id, state_info in self.states_analysis.items():
            if 'ObjectActions' in state_info and state_info['ObjectActions']:
                if target_name in state_info['ObjectActions']:
                    obj1_actions = state_info['ObjectActions'][target_name]
                    for action in obj1_actions:
                        if action['Action'] == 'Obj_SetLongitudinalSpeed':
                            start_action = self.VehicleDefines.obj_acceleration_actions(target_name,
                                                                                        transition_time=self.obj_transition_time,
                                                                                        state_data=self.states_analysis,
                                                                                        param_data=self.paramlist_analysis)

                            target_next_event = self.VehicleDefines.define_target_action_event(start_trig=start_trig,
                                                                                               start_action=start_action)
                            all_target_events.append(target_next_event)
