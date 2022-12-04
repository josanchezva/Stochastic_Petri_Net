from spn_simulator.spn import *
from spn_simulator.spn_simulate import simulate
from spn_simulator.spn_io import print_petri_net
from spn_simulator.spn_visualization import *
from spn_simulator.spn_io import print_statistics

spn = SPN()


#main column places
p1 = Place(label="IDLE(0)", n_tokens=0)
p2 = Place(label="SENDING PACKET(0)", n_tokens=0)
p3 = Place(label="PACKET CHECK(0)", n_tokens=0)
p4 = Place(label="SENDING ACK(0)", n_tokens=0)
p5 = Place(label="ACK CHECK(0)", n_tokens=0)
p6 = Place(label="IDLE(1)", n_tokens=0)
p7 = Place(label="SENDING PACKET(1)", n_tokens=0)
p8 = Place(label="PACKET CHECK(1)", n_tokens=0)
p9 = Place(label="SENDING ACK(1)", n_tokens=0)
p10 = Place(label="ACK CHECK(1)", n_tokens=0)

spn.add_place(p1)
spn.add_place(p2)
spn.add_place(p3)
spn.add_place(p4)
spn.add_place(p5)
spn.add_place(p6)
spn.add_place(p7)
spn.add_place(p10)
spn.add_place(p8)
spn.add_place(p9)

#loop places
p11 = Place(label="LOOP(Q11)", n_tokens=0)
p12 = Place(label="LOOP(Q13)", n_tokens=0)
p13 = Place(label="LOOP(Q16)", n_tokens=0)
p14 = Place(label="LOOP(Q18)", n_tokens=0)

spn.add_place(p11)
spn.add_place(p12)
spn.add_place(p13)
spn.add_place(p14)

#main column transitions
t1 = Transition(label="q19", t_type="T")
t1.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
t2 = Transition(label="q10", t_type="T")
t2.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
t3 = Transition(label="q11", t_type="T")
t3.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
t4 = Transition(label="q12", t_type="T")
t4.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
t5 = Transition(label="q13", t_type="T")
t5.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
t6 = Transition(label="q14", t_type="T")
t6.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
t7 = Transition(label="q15", t_type="T")
t7.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
t8 = Transition(label="q16", t_type="T")
t8.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
t9 = Transition(label="q17", t_type="T")
t9.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
t10 = Transition(label="q18", t_type="T")
t10.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)

spn.add_transition(t1)
spn.add_transition(t2)
spn.add_transition(t3)
spn.add_transition(t4)
spn.add_transition(t5)
spn.add_transition(t6)
spn.add_transition(t7)
spn.add_transition(t8)
spn.add_transition(t9)
spn.add_transition(t10)

#loop transitions

#(0) loop
t11 = Transition(label="Tp(0)", t_type="T")
t11.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
t12 = Transition(label="Ta(0)", t_type="T")
t12.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
#(1) loop
t13 = Transition(label="Tp(1)", t_type="T")
t13.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)
t14 = Transition(label="Ta(1)", t_type="T")
t14.set_distribution(distribution="EXP", parameter1=0.5, parameter2=0.0)

spn.add_transition(t11)
spn.add_transition(t12)
spn.add_transition(t13)
spn.add_transition(t14)

#main column arcs

spn.add_output_arc(t1,p1)
spn.add_input_arc(p1,t2)
spn.add_output_arc(t2,p2)
spn.add_input_arc(p2,t3)
spn.add_output_arc(t3,p3)
spn.add_input_arc(p3,t4)
spn.add_output_arc(t4,p4)
spn.add_input_arc(p4,t5)
spn.add_output_arc(t5,p5)
spn.add_input_arc(p5,t6)
spn.add_output_arc(t6,p6)
spn.add_input_arc(p6,t7)
spn.add_output_arc(t7,p7)
spn.add_input_arc(p7,t8)
spn.add_output_arc(t8,p8)
spn.add_input_arc(p8,t9)
spn.add_output_arc(t9,p9)
spn.add_input_arc(p9,t10)
spn.add_output_arc(t10,p10)

#loop arcs
#tp(0)
spn.add_output_arc(t3,p11)
spn.add_input_arc(p11,t11)
spn.add_output_arc(t11,p2)
#ta(0)
spn.add_output_arc(t5,p12)
spn.add_input_arc(p12,t12)
spn.add_output_arc(t12,p2)
#tp(1)
spn.add_output_arc(t8,p13)
spn.add_input_arc(p13,t13)
spn.add_output_arc(t13,p7)
#ta(1)
spn.add_output_arc(t10,p14)
spn.add_input_arc(p14,t14)
spn.add_output_arc(t14,p7)

spn.add_output_arc(t14,p7)


final_spn, SIMULATIONTIME = simulate(spn, max_time = 100, verbosity = 3, protocol = True)
print('Resultados última operación:')
unidadesTp = [t11,t13] #Paquetes perdidos
unidadesTa = [t12,t14] #Paquetes recuperados
lost_packages = 0
for transition in final_spn.transitions:
    if transition in unidadesTp:
        print(transition.label)
        lost_packages += transition.n_times_fired
        print(" Mean firing rate:    {}".format(transition.n_times_fired/SIMULATIONTIME))
        print(f'curently lost packages: {lost_packages}')
    if transition in unidadesTa:
        print(transition.label)
        lost_packages -= transition.n_times_fired
        print(" Mean firing rate:    {}".format(transition.n_times_fired/SIMULATIONTIME))
        print(f'curently acknowledged packages: {lost_packages}')
print('Paquetes enviados: {}'.format(final_spn.transitions[0].n_times_fired))
print('Paquetes perdidos: {}'.format(lost_packages))
print('Porcentaje paquetes perdidos: {}%'.format(100*lost_packages/(final_spn.transitions[0].n_times_fired)))
#print_petri_net(spn)
draw_spn(spn, show=False)