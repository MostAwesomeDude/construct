from types import ModuleType
source = open('compile-example-1.py', 'rt').read()
compiled = compile(source, '', 'exec')
module = ModuleType("construct_compile_target")
exec(compiled, module.__dict__)
module.parse_all
