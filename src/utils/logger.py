import logging

logging.basicConfig(
    filename='pentest_automation.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def safe_run(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
        logging.info(f"Successfully executed {function.__name__}")
    except Exception as e:
        logging.error(f"Error in {function.__name__}: {e}")
