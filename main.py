from Lexer import Lexer
from parser import Parser
from AST import Program
import time
import json
from compiler import Compiler
from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float
import os



Lexer_Bug=False
Parse_Bug=False
Compiler_Bug = False
RUN_CODE = True
PROD_DEBUG = False


if __name__=='__main__':
    
    for filename in os.listdir('.'):
        if filename.endswith('.Pneuma'):
            new_filename = filename.replace('.Pneuma', '.pn')
            os.rename(filename, new_filename)

    with open("Test/main.pn", 'r') as f:
        code=f.read()

    #lexer debug
    if Lexer_Bug:
        debug=Lexer(source=code)
        while debug.current_character is not None:
            print(debug.next_token())

    l=Lexer(source=code)
    p = Parser(lexer=l)

    parse_start = time.time()
    program = p.parse_program()
    parse_end = time.time()

    if len(p.errors)>0:
         for err in p.errors:
             print(err)
         exit(1)

    #parser debug
    if Parse_Bug:
        print("Parser Debug")
        #program = p.parse_program()
        with open("debug/ast.json", "w") as f:
            json.dump(program.json(), f, indent=4)
        print("wrote AST to debug/ast.json sucessfully")


    #compiler debug
    c=Compiler()

    compiler_start = time.time()
    c.compile(node=program)
    compiler_end = time.time()
    


    #output
    module=c.module
    module.triple = llvm.get_default_triple()
    if Compiler_Bug:
        with open("debug/ir.ll", "w") as f:
            f.write(str(module))
    if RUN_CODE:
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        try:
            llvm_ir_parsed = llvm.parse_assembly(str(module))
            llvm_ir_parsed.verify()
        except Exception as e:
            print(e)
            raise

        target_machine = llvm.Target.from_default_triple().create_target_machine()

        engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
        engine.finalize_object()

        entry = engine.get_function_address('main')
        cfunc = CFUNCTYPE(c_int)(entry)
        st=time.time()
        result = cfunc()
        et = time.time()

        if PROD_DEBUG:
            print(f"Parsed in : {round ((parse_end - parse_start)* 1000, 6)} ms.")
            print(f"Compiled in : {round ((compiler_end - compiler_start)* 1000, 6)} ms.")

        print(f'\n\nResult: {result}\n===Executed in {round((et-st)*1000, 6)}  ms\n')