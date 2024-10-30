import os
import sys
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
from e2xostream.src.acts_algo import ego_acts, obj_acts
from e2xostream.stk.fun_register_dispatch import FunctionRegisterDispatcher


MAIN_PATH = os.path.abspath(os.path.join(__file__, "..", "..", "..", ".."))
CURRENT_WORKING_FILE_DIRECTORY = os.path.abspath(os.path.join(__file__))
CURRENT_WORKING_DIRECTORY = os.path.abspath(os.path.join(__file__, ".."))

if MAIN_PATH not in sys.path:
    sys.path.append(MAIN_PATH)

dir_path = os.path.dirname(os.path.realpath(__file__))
for root, dirs, files in os.walk(dir_path):
    sys.path.append(root)


class EgoScnearioActs:
    def __init__(self, egoname, states_analysis, paramlist_analysis, state_events, param_events, esmini_path):
        self.states_analysis = states_analysis
        self.paramlist_analysis = paramlist_analysis
        self.state_events = state_events
        self.param_events = param_events
        self.esmini_path = esmini_path

        self.egoname = egoname
        self.open_scenario_version = 0
        self.ego_speed, self.ego_transition_time = EBTB_API_data.get_ego_speed_transition_time(states_analysis=self.states_analysis)

        # self.ego_speed, self.obj_speed, self.ego_transition_time, self.obj_transition_time = EBTB_API_data.get_ego_obj_speed_transition_time(
        #     states_analysis=self.states_analysis)

        self.VehicleControls = vehiclecontrol()
        self.Data_Controls = datacontrol()
        self.VehicleDefines = VehicleScenario()

        self.EGO_algo_acts = ego_acts.Ego_Acts(egoname, states_analysis, paramlist_analysis,
                                               state_events, param_events, esmini_path)

        self.register_dispatch = FunctionRegisterDispatcher()
        # Register the functions
        # dispatcher.register('a', func_a)
        # Dispatch the function
        # dispatcher.dispatch('a', 'Hello', 'World')
        # dispatcher.dispatch('b', 'Test', kwarg1='Optional')
        # dispatcher.dispatch('c', 1, 2, 3)

    def __call__(self, all_ego_events):
        self.maneuver_api_mapping()
        self.check_api_dispatch_function(all_ego_events)

    # def maneuver_api_mapping(self, api_name):
    #     def register_func(func):
    #         self.register_dispatch.register(api_name, func)
    #         return func
    #     return register_func

    def maneuver_api_mapping(self):

        self.register_dispatch.register(EgoAPI.Dri_PrepareVehicle, self.initial_acceleration)
        self.register_dispatch.register(EgoAPI.Dri_SetAccelerationPedal, self.throttle_acts)
        self.register_dispatch.register(EgoAPI.Dri_SetBrakePedal, self.brake_acts)
        self.register_dispatch.register(OtherAPI.E_SysVehicleVelocity, self.E_sysvehiclevelocity)
        self.register_dispatch.register(EgoAPI.Dri_SetLateralDisplacement, self.dri_setLateralDisplacement)
        #self.register_dispatch.register(EgoAPI.Dri_SetLateralReference, self.dri_setLateralReference)
        self.register_dispatch.register(OtherAPI.E_ObjectDistanceLaneBased, self.ego_ObjectDistanceLaneBased)
        self.register_dispatch.register(OtherAPI.E_DistanceTimeBased, self.ego_E_DistanceTimeBased)
        #self.register_dispatch.register(EgoAPI.Dri_SetLongitudinalSpeed, self.dri_setlongitudinalspeed)
        #self.register_dispatch.register(OtherAPI.E_ADASState,self.ego_E_ADASState)
        #self.register_dispatch.register(EgoAPI.Dri_SetIndicatorState,self.dri_setIndicatorState)
        #self.register_dispatch.register(EgoAPI.Dri_SetVehicleDoor,self.ego_dri_SetVehicleDoor)
        # self.register_dispatch.register(EgoAPI)
        # self.register_dispatch.register(EgoAPI) E_ObjectCollision
        self.register_dispatch.register(EgoAPI.Dri_SwitchGear, self.ego_dri_SwitchGear)
        # self.register_dispatch.register(EgoAPI) Dri_SetVehicleDoor
        self.register_dispatch.register(EgoAPI.Dri_SetParkingBrake, self.ego_dri_SetParkingBrake)
        self.register_dispatch.register(EgoAPI.Dri_SetSteeringWheelAngle, self.ego_dri_SetSteeringWheelAngle)

    def check_api_dispatch_function(self, all_ego_events):
        for statekey, statevalue in self.states_analysis.items():
            ego_actions = statevalue.get("EgoActions", [])
            if not ego_actions:
                continue
            for egoaction in ego_actions:
                action = egoaction.get("Action")
                if action:
                    try:
                        self.register_dispatch.dispatch(action, all_ego_events)
                    except KeyError:
                        # Handle specific exception if the action is not found in the dispatcher
                        continue
                    except Exception as e:
                        # Log the exception if needed
                        print(f"Error dispatching action {action}: {e}")
                        continue

    def initial_acceleration(self, all_ego_events):
        # initial Acceleration act
        self.EGO_algo_acts.ego_accelration_act(all_ego_events)

    # def dri_setlongitudinalspeed(self,all_ego_events):
    #     # speed
    #     self.EGO_algo_acts.ego_accelration_act(all_ego_events)
    def throttle_acts(self, all_ego_events):
        # Ego Throttle act
        self.EGO_algo_acts.ego_throttle_act(all_ego_events)

    def brake_acts(self, all_ego_events):
        # Ego brake act
        self.EGO_algo_acts.ego_brake_act(all_ego_events)

    def dri_setLateralDisplacement(self, all_ego_events):
        # dri_setLateralDisplacement
        self.EGO_algo_acts.ego_Dri_SetLateralDisplacement(all_ego_events)

    def ego_E_DistanceTimeBased(self, all_ego_events):
        self.EGO_algo_acts.ego_E_DistanceTimeBased(all_ego_events)

    # def dri_setLateralReference(self,all_ego_events):
    #     self.EGO_algo_acts.ego_Dri_SetLateralReference(all_ego_events)

    def ego_ObjectDistanceLaneBased(self, all_ego_events):
        # E_ObjectDistanceLaneBased
        self.EGO_algo_acts.ego_E_ObjectDistanceLaneBased(all_ego_events)

    def ego_ObjectCollision(self, all_ego_events):
        # E_ObjectCollision
        self.EGO_algo_acts.ego_E_ObjectCollision(all_ego_events)

    def ego_dri_SwitchGear(self, all_ego_events):
        # Dri_SwitchGear
        self.EGO_algo_acts.ego_Dri_SwitchGear(all_ego_events)

    def ego_dri_SetVehicleDoor(self, all_ego_events):
        # Dri_SetVehicleDoor
        self.EGO_algo_acts.ego_Dri_SetVehicleDoor(all_ego_events)

    def ego_dri_SetVehicleDoor(self,all_ego_events):
        self.EGO_algo_acts.ego_Dri_SetVehicleDoor(all_ego_events)

    def ego_dri_SetParkingBrake(self, all_ego_events):
        # Dri_SetParkingBrake
        self.EGO_algo_acts.ego_Dri_SetParkingBrake(all_ego_events)

    def ego_dri_SetSteeringWheelAngle(self, all_ego_events):
        # Dri_SetSteeringWheelAngle
        self.EGO_algo_acts.ego_Dri_SetSteeringWheelAngle(all_ego_events)

    def ego_SetTrafficLightState(self, all_ego_events):
        # Env_SetTrafficLightState
        self.EGO_algo_acts.ego_Env_SetTrafficLightState(all_ego_events)

    def ego_E_ADASState(self, all_ego_events):
        self.EGO_algo_acts.ego_E_ADASState(all_ego_events)

    def E_sysvehiclevelocity(self, all_ego_events):
        self.EGO_algo_acts.ego_E_SysVehicleVelocity(all_ego_events)

    def dri_setIndicatorState(self,all_ego_events):
        self.EGO_algo_acts.Dri_SetIndicatorState(all_ego_events)






