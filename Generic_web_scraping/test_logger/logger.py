# # import logging
# # import sys
# # from logging.handlers import TimedRotatingFileHandler
# # FORMATTER = log_formatter = logging.Formatter(
# #     '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# # LOG_FILE = "my_app.log"


# # def get_console_handler():
# #     console_handler = logging.StreamHandler(sys.stdout)
# #     console_handler.setFormatter(FORMATTER)
# #     return console_handler


# # def get_file_handler():
# #     #    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
# #     file_handler = TimedRotatingFileHandler(LOG_FILE,
# #                                             when="m",
# #                                             interval=1,
# #                                             backupCount=5)
# #     file_handler.setFormatter(FORMATTER)
# #     return file_handler


# # def get_logger(logger_name):
# #     logger = logging.getLogger(logger_name)
# #     # better to have too much log than not enough
# #     logger.setLevel(logging.INFO)
# #     logger.addHandler(get_console_handler())
# #     logger.addHandler(get_file_handler())
# #     # with this pattern, it's rarely necessary to propagate the error up to parent
# #     logger.propagate = False
# #     return logger


# # ---------------------------------------------------------------------------------------------------

# import logging
# import sys
# from logging.handlers import TimedRotatingFileHandler

# # FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
# FORMATTER = log_formatter = logging.Formatter(
#     '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# LOG_FILE = "my_app.log"


# def get_console_handler():
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setFormatter(FORMATTER)
#     return console_handler


# def get_file_handler():
#     file_handler = TimedRotatingFileHandler(LOG_FILE,  when='midnight')

#     # file_handler = TimedRotatingFileHandler(
#         # LOG_FILE, when="m", interval=1, backupCount=5)
#     file_handler.setFormatter(FORMATTER)
#     return file_handler

# def create_timed_rotating_log(path):
#     """"""
#     logger = logging.getLogger("Rotating Log")
#     log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s(%(lineno)d) %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#     logger.setLevel(logging.INFO)
    
#     handler = TimedRotatingFileHandler(path,
#                                        when="m",
#                                        interval=1,
#                                        backupCount=5)
#     logger.addHandler(handler)
#     handler.setFormatter(log_formatter)
#     for i in range(1):
#         logger.info("Started")
        
    
# def get_logger(logger_name):
#     logger = logging.getLogger(logger_name)
#     # better to have too much log than not enough
#     logger.setLevel(logging.DEBUG)
#     # logger.addHandler(get_console_handler())
#     logger.addHandler(get_file_handler())
#     # create_timed_rotating_log(LOG_FILE)
#     # with this pattern, it's rarely necessary to propagate the error up to parent
#     logger.propagate = False
#     return logger
