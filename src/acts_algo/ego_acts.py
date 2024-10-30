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

MAIN_PATH = os.path.abspath(os.path.join(__file__, "..", "..", "..", ".."))
CURRENT_WORKING_FILE_DIRECTORY = os.path.abspath(os.path.join(__file__))
CURRENT_WORKING_DIRECTORY = os.path.abspath(os.path.join(__file__, ".."))

if MAIN_PATH not in sys.path:
    sys.path.append(MAIN_PATH)

dir_path = os.path.dirname(os.path.realpath(__file__))
for root, dirs, files in os.walk(dir_path):
    sys.path.append(root)


class Ego_Acts:
    def __init__(self, egoname, states_analysis, paramlist_analysis, state_events, param_events, esmini_path):
        self.states_analysis = states_analysis
        self.paramlist_analysis = paramlist_analysis
        self.state_events = state_events
        self.param_events = param_events
        self.esmini_path = esmini_path
        self.egoname = egoname
        self.open_scenario_version = 0
        # self.last_processed_index = -1
        # self.last_processed_index1 = -1

        # self.ego_speed, self.obj_speed, self.ego_transition_time, self.obj_transition_time = EBTB_API_data.get_ego_obj_speed_transition_time(
        #     states_analysis=self.states_analysis)
        self.ego_speed, self.ego_transition_time = EBTB_API_data.get_ego_speed_transition_time(states_analysis=self.states_analysis)
        self.VehicleControls = vehiclecontrol()
        self.Data_Controls = datacontrol()
        self.VehicleDefines = VehicleScenario()

        self.TBA_value = EBTB_API_data.get_TBA_key_value(states_analysis=self.states_analysis)
        self.throttle = EBTB_API_data.get_vehicle_throttle_info(TBA_eval_key=self.TBA_value,
                                                                states_analysis=self.states_analysis)
        self.brake = EBTB_API_data.get_vehicle_braking_info(TBA_eval_key=self.TBA_value,
                                                            states_analysis=self.states_analysis)


    def ego_accelration_act(self, all_ego_events):
        trigger_created = False
        for state,value in self.states_analysis.items():
            ego_actions = value.get('EgoActions', [])
            for action in ego_actions:
                if action.get('Action', []) == "Dri_SetLongitudinalSpeed":
                    all_actions = value.get('EgoActions')
                    acts = [item['Action'] for item in all_actions]
                    if "E_SysVehicleVelocity" in acts:
                        sys_vehicle_velocity_event = self.state_events.get(OtherAPI.E_SysVehicleVelocity)

                        if sys_vehicle_velocity_event:
                            velocity_value = sys_vehicle_velocity_event.get("Velocity")
                            operator = sys_vehicle_velocity_event.get("Operator")
                            self.start_trig_throttle = self.VehicleDefines.create_speed_condition_trigger(
                                operator, self.egoname, speed=velocity_value
                            )
                            trigger_created = True

                    elif "E_ObjectDistanceLaneBased" in acts:
                        object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)

                        if object_distance_event:
                            distance_value = object_distance_event.get("Distance")
                            relational_operator = object_distance_event.get("RelationalOperator")
                            reference_object = object_distance_event.get("ReferenceObject")
                            object_id = object_distance_event.get("ObjectID")
                            self.start_trig_throttle = self.VehicleDefines.create_relative_distance_condition_trigger(
                                distance_value, relational_operator, reference_object, object_id)
                            trigger_created = True

                    elif "E_TimeToCollision" in acts:
                        time_to_collision_event = self.state_events.get(OtherAPI.E_TimeToCollision)

                        if time_to_collision_event:
                            reference_time_value = time_to_collision_event.get("ReferenceTime")
                            self.start_trig_throttle = self.VehicleDefines.add_time_to_collision_start_trigger(
                                value=float(reference_time_value))
                            trigger_created = True

                    else:
                        self.start_trig_throttle = self.VehicleDefines.create_ego_event(value=15)
                        trigger_created = True

                    if trigger_created:
                        break  # Exit inner loop

            if trigger_created:
                break  # Exit outer loop
        start_action = self.VehicleDefines.ego_acceleration_actions(self.ego_speed,
                                                                    self.ego_transition_time,
                                                                    state_data=self.states_analysis,
                                                                    param_data=self.paramlist_analysis)
        all_ego_events.append(
            self.VehicleDefines.define_ego_action_event(start_trig=self.start_trig_throttle, start_action=start_action))

        # sys_vehicle_velocity_event = self.state_events.get(OtherAPI.E_SysVehicleVelocity)
        #
        # if sys_vehicle_velocity_event:
        #
        #     velocity_value = sys_vehicle_velocity_event.get("Velocity")
        #     print("velocity",velocity_value)
        #     operator = sys_vehicle_velocity_event.get("Operator")
        #     start_trig_throttle = self.VehicleDefines.create_speed_condition_trigger(operator, self.egoname,
        #                                                                     speed=velocity_value)
        #
        # # object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)
        # # if object_distance_event:
        # #     distance_value = object_distance_event.get("Distance")
        # #     relational_operator = object_distance_event.get("RelationalOperator")
        # #     reference_object = object_distance_event.get("ReferenceObject")
        # #     object_id = object_distance_event.get("ObjectID")
        # #     if distance_value is not None:
        # #         start_trig_throttle = self.VehicleDefines.create_relative_distance_condition_trigger(
        # #             distance_value, relational_operator,reference_object,object_id)
        #
        # if not (sys_vehicle_velocity_event):
        #     start_trig_throttle = self.VehicleDefines.create_ego_event(value=10)
        # # start_trig_throttle = self.VehicleDefines.create_ego_event(value=10)
        # start_action = self.VehicleDefines.ego_acceleration_actions(self.ego_speed,
        #                                                             self.ego_transition_time,
        #                                                             state_data=self.states_analysis,
        #                                                             param_data=self.paramlist_analysis)
        # all_ego_events.append(
        #     self.VehicleDefines.define_ego_action_event(start_trig=start_trig_throttle, start_action=start_action))

    def ego_E_SysVehicleVelocity(self, all_ego_events):
        pass

    def ego_throttle_act(self, all_ego_events):
        global value_throttle

        if not hasattr(self, 'start_trig_throttle'):
            self.start_trig_throtle = 0

        if not hasattr(self, 'last_processed_index'):
            self.last_processed_index1 = 0

            trigger_created = False  # Flag to indicate trigger creation
            keys = list(self.states_analysis.keys())  # Convert keys to a list for indexed access

            # Loop starting from last processed index
            for i in range(self.last_processed_index1, len(keys)):
                key = keys[i]
                value = self.states_analysis[key]

                ego_actions = value.get('EgoActions', [])
                for action in ego_actions:
                    if action.get('Action', []) == "Dri_SetAccelerationPedal":
                        throttle_value = self.throttle["Throttle"]
                        all_actions = value.get('EgoActions')
                        acts = [item['Action'] for item in all_actions]
                        param = action.get('Parameters')
                        value_throttle = (param[0]['Position'])

                        if "E_SysVehicleVelocity" in acts:
                            sys_vehicle_velocity_event = self.state_events.get(OtherAPI.E_SysVehicleVelocity)

                            if sys_vehicle_velocity_event:
                                velocity_value = sys_vehicle_velocity_event.get("Velocity")
                                operator = sys_vehicle_velocity_event.get("Operator")
                                self.start_trig_brake = self.VehicleDefines.create_speed_condition_trigger(
                                    operator, self.egoname, speed=velocity_value
                                )
                                trigger_created = True

                        elif "E_TimeToCollision" in acts:
                            time_to_collision_event = self.state_events.get(OtherAPI.E_TimeToCollision)
                            if time_to_collision_event:
                                reference_time_value = time_to_collision_event.get("ReferenceTime")
                                self.start_trig_throttle = self.VehicleDefines.add_time_to_collision_start_trigger(
                                    value=float(reference_time_value))
                                trigger_created = True

                        else:
                            self.start_trig_throttle = self.VehicleDefines.create_ego_event(value=40)
                            trigger_created = True

                        if trigger_created:
                            # Update the last processed index and break out of both loops
                            self.last_processed_index1 = i + 1
                            break  # Exit inner loop

                if trigger_created:
                    break  # Exit outer loop
        start_action = self.VehicleDefines.create_controller_override_action(throttle=value_throttle,
                                                                             brake=0, clutch=0, parkingbrake=0,
                                                                             steeringwheel=0, gear=0)

        all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=self.start_trig_throttle,
                                                                          start_action=start_action))

    # if self.throttle["Throttle"] != -1:
            # Initialize last_processed_index if it doesn’t exist



        # if self.throttle["Throttle"] != -1:
        #     # Handle "E_ObjectDistanceLaneBased" event
        #     object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)
        #     if object_distance_event:
        #         distance_value = object_distance_event.get("Distance")
        #         relational_operator = object_distance_event.get("RelationalOperator")
        #         reference_object = object_distance_event.get("ReferenceObject")
        #         object_id = object_distance_event.get("ObjectID")
        #         if distance_value is not None:
        #             start_trig_throttle = self.VehicleDefines.create_relative_distance_condition_trigger(
        #                 distance_value, relational_operator, reference_object,object_id)
        #
        #     # Handle "E_TimeToCollision" event
        #     time_to_collision_event = self.state_events.get(OtherAPI.E_TimeToCollision)
        #     if time_to_collision_event:
        #         reference_time_value = time_to_collision_event.get("ReferenceTime")
        #         if reference_time_value is not None:
        #             start_trig_throttle = self.VehicleDefines.add_time_to_collision_start_trigger(
        #                 value=float(reference_time_value))
        #
        #     # Assuming you want to create an ego event if neither of the specific events are found
        #     if not (object_distance_event or time_to_collision_event):
        #         start_trig_throttle = self.VehicleDefines.create_ego_event(value=40)



    def ego_brake_act(self, all_ego_events):
        global value_break
        if not hasattr(self, 'start_trig_brake'):
            self.start_trig_brake = 0

        if not hasattr(self, 'last_processed_index'):
            self.last_processed_index = 0

        trigger_created = False  # Flag to indicate trigger creation
        keys = list(self.states_analysis.keys())  # Convert keys to a list for indexed access

        # Loop starting from last processed index
        for i in range(self.last_processed_index, len(keys)):
            key = keys[i]
            value = self.states_analysis[key]

            ego_actions = value.get('EgoActions', [])
            for action in ego_actions:
                if action.get('Action', []) == "Dri_SetBrakePedal":
                    all_actions = value.get('EgoActions')
                    acts = [item['Action'] for item in all_actions]
                    param = action.get('Parameters')
                    value_break = (param[0]['Position'])

                    if "E_SysVehicleVelocity" in acts:
                        sys_vehicle_velocity_event = self.state_events.get(OtherAPI.E_SysVehicleVelocity)

                        if sys_vehicle_velocity_event:
                            velocity_value = sys_vehicle_velocity_event.get("Velocity")
                            operator = sys_vehicle_velocity_event.get("Operator")
                            self.start_trig_brake = self.VehicleDefines.create_speed_condition_trigger(
                                operator, self.egoname, speed=velocity_value
                            )
                            trigger_created = True
                    else:
                        self.start_trig_brake = self.VehicleDefines.create_ego_event(value=40)
                        trigger_created = True

                    if trigger_created:
                        # Update the last processed index and break out of both loops
                        self.last_processed_index = i + 1
                        break  # Exit inner loop

            if trigger_created:
                break  # Exit outer loop

        start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
                                                                         brake=value_break,
                                                                         clutch=0, parkingbrake=0,
                                                                         steeringwheel=0, gear=0)

        all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=self.start_trig_brake,
                                                                      start_action=start_action))

        # if self.brake["Brake"] != -1:
        #     print(self.brake["Brake"])
            # Initialize last_processed_index if it doesn’t exist




        # if self.brake["Brake"] != -1:
        #     self.start_trig_brake = 0
        #     trigger_created = False
        #
        # for key,value in self.states_analysis.items():
        #     ego_actions = value.get('EgoActions', [])
        #     for action in ego_actions:
        #         if action.get('Action', []) == "Dri_SetBrakePedal":
        #             print("enter brake ego acts")
        #             all_actions = value.get('EgoActions')
        #             acts = [item['Action'] for item in all_actions]
        #             if "E_SysVehicleVelocity" in acts:
        #                 print("enter sys velocity")
        #                 sys_vehicle_velocity_event = self.state_events.get(OtherAPI.E_SysVehicleVelocity)
        #
        #                 if sys_vehicle_velocity_event:
        #                     velocity_value = sys_vehicle_velocity_event.get("Velocity")
        #                     operator = sys_vehicle_velocity_event.get("Operator")
        #                     self.start_trig_brake = self.VehicleDefines.create_speed_condition_trigger(
        #                         operator, self.egoname, speed=velocity_value
        #                     )
        #                     trigger_created = True
        #             else:
        #                 self.start_trig_brake = self.VehicleDefines.create_ego_event(value=40)
        #                 trigger_created = True



        # # Initialize start_trig_brake if it doesn’t exist, so it retains the last value
        # if not hasattr(self, 'start_trig_brake'):
        #     print("init")
        #     self.start_trig_brake = 0
        #
        # if self.brake["Brake"] != -1:
        #     print("selfbrake")
        #     # Initialize last_processed_index if it doesn’t exist
        #     if not hasattr(self, 'last_processed_index'):
        #         print("last_proc_index")
        #         self.last_processed_index = 0
        #
        #     trigger_created = False  # Flag to indicate trigger creation
        #     keys = list(self.states_analysis.keys())  # Convert keys to a list for indexed access
        #
        #     # Loop starting from last processed index
        #     for i in range(self.last_processed_index, len(keys)):
        #         print("loop")
        #         key = keys[i]
        #         value = self.states_analysis[key]
        #
        #         ego_actions = value.get('EgoActions', [])
        #         for action in ego_actions:
        #             if action.get('Action', []) == "Dri_SetBrakePedal":
        #                 print("enter brake ego acts")
        #                 all_actions = value.get('EgoActions')
        #                 acts = [item['Action'] for item in all_actions]
        #                 if "E_SysVehicleVelocity" in acts:
        #                     print("enter sys velocity")
        #                     sys_vehicle_velocity_event = self.state_events.get(OtherAPI.E_SysVehicleVelocity)
        #
        #                     if sys_vehicle_velocity_event:
        #                         velocity_value = sys_vehicle_velocity_event.get("Velocity")
        #                         operator = sys_vehicle_velocity_event.get("Operator")
        #                         self.start_trig_brake = self.VehicleDefines.create_speed_condition_trigger(
        #                             operator, self.egoname, speed=velocity_value
        #                         )
        #                         trigger_created = True
        #                 else:
        #                     self.start_trig_brake = self.VehicleDefines.create_ego_event(value=40)
        #                     trigger_created = True
        #
        #                 if trigger_created:
        #                     # Update the last processed index and break out of both loops
        #                     self.last_processed_index = i + 1
        #                     break  # Exit inner loop
        #
        #         if trigger_created:
        #             break  # Exit outer loop



            # def ego_brake_act(self, all_ego_events):
    #     if self.brake["Brake"] != -1:
    #         start_trig_brake = 0
    #
    #         trigger_created = False  # Flag to indicate trigger creation
    #
    #         for key, value in self.states_analysis.items():
    #             if trigger_created:
    #                 break  # Exit outer loop if trigger is created
    #             ego_actions = value.get('EgoActions', [])
    #             for action in ego_actions:
    #                 if action.get('Action', []) == "Dri_SetBrakePedal":
    #                     print("key val", key)
    #                     all_actions = value.get('EgoActions')
    #                     acts = [item['Action'] for item in all_actions]
    #                     print(acts)
    #                     if "E_SysVehicleVelocity" in acts:
    #                         sys_vehicle_velocity_event = self.state_events.get(OtherAPI.E_SysVehicleVelocity)
    #
    #                         if sys_vehicle_velocity_event:
    #                             velocity_value = sys_vehicle_velocity_event.get("Velocity")
    #                             operator = sys_vehicle_velocity_event.get("Operator")
    #                             start_trig_brake = self.VehicleDefines.create_speed_condition_trigger(
    #                                 operator, self.egoname, speed=velocity_value
    #                             )
    #                             trigger_created = True
    #                             break  # Exit inner loop
    #                     else:
    #                         start_trig_brake = self.VehicleDefines.create_ego_event(value=40)
    #                         trigger_created = True
    #                         break  # Exit inner loop

            # for key, value in self.states_analysis.items():
            #     ego_actions = value.get('EgoActions', [])
            #     for action in ego_actions:
            #         if action.get('Action', []) == "Dri_SetBrakePedal":
            #             print("key val",key)
            #             all_actions = value.get('EgoActions')
            #             acts = [item['Action'] for item in all_actions]
            #             print(acts)
            #             if "E_SysVehicleVelocity" in acts:
            #                 sys_vehicle_velocity_event = self.state_events.get(OtherAPI.E_SysVehicleVelocity)
            #
            #                 if sys_vehicle_velocity_event:
            #                     velocity_value = sys_vehicle_velocity_event.get("Velocity")
            #                     operator = sys_vehicle_velocity_event.get("Operator")
            #                     start_trig_brake = self.VehicleDefines.create_speed_condition_trigger(operator, self.egoname,
            #                                                                                              speed=velocity_value)
            #             else:
            #                 start_trig_brake = self.VehicleDefines.create_ego_event(value=40)


            # object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)
            # if object_distance_event:
            #     distance_value = object_distance_event.get("Distance")
            #     relational_operator = object_distance_event.get("RelationalOperator")
            #     reference_object = object_distance_event.get("ReferenceObject")
            #     object_id = object_distance_event.get("ObjectID")
            #     if distance_value is not None:
            #         start_trig_brake = self.VehicleDefines.create_relative_distance_condition_trigger(
            #             distance_value, relational_operator, reference_object,object_id)
            #
            # # Handle "E_TimeToCollision" event
            # time_to_collision_event = self.state_events.get(OtherAPI.E_TimeToCollision)
            # if time_to_collision_event:
            #     reference_time_value = time_to_collision_event.get("ReferenceTime")
            #     if reference_time_value is not None:
            #         start_trig_brake = self.VehicleDefines.add_time_to_collision_start_trigger(
            #             value=float(reference_time_value))
            #
            # # Assuming you want to create an ego event if neither of the specific events are found
            # if not (object_distance_event or time_to_collision_event):
            #     start_trig_brake = self.VehicleDefines.create_ego_event(value=40)



    def ego_Dri_SetLateralDisplacement(self, all_ego_events):
        for key, value in self.states_analysis.items():
            ego_actions = value.get('EgoActions', [])
            for action in ego_actions:
                if action.get('Action', []) == "Dri_SetLateralDisplacement":
                    parameters = action.get('Parameters', [])
                    dispvalue=parameters[0]["TargetDisplacement"]

        start_trig = self.VehicleDefines.create_ego_event(value=5)
        start_action = self.VehicleDefines.create_lateral_distance_action(value=dispvalue)
        all_ego_events.append(
             self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))

    def ego_Dri_SetLateralReference(self, all_ego_events):
        for key, value in self.states_analysis.items():
            ego_actions = value.get('EgoActions', [])
            for action in ego_actions:
                if action.get('Action', []) == "Dri_SetLateralReference":
                    parameters = action.get('Parameters', [])
                    lane_value_str = parameters[0]["LaneSelection"]
                    lane = self.VehicleControls.split_string(lane_value_str)
                    if lane[0] == "Right":
                        lane_value = self.VehicleControls.right_position(lane[1])
                    elif lane[0] == "Left":
                        lane_value = self.VehicleControls.left_position(lane[1])

        start_trig = self.VehicleDefines.create_ego_event(value=5)
        start_action = self.VehicleDefines.create_lateral_reference_action(lane=lane_value)
        all_ego_events.append(
            self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))

    def ego_E_ObjectDistanceLaneBased(self, all_ego_events):
        object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)
        if object_distance_event:
            distance_value = object_distance_event.get("Distance")
            relational_operator = object_distance_event.get("RelationalOperator")
            reference_object = object_distance_event.get("ReferenceObject")
            object_id = object_distance_event.get("ObjectID")
            if distance_value is not None:
                start_trig = self.VehicleDefines.create_relative_distance_condition_trigger(
                    distance_value, relational_operator, reference_object, object_id)

        start_action = self.VehicleDefines.create_custom_command_action("userdef")

        all_ego_events.append(
            self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))


    def Dri_SetIndicatorState(self,all_ego_events):
        for key, value in self.states_analysis.items():
            ego_actions = value.get('EgoActions', [])
            for action in ego_actions:
                if action.get('Action', []) == "Dri_SetIndicatorState":
                    parameters = action.get('Parameters', [])
                    State_Indicator = parameters[0]["State"]
                    State_Duration = parameters[0]["Duration"]

        start_trig = self.VehicleDefines.create_ego_event(value=3)
        if State_Indicator == "Left":
            start_action = self.VehicleDefines.create_set_indicator_state(State_Indicator="indicatorLeft",State_Duration=State_Duration)
        elif State_Indicator == "Right":
            start_action = self.VehicleDefines.create_set_indicator_state(State_Indicator="indicatorRight",State_Duration=State_Duration)
        all_ego_events.append(
            self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))

    def ego_E_ObjectCollision(self, all_ego_events):
        pass

    def ego_Dri_SwitchGear(self, all_ego_events):
        for key, value in self.states_analysis.items():
            ego_actions = value.get('EgoActions', [])
            for action in ego_actions:
                if action.get('Action', []) == "Dri_SwitchGear":
                    parameters = action.get('Parameters', [])
                    gear_value = parameters[0]["Position"]

        start_trig = self.VehicleDefines.create_ego_event(value=5)
        if gear_value == "D":
            start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
                                                                                 brake=0, clutch=0, parkingbrake=0,
                                                                                 steeringwheel=0, gear=1)
        elif gear_value == "R":
            start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
                                                                                 brake=0, clutch=0, parkingbrake=0,
                                                                                 steeringwheel=0, gear=2)
        elif gear_value == "N":
            start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
                                                                                 brake=0, clutch=0, parkingbrake=0,
                                                                                 steeringwheel=0, gear=0)
        elif gear_value == "P":
            start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
                                                                                 brake=0, clutch=0, parkingbrake=1,
                                                                                 steeringwheel=0, gear=0)
        all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig,
                                                                          start_action=start_action))

    def ego_Dri_SetVehicleDoor(self, all_ego_events):
        for key, value in self.states_analysis.items():
            ego_actions = value.get('EgoActions', [])
            for action in ego_actions:
                if action.get('Action', []) == "Dri_SetVehicleDoor":
                    parameters = action.get('Parameters', [])
                    vehicle_door_value = parameters[0]["Door"]
                    vehicle_door_state_value = parameters[0]["State"]
        start_trig = self.VehicleDefines.create_ego_event(value=3)
        start_action = self.VehicleDefines.create_setVehicleDoor(vehicle_door_value,vehicle_door_state_value)
        all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig,
                                                                          start_action=start_action))

    def ego_E_DistanceTimeBased(self, all_ego_events):

        obj_distance_time_event = self.state_events.get(OtherAPI.E_DistanceTimeBased)
        if obj_distance_time_event:
            dist_value = obj_distance_time_event.get("Offset")
            relational_operator = obj_distance_time_event.get("RelationalOperator")
            reference_object = obj_distance_time_event.get("ReferenceObject")
            object = obj_distance_time_event.get("Object")
            start_trig = self.VehicleDefines.create_time_headway_condition_trigger(
                dist_value, relational_operator, object, reference_object)

        start_action = self.VehicleDefines.create_custom_command_action(custom_command="userdef")

        all_ego_events.append(
            self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))
    def ego_Dri_SetParkingBrake(self, all_ego_events):

        for key, value in self.states_analysis.items():
            ego_actions = value.get('EgoActions', [])
            for action in ego_actions:
                if action.get('Action', []) == "Dri_SetParkingBrake":
                    parameters = action.get('Parameters', [])
                    brake_value = parameters[0]["State"]

        start_trig_parkingbrake = 0
        # object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)
        # if object_distance_event:
        #     distance_value = object_distance_event.get("Distance")
        #     relational_operator = object_distance_event.get("RelationalOperator")
        #     reference_object = object_distance_event.get("ReferenceObject")
        #     object_id = object_distance_event.get("ObjectID")
        #     if distance_value is not None:
        #         start_trig_parkingbrake = self.VehicleDefines.create_relative_distance_condition_trigger(
        #             distance_value, relational_operator, reference_object,object_id)
        #
        #
        #
        # # Handle "E_TimeToCollision" event
        # time_to_collision_event = self.state_events.get(OtherAPI.E_TimeToCollision)
        # if time_to_collision_event:
        #     reference_time_value = time_to_collision_event.get("ReferenceTime")
        #     if reference_time_value is not None:
        #         start_trig_parkingbrake = self.VehicleDefines.add_time_to_collision_start_trigger(
        #             value=float(reference_time_value))

        # Assuming you want to create an ego event if neither of the specific events are found
        #if not (object_distance_event or time_to_collision_event):
        start_trig_parkingbrake = self.VehicleDefines.create_ego_event(value=5)

        if brake_value == "Engage":
            start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
                                                                                 brake=0, clutch=0, parkingbrake=1,
                                                                                 steeringwheel=0, gear=0)
        elif brake_value == "Release":
            start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
                                                                                 brake=0, clutch=0, parkingbrake=0,
                                                                                 steeringwheel=0, gear=0)



        all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig_parkingbrake,
                                                                          start_action=start_action))

    def ego_Dri_SetSteeringWheelAngle(self, all_ego_events):
        for key, value in self.states_analysis.items():
            ego_actions = value.get('EgoActions', [])
            for action in ego_actions:
                if action.get('Action', []) == "Dri_SetSteeringWheelAngle":
                    parameters = action.get('Parameters', [])
                    wheel_angle_value=parameters[0]["Angle"]

        start_trig_steeringwheel = 0

        # # Handle "E_TimeToCollision" event
        # time_to_collision_event = self.state_events.get(OtherAPI.E_TimeToCollision)
        # if time_to_collision_event:
        #     reference_time_value = time_to_collision_event.get("ReferenceTime")
        #     if reference_time_value is not None:
        #         start_trig_steeringwheel  = self.VehicleDefines.add_time_to_collision_start_trigger(
        #             value=float(reference_time_value))

        # Assuming you want to create an ego event if neither of the specific events are found
        # if not time_to_collision_event:
        start_trig_steeringwheel  = self.VehicleDefines.create_ego_event(value=5)

        start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
                                                                             brake=0, clutch=0, parkingbrake=0,
                                                                             steeringwheel=wheel_angle_value, gear=0)
        all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig_steeringwheel ,
                                                                          start_action=start_action))

    def ego_Env_SetTrafficLightState(self, all_ego_events):
        pass

    def ego_E_ADASState(self, all_ego_events):
        keys_to_print = []
        for key, value in self.states_analysis.items():
            ego_actions = value.get('EgoActions', [])
            for action in ego_actions:
                if action.get('Action', []) == "E_ADASState":
                    parameters = action.get('Parameters', [])
                    keys = (int(key)) + 1
                    keys_to_print.append(keys)
        print(keys)

        for key in self.states_analysis:
            if (int(key)) in keys_to_print:
                keys_str = str(keys)
                next_value = self.states_analysis[keys_str]
                next_ego_actions = next_value.get('EgoActions', [])
                if next_ego_actions:  # Ensure next_ego_actions is not empty
                    first_next_action = next_ego_actions[0]  # Get the first action
                    print(first_next_action.get('Action'))


        adasstate_event = self.state_events.get(OtherAPI.E_ADASState)
        cms_visual_warning = adasstate_event.get("CMSVisualWarning")
        acceleration_request = adasstate_event.get("ADASVehicleAccelerationRequest")

        if (cms_visual_warning or acceleration_request):
            if("Dri_SetAccelerationPedal" == first_next_action.get('Action')):
                start_trig_throttle = self.VehicleDefines.add_time_to_collision_start_trigger(
                    value=float(4))

                start_action = self.VehicleDefines.create_controller_override_action(
                    throttle=self.throttle["Throttle"],
                    brake=0, clutch=0, parkingbrake=0,
                    steeringwheel=0, gear=0)
                all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig_throttle,
                                                                                  start_action=start_action))

            elif("Dri_SetBrakePedal" == first_next_action.get('Action')):
                start_trig_brake = self.VehicleDefines.add_time_to_collision_start_trigger(
                    value=float(4))
                start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
                                                                                     brake=self.brake["Brake"],
                                                                                     clutch=0, parkingbrake=0,
                                                                                     steeringwheel=0, gear=0)

                all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig_brake,
                                                                                  start_action=start_action))

            elif("Dri_SetLateralDisplacement" == first_next_action.get('Action')):
                start_trig = self.VehicleDefines.add_time_to_collision_start_trigger(
                            value=float(4))
                start_action = self.VehicleDefines.create_lateral_distance_action(lane_offset=0)
                all_ego_events.append(
                    self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))

            else:
                pass


# import os
# import sys
#
# from sphinx.environment.adapters.toctree import ET
# from e2xostream.config.api_constants import api_methods_constants as AMC
#
# from e2xostream.stk.scenariogeneration import xosc, prettyprint, ScenarioGenerator
# from e2xostream.stk.vehicledynamics.VehicleControl import VehicleControlMovements as vehiclecontrol
# from e2xostream.stk.vehicledynamics.DataControl import DataControls as datacontrol
# from e2xostream.stk.vehicledynamics.VehicleScenarioSetup import VehicleScenario
# from e2xostream.src.vehiclestream.ebtb_stream import EBTBAnalyzer, EBTB_API_data
# from e2xostream.config import default_properties, global_parameters, settings
# from e2xostream.config.api_constants import (api_methods_constants as ApiMethods,
#                                              ego_api_constants as EgoAPI,
#                                              obj_api_constants as ObjAPI,
#                                              other_api_constants as OtherAPI)
# from e2xostream.src.scenario_generator import basescenario as BS
#
# MAIN_PATH = os.path.abspath(os.path.join(__file__, "..", "..", "..", ".."))
# CURRENT_WORKING_FILE_DIRECTORY = os.path.abspath(os.path.join(__file__))
# CURRENT_WORKING_DIRECTORY = os.path.abspath(os.path.join(__file__, ".."))
#
# if MAIN_PATH not in sys.path:
#     sys.path.append(MAIN_PATH)
#
# dir_path = os.path.dirname(os.path.realpath(__file__))
# for root, dirs, files in os.walk(dir_path):
#     sys.path.append(root)
#
#
# class Ego_Acts:
#     def __init__(self, egoname, states_analysis, paramlist_analysis, state_events, param_events, esmini_path):
#         self.states_analysis = states_analysis
#         self.paramlist_analysis = paramlist_analysis
#         self.state_events = state_events
#         self.param_events = param_events
#         self.esmini_path = esmini_path
#         self.egoname = egoname
#         self.open_scenario_version = 0
#
#         # self.ego_speed, self.obj_speed, self.ego_transition_time, self.obj_transition_time = EBTB_API_data.get_ego_obj_speed_transition_time(
#         #     states_analysis=self.states_analysis)
#         self.ego_speed,self.ego_transition_time = EBTB_API_data.get_ego_speed_transition_time(states_analysis=self.states_analysis)
#
#         self.VehicleControls = vehiclecontrol()
#         self.Data_Controls = datacontrol()
#         self.VehicleDefines = VehicleScenario()
#
#         self.TBA_value = EBTB_API_data.get_TBA_key_value(states_analysis=self.states_analysis)
#         self.throttle = EBTB_API_data.get_vehicle_throttle_info(TBA_eval_key=self.TBA_value,
#                                                                 states_analysis=self.states_analysis)
#         self.brake = EBTB_API_data.get_vehicle_braking_info(TBA_eval_key=self.TBA_value,
#                                                             states_analysis=self.states_analysis)
#
#     def ego_accelration_act(self, all_ego_events):
#
#         sys_vehicle_velocity_event = self.state_events.get(OtherAPI.E_SysVehicleVelocity)
#         if sys_vehicle_velocity_event:
#             velocity_value = sys_vehicle_velocity_event.get("Velocity")
#             operator = sys_vehicle_velocity_event.get("Operator")
#             start_trig = self.VehicleDefines.create_speed_condition_trigger(operator, self.egoname, speed=velocity_value)
#
#         object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)
#         if object_distance_event:
#             distance_value = object_distance_event.get("Distance")
#             relational_operator = object_distance_event.get("RelationalOperator")
#             reference_object = object_distance_event.get("ReferenceObject")
#             if distance_value is not None:
#                 start_trig = self.VehicleDefines.create_relative_distance_condition_trigger(
#                     distance=distance_value, relational_operator=relational_operator,
#                     reference_object=reference_object)
#
#         if not (object_distance_event or sys_vehicle_velocity_event):
#             start_trig_throttle = self.VehicleDefines.create_ego_event(value=10)
#
#
#         start_action = self.VehicleDefines.ego_acceleration_actions(self.ego_speed,
#                                                                 self.ego_transition_time,
#                                                                 state_data=self.states_analysis,
#                                                                 param_data=self.paramlist_analysis)
#         all_ego_events.append(
#             self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))
#
#
#
#     def ego_throttle_act(self, all_ego_events):
#         if self.throttle["Throttle"] != -1:
#             # Handle "E_ObjectDistanceLaneBased" event
#             start_trig_throttle = 0
#
#             object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)
#             if object_distance_event:
#                 distance_value = object_distance_event.get("Distance")
#                 relational_operator = object_distance_event.get("RelationalOperator")
#                 reference_object = object_distance_event.get("ReferenceObject")
#                 if distance_value is not None:
#                     start_trig_throttle = self.VehicleDefines.create_relative_distance_condition_trigger(
#                         distance=distance_value,relational_operator=relational_operator,
#                         reference_object=reference_object)
#
#             # Handle "E_TimeToCollision" event
#             time_to_collision_event = self.state_events.get(OtherAPI.E_TimeToCollision)
#             if time_to_collision_event:
#                 reference_time_value = time_to_collision_event.get("ReferenceTime")
#                 if reference_time_value is not None:
#                     start_trig_throttle = self.VehicleDefines.add_time_to_collision_start_trigger(
#                         value=float(reference_time_value))
#
#             # Assuming you want to create an ego event if neither of the specific events are found
#             if not (object_distance_event or time_to_collision_event):
#                 start_trig_throttle = self.VehicleDefines.create_ego_event(value=40)
#
#
#             start_action = self.VehicleDefines.create_controller_override_action(throttle=self.throttle["Throttle"],
#                                                                                  brake=0, clutch=0, parkingbrake=0,
#                                                                                  steeringwheel=0, gear=0)
#
#             all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig_throttle,
#                                                                               start_action=start_action))
#
#     def ego_brake_act(self, all_ego_events):
#         if self.brake["Brake"] != -1:
#             # Handle "E_ObjectDistanceLaneBased" event
#             start_trig_brake = 0
#
#             object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)
#             if object_distance_event:
#                 distance_value = object_distance_event.get("Distance")
#                 relational_operator = object_distance_event.get("RelationalOperator")
#                 reference_object = object_distance_event.get("ReferenceObject")
#                 if distance_value is not None:
#                     start_trig_brake = self.VehicleDefines.create_relative_distance_condition_trigger(
#                         distance=distance_value,relational_operator=relational_operator,
#                         reference_object=reference_object)
#
#             # object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)
#             # if object_distance_event:
#             #     distance_value = object_distance_event.get("Distance")
#             #     if distance_value is not None:
#             #         start_trig_brake = self.VehicleDefines.add_distance_condition_start_trigger(
#             #             value=float(distance_value))
#
#             # Handle "E_TimeToCollision" event
#             time_to_collision_event = self.state_events.get(OtherAPI.E_TimeToCollision)
#             if time_to_collision_event:
#                 reference_time_value = time_to_collision_event.get("ReferenceTime")
#                 if reference_time_value is not None:
#                     start_trig_brake = self.VehicleDefines.add_time_to_collision_start_trigger(
#                         value=float(reference_time_value))
#
#             # Assuming you want to create an ego event if neither of the specific events are found
#             if not (object_distance_event or time_to_collision_event):
#                 start_trig_brake = self.VehicleDefines.create_ego_event(value=40)
#
#             start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
#                                                                                  brake=self.brake["Brake"], clutch=0, parkingbrake=0,
#                                                                                  steeringwheel=0, gear=0)
#
#             all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig_brake,
#                                                                               start_action=start_action))
#
#
#     def ego_Dri_SetLateralDisplacement(self, all_ego_events):
#         for key, value in self.states_analysis.items():
#             ego_actions = value.get('EgoActions', [])
#             for action in ego_actions:
#                 if action.get('Action', []) == "Dri_SetLateralDisplacement":
#                     parameters = action.get('Parameters', [])
#                     dispvalue=parameters[0]["TargetDisplacement"]
#
#         start_trig = self.VehicleDefines.create_ego_event(value=3)
#         start_action = self.VehicleDefines.create_lateral_distance_action(value=dispvalue)
#         all_ego_events.append(
#              self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))
#
#     def ego_Dri_SetLateralReference(self, all_ego_events):
#         for key, value in self.states_analysis.items():
#             ego_actions = value.get('EgoActions', [])
#             for action in ego_actions:
#                 if action.get('Action', []) == "Dri_SetLateralReference":
#                     parameters = action.get('Parameters', [])
#                     lane_value_str = parameters[0]["LaneSelection"]
#                     lane = self.VehicleControls.split_string(lane_value_str)
#                     if lane[0] == "Right":
#                         lane_value = self.VehicleControls.right_position(lane[1])
#                     elif lane[0] == "Left":
#                         lane_value = self.VehicleControls.left_position(lane[1])
#
#         start_trig = self.VehicleDefines.create_ego_event(value=3)
#         start_action = self.VehicleDefines.create_lateral_reference_action(lane=lane_value)
#         all_ego_events.append(
#             self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))
#
#     def ego_E_ObjectDistanceLaneBased(self, all_ego_events):
#         pass
#
#     def ego_E_SysVehicleVelocity(self,all_ego_events):
#         pass
#
#     def ego_E_DistanceTimeBased(self,all_ego_events):
#         start_trig = self.VehicleDefines.create_ego_event(value=3)
#
#         obj_distance_time_event = self.state_events.get(OtherAPI.E_DistanceTimeBased)
#         if obj_distance_time_event:
#             dist_value = obj_distance_time_event.get("Offset")
#             relational_operator = obj_distance_time_event.get("RelationalOperator")
#             reference_object = obj_distance_time_event.get("ReferenceObject")
#             start_action = self.VehicleDefines.create_time_headway_condition_trigger(
#                     dist_value, relational_operator ,reference_object)
#
#         all_ego_events.append(
#             self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))
#
#     def Dri_SetIndicatorState(self,all_ego_events):
#         for key, value in self.states_analysis.items():
#             ego_actions = value.get('EgoActions', [])
#             for action in ego_actions:
#                 if action.get('Action', []) == "Dri_SetIndicatorState":
#                     parameters = action.get('Parameters', [])
#                     State_Indicator = parameters[0]["State"]
#                     State_Duration = parameters[0]["Duration"]
#
#         start_trig = self.VehicleDefines.create_ego_event(value=3)
#         if State_Indicator == "Left":
#             start_action = self.VehicleDefines.create_set_indicator_state(State_Indicator="indicatorLeft",State_Duration=State_Duration)
#         elif State_Indicator == "Right":
#             start_action = self.VehicleDefines.create_set_indicator_state(State_Indicator="indicatorRight",State_Duration=State_Duration)
#         all_ego_events.append(
#             self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))
#
#     def ego_E_ObjectCollision(self, all_ego_events):
#         pass
#
#     def ego_Dri_SwitchGear(self, all_ego_events):
#         for key, value in self.states_analysis.items():
#             ego_actions = value.get('EgoActions', [])
#             for action in ego_actions:
#                 if action.get('Action', []) == "Dri_SwitchGear":
#                     parameters = action.get('Parameters', [])
#                     gear_value = parameters[0]["Position"]
#
#         start_trig = self.VehicleDefines.create_ego_event(value=15)
#         if gear_value == "D":
#             start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
#                                                                                  brake=0, clutch=0, parkingbrake=0,
#                                                                                  steeringwheel=0, gear=1)
#         elif gear_value == "R":
#             start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
#                                                                                  brake=0, clutch=0, parkingbrake=0,
#                                                                                  steeringwheel=0, gear=2)
#         elif gear_value == "N":
#             start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
#                                                                                  brake=0, clutch=0, parkingbrake=0,
#                                                                                  steeringwheel=0, gear=0)
#
#         all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig,
#                                                                           start_action=start_action))
#
#     def ego_Dri_SetVehicleDoor(self, all_ego_events):
#         for key, value in self.states_analysis.items():
#             ego_actions = value.get('EgoActions', [])
#             for action in ego_actions:
#                 if action.get('Action', []) == "Dri_SetVehicleDoor":
#                     parameters = action.get('Parameters', [])
#                     vehicle_door_value = parameters[0]["Door"]
#                     vehicle_door_state_value = parameters[0]["State"]
#         start_trig = self.VehicleDefines.create_ego_event(value=3)
#         start_action = self.VehicleDefines.create_setVehicleDoor(vehicle_door_value,vehicle_door_state_value)
#         all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig,
#                                                                           start_action=start_action))
#
#     def ego_Dri_SetParkingBrake(self, all_ego_events):
#
#         for key, value in self.states_analysis.items():
#             ego_actions = value.get('EgoActions', [])
#             for action in ego_actions:
#                 if action.get('Action', []) == "Dri_SetParkingBrake":
#                     parameters = action.get('Parameters', [])
#                     brake_value = parameters[0]["State"]
#
#         start_trig_parkingbrake = 0
#         object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)
#         if object_distance_event:
#             distance_value = object_distance_event.get("Distance")
#             if distance_value is not None:
#                 start_trig_parkingbrake = self.VehicleDefines.add_distance_condition_start_trigger(
#                     value=float(distance_value))
#
#         # Handle "E_TimeToCollision" event
#         time_to_collision_event = self.state_events.get(OtherAPI.E_TimeToCollision)
#         if time_to_collision_event:
#             reference_time_value = time_to_collision_event.get("ReferenceTime")
#             if reference_time_value is not None:
#                 start_trig_parkingbrake = self.VehicleDefines.add_time_to_collision_start_trigger(
#                     value=float(reference_time_value))
#
#         # Assuming you want to create an ego event if neither of the specific events are found
#         if not (object_distance_event or time_to_collision_event):
#             start_trig_parkingbrake = self.VehicleDefines.create_ego_event(value=15)
#
#         if brake_value == "Engage":
#             start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
#                                                                                  brake=0, clutch=0, parkingbrake=1,
#                                                                                  steeringwheel=0, gear=0)
#         elif brake_value == "Release":
#             start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
#                                                                                  brake=0, clutch=0, parkingbrake=0,
#                                                                                  steeringwheel=0, gear=0)
#
#
#
#         all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig_parkingbrake,
#                                                                           start_action=start_action))
#
#     def ego_Dri_SetSteeringWheelAngle(self, all_ego_events):
#         for key, value in self.states_analysis.items():
#             ego_actions = value.get('EgoActions', [])
#             for action in ego_actions:
#                 if action.get('Action', []) == "Dri_SetSteeringWheelAngle":
#                     parameters = action.get('Parameters', [])
#                     wheel_angle_value=parameters[0]["Angle"]
#
#         start_trig_steeringwheel = 0
#         object_distance_event = self.state_events.get(OtherAPI.E_ObjectDistanceLaneBased)
#         if object_distance_event:
#             distance_value = object_distance_event.get("Distance")
#             if distance_value is not None:
#                 start_trig_steeringwheel  = self.VehicleDefines.add_distance_condition_start_trigger(
#                     value=float(distance_value))
#
#         # Handle "E_TimeToCollision" event
#         time_to_collision_event = self.state_events.get(OtherAPI.E_TimeToCollision)
#         if time_to_collision_event:
#             reference_time_value = time_to_collision_event.get("ReferenceTime")
#             if reference_time_value is not None:
#                 start_trig_steeringwheel  = self.VehicleDefines.add_time_to_collision_start_trigger(
#                     value=float(reference_time_value))
#
#         # Assuming you want to create an ego event if neither of the specific events are found
#         if not (object_distance_event or time_to_collision_event):
#             start_trig_steeringwheel  = self.VehicleDefines.create_ego_event(value=5)
#
#         start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
#                                                                              brake=0, clutch=0, parkingbrake=0,
#                                                                              steeringwheel=wheel_angle_value, gear=0)
#         all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig_steeringwheel ,
#                                                                           start_action=start_action))
#
#     def ego_Env_SetTrafficLightState(self, all_ego_events):
#         pass
#
#     def ego_E_ADASState(self, all_ego_events):
#         keys_to_print = []
#         for key, value in self.states_analysis.items():
#             ego_actions = value.get('EgoActions', [])
#             for action in ego_actions:
#                 if action.get('Action', []) == "E_ADASState":
#                     parameters = action.get('Parameters', [])
#                     keys = (int(key)) + 1
#                     keys_to_print.append(keys)
#         print(keys)
#
#         for key in self.states_analysis:
#             if (int(key)) in keys_to_print:
#                 keys_str = str(keys)
#                 next_value = self.states_analysis[keys_str]
#                 next_ego_actions = next_value.get('EgoActions', [])
#                 if next_ego_actions:  # Ensure next_ego_actions is not empty
#                     first_next_action = next_ego_actions[0]  # Get the first action
#                     print(first_next_action.get('Action'))
#
#
#         adasstate_event = self.state_events.get(OtherAPI.E_ADASState)
#         cms_visual_warning = adasstate_event.get("CMSVisualWarning")
#         acceleration_request = adasstate_event.get("ADASVehicleAccelerationRequest")
#
#         if (cms_visual_warning or acceleration_request):
#             if("Dri_SetAccelerationPedal" == first_next_action.get('Action')):
#                 start_trig_throttle = self.VehicleDefines.add_time_to_collision_start_trigger(
#                     value=float(4))
#
#                 start_action = self.VehicleDefines.create_controller_override_action(
#                     throttle=self.throttle["Throttle"],
#                     brake=0, clutch=0, parkingbrake=0,
#                     steeringwheel=0, gear=0)
#                 all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig_throttle,
#                                                                                   start_action=start_action))
#
#             elif("Dri_SetBrakePedal" == first_next_action.get('Action')):
#                 start_trig_brake = self.VehicleDefines.add_time_to_collision_start_trigger(
#                     value=float(4))
#                 start_action = self.VehicleDefines.create_controller_override_action(throttle=0,
#                                                                                      brake=self.brake["Brake"],
#                                                                                      clutch=0, parkingbrake=0,
#                                                                                      steeringwheel=0, gear=0)
#
#                 all_ego_events.append(self.VehicleDefines.define_ego_action_event(start_trig=start_trig_brake,
#                                                                                   start_action=start_action))
#
#             elif("Dri_SetLateralDisplacement" == first_next_action.get('Action')):
#                 start_trig = self.VehicleDefines.add_time_to_collision_start_trigger(
#                             value=float(4))
#                 start_action = self.VehicleDefines.create_lateral_distance_action(lane_offset=0)
#                 all_ego_events.append(
#                     self.VehicleDefines.define_ego_action_event(start_trig=start_trig, start_action=start_action))
#
#             else:
#                 pass