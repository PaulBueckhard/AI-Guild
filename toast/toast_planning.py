#############################################
# Here's the set of actions. They have the following meaning:
# - plug_in_toaster will connect the toaster to the socket, if it isn't already connected
# - unplug_toaster will disconnect the toaster from the socket.
#        If toaster is on, it switches to off automatically.
# - put_in_bread will move the bread from plate to toaster. 
#        This is only possible if the toaster is switched off.
# - take_out_brad will move the bread from toaster to plate. 
#        This is only possible if the toaster is switched off.
# - switch_on_toaster will switch the toaster on, if it is not on already.
# - wait will wait for a while. 
#       If the toaster is switched on, it will switch off.
#       If the toaster is switched on and contains bread, the bread will be toasted afterwards
#
# Each action will take one time unit to execute. Except for wait. That takes 10 time units
##############################################
actions=(
    "plug_in_toaster",
    "unplug_toaster",
    "put_in_bread",
    "take_out_bread",
    "switch_on_toaster",
    "wait")

##############################################
# Heres the model of the state. 
# It contains two variables that describe the toaster:
# - toaster_has_power: indicates whether the toaster is connected to the socket
# - toaster_is_on: Indicates whether the toaster is currently on or off
# It contains two variables that describe the bread:
# - bread_location: whether the bread is currently on the plate or in the toaster
# - bread_state: untoasted or toasted?
# In addition, we have one variable time which measures how long the process takes. This is an additional quality measure, as we may want to toast the bread in as little time as possible. 
#
# note that this is just an example of one start state. We will test your function with different start states.
##############################################
state={
    "toaster_has_power":False,
    "toaster_is_on":False,
    "bread_location":"plate",
    "bread_state":"untoasted",
    "time":0
    }

##############################################
# This function implements the goal.
# The toasting process is considered successfull, if the bread is on the plate and toasted.
##############################################
def goal(state):
    return state["bread_location"] == "plate" and state["bread_state"] == "toasted"

##############################################
# The state transition function. 
# It implements the meaning of actions, as described for the action variable.
##############################################
def state_transition(state, action):
    newState = state.copy()
    if action =="plug_in_toaster":
        # toaster now has power
        newState["toaster_has_power"] = True
        newState["time"] += 1
    elif action =="unplug_toaster":
        # unpower toaster and stop toasting process
        newState["toaster_has_power"] = False
        newState["toaster_is_on"] = False
        newState["time"] += 1
    elif action == "put_in_bread":
        # move bread into toaster. Only possible if toaster is not on (casue it locks)
        if not newState["toaster_is_on"]:
            newState["bread_location"] = "toaster"
        newState["time"] += 1
    elif action == "take_out_bread":
        # move bread from toaster to plate. Only possible if toaster is not on (casue it locks)
        if not newState["toaster_is_on"]:
            newState["bread_location"]="plate"
        newState["time"] += 1
    elif action == "switch_on_toaster": 
        # switch on the toaster
        if(newState["toaster_has_power"]):
            newState["toaster_is_on"]=True
        newState["time"] += 1
    elif action == "wait":
        # wait for ten steps
        newState["time"] += 10
        # if toaster is on, it is switched off, if bread was in toaster, it is toasted now.
        if newState["toaster_is_on"]:
            if newState["bread_location"] == "toaster":
                newState["bread_state"] = "toasted"
            else:
                print(newState["bread_location"])
            newState["toaster_is_on"] = False
    return newState

####################################################
# This is the function you should be implementing for this exercise.
# The function gets a start state as input and should output a python list of actions that fulfill the goal
# I recommend implementing it the three following ways (with rising difficulty:)
# 1) Implement breadth first search first.
# 2) Implement a function that also optimizes the final value of the parameter "time"
# 3) Implement a function that fulfills 2) and is as fast as possible!
###################################################
def plan(start_state):
    queue = [(start_state, [])]
    front = 0  # Index of the front element in the queue

    while front < len(queue):
        current_state, current_plan = queue[front]
        front += 1

        # Check if the current state satisfies the goal
        if goal(current_state):
            return current_plan

        # Generate possible actions and explore new states
        for action in actions:
            new_state = state_transition(current_state, action)

            # Only consider valid actions that lead to a new state
            if new_state != current_state:
                new_plan = current_plan + [action]
                queue.append((new_state, new_plan))

    # If no plan is found, return an empty list
    return []


# this is a test function. It tests your plan function 
def test(start_state):
    print("\n\n testing:",start_state)

    # call plan function
    sequence = plan(start_state)
    print("\t found sequence:",sequence)

    # apply plan to start state
    state = start_state
    for action in sequence:
        state = state_transition(state,action)
    
    # check whether result fulfills the goal
    print("\t fulfills goal?", goal(state))
    print("\t in world time",state["time"])

# execute the test for a few test cases
test(state)
test({'toaster_has_power': True, 'toaster_is_on': False, 'bread_location': 'toaster', 'bread_state': 'untoasted', 'time': 0})
test({'toaster_has_power': True, 'toaster_is_on': True, 'bread_location': 'plate', 'bread_state': 'untoasted', 'time': 0})
test({'toaster_has_power': False, 'toaster_is_on': True, 'bread_location': 'plate', 'bread_state': 'untoasted', 'time': 0})


