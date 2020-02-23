get_ipython().system(u'pip install pint')
# Configure Jupyter so figures appear in the notebook
get_ipython().magic(u'matplotlib inline')

# Configure Jupyter to display the assigned value after an assignment
get_ipython().magic(u"config InteractiveShell.ast_node_interactivity='last_expr_or_assign'")

# import functions from the modsim library
from modsim import *

# set the random number generator
np.random.seed(7)

"""Start a new Cell Here"""

bikeshare = State(Brooklyn=10, Manhattan=2, Co2Subway=0, Co2Car=0, ride=0)
rideswithcar = TimeSeries()
rideswithtrain = TimeSeries()
rideswithbike = TimeSeries()

def bike_to_Manhattan(state):
    """Move one bike from Brooklyn to Manhattan.
    state: bikeshare State object
    """
    if state.Brooklyn == 0:
        return
    state.Brooklyn -= 1
    state.Manhattan += 1


def bike_to_Brooklyn(state):
    """Move one bike from Manhatten to Brooklyn.
    state: bikeshare State object
    """
    if state.Manhattan == 0:
        return
    state.Manhattan -= 1
    state.Brooklyn += 1


def step(state, p1, p2):
    if flip(p1):
        bike_to_Manhattan(state)
        state.ride += 1

    if flip(p2):
        bike_to_Brooklyn(state)
        state.ride += 1

def CO2SavedfromCar(state):
    """ The average passenger vehicle emits about 404 grams of CO2 per mile
        https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle
        Average distance between Downtown Brooklyn and the Lower East Side is 2 miles
        404 * 2 = 808, 808 grams = 1.78134~ lbs"""
    return state.ride * 1.78
    
def Co2SavedfromTrain(state):
    # We will use the data collected in the bikeshare model to calculate how much Co2 Emmissions were saved
    """An average commute by passenger vehicle causes the emission of over 4,000 pounds of CO2 per year
       An average commute of the same distance via subway is responsible for just 820 pounds of CO2 per year
       A walking or bicycling commute generates zero CO2 emissions.
       Source: https://www.transalt.org/sites/default/files/news/reports/2008/Rolling_Carbon.pdf """

    # Subways in New York run almost every day
    # To figure out how much CO2 emmissions a single Subway ride causes we will
    # Assume a subway train runs at least once a day everyday for a year
    # So that gives us 820/365 which is approximately 3 pounds of CO2 emmisions per ride

    return state.ride * 3


"""Start a new Cell Here"""

for m in range(365):
    for i in range(200):
        step(bikeshare, .3, .3)
    rideswithtrain[m] = Co2SavedfromTrain(bikeshare)
    rideswithcar[m] = CO2SavedfromCar(bikeshare)
    rideswithbike[m] = 0
bikeshare.Co2Car = bikeshare.ride * 1.78
bikeshare.Co2Subway = bikeshare.ride * 3
bikeshare

"""New Cell"""
plot(rideswithtrain,"--",label="train")
plot(rideswithcar,"-",label="car")
plot(rideswithbike,"-.",label="bike")
decorate(title='Amount of CO2 Saved',xlabel='Days',ylabel='Lbs of Co2')