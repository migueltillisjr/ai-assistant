import logging

#Configure logging
logging.basicConfig(level=logging.INFO, filename="app.log", filemode="a", format='%(asctime)s - %(name)s - %(levelname)s %(message)s')