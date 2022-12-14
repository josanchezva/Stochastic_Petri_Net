import random

from .spn import *
from .spn_io import *
from .RNGFactory import *

SIMULATION_TIME = 0
VERBOSITY = 0
PROTOCOL = False


def reset_state(spn: SPN):
    None


def complete_statistics():
    None


def set_firing_time(transition: Transition):
    """Sets the firing time of a transition based on the transition type and distribution"""
    transition.enabled_at = SIMULATION_TIME

    if transition.t_type == "I":
        transition.firing_delay = 0.0
    elif transition.t_type == "T" and transition.distribution == "DET":
        transition.firing_delay = transition.dist_par1
    elif transition.t_type == "T" and transition.distribution == "EXP":
        transition.firing_delay = get_delay("EXP", lmbda=transition.dist_par1)
    elif transition.t_type == "T" and transition.distribution == "NORM":
        transition.firing_delay = get_delay(
            "NORM", a=transition.dist_par1, b=transition.dist_par2)
    else:
        raise Exception(
            "Distribution undefined for transition {}".format(transition))

    transition.firing_time = transition.enabled_at + transition.firing_delay


def is_enabled(transition: Transition):
    """Checks wheter a transition is currently enabled"""
    input_arcs = transition.input_arcs
    inhibitor_arcs = transition.inhibitor_arcs

    arc: InhibitorArc
    for arc in inhibitor_arcs:
        if arc.from_place.n_tokens > 0:
            #print("inhibitor arc is blocking transition: " + transition.label)
            return False

    arc: InputArc
    for arc in input_arcs:
        if arc.from_place.n_tokens > 0:
            continue
        else:
            #print("not enough tokens to enable transition: " + transition.label)
            return False
    return True


def update_enabled_flag(spn: SPN):
    """Updates the enabled flag for all transitions in a SPN"""
    transition: Transition
    for transition in spn.transitions:
        if is_enabled(transition) == True:
            transition.enabled = True
            if transition.firing_time == 0:
                set_firing_time(transition)
            else:
                continue
        else:
            continue


def fire_transition(transition: Transition):
    """Fires a transition"""
    output_arcs = transition.output_arcs
    input_arcs = transition.input_arcs

    oarc: OutputArc
    place: Place
    for oarc in output_arcs:
        place = oarc.to_place
        # needs to be changed based on multiplicity of arc
        place.add_n_tokens(1)
        place.time_changed = SIMULATION_TIME
        if PROTOCOL == True:
            write_to_protocol(place.label, SIMULATION_TIME, place.n_tokens)

    iarc: InputArc
    for iarc in input_arcs:
        place = iarc.from_place
        # needs to be changed based on multiplicity of arc
        place.remove_n_tokens(1)
        place.time_changed = SIMULATION_TIME
        if PROTOCOL == True:
            write_to_protocol(place.label, SIMULATION_TIME, place.n_tokens)

    transition.n_times_fired += 1
    transition.reset()


def find_next_firing(spn: SPN):
    """Finds the next transition that need to be fired based on min(firing times)"""
    firing_times = {}
    transition: Transition
    for transition in spn.transitions:
        if transition.enabled == False:
            continue
        else:
            firing_times[transition] = transition.firing_time
    return random.choice([t for t in firing_times if firing_times[t] == min(firing_times.values())])


def process_next_event(spn: SPN):

    global SIMULATION_TIME

    next_transition: Transition
    next_transition = find_next_firing(spn)

    SIMULATION_TIME = next_transition.firing_time

    fire_transition(next_transition)

    if VERBOSITY > 1:
        print("\nTransition {} fires at time {}".format(
            next_transition.label, round(SIMULATION_TIME, 2)))

    if VERBOSITY > 2:
        print_marking(spn, SIMULATION_TIME)

    update_enabled_flag(spn)


def simulate(spn: SPN, max_time=10, verbosity=2, protocol=True):

    global SIMULATION_TIME, VERBOSITY, PROTOCOL

    VERBOSITY = verbosity
    PROTOCOL = protocol

    # clear protocol
    if protocol == True:
        with open("output/protocol/protocol.csv", "w", newline="") as protocol:
            writer = csv.writer(protocol)
            writer.writerow(["Place", "Time", "Marking"])

    if VERBOSITY > 0:
        print("Starting simulation...")
        print("Simulation time limit = {}".format(max_time))

    reset_state(spn)

    if VERBOSITY > 1:
        print_marking(spn, SIMULATION_TIME)

    update_enabled_flag(spn)

    if VERBOSITY > 1:
        print_state(spn, SIMULATION_TIME)

    spn_final_state: SPN
    while SIMULATION_TIME < max_time:
        process_next_event(spn)
        if verbosity > 2:
            spn_final_state = spn
            print_state(spn, SIMULATION_TIME)

    if VERBOSITY > 0:
        print("\nTime: {}. Simulation terminated.\n".format(SIMULATION_TIME))

    complete_statistics()

    if VERBOSITY > 0:
        print_statistics(spn, SIMULATION_TIME)
    return spn_final_state, SIMULATION_TIME
