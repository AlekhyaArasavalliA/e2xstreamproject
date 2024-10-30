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



class BaseScenario:
    def __init__(self):

        self.VehicleControls = vehiclecontrol()
        self.Data_Controls = datacontrol()
        self.VehicleDefines = VehicleScenario()
        road_len = None

    def trigger_condition(self, targetname):
        """
        Trigger condition creation
        Parameters
        ----------
        targetname

        Returns
        -------

        """
        trigcond = xosc.StandStillCondition(0.5)
        standstill_trigger = xosc.EntityTrigger(
            "standstill trigger", 0.1, xosc.ConditionEdge.none, trigcond, targetname
        )

        return standstill_trigger

    def integrate_new_actions(self, init, egoname):
        """
        Integrate new actions
        Returns
        -------

        """
        # Create a controller override action
        override_action = self.VehicleDefines.create_controller_override_action()

        # Assuming you want to apply this action at the start, add it to the init actions for the ego
        init.add_init_action(egoname, override_action)

        # Create a time-to-collision trigger and integrate it
        # This example assumes the target entity reference and other details are known and static.
        # You might want to adapt these values based on your scenario's requirements.
        condition_trigger = self.VehicleDefines.add_time_to_collision_start_trigger(
            target_entity_ref="4bdc6cf0-d460-11ee-bd54-59f53ea26ff9",
            triggering_entity=egoname,
            value=4,  # Time to collision value
            rule="lessThan"
        )
        return condition_trigger

    def ego_startevent_maneuver_group(self, total_events, egoname):
        """
        Create Ego Manuever group
        Parameters
        ----------
        total_events

        Returns
        -------

        """
        ego_man = xosc.Maneuver("EgoManeuver")
        for te in total_events:
            ego_man.add_event(te)
        # ego_man.add_event(ego_event)
        # ego_man.add_event(egothrottle_event)

        ego_mangr = xosc.ManeuverGroup("Ego")
        ego_mangr.add_actor(egoname)
        ego_mangr.add_maneuver(ego_man)

        return ego_mangr

    def target_startevent_maneuver_group(self, target_events, target_name="Obj1"):
        """
        Create Target Manuver group
        Parameters
        ----------
        target_start_event
        target_event
        target_name

        Returns
        -------

        """
        target_man = xosc.Maneuver("targetManeuver")

        for tgt_evnt in target_events:
            target_man.add_event(tgt_evnt)
        # target_man.add_event(target_event)

        target_mangr = xosc.ManeuverGroup(target_name)
        target_mangr.add_actor(target_name)
        target_mangr.add_maneuver(target_man)

        return target_mangr

    def define_ego_entities(self, properties, vehicle_entities, width=2.0, length=5.0, egoname="Ego"):
        """
        Define the Ego entities
        Parameters
        ----------
        properties
        width
        length

        Returns
        -------

        """
        # properties["model_id"] = "0"
        properties = {"Ego": properties}

        ego_veh = self.VehicleDefines.ego_vehicle_and_entities(egoname=egoname,
                                                               model=properties['Ego']["model"],
                                                               properties=properties["Ego"],
                                                               VehicleWidth=float(width),
                                                               VehicleLength=float(length))

        vehicle_entities.add_scenario_object(egoname, ego_veh)

    def define_target_entities(self, properties, paramlist_analysis, vehicle_entities):
        """
        Define target entities
        Parameters
        ----------
        properties

        Returns
        -------

        """
        obj_entities, obj_list = EBTB_API_data.get_obj_entities(paramlist_analysis=paramlist_analysis)

        for obj, value in obj_entities.items():

            if obj_entities[obj][3] == 'car':

                target_obj = self.VehicleDefines.target_vehicle_and_entities(target_name=obj, model=value[4],
                                                                             default_cat=False, entity_type='Vehicle',
                                                                             properties=properties.get('car'),
                                                                             vehicle_category=value[3],
                                                                             width=float(value[0]), length=float(value[1]),
                                                                             height=float(value[2]))
                # vehicle_entities.add_scenario_object(obj, target_obj)
            elif obj_entities[obj][3] == 'bicycle':
                target_obj = self.VehicleDefines.target_vehicle_and_entities(target_name=obj, model=value[4],
                                                                             default_cat=False, entity_type='Vehicle',
                                                                             properties=properties.get('bicycle'),
                                                                             vehicle_category=value[3],
                                                                             width=float(value[0]),
                                                                             length=float(value[1]),
                                                                             height=float(value[2]))
                # vehicle_entities.add_scenario_object(obj, target_obj)
            elif obj_entities[obj][3] == 'pedestrian':
                target_obj = self.VehicleDefines.target_vehicle_and_entities(target_name=obj, model=value[4],
                                                                             default_cat=False, entity_type='Pedestrian',
                                                                             properties=properties.get('human'),
                                                                             vehicle_category=value[3],
                                                                             width=float(value[0]),
                                                                             length=float(value[1]),
                                                                             height=float(value[2]))
            elif obj_entities[obj][3] == 'bicycle':
                target_obj = self.VehicleDefines.target_vehicle_and_entities(target_name=obj, model=value[4],
                                                                             default_cat=False, entity_type='Vehicle',
                                                                             properties=properties.get('twowheeler'),
                                                                             vehicle_category=value[3],
                                                                             width=float(value[0]),
                                                                             length=float(value[1]),
                                                                             height=float(value[2]))

            vehicle_entities.add_scenario_object(obj, target_obj)







            # target_obj = self.VehicleDefines.target_vehicle_and_entities(target_name=obj, model=value[4],
            #                                                              default_cat=False, entity_type='Vehicle',
            #                                                              properties=properties,
            #                                                              vehicle_category=value[3],
            #                                                              width=float(value[0]), length=float(value[1]),
            #                                                              height=float(value[2]))
            #
            # vehicle_entities.add_scenario_object(obj, target_obj)

        return obj_entities, obj_list



    def Ego_initialize(self, init, step_time, paramlist_analysis):
        """
        Ego Initialize
        Returns
        -------

        """
        global road_len
        envp_landmark_offset = EBTB_API_data.get_landmark_offset_ego(paramlist_analysis=paramlist_analysis)
        envp_lane_selection = EBTB_API_data.get_lane_selection_ego(paramlist_analysis=paramlist_analysis)
        road_len = EBTB_API_data.extract_lenthoflane(paramlist_analysis=paramlist_analysis)
        envp_landmark_offset = float(envp_landmark_offset)

        # if isinstance(road_len, (int, float)) and isinstance(envp_landmark_offset, (int, float)):
        if road_len is not None:
            x_value = (road_len / 2) + envp_landmark_offset
        else:
            x_value = envp_landmark_offset


        if(envp_lane_selection == "Right1"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y = -1,
                                               x=x_value)
        elif(envp_lane_selection == "Right2"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y = -2,
                                               x=x_value)
        elif (envp_lane_selection == "Right3"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y=-3,
                                               x=x_value)
        elif(envp_lane_selection == "Right4"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y = -4,
                                               x=x_value)
        elif (envp_lane_selection == "Right5"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y=-5,
                                               x=x_value)
        elif (envp_lane_selection == "Right6"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y=-6,
                                               x=x_value)
        elif (envp_lane_selection == "Left1"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y=1,
                                               x=x_value)
        elif (envp_lane_selection == "Left2"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y=2,
                                               x=x_value)
        elif (envp_lane_selection == "Left3"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y=3,
                                               x=x_value)
        elif (envp_lane_selection == "Left4"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y=4,
                                               x=x_value)
        elif (envp_lane_selection == "Left5"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y=5,
                                               x=x_value)
        elif (envp_lane_selection == "Left6"):
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                               y=6,
                                               x=x_value)
        else:
            self.VehicleDefines.ego_initialize(init=init, step_time=step_time, ini_speed=0,
                                              y = -4.625,
                                              x=x_value)

    def Target_initialize(self, init, step_time,target_name, states_analysis,overlap_data=None):
        from e2xostream.src.vehiclestream.xosc_stream.XOSCScenarioDevelop import FuncScenario as funcscenario
        """
        Target initialize
        Returns
        -------

        """
        global road_len
        obj_lane_selection = EBTB_API_data.get_lane_selection_object(states_analysis=states_analysis,
                                                                     target_name=target_name)
        obj_landmark_offset = EBTB_API_data.get_landmark_offset(states_analysis=states_analysis,
                                                                target_name=target_name)
        obj_landmark_offset = float(obj_landmark_offset)
        x_val = (road_len / 2) + obj_landmark_offset
        if (obj_lane_selection == "Right1"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name, x=x_val, y=-1)
        elif (obj_lane_selection == "Right2"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=-2,
                                                  x=x_val)
        elif (obj_lane_selection == "Right3"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=-3,
                                                  x=x_val)
        elif (obj_lane_selection == "Right4"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=-4,
                                                  x=x_val)
        elif (obj_lane_selection == "Right5"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=-5,
                                                  x=x_val)
        elif (obj_lane_selection == "Right6"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=-6,
                                                  x=x_val)
        elif (obj_lane_selection == "Left1"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=1,
                                                  x=x_val)
        elif (obj_lane_selection == "Left2"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=2,
                                                  x=x_val)
        elif (obj_lane_selection == "Left3"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=3,
                                                  x=x_val)
        elif (obj_lane_selection == "Left4"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=4,
                                                  x=x_val)
        elif (obj_lane_selection == "Left5"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=5,
                                                  x=x_val)
        elif (obj_lane_selection == "Left6"):
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=6,
                                                  x=x_val)
        else:
            self.VehicleDefines.target_initialize(init=init, step_time=step_time,
                                                  targetname=target_name,
                                                  y=-4.625,
                                                  x=x_val)



    # # if param["ObjectId"] == "Obj2":
    # if target_name = param["ObjectId"]:
    #     obj_lane_selection = EBTB_API_data.get_lane_selection_object(states_analysis=states_analysis,
    #                                                                  target_name=target_name)
    #     obj_landmark_offset = EBTB_API_data.get_landmark_offset(states_analysis=states_analysis,
    #                                                             target_name=target_name)
    #     obj_landmark_offset = float(obj_landmark_offset)
    #     x_val = (road_len / 2) + obj_landmark_offset
    #     if obj_id == "Obj2":
    #         if (obj_lane_selection == "Right1"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time,
    #                                                   targetname="Obj2", x=x_val, y=-1)
    #         elif (obj_lane_selection == "Right2"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=-2,
    #                                                   x=x_val)
    #         elif (obj_lane_selection == "Right3"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=-3,
    #                                                   x=x_val)
    #         elif (obj_lane_selection == "Right4"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=-4,
    #                                                   x=x_val)
    #         elif (obj_lane_selection == "Right5"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=-5,
    #                                                   x=x_val)
    #         elif (obj_lane_selection == "Right6"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=-6,
    #                                                   x=x_val)
    #         elif (obj_lane_selection == "Left1"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=1,
    #                                                   x=x_val)
    #         elif (obj_lane_selection == "Left2"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=2,
    #                                                   x=x_val)
    #         elif (obj_lane_selection == "Left3"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=3,
    #                                                   x=x_val)
    #         elif (obj_lane_selection == "Left4"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=4,
    #                                                   x=x_val)
    #         elif (obj_lane_selection == "Left5"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=5,
    #                                                   x=x_val)
    #         elif (obj_lane_selection == "Left6"):
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=6,
    #                                                   x=x_val)
    #         else:
    #             self.VehicleDefines.target_initialize(init=init, step_time=step_time, targetname="Obj2",
    #                                                   y=-4.625,
    #                                                   x=x_val)

    # obj_lane_selection = EBTB_API_data.get_lane_selection_object(states_analysis=states_analysis)
        # obj_landmark_offset = EBTB_API_data.get_landmark_offset(states_analysis=states_analysis)if(obj_lane_selection == "Right4"):
        #     try:
        #         overlap_data = EBTB_API_data.get_Obj_set_lateral_relative(states_analysis=states_analysis)
        #         overlap_value = self.Data_Controls.calculate_overlap(overlap_data)
        #     except:
        #         overlap_value = -8.375
        # elif(obj_lane_selection == "Right3"):
        #     overlap_value = -4.625
        # else:
        #     overlap_value = -4.625

        # obj_dict = EBTB_API_data.get_landmark_offset_obj(states_analysis=states_analysis)


        # for obj in obj_dict:
        # self.VehicleDefines.target_initialize(init=init, step_time=step_time,
        #                                       targetname=obj, x=obj_dict[obj], y=overlap_value)