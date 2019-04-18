from UserInfo import *
from FlightInfo import *
import Const
from FlightImplements import *


def orderTicket(usr, flightInfo):
    """
    用户订票
    :param usr:
    :type usr: dict
    :param flightInfo: dict{"origin":"", "terminal":"", "date":{}}
    :return: bool
    """
    revFlightInfo()

