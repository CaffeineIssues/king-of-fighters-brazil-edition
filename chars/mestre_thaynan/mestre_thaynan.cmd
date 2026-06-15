; Mestre Thaynan WIP command file

[Command]
name = "QCF_x"
command = ~D, DF, F, x
time = 15

[Command]
name = "QCF_y"
command = ~D, DF, F, y
time = 15

[Command]
name = "DP_x"
command = ~F, D, DF, x
time = 15

[Command]
name = "DP_y"
command = ~F, D, DF, y
time = 15

[Command]
name = "QCB_x"
command = ~D, DB, B, x
time = 15

[Command]
name = "QCB_y"
command = ~D, DB, B, y
time = 15

[Command]
name = "QCF_a"
command = ~D, DF, F, a
time = 15

[Command]
name = "QCF_b"
command = ~D, DF, F, b
time = 15

[Command]
name = "QCB_a"
command = ~D, DB, B, a
time = 15

[Command]
name = "QCB_b"
command = ~D, DB, B, b
time = 15

[Command]
name = "x"
command = x
time = 1

[Command]
name = "y"
command = y
time = 1

[Command]
name = "a"
command = a
time = 1

[Command]
name = "b"
command = b
time = 1

[Command]
name = "recovery"
command = x+y
time = 1

[Command]
name = "holdfwd"
command = /$F
time = 1

[Command]
name = "holdback"
command = /$B
time = 1

[Command]
name = "holdup"
command = /$U
time = 1

[Command]
name = "holddown"
command = /$D
time = 1

[Statedef -1]

[State -1, Black Tiger Palm]
type = ChangeState
value = 1000
triggerall = command = "QCF_x" || command = "QCF_y"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Crane Anti-Air]
type = ChangeState
value = 1100
triggerall = command = "DP_x" || command = "DP_y"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Prayer Guard]
type = ChangeState
value = 1200
triggerall = command = "QCB_x" || command = "QCB_y"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Sidewalk Step]
type = ChangeState
value = 1300
triggerall = command = "QCF_a" || command = "QCF_b"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Tiger Roar]
type = ChangeState
value = 1400
triggerall = command = "QCB_a" || command = "QCB_b"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Air Attack]
type = ChangeState
value = 600
triggerall = command = "x" || command = "y" || command = "a" || command = "b"
triggerall = statetype = A
triggerall = ctrl
trigger1 = 1

[State -1, LP]
type = ChangeState
value = 200
triggerall = command = "x"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, HP]
type = ChangeState
value = 210
triggerall = command = "y"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, LK]
type = ChangeState
value = 230
triggerall = command = "a"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, HK]
type = ChangeState
value = 240
triggerall = command = "b"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1
