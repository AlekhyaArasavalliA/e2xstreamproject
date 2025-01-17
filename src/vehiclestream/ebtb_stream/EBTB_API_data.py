import os
import sys
import xml.etree.ElementTree as ET


from e2xostream.config import default_properties, global_parameters, settings
from e2xostream.stk.vehicledynamics.DataControl import DataControls as datacontrol
from e2xostream.config.api_constants import (api_methods_constants as ApiMethods,
                                             ego_api_constants as EgoAPI,
                                             obj_api_constants as ObjAPI,
                                             other_api_constants as OtherAPI)
from e2xostream.config.api_constants import api_methods_constants as AMC

last_index = {}



def EBTB_anlyses_info(paramlist_analysis, states_analysis):
    """
    EBTB Anlyzed information display
    Returns
    -------

    """
    print("\nParameterList Analysis:")
    for k, v in paramlist_analysis.items():
        print(v.get("EgoActions")[0])
        print(v.get("ObjectActions"))

    print("\nStates Analysis:")
    for k, v in states_analysis.items():
        print("\n*********", k, "**********")
        # print(v.get("EgoActions"))
        # print(v.get("ObjectActions"))
        # print(v.get("OtherConditions"))
        # print(v.get("E_ObjectDistanceLaneBasedActions"))
        print(v)


# def get_ego_obj_speed_transition_time(states_analysis):
#
#     """
#     ParameterList_info, States_info, ego_speed, obj_speed, ego_transition_time, obj_transition_time
#     """
#     extracted_info = {}
#     for k, v in states_analysis.items():
#         for action in v.get('EgoActions', []):
#             if action.get('Action') == EgoAPI.Dri_SetLongitudinalSpeed:
#                 for param in action.get('Parameters', []):
#                     extracted_values = {'TargetSpeed': param.get('TargetSpeed', 'Not Available')}
#                     if 'TransitionTime' in param:
#                         extracted_values['TransitionTime'] = param['TransitionTime']
#                     else:
#                         extracted_values['TransitionTime'] = 0.0  # Or any default value or indication
#
#                     extracted_info[EgoAPI.Dri_SetLongitudinalSpeed] = extracted_values
#
#         for obj_id, actions in v.get('ObjectActions', {}).items():
#             for action in actions:
#                 if action.get('Action') == ObjAPI.Obj_SetLongitudinalSpeed:
#                     for param in action.get('Parameters', []):
#                         # Initialize a dict to hold the extracted values for this iteration
#                         extracted_values = {'TargetSpeed': param.get('TargetSpeed', 'Not Available')}
#
#                         # Check for TransitionTime and add it if available
#                         if 'TransitionTime' in param:
#                             extracted_values['TransitionTime'] = param['TransitionTime']
#                         else:
#                             extracted_values['TransitionTime'] = 0.0  # Default value
#
#                         # If the obj_id key already exists in extracted_info, append the new data
#                         if f'{obj_id}_Obj_SetLongitudinalSpeed' in extracted_info:
#                             extracted_info[f'{obj_id}_Obj_SetLongitudinalSpeed'].append(extracted_values)
#                         else:
#                             # Otherwise, create a new list with the first set of extracted values
#                             extracted_info[f'{obj_id}_Obj_SetLongitudinalSpeed'] = [extracted_values]
#
#
#
#     for key, value in extracted_info.items():
#         if isinstance(value, dict):
#             extracted_info[key] = [value]
#     print("extr",extracted_info)
#
#     if EgoAPI.Dri_SetLongitudinalSpeed in extracted_info:
#         # Extract speed and convert it
#         speed_kmhr = float(extracted_info[EgoAPI.Dri_SetLongitudinalSpeed][0]['TargetSpeed'])
#         speed_ms_float = datacontrol().kmhr_to_ms(speed_kmhr)
#         ego_speed_ms = round(speed_ms_float, 2)
#         # Optionally, extract TransitionTime if you need to use it
#         ego_transition_time = extracted_info[EgoAPI.Dri_SetLongitudinalSpeed][0]['TransitionTime']
#     else:
#         ego_speed_ms = 0
#         ego_transition_time = 0  # Or any default/fallback value
#     if 'Obj1_Obj_SetLongitudinalSpeed' in extracted_info:
#         for i in range(0,len(extracted_info['Obj1_Obj_SetLongitudinalSpeed'])):
#             obj_speed_kmhr = float(extracted_info['Obj1_Obj_SetLongitudinalSpeed'][i]['TargetSpeed'])
#             obj_speed_ms_float = datacontrol().kmhr_to_ms(obj_speed_kmhr)
#             obj_speed_ms = round(obj_speed_ms_float, 2)
#             obj_transition_time = extracted_info['Obj1_Obj_SetLongitudinalSpeed'][i]['TransitionTime']
#
#     if 'Obj2_Obj_SetLongitudinalSpeed' in extracted_info:
#         for i in range(0, len(extracted_info['Obj2_Obj_SetLongitudinalSpeed'])):
#
#             obj_speed_kmhr = float(extracted_info['Obj2_Obj_SetLongitudinalSpeed'][i]['TargetSpeed'])
#             obj_speed_ms_float = datacontrol().kmhr_to_ms(obj_speed_kmhr)
#             obj_speed_ms = round(obj_speed_ms_float, 2)
#             obj_transition_time = extracted_info['Obj2_Obj_SetLongitudinalSpeed'][i]['TransitionTime']
#
#     return ego_speed_ms, obj_speed_ms, ego_transition_time, obj_transition_time

def get_ego_obj_speed_transition_time(states_analysis):
    extracted_info = {}

    # Iterate over the states analysis dictionary
    for k, v in states_analysis.items():
        # Process EgoActions
        for action in v.get('EgoActions', []):
            if action.get('Action') == EgoAPI.Dri_SetLongitudinalSpeed:
                for param in action.get('Parameters', []):
                    target_speed = param.get('TargetSpeed', 'Not Available')
                    transition_time = param.get('TransitionTime', 0.0)  # Default to 0.0 if missing
                    extracted_info[EgoAPI.Dri_SetLongitudinalSpeed] = [
                        {'TargetSpeed': target_speed, 'TransitionTime': transition_time}]

        # Process ObjectActions
        for obj_id, actions in v.get('ObjectActions', {}).items():
            for action in actions:
                if action.get('Action') == ObjAPI.Obj_SetLongitudinalSpeed:
                    for param in action.get('Parameters', []):
                        target_speed = param.get('TargetSpeed', 'Not Available')
                        transition_time = param.get('TransitionTime', 0.0)  # Default to 0.0 if missing
                        # Append the object action information
                        obj_key = f'{obj_id}_Obj_SetLongitudinalSpeed'
                        if obj_key not in extracted_info:
                            extracted_info[obj_key] = []
                        extracted_info[obj_key].append(
                            {'TargetSpeed': target_speed, 'TransitionTime': transition_time})

    print("extras", extracted_info)
    # Ensure all values are lists for consistency
    for key, value in extracted_info.items():
        if isinstance(value, dict):
            extracted_info[key] = [value]

    # Extract ego vehicle information
    if EgoAPI.Dri_SetLongitudinalSpeed in extracted_info:
        speed_kmhr = float(extracted_info[EgoAPI.Dri_SetLongitudinalSpeed][0]['TargetSpeed'])
        speed_ms_float = datacontrol().kmhr_to_ms(speed_kmhr)
        ego_speed_ms = round(speed_ms_float, 2)
        ego_transition_time = extracted_info[EgoAPI.Dri_SetLongitudinalSpeed][0]['TransitionTime']
    else:
        ego_speed_ms = 0
        ego_transition_time = 0  # Default if no ego action found

    # Extract object vehicle information (Obj1 and Obj2)
    obj_speeds = []
    obj_transition_times = []

    for obj_id in ['Obj1', 'Obj2']:
        obj_key = f'{obj_id}_Obj_SetLongitudinalSpeed'
        if obj_key in extracted_info:
            for i in range(len(extracted_info[obj_key])):
                obj_speed_kmhr = float(extracted_info[obj_key][i]['TargetSpeed'])
                obj_speed_ms_float = round(datacontrol().kmhr_to_ms(obj_speed_kmhr), 2)
                obj_speed = round(obj_speed_ms_float,2)
                # obj_speeds.append(obj_speed_ms_float)  # Collect speeds
                obj_transition_time = extracted_info[obj_key][i]['TransitionTime']  # Collect transition times

    # Return the extracted values
    return ego_speed_ms, obj_speed, ego_transition_time, obj_transition_time



    # extracted_info = {}

    # Iterate over the states analysis dictionary
    # for k, v in states_analysis.items():
    #
    #     # Process EgoActions
    #     for action in v.get('EgoActions', []):
    #         if action.get('Action') == EgoAPI.Dri_SetLongitudinalSpeed:
    #             for param in action.get('Parameters', []):
    #                 target_speed = param.get('TargetSpeed', 'Not Available')
    #                 transition_time = param.get('TransitionTime', 0.0)  # Default to 0.0 if missing
    #                 extracted_info[EgoAPI.Dri_SetLongitudinalSpeed] = [
    #                     {'TargetSpeed': target_speed, 'TransitionTime': transition_time}]
    #
    #     # Process ObjectActions
    #     for obj_id, actions in v.get('ObjectActions', {}).items():
    #         for action in actions:
    #             if action.get('Action') == ObjAPI.Obj_SetLongitudinalSpeed:
    #                 for param in action.get('Parameters', []):
    #                     target_speed = param.get('TargetSpeed', 'Not Available')
    #                     transition_time = param.get('TransitionTime', 0.0)  # Default to 0.0 if missing
    #                     # Append the object action information
    #                     obj_key = f'{obj_id}_Obj_SetLongitudinalSpeed'
    #                     if obj_key not in extracted_info:
    #                         extracted_info[obj_key] = []
    #                     extracted_info[obj_key].append({'TargetSpeed': target_speed, 'TransitionTime': transition_time})
    #
    # print("extras", extracted_info)
    # # Ensure all values are lists for consistency
    # for key, value in extracted_info.items():
    #     if isinstance(value, dict):
    #         extracted_info[key] = [value]
    #
    # obj2_processed = False
    # # Extract ego vehicle information
    # if EgoAPI.Dri_SetLongitudinalSpeed in extracted_info:
    #     speed_kmhr = float(extracted_info[EgoAPI.Dri_SetLongitudinalSpeed][0]['TargetSpeed'])
    #     speed_ms_float = datacontrol().kmhr_to_ms(speed_kmhr)
    #     ego_speed_ms = round(speed_ms_float, 2)
    #     ego_transition_time = extracted_info[EgoAPI.Dri_SetLongitudinalSpeed][0]['TransitionTime']
    # else:
    #     ego_speed_ms = 0
    #     ego_transition_time = 0  # Default if no ego action found
    #
    # # Extract object vehicle information (Obj1 or Obj2 based on availability)
    # if 'Obj1_Obj_SetLongitudinalSpeed' in extracted_info:
    #     for i in range(0, len(extracted_info['Obj1_Obj_SetLongitudinalSpeed'])):
    #         obj_speed_kmhr = float(extracted_info['Obj1_Obj_SetLongitudinalSpeed'][i]['TargetSpeed'])
    #         obj_speed_ms_float = datacontrol().kmhr_to_ms(obj_speed_kmhr)
    #         obj_speed_ms = round(obj_speed_ms_float, 2)
    #         obj_transition_time = extracted_info['Obj1_Obj_SetLongitudinalSpeed'][i]['TransitionTime']
    #
    # if 'Obj2_Obj_SetLongitudinalSpeed' in extracted_info and not obj2_processed:
    #     for i in range(0, len(extracted_info['Obj2_Obj_SetLongitudinalSpeed'])):
    #         obj_speed_kmhr = float(extracted_info['Obj2_Obj_SetLongitudinalSpeed'][i]['TargetSpeed'])
    #         obj_speed_ms_float = datacontrol().kmhr_to_ms(obj_speed_kmhr)
    #         obj_speed_ms = round(obj_speed_ms_float, 2)
    #         obj_transition_time = extracted_info['Obj2_Obj_SetLongitudinalSpeed'][i]['TransitionTime']
    #         obj2_processed = True
    #
    # # Return the extracted values
    # return ego_speed_ms, obj_speed_ms, ego_transition_time, obj_transition_time


# def get_ego_obj_speed_transition_time1(states_analysis):
#
#     """
#     ParameterList_info, States_info, ego_speed, obj_speed, ego_transition_time, obj_transition_time
#     """
#     extracted_info = {}
#     for k, v in states_analysis.items():
#         for action in v.get('EgoActions', []):
#             if action.get('Action') == EgoAPI.Dri_SetLongitudinalSpeed:
#                 for param in action.get('Parameters', []):
#                     extracted_values = {'TargetSpeed': param.get('TargetSpeed', 'Not Available')}
#                     if 'TransitionTime' in param:
#                         extracted_values['TransitionTime'] = param['TransitionTime']
#                     else:
#                         extracted_values['TransitionTime'] = 0.0  # Or any default value or indication
#
#                     extracted_info[EgoAPI.Dri_SetLongitudinalSpeed] = extracted_values
#
#


def get_ego_speed_transition_time(states_analysis):
    extracted_info = {}

    # Iterate over the states analysis dictionary
    for k, v in states_analysis.items():
        # Process EgoActions
        for action in v.get('EgoActions', []):
            if action.get('Action') == EgoAPI.Dri_SetLongitudinalSpeed:
                for param in action.get('Parameters', []):
                    target_speed = param.get('TargetSpeed', 'Not Available')
                    transition_time = param.get('TransitionTime', 0.0)  # Default to 0.0 if missing
                    extracted_info[EgoAPI.Dri_SetLongitudinalSpeed] = [
                        {'TargetSpeed': target_speed, 'TransitionTime': transition_time}]

    if EgoAPI.Dri_SetLongitudinalSpeed in extracted_info:
        speed_kmhr = float(extracted_info[EgoAPI.Dri_SetLongitudinalSpeed][0]['TargetSpeed'])
        speed_ms_float = datacontrol().kmhr_to_ms(speed_kmhr)
        speed = round(speed_ms_float, 2)
        transition_time = extracted_info[EgoAPI.Dri_SetLongitudinalSpeed][0]['TransitionTime']
    else:
        speed = 0
        transition_time = 0  # Default if no ego action found
    return speed,transition_time



def get_obj_speed_transition_time(target_name,states_analysis):
    extracted_info = {}

    for k, v in states_analysis.items():
        for obj_id, actions in v.get('ObjectActions', {}).items():
            for action in actions:
                if action.get('Action') == ObjAPI.Obj_SetLongitudinalSpeed:
                    for param in action.get('Parameters', []):
                        target_speed = param.get('TargetSpeed', 'Not Available')
                        transition_time = param.get('TransitionTime', 0.0)  # Default to 0.0 if missing
                        # Append the object action information
                        obj_key = f'{obj_id}_Obj_SetLongitudinalSpeed'
                        if obj_key not in extracted_info:
                            extracted_info[obj_key] = []
                        extracted_info[obj_key].append(
                            {'TargetSpeed': target_speed, 'TransitionTime': transition_time})

    key_to_access = f"{target_name}_Obj_SetLongitudinalSpeed"

    global last_index  # Use global dictionary to retain state across calls

    if key_to_access not in last_index:
        last_index[key_to_access] = 0

        # Check if the key exists in extracted_info
    if key_to_access in extracted_info:
        # Get the list of values for the key
        extracted_value = extracted_info[key_to_access]

        # Ensure last_index does not exceed the list length
        if last_index[key_to_access] < len(extracted_value):
            # Access the current value based on last accessed index
            current_value = extracted_value[last_index[key_to_access]]
            speed_kmhr = float(current_value['TargetSpeed'])
            speed_ms_float = round(datacontrol().kmhr_to_ms(speed_kmhr), 2)
            speed = round(speed_ms_float, 2)
            transition_time = current_value['TransitionTime']

            # Update the last accessed index to move to the next item on the next call
            last_index[key_to_access] += 1
        else:
            # Reset or handle if all values have been processed
            speed = 0
            transition_time = 0
            last_index[key_to_access] = 0  # Optional reset if you want to loop back
    else:
        # Default values if key is not found
        speed = 0
        transition_time = 0

    print("return speed",speed)
    print("return time",transition_time)

    return speed, transition_time
    #
    # print("tarnme_ebtbapi", target_name)
    #
    # if key_to_access in extracted_info:
    #     extracted_value = extracted_info[key_to_access]
    #     print(f"Extracted Value for {key_to_access}: {extracted_value}")
    #     speed_kmhr = float(extracted_value[0]['TargetSpeed'])
    #     print(speed_kmhr)
    #     speed_ms_float = round(datacontrol().kmhr_to_ms(speed_kmhr), 2)
    #     speed = round(speed_ms_float, 2)
    #     transition_time = extracted_value[0]['TransitionTime']
    # else:
    #     speed = 0
    #     transition_time = 0
    #
    # return speed, transition_time





    # if key_to_access not in self.last_index:
    #     self.last_index[key_to_access] = 0
    #
    # # Check if the key exists in extracted_info
    # if key_to_access in extracted_info:
    #     # Get the list of values for the key
    #     extracted_value = extracted_info[key_to_access]
    #
    #     # If the last index exceeds the list length, reset to 0 or handle as needed
    #     if self.last_index[key_to_access] >= len(extracted_value):
    #         self.last_index[key_to_access] = 0
    #
    #     # Get the current value based on last accessed index
    #     current_value = extracted_value[self.last_index[key_to_access]]
    #     speed_kmhr = float(current_value['TargetSpeed'])
    #     speed_ms_float = round(datacontrol().kmhr_to_ms(speed_kmhr), 2)
    #     speed = round(speed_ms_float, 2)
    #     transition_time = current_value['TransitionTime']
    #
    #     # Update the last accessed index
    #     self.last_index[key_to_access] += 1
    # else:
    #     # Default values if key is not found
    #     speed = 0
    #     transition_time = 0
    #
    # return speed, transition_time



def xlmr_to_xodr_mapping(paramlist_analysis):
    print("param",paramlist_analysis)
    """
    Mapping xlmr to xodr
    Parameters
    ----------
    paramlist_analysis

    Returns
    -------
    """
    # Loop over paramlist_analysis and return XlmrFile key value
    xlmr_file = "germany_hw_4lanes_rq31_10km_straight_v2.xlmr"
    for key, value in paramlist_analysis.items():
        ego_actions = value.get('EgoActions', [])
        for action in ego_actions:
            if action.get('Action', []) == OtherAPI.EnvP_RoadNetwork:
                parameters = action.get('Parameters', [])
                for param in parameters:
                    if AMC.XlmrFile in param:
                        xlmr_file = param[AMC.XlmrFile]
                        break
                else:
                    continue
                break

    # xlmr_file to xodr mapping
    xodr_path = global_parameters.XLMR[
        xlmr_file] if xlmr_file in global_parameters.XLMR else "dd878027-4265-43bd-9ff1-5fd9f688f1f7.xodr"

    return xodr_path

def extract_lenthoflane(paramlist_analysis):
    folder_path = r"C:\Users\prchan\PycharmProjects\project upto 25october\pythonProject\e2xstreamline-main1 1\e2xstreamline-main11\mye2x\e2xostream\stk\xodrmaps"  # Folder where you want to search for the .xodr file

    for key, value in paramlist_analysis.items():
        ego_actions = value.get('EgoActions', [])
        for action in ego_actions:
            if action.get('Action', []) == OtherAPI.EnvP_RoadNetwork:
                parameters = action.get('Parameters', [])
                for param in parameters:
                    if AMC.XlmrFile in param:
                        xlmr_file = param[AMC.XlmrFile]
                        break
                else:
                    continue
                break
        cleaned_file_path = os.path.basename(xlmr_file)


    """
    Converts the given .xlmr file name to .xodr, compares it with files in the folder,
    parses the .xodr file as XML, and extracts data from <lanes> and <laneSections> tags.
    For each lane, checks for the <left> tag and prints the lane id and width.

    Parameters
    ----------
    xlmr_file_name : str
        Name of the .xlmr file to be converted to .xodr and searched.
    folder_path : str
        Path to the folder where files are located.
    """
    try:
        xodr_map = cleaned_file_path.replace('.xlmr', '.xodr')
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Iterate over files in the folder
            for filename in os.listdir(folder_path):
                # Compare the filename with the generated xodr_map
                if filename == xodr_map:
                    file_path = os.path.join(folder_path, filename)

                    # Parse the .xodr file as XML
                    try:
                        tree = ET.parse(file_path)
                        root = tree.getroot()

                        # Navigate to <road> tag
                        road = root.find(".//road")
                        if road is not None:
                            # Extract the 'length' attribute
                            length_str = road.get('length')
                            if length_str:
                                try:
                                    road_length = float(length_str)  # Convert the string to a float
                                    return road_length  # Return the length value
                                except ValueError:
                                    print(f"Error converting length to float: {length_str}")
                                    return None
                            else:
                                print("No 'length' attribute found in the <road> tag.")
                                return None
                        else:
                            print("<road> tag not found in the file.")
                            return None

                    except ET.ParseError as e:
                        print(f"Error parsing the .xodr file: {e}")
                        return None
            print(f"File {xodr_map} not found in the folder {folder_path}.")
            return None
        else:
            print(f"The folder {folder_path} does not exist.")
            return None
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None



folder_path = r"C:\Users\prchan\PycharmProjects\project upto 25october\pythonProject\e2xstreamline-main1 1\e2xstreamline-main11\mye2x\e2xostream\stk\xodrmaps"  # Folder where you want to search for the .xodr file


def extract_xodr():
    lane_length = 5
    # lane_length = extract_lenthoflane(paramlist_analysis=None)
    return lane_length

def getroadnetwork(paramlist_analysis):
    xodr_path = xlmr_to_xodr_mapping(paramlist_analysis)
    return xodr_path


def get_obj_entities(paramlist_analysis):
    """
    Get the Object entities
    Returns
    -------

    """
    obj_details = {}
    obj_list = []
    if 'Default' in paramlist_analysis and 'ObjectActions' in paramlist_analysis['Default']:
        for obj_name, obj_data in paramlist_analysis['Default']['ObjectActions'].items():
            if obj_data and obj_data[0]['Parameters']:
                obj_parameters = obj_data[0]['Parameters'][0]
                obj_id = obj_parameters.get('ObjectID')
                asset_id = (obj_parameters.get('AssetID').split('/')[0] if obj_parameters.get('AssetID') else None)


                if asset_id is not None:
                    asset_id = global_parameters.VEHICLE_CATEGORIES.get(asset_id.lower(), 'car')
                else:
                     asset_id = "car"


                if asset_id == "bicycle":
                    vehicle_name = global_parameters.VEHICLE_NAME.get(asset_id.lower(),'bicycle')
                    width = default_properties.DEFAULT_SIZE_PROPERTIES.get('bicycle')['width']
                    length = default_properties.DEFAULT_SIZE_PROPERTIES.get('bicycle')['length']
                    height = default_properties.DEFAULT_SIZE_PROPERTIES.get('bicycle')['height']
                elif asset_id == "van" :
                    vehicle_name = global_parameters.VEHICLE_NAME.get(asset_id.lower(),'van')
                    width = default_properties.DEFAULT_SIZE_PROPERTIES.get('van')['width']
                    length = default_properties.DEFAULT_SIZE_PROPERTIES.get('van')['length']
                    height = default_properties.DEFAULT_SIZE_PROPERTIES.get('van')['height']
                elif asset_id == "truck":
                    vehicle_name = global_parameters.VEHICLE_NAME.get(asset_id.lower(),'truck')
                    width = default_properties.DEFAULT_SIZE_PROPERTIES.get('truck')['width']
                    length = default_properties.DEFAULT_SIZE_PROPERTIES.get('truck')['length']
                    height = default_properties.DEFAULT_SIZE_PROPERTIES.get('truck')['height']
                elif asset_id == "trailer":
                    vehicle_name = global_parameters.VEHICLE_NAME.get(asset_id.lower(),'trailer')
                    width = default_properties.DEFAULT_SIZE_PROPERTIES.get('trailer')['width']
                    length = default_properties.DEFAULT_SIZE_PROPERTIES.get('trailer')['length']
                    height = default_properties.DEFAULT_SIZE_PROPERTIES.get('trailer')['height']
                elif asset_id == "semitrailer":
                    vehicle_name = global_parameters.VEHICLE_NAME.get(asset_id.lower(),'semitrailer')
                    width = default_properties.DEFAULT_SIZE_PROPERTIES.get('semitrailer')['width']
                    length = default_properties.DEFAULT_SIZE_PROPERTIES.get('semitrailer')['length']
                    height = default_properties.DEFAULT_SIZE_PROPERTIES.get('semitrailer')['height']
                elif asset_id == "bus":
                    vehicle_name = global_parameters.VEHICLE_NAME.get(asset_id.lower(),'bus')
                    width = default_properties.DEFAULT_SIZE_PROPERTIES.get('bus')['width']
                    length = default_properties.DEFAULT_SIZE_PROPERTIES.get('bus')['length']
                    height = default_properties.DEFAULT_SIZE_PROPERTIES.get('bus')['height']
                elif asset_id == "bicycle":
                    vehicle_name = global_parameters.VEHICLE_NAME.get(asset_id.lower(),'twowheeler')
                    width = default_properties.DEFAULT_SIZE_PROPERTIES.get('twowheeler')['width']
                    length = default_properties.DEFAULT_SIZE_PROPERTIES.get('twowheeler')['length']
                    height = default_properties.DEFAULT_SIZE_PROPERTIES.get('twowheeler')['height']
                elif asset_id == "train":
                    vehicle_name = global_parameters.VEHICLE_NAME.get(asset_id.lower(),'train')
                    width = default_properties.DEFAULT_SIZE_PROPERTIES.get('train')['width']
                    length = default_properties.DEFAULT_SIZE_PROPERTIES.get('train')['length']
                    height = default_properties.DEFAULT_SIZE_PROPERTIES.get('train')['height']
                elif asset_id == "tram":
                    vehicle_name = global_parameters.VEHICLE_NAME.get(asset_id.lower(),'tram')
                    width = default_properties.DEFAULT_SIZE_PROPERTIES.get('tram')['width']
                    length = default_properties.DEFAULT_SIZE_PROPERTIES.get('tram')['length']
                    height = default_properties.DEFAULT_SIZE_PROPERTIES.get('tram')['height']
                elif asset_id == "pedestrian":
                    vehicle_name = global_parameters.VEHICLE_NAME.get(asset_id.lower(),'human')
                    width = default_properties.DEFAULT_SIZE_PROPERTIES.get('human')['width']
                    length = default_properties.DEFAULT_SIZE_PROPERTIES.get('human')['length']
                    height = default_properties.DEFAULT_SIZE_PROPERTIES.get('human')['height']
                else:

                    vehicle_name = global_parameters.VEHICLE_NAME.get(asset_id.lower(),'car')
                    width = default_properties.DEFAULT_SIZE_PROPERTIES.get('car')['width']
                    length = default_properties.DEFAULT_SIZE_PROPERTIES.get('car')['length']
                    height = default_properties.DEFAULT_SIZE_PROPERTIES.get('car')['height']


                if obj_id and width and length and height:
                    obj_details[obj_id] = [width, length, height, str(asset_id), vehicle_name]

                else:
                    obj_details[obj_id] = [1.8, 4.5, 1.5, str(asset_id), vehicle_name]


                obj_list.append(obj_id)


    return obj_details, obj_list


def get_landmark_offset_obj(states_analysis):
    """
    Get the landmark offset for Obj
    Returns
    -------

    """
    landmark_offsets = {}
    for entity_id, entity_data in states_analysis.items():
        if 'ObjectActions' in entity_data:
            object_actions = entity_data['ObjectActions']
            for obj_name, obj_data in object_actions.items():
                for obj_action in obj_data:
                    if 'Parameters' in obj_action:
                        parameters = obj_action['Parameters']
                        for parameter in parameters:
                            landmark_offset = parameter.get(AMC.LandmarkOffset)
                            if landmark_offset is not None:
                                landmark_offsets[obj_name] = landmark_offset
    # print("Landmark offset for obj", landmark_offsets)
    return landmark_offsets


def get_Obj_set_lateral_relative(states_analysis):
    result = []

    for key, value in states_analysis.items():
        if 'ObjectActions' in value:
            for obj_key, actions in value['ObjectActions'].items():
                for action in actions:
                    if action['Action'] == ObjAPI.Obj_SetLateralRelativePosition:
                        result.append(action)

    return result[-1]["Parameters"]


def get_vehicle_braking_info(TBA_eval_key, states_analysis):
    """
    Get the vehicle braking info
    Parameters
    ----------
    TBA_eval_key

    Returns
    -------

    """
    driver_set_brake = {"Brake": 0}
    # TBA_eval_key = -1

    for k, v in states_analysis.items():
        if k != TBA_eval_key:
            for egoaction in v["EgoActions"]:
                try:
                    if egoaction["Action"] == EgoAPI.Dri_SetBrakePedal:
                        # print(k, egoaction["Action"], egoaction["Parameters"][0]["Position"])
                        driver_set_brake["Brake"] = int(egoaction["Parameters"][0]["Position"])

                        return driver_set_brake
                    else:
                        pass
                except:
                    pass
        else:
            driver_set_brake["Brake"] = -1
    return driver_set_brake


def get_vehicle_throttle_info(TBA_eval_key, states_analysis):
    """
    Get the vehicle throttle info
    Parameters
    ----------
    TBA_eval_key

    Returns
    -------

    """
    driver_set_acc = {"Throttle": 0}

    for k, v in states_analysis.items():
        if k != TBA_eval_key:
            for egoaction in v["EgoActions"]:
                # print("egoaction", egoaction)
                try:
                    if egoaction["Action"] == EgoAPI.Dri_SetAccelerationPedal:
                        # print(k, egoaction["Action"], egoaction["Parameters"][0]["Position"])
                        driver_set_acc["Throttle"] = int(egoaction["Parameters"][0]["Position"])
                        return driver_set_acc
                    else:
                        pass
                except:
                    driver_set_acc["Throttle"] = 5
                    return driver_set_acc
        else:
            driver_set_acc["Throttle"] = -1

    return driver_set_acc


def get_TBA_key_value(states_analysis):
    """
    Get the TBA key value
    Returns
    -------

    """
    TBA_eval_key = -1
    for k, v in states_analysis.items():
        #print("States_analysis: ", states_analysis)
        for egoaction in v["EgoActions"]:
            try:
                if egoaction["Action"] == OtherAPI.TBA_WriteEvaluationEvent:
                    if egoaction["Parameters"][0]['Type'] == "Stop":
                        TBA_eval_key = k
                        return TBA_eval_key
                else:
                    pass
                    # print("TBA_WriteEvaluationEvent not found.")
            except:
                pass
    return TBA_eval_key


def get_landmark_offset_ego(paramlist_analysis):
    """
    Get the Landmark offset of Ego
    Returns
    -------

    """
    envp_landmark_offset = 10.125
    ego_actions = paramlist_analysis['Default']['EgoActions']
    for ego_action in ego_actions:
        parameters = ego_action['Parameters']
        for parameter in parameters:
            envp_landmark_offset = parameter.get(AMC.LandmarkOffset)
    # print("LandmarkOffset for ego :", self.envp_landmark_offset)
    return envp_landmark_offset

def get_lane_selection_ego(paramlist_analysis):
    """
    Get the Landmark offset of Ego
    Returns
    -------

    """
    ego_actions = paramlist_analysis['Default']['EgoActions']
    for ego_action in ego_actions:
        parameters = ego_action['Parameters']
        for parameter in parameters:
            envp_lane_selection = parameter.get(AMC.LaneSelection)
    # print("LandmarkOffset for ego :", self.envp_landmark_offset)
    return envp_lane_selection
def get_lane_selection_object(states_analysis, target_name):
    extracted_info = {}
    for k, v in states_analysis.items():
        for obj_id, actions in v.get('ObjectActions', {}).items():
            for action in actions:
                if action.get('Action') == ObjAPI.Obj_Initialize:
                    for param in action.get('Parameters', []):
                        lane_selection = param.get('LaneSelection', 'Not Available')

                        # Append the object action information
                        obj_key = f'{obj_id}_Obj_Initialize'
                        if obj_key not in extracted_info:
                            extracted_info[obj_key] = []
                        extracted_info[obj_key].append(
                            {'LaneSelection': lane_selection})

    key_to_access = f"{target_name}_Obj_Initialize"
    if key_to_access in extracted_info:
        extracted_value = extracted_info[key_to_access]
        lane_selection = extracted_value[0]['LaneSelection']
    return lane_selection



# Testing for object
# def get_lane_selection_object(states_analysis,target_name):
#     """
#     Get the Landmark offset of Ego
#     Returns
#     -------

    # """



    # for k, v in states_analysis.items():
    #     for obj_id, actions in v.get('ObjectActions', {}).items():
    #         for action in actions:
    #             if action.get('Action') == ObjAPI.Obj_Initialize:
    #                 for param in action.get('Parameters', []):
    #                     if param.get('ObjectId') == target_name:
    #                         obj_lane_selection = param.get('LaneSelection')
    #
    #
    #     return obj_lane_selection

def get_landmark_offset(states_analysis, target_name):
    extracted_info = {}
    for k, v in states_analysis.items():
        for obj_id, actions in v.get('ObjectActions', {}).items():
            for action in actions:
                if action.get('Action') == ObjAPI.Obj_Initialize:
                    for param in action.get('Parameters', []):
                        landmark_offset= param.get('LandmarkOffset', 'Not Available')

                        # Append the object action information
                        obj_key = f'{obj_id}_Obj_Initialize'
                        if obj_key not in extracted_info:
                            extracted_info[obj_key] = []
                        extracted_info[obj_key].append(
                            {'LandmarkOffset':landmark_offset })


    key_to_access = f"{target_name}_Obj_Initialize"
    if key_to_access in extracted_info:
         extracted_value = extracted_info[key_to_access]
         landmark_offset =  float(extracted_value[0]['LandmarkOffset'])
    return landmark_offset

# def get_landmark_offset(states_analysis,target_name):
#
#     for k, v in states_analysis.items():
#         for obj_id, actions in v.get('ObjectActions', {}).items():
#             for action in actions:
#                 if action.get('Action') == ObjAPI.Obj_Initialize:
#                     for param in action.get('Parameters', []):
#                         if param.get('ObjectId') == target_name:
#                             landmark_offset = param.get('LandmarkOffset')

        # return landmark_offset