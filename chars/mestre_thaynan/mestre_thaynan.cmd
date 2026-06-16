; Mestre Thaynan minimal WIP command file

[Command]
name = "x"
command = x
time = 1

[Command]
name = "y"
command = y
time = 1

[Command]
name = "z"
command = z
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

[State -1, Light Punch]
type = ChangeState
value = 200
triggerall = command = "x"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Medium Punch]
type = ChangeState
value = 205
triggerall = command = "z"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Heavy Punch]
type = ChangeState
value = 210
triggerall = command = "y"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, High Kick]
type = ChangeState
value = 240
triggerall = command = "b"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1
