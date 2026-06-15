; Mestre Thaynan WIP command file

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
