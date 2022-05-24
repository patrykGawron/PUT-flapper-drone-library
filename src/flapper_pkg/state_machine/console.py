from statemachine import Transition
import itertools
def print_transitions(state_machine):
    print(f'Available transitions for diagram : {state_machine.name}')
    for i in state_machine.transitions:
            if i.source.name == state_machine.current_state.name:
                print(i.identifier)

def check_transition(state_machines, state_machine_name, trans_nr):
    znalazło = False
    for machine in state_machines:
        if machine.name == state_machine_name:
            for transition in machine.transitions:
                    if transition.identifier == trans_nr:
                        znalazło = True
    if znalazło == True:
        correct_nr = True
    else:
        correct_nr = False
    return correct_nr


def process(state_machines, name, nr_transition):
    for machine in state_machines:
        if machine.name == name:
            for transition in machine.transitions:
                    if transition.identifier == nr_transition:
                        number = nr_transition[-3:]
                        construct = f"callable_{number}"
                        atr = getattr(machine, construct, None)
                        if atr is not None:
                            atr()
                        machine.current_state = transition.destinations[0]
                        print(f'{machine.name} current state: {machine.current_state}')


def console_interface(drone, drone_transitions, drone_from_to, redraw):
    drone.name = "drone"
    pause = "---------------------------------------------------------------------------------------------------------------------"
    print(pause)
    print("FLAPPER DRONE :)")

    error = "Try again, probably the value you wrote down was incorect"

    state_machines = [drone]
    # machine = state_machines[0]
    # print(f'{machine.name} current state: {machine.current_state}')

    while True:
        print(pause)
        redraw(curr_drone=drone.current_state.name)
        for state in state_machines:
            print_transitions(state)
        correct_name = True
        correct_nr = True
        while correct_name:
            print('First choose name of automata and press enter')
            name = input()
            if name == 'drone':
                correct_name = False
        print('Now write down number of transition in format <int>_<int> and press enter')
        nr_transition = input()
        t = 'transition_'+nr_transition
        correct_nr = check_transition(state_machines, name, t)
        while correct_nr:
            if correct_nr == True:
                process(state_machines, name, t)
                break
            else:
                correct_nr == False


def testing(drone, drone_transitions, drone_from_to, redraw):
    drone.name = "drone"
    pause = "---------------------------------------------------------------------------------------------------------------------"
    print(pause)
    state_machines = [drone]

    answers = [("Taking off"),
               ("Hovering"),
               ("Landing"),
               ("LANDED"),
               ("Taking off"),
               ("Hovering"),
               ("Flight"),
               ("Hovering"),
               ("Flight"),
               ("Emergency Landing"),
               ("LANDED"),
               ("Emergency"),
               ("Emergency Landing"),
               ("LANDED"),
               ("Taking off"),
               ("Hovering"),
               ("Emergency"),
               ("Emergency Landing"),
               ("LANDED"),
               ("Taking off"),
               ("Hovering"),
               ("Emergency Landing"),
               ("LANDED"),
               ("Taking off"),
               ("Hovering"),
               ("Flight"),
               ("Emergency"),
               ("Emergency Landing"),
               ("LANDED")]


    path = [("drone", "transition_0_1"),
            ("drone", "transition_1_2"),
            ("drone", "transition_2_3"),
            ("drone", "transition_3_0"),
            ("drone", "transition_0_1"),
            ("drone", "transition_1_2"),
            ("drone", "transition_2_5"),
            ("drone", "transition_5_2"),
            ("drone", "transition_2_5"),
            ("drone", "transition_5_6"),
            ("drone", "transition_6_0"),
            ("drone", "transition_0_4"),
            ("drone", "transition_4_6"),
            ("drone", "transition_6_0"),
            ("drone", "transition_0_1"),
            ("drone", "transition_1_2"),
            ("drone", "transition_2_4"),
            ("drone", "transition_4_6"),
            ("drone", "transition_6_0"),
            ("drone", "transition_0_1"),
            ("drone", "transition_1_2"),
            ("drone", "transition_2_6"),
            ("drone", "transition_6_0"),
            ("drone", "transition_0_1"),
            ("drone", "transition_1_2"),
            ("drone", "transition_2_5"),
            ("drone", "transition_5_4"),
            ("drone", "transition_4_6"),
            ("drone", "transition_6_0")]

    for step, ans in zip(path, answers):
        name, t = step
        drone_state = ans

        process(state_machines, name, t)
        assert drone.current_state.value == drone_state
    print("Test completed successfully!")