from flapper_pkg.state_machine.flapper import *

drone = Gen.create_object(drone_states, drone_transitions, drone_from_to, clbck)
    # testing(drone, drone_transitions, drone_from_to, redraw)
console_interface(drone, drone_transitions, drone_from_to, redraw)