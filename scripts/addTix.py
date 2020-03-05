import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src import *
from datetime import date, timedelta
import time


if __name__ == "__main__":
    db = Database()
    cards = getCards();
    
