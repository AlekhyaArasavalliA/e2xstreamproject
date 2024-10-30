# import os
# import sys
# import logging
# import argparse
# import time
# from pathlib import Path
# from e2xostream.src import E2X_Convert
# import platform
#
# # Configure logging to write to both the console and a file in the user's home directory
# log_file_path = os.path.join(os.path.expanduser("~"), 'generate_doc.log')
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
#
# # Create file handler which logs to a file
# file_handler = logging.FileHandler(log_file_path)
# file_handler.setLevel(logging.DEBUG)
#
# # Create console handler which logs to the console (CMD)
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
#
# # Create a formatter and set it for both handlers
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)
#
# # Add both handlers to the logger
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)
#
# logger.info("Logging initialized successfully.")
#
# MAIN_PATH = os.path.abspath(os.path.join(__file__, "..", ".."))
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
# def create_path_if_not_exists(path):
#     """
#     Create the path if not exists
#     """
#     if not os.path.exists(path):
#         os.makedirs(path)
#         logger.info(f"Path '{path}' created.")
#     else:
#         logger.info(f"Path '{path}' already exists.")
#
#
# def find_and_read_xebtb_files(directory):
#     """
#     Find the EBTB files and read the content
#     """
#     ebtb_files = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.xebtb'):
#                 filepath = os.path.join(root, file)
#                 ebtb_files.append(filepath)
#
#     logger.debug(f"Found {len(ebtb_files)} .xebtb files in directory '{directory}'.")
#     return ebtb_files
#
#
# def args_data():
#     """
#     Read the arguments passed to this script
#     """
#     parser = argparse.ArgumentParser(description="Read the XEBTB files from a directory or direct file and "
#                                                  "read the user choice function")
#     parser.add_argument('--ebtb', type=str, required=True,
#                         help="The path to the .xebtb file or directory containing .xebtb files")
#     parser.add_argument('--function', type=str, required=True,
#                         help="The function to convert and create folder")
#     parser.add_argument('--report', type=str, required=True, help="XOSC result output path")
#     parser.add_argument('--esmini', default="False", type=str, required=False, help="Use esmini simulator")
#
#     args = parser.parse_args()
#
#     esmini_tool_path = None
#     if str(args.esmini) == "True":
#         if platform.system() == "Linux":
#             esmini_tool_path = os.path.join(CURRENT_WORKING_DIRECTORY, "stk", "simulator_tools", "esmini_linux", "esmini")
#         elif platform.system() == "Windows":
#             esmini_tool_path = os.path.join(CURRENT_WORKING_DIRECTORY, "stk", "simulator_tools", "esmini_win", "esmini")
#
#     create_path_if_not_exists(args.report)
#
#     if os.path.isfile(args.ebtb) and args.ebtb.endswith('.xebtb'):
#         logger.info(f"Provided path is a single .xebtb file: {args.ebtb}")
#         return args.ebtb, args.function, args.report, esmini_tool_path
#     elif os.path.isdir(args.ebtb):
#         logger.info(f"Provided path is a directory: {args.ebtb}")
#         return find_and_read_xebtb_files(args.ebtb), args.function, args.report, esmini_tool_path
#     else:
#         logger.error("The provided path is neither a .xebtb file nor a directory.")
#         sys.exit(1)
#
#
# # ... [other imports and logging setup] ...
#
# class E2XOStream:
#     def __init__(self, **kwargs):
#         """Constructor with kwargs."""
#         self.Kwargs = kwargs
#         self.function_map = {
#             # Mapping of available functions
#         }
#
#     def dispatch(self, key, *args, **kwargs):
#         if key in self.function_map:
#             return self.function_map[key](*args, **kwargs)
#         else:
#             message = f"No function mapped to {key}"
#             logger.warning(message)
#             print(message)
#
#     def XOSCStream(self, destination_directory, original_file_path, xml_file_path, report_path, esmini_path):
#         """
#         Define scenario streamline
#         """
#         destination_file_path = os.path.join(destination_directory, f"{Path(xml_file_path).stem}.xosc")
#         self.dispatch('some_key')  # Example usage, replace with actual logic
#         separator = "*" * 20
#         logger.info(f"{separator}\nEBTB Input File: {xml_file_path}\n")
#         logger.info(f"XOSC generated at: {destination_file_path}\n{separator}\n")
#
#
# if __name__ == "__main__":
#     # ... [argument parsing and initializations] ...
#
#     E2XObj = E2XOStream()
#
#     if os.path.isfile(xml_file_path) and xml_file_path.endswith('.xebtb'):
#         E2XObj.XOSCStream(destination_directory=destination_directory,
#                           original_file_path=original_file_path,
#                           xml_file_path=xml_file_path,
#                           report_path=report_path,
#                           esmini_path=esmini_path)
#         logger.info(f"Processed file: {xml_file_path}")
#     else:
#         for xml_file in xml_file_path:
#             E2XObj.XOSCStream(destination_directory=destination_directory,
#                               original_file_path=original_file_path,
#                               xml_file_path=xml_file,
#                               report_path=report_path,
#                               esmini_path=esmini_path)
#             logger.info(f"Processed file: {xml_file}")
#             time.sleep(1)
#
#     logger.info("Script execution finished.")



# import os
# import sys
# import logging
# import argparse
# import time
# from pathlib import Path
# from e2xostream.src import E2X_Convert
# import platform
#
# # Configure logging to write to both the console and a file in the user's home directory
# log_file_path = os.path.join(os.path.expanduser("~"), 'generate_doc.log')
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
#
# # Create file handler which logs to a file
# file_handler = logging.FileHandler(log_file_path)
# file_handler.setLevel(logging.DEBUG)
#
# # Create console handler which logs to the console (CMD)
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
#
# # Create a formatter and set it for both handlers
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)
#
# # Add both handlers to the logger
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)
#
# logger.info("Logging initialized successfully.")
#
# MAIN_PATH = os.path.abspath(os.path.join(__file__, "..", ".."))
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
# def create_path_if_not_exists(path):
#     """
#     Create the path if not exists
#     """
#     if not os.path.exists(path):
#         os.makedirs(path)
#         logger.info(f"Path '{path}' created.")
#     else:
#         logger.info(f"Path '{path}' already exists.")
#
#
# def find_and_read_xebtb_files(directory):
#     """
#     Find the EBTB files and read the content
#     """
#     ebtb_files = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.xebtb'):
#                 filepath = os.path.join(root, file)
#                 ebtb_files.append(filepath)
#
#     logger.debug(f"Found {len(ebtb_files)} .xebtb files in directory '{directory}'.")
#     return ebtb_files
#
#
# def args_data():
#     """
#     Read the arguments passed to this script
#     """
#     parser = argparse.ArgumentParser(description="Read the XEBTB files from a directory or direct file and "
#                                                  "read the user choice function")
#     parser.add_argument('--ebtb', type=str, required=True,
#                         help="The path to the .xebtb file or directory containing .xebtb files")
#     parser.add_argument('--function', type=str, required=True,
#                         help="The function to convert and create folder")
#     parser.add_argument('--report', type=str, required=True, help="XOSC result output path")
#     parser.add_argument('--esmini', default="False", type=str, required=False, help="Use esmini simulator")
#
#     args = parser.parse_args()
#
#     esmini_tool_path = None
#     if str(args.esmini) == "True":
#         if platform.system() == "Linux":
#             esmini_tool_path = os.path.join(CURRENT_WORKING_DIRECTORY, "stk", "simulator_tools", "esmini_linux", "esmini")
#         elif platform.system() == "Windows":
#             esmini_tool_path = os.path.join(CURRENT_WORKING_DIRECTORY, "stk", "simulator_tools", "esmini_win", "esmini")
#
#     create_path_if_not_exists(args.report)
#
#     if os.path.isfile(args.ebtb) and args.ebtb.endswith('.xebtb'):
#         logger.info(f"Provided path is a single .xebtb file: {args.ebtb}")
#         return args.ebtb, args.function, args.report, esmini_tool_path
#     elif os.path.isdir(args.ebtb):
#         logger.info(f"Provided path is a directory: {args.ebtb}")
#         return find_and_read_xebtb_files(args.ebtb), args.function, args.report, esmini_tool_path
#     else:
#         logger.error("The provided path is neither a .xebtb file nor a directory.")
#         sys.exit(1)
#
#
# class E2XOStream:
#     def __init__(self, **kwargs):
#         """Constructor with kwargs."""
#         self.Kwargs = kwargs
#         self.function_map = {
#             # Mapping of available functions
#         }
#
#     def dispatch(self, key, *args, **kwargs):
#         if key in self.function_map:
#             return self.function_map[key](*args, **kwargs)
#         else:
#             message = f"No function mapped to {key}"
#             logger.warning(message)  # Log this message to the log file and console
#             print(message)  # Also print to console
#
#     def XOSCStream(self, destination_directory, original_file_path, xml_file_path, report_path, esmini_path):
#         """
#         Define scenario streamline
#         """
#         original_file_path = os.path.join(original_file_path, "XOSCScenarioDevelop0.xosc")
#         new_file_path = str(Path(xml_file_path).stem) + ".xosc"
#         self.dispatch('some_key')  # Example of dispatch usage
#         # Other operations...
#         separator = "*" * 20
#         logger.info(f"{separator}\nEBTB Input File: {xml_file_path}\n")
#         logger.info(f"XOSC generated at: {destination_directory}\n{separator}\n")
#
#
# if __name__ == "__main__":
#     """
#     Execute the main script
#     """
#     logger.info("Script execution started.")
#     try:
#         xml_file_path, function, report_path, esmini_path = args_data()
#         original_file_path = os.path.join(report_path, "xosc")
#         destination_directory = Path(os.path.join(report_path, "FinalXOSC", str(function)))
#
#         E2XObj = E2XOStream()
#
#         if os.path.isfile(xml_file_path) and xml_file_path.endswith('.xebtb'):
#             E2XObj.XOSCStream(destination_directory=destination_directory,
#                               original_file_path=original_file_path,
#                               xml_file_path=xml_file_path,
#                               report_path=report_path,
#                               esmini_path=esmini_path)
#             logger.info(f"Processed file: {xml_file_path}")
#         else:
#             for xml_file in xml_file_path:
#                 E2XObj.XOSCStream(destination_directory=destination_directory,
#                                   original_file_path=original_file_path,
#                                   xml_file_path=xml_file,
#                                   report_path=report_path,
#                                   esmini_path=esmini_path)
#                 logger.info(f"Processed file: {xml_file}")
#                 time.sleep(1)
#
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")
#
#     logger.info("Script execution finished.")



import os
import sys
import argparse
import time
import logging
from pathlib import Path
from e2xostream.src import E2X_Convert
import platform

# Configure logging to write to both the console and a file in the user's home directory
log_file_path = os.path.join(os.path.expanduser("~"), 'script.log')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create file handler which logs to a file
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

# Create console handler which logs to the console (CMD)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Logging initialized successfully.")

MAIN_PATH = os.path.abspath(os.path.join(__file__, "..", ".."))
CURRENT_WORKING_FILE_DIRECTORY = os.path.abspath(os.path.join(__file__))
CURRENT_WORKING_DIRECTORY = os.path.abspath(os.path.join(__file__, ".."))

if MAIN_PATH not in sys.path:
    sys.path.append(MAIN_PATH)

dir_path = os.path.dirname(os.path.realpath(__file__))
for root, dirs, files in os.walk(dir_path):
    sys.path.append(root)

def create_path_if_not_exists(path):
    """
    Create the path if not exists
    """
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Path '{path}' created.")
    else:
        logger.info(f"Path '{path}' already exists.")

def find_and_read_xebtb_files(directory):
    """
    Find the EBTB files and read the content
    """
    ebtb_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xebtb'):
                filepath = os.path.join(root, file)
                ebtb_files.append(filepath)

    logger.debug(f"Found {len(ebtb_files)} .xebtb files in directory '{directory}'.")
    return ebtb_files

def args_data():
    """
    Read the arguments passed to this script
    """
    parser = argparse.ArgumentParser(description="Read the XEBTB files from a directory or direct file and "
                                                 "read the user choice function")
    parser.add_argument('--ebtb', type=str, required=True,
                        help="The path to the .xebtb file or directory containing .xebtb files")
    parser.add_argument('--function', type=str, required=True,
                        help="The function to convert and create folder")
    parser.add_argument('--report', type=str, required=True, help="XOSC result output path")
    parser.add_argument('--esmini', default="False", type=str, required=False, help="Use esmini simulator")

    args = parser.parse_args()

    esmini_tool_path = None
    if str(args.esmini) == "True":
        if platform.system() == "Linux":
            esmini_tool_path = os.path.join(CURRENT_WORKING_DIRECTORY, "stk", "simulator_tools", "esmini_linux", "esmini")
        elif platform.system() == "Windows":
            esmini_tool_path = os.path.join(CURRENT_WORKING_DIRECTORY, "stk", "simulator_tools", "esmini_win", "esmini")

    create_path_if_not_exists(args.report)

    if os.path.isfile(args.ebtb) and args.ebtb.endswith('.xebtb'):
        logger.info(f"Provided path is a single .xebtb file: {args.ebtb}")
        return args.ebtb, args.function, args.report, esmini_tool_path
    elif os.path.isdir(args.ebtb):
        logger.info(f"Provided path is a directory: {args.ebtb}")
        return find_and_read_xebtb_files(args.ebtb), args.function, args.report, esmini_tool_path
    else:
        logger.error("The provided path is neither a .xebtb file nor a directory.")
        sys.exit(1)

if __name__ == "__main__":
    """
    Execute the main script
    """
    logger.info("Script execution started.")
    try:
        xml_file_path, function, report_path, esmini_path = args_data()
        original_file_path = os.path.join(report_path, "xosc")
        destination_directory = Path(os.path.join(report_path, "FinalXOSC", str(function)))

        E2XObj = E2X_Convert.E2XOStream()

        if os.path.isfile(xml_file_path) and xml_file_path.endswith('.xebtb'):
            E2XObj.XOSCStream(destination_directory=destination_directory,
                              original_file_path=original_file_path,
                              xml_file_path=xml_file_path,
                              report_path=report_path,
                              esmini_path=esmini_path)
            logger.info(f"Processed file: {xml_file_path}")
        else:
            for xml_file in xml_file_path:
                E2XObj.XOSCStream(destination_directory=destination_directory,
                                  original_file_path=original_file_path,
                                  xml_file_path=xml_file,
                                  report_path=report_path,
                                  esmini_path=esmini_path)
                logger.info(f"Processed file: {xml_file}")
                time.sleep(1)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        for xml_file in xml_file_path:
            try:
                E2XObj.XOSCStream(destination_directory=destination_directory,
                                  original_file_path=original_file_path,
                                  xml_file_path=xml_file,
                                  report_path=report_path,
                                  esmini_path=esmini_path)
                logger.info(f"Processed file in exception handler: {xml_file}")
                time.sleep(1)
            except Exception as ex:
                logger.error(f"Failed to process file {xml_file}: {str(ex)}")

    logger.info("Script execution finished.")



# import os
# import sys
# import argparse
# import time
# import logging
# from pathlib import Path
# from e2xostream.src import E2X_Convert
# import platform
#
# # Create a custom FileHandler class to ensure that logs are flushed immediately
# class FlushFileHandler(logging.FileHandler):
#     def emit(self, record):
#         super().emit(record)
#         self.flush()  # Flush after every log record
#
# # Configure logging to write to both the console and a file in the user's home directory
# log_file_path = os.path.join(os.path.expanduser("~"), 'script.log')
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
#
# # Create file handler which logs to a file
# file_handler = FlushFileHandler(log_file_path, mode='a')
# file_handler.setLevel(logging.DEBUG)
#
# # Create console handler which logs to the console (CMD)
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
#
# # Create a formatter and set it for both handlers
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)
#
# # Add both handlers to the logger
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)
#
# logger.info("Logging initialized successfully.")
#
# MAIN_PATH = os.path.abspath(os.path.join(__file__, "..", ".."))
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
# def create_path_if_not_exists(path):
#     """
#     Create the path if not exists
#     """
#     if not os.path.exists(path):
#         os.makedirs(path)
#         logger.info(f"Path '{path}' created.")
#     else:
#         logger.info(f"Path '{path}' already exists.")
#
# def find_and_read_xebtb_files(directory):
#     """
#     Find the EBTB files and read the content
#     """
#     ebtb_files = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.xebtb'):
#                 filepath = os.path.join(root, file)
#                 ebtb_files.append(filepath)
#
#     logger.debug(f"Found {len(ebtb_files)} .xebtb files in directory '{directory}'.")
#     return ebtb_files
#
# def args_data():
#     """
#     Read the arguments passed to this script
#     """
#     parser = argparse.ArgumentParser(description="Read the XEBTB files from a directory or direct file and "
#                                                  "read the user choice function")
#     parser.add_argument('--ebtb', type=str, required=True,
#                         help="The path to the .xebtb file or directory containing .xebtb files")
#     parser.add_argument('--function', type=str, required=True,
#                         help="The function to convert and create folder")
#     parser.add_argument('--report', type=str, required=True, help="XOSC result output path")
#     parser.add_argument('--esmini', default="False", type=str, required=False, help="Use esmini simulator")
#
#     args = parser.parse_args()
#
#     esmini_tool_path = None
#     if str(args.esmini) == "True":
#         if platform.system() == "Linux":
#             esmini_tool_path = os.path.join(CURRENT_WORKING_DIRECTORY, "stk", "simulator_tools", "esmini_linux", "esmini")
#         elif platform.system() == "Windows":
#             esmini_tool_path = os.path.join(CURRENT_WORKING_DIRECTORY, "stk", "simulator_tools", "esmini_win", "esmini")
#
#     create_path_if_not_exists(args.report)
#
#     if os.path.isfile(args.ebtb) and args.ebtb.endswith('.xebtb'):
#         logger.info(f"Provided path is a single .xebtb file: {args.ebtb}")
#         return args.ebtb, args.function, args.report, esmini_tool_path
#     elif os.path.isdir(args.ebtb):
#         logger.info(f"Provided path is a directory: {args.ebtb}")
#         return find_and_read_xebtb_files(args.ebtb), args.function, args.report, esmini_tool_path
#     else:
#         logger.error("The provided path is neither a .xebtb file nor a directory.")
#         sys.exit(1)
#
# if __name__ == "__main__":
#     """
#     Execute the main script
#     """
#     logger.info("Script execution started.")
#     try:
#         xml_file_path, function, report_path, esmini_path = args_data()
#         original_file_path = os.path.join(report_path, "xosc")
#         destination_directory = Path(os.path.join(report_path, "FinalXOSC", str(function)))
#
#         E2XObj = E2X_Convert.E2XOStream()
#
#         if os.path.isfile(xml_file_path) and xml_file_path.endswith('.xebtb'):
#             E2XObj.XOSCStream(destination_directory=destination_directory,
#                               original_file_path=original_file_path,
#                               xml_file_path=xml_file_path,
#                               report_path=report_path,
#                               esmini_path=esmini_path)
#             logger.info(f"Processed file: {xml_file_path}")
#         else:
#             for xml_file in xml_file_path:
#                 E2XObj.XOSCStream(destination_directory=destination_directory,
#                                   original_file_path=original_file_path,
#                                   xml_file_path=xml_file,
#                                   report_path=report_path,
#                                   esmini_path=esmini_path)
#                 logger.info(f"Processed file: {xml_file}")
#                 time.sleep(1)
#
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")
#         if isinstance(xml_file_path, list):
#             for xml_file in xml_file_path:
#                 try:
#                     E2XObj.XOSCStream(destination_directory=destination_directory,
#                                       original_file_path=original_file_path,
#                                       xml_file_path=xml_file,
#                                       report_path=report_path,
#                                       esmini_path=esmini_path)
#                     logger.info(f"Processed file in exception handler: {xml_file}")
#                     time.sleep(1)
#                 except Exception as ex:
#                     logger.error(f"Failed to process file {xml_file}: {str(ex)}")
#         else:
#             logger.error(f"Failed to process single file {xml_file_path}")
#
#     logger.info("Script execution finished.")





# if __name__ == "__main__":
#     logger.info("Script execution started.")
#     try:
#         xml_file_path, function, report_path, esmini_path = args_data()
#         original_file_path = os.path.join(report_path, "xosc")
#         destination_directory = Path(os.path.join(report_path, "FinalXOSC", str(function)))
#
#         # Create the E2XOStream object
#         E2XObj = E2X_Convert.E2XOStream()
#
#         # Log the function (key) and attempt dispatch
#         logger.info(f"Dispatching function '{function}' for file(s): {xml_file_path}")
#
#         if os.path.isfile(xml_file_path) and xml_file_path.endswith('.xebtb'):
#             logger.debug(f"Processing single .xebtb file: {xml_file_path}")
#             result = E2XObj.dispatch(function, destination_directory=destination_directory,
#                                      original_file_path=original_file_path,
#                                      xml_file_path=xml_file_path,
#                                      report_path=report_path,
#                                      esmini_path=esmini_path)
#
#             if result is None:
#                 logger.error(f"Function '{function}' not mapped. Processing halted for file: {xml_file_path}")
#             else:
#                 logger.info(f"Processed file: {xml_file_path}")
#         else:
#             for xml_file in xml_file_path:
#                 logger.debug(f"Processing .xebtb file: {xml_file}")
#                 result = E2XObj.dispatch(function, destination_directory=destination_directory,
#                                          original_file_path=original_file_path,
#                                          xml_file_path=xml_file,
#                                          report_path=report_path,
#                                          esmini_path=esmini_path)
#
#                 if result is None:
#                     logger.error(f"Function '{function}' not mapped. Processing halted for file: {xml_file}")
#                 else:
#                     logger.info(f"Processed file: {xml_file}")
#                 time.sleep(1)
#
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")
#         if isinstance(xml_file_path, list):
#             for xml_file in xml_file_path:
#                 try:
#                     logger.debug(f"Attempting to process file in exception handler: {xml_file}")
#                     result = E2XObj.dispatch(function, destination_directory=destination_directory,
#                                              original_file_path=original_file_path,
#                                              xml_file_path=xml_file,
#                                              report_path=report_path,
#                                              esmini_path=esmini_path)
#                     if result is None:
#                         logger.error(f"Function '{function}' not mapped. Processing halted for file: {xml_file}")
#                     else:
#                         logger.info(f"Processed file in exception handler: {xml_file}")
#                     time.sleep(1)
#                 except Exception as ex:
#                     logger.error(f"Failed to process file {xml_file}: {str(ex)}")
#         else:
#             logger.error(f"Failed to process single file {xml_file_path}")
#
#     logger.info("Script execution finished.")
