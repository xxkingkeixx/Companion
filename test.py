command = raw_input("Enter CMD here: ")
cmd = command[0:]

prfx = cmd[0] == ">"
cmd = cmd[1:] if prfx else cmd
try:
    cmd, _ = cmd.split(" ", 1)
except:
      cmd, _ = cmd, ""

result = {
  prfx and 'a': lambda _: int(_) * 5,
  prfx and 'b': lambda _:'hi',
  prfx and 'c': lambda _: _ - 2
}[cmd](_)

print result