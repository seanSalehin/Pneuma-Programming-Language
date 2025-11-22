from llvmlite import ir

from AST import NodeType, Statement, Expression, Program, ExpressionStatement, InfixExpression, IntegerLiteral, FloatLiteral, IdentifierLiteral
from Environment import Environment
from AST import FunctionStatement, BlockStatement, ReturnStatement, AssignStatement, IfStatement, BooleanLiteral

class Compiler:

    def __init__(self):
        self.type_map={
            'int':ir.IntType(32),
            'float':ir.FloatType(),
            'bool': ir.IntType(1)
        }
        self.module = ir.Module('main')
        self.builder = ir.IRBuilder()
        self.env = Environment()
        #keeping track of errors
        self.errors=[]
        self.__initialize_builtins()
    


    def __initialize_builtins(self):
        def __init_booleans():
            bool_type = self.type_map['bool']
            true_var = ir.GlobalVariable(self.module, bool_type, 'true')
            true_var.initializer = ir.Constant(bool_type, 1) #1 = true
            true_var.global_constant=True

            false_var = ir.GlobalVariable(self.module, bool_type, 'false')
            false_var.initializer = ir.Constant(bool_type, 0) #0 = false
            false_var.global_constant=True #fixed immutable values

            return true_var, false_var
        
        true_var, false_var = __init_booleans()
        self.env.define('true', true_var, true_var.type)
        self.env.define('false', false_var, false_var.type)


    def compile(self, node):
        match node.type():
            case NodeType.Program:
                self.__visit_program(node)

            case NodeType.ExpressionStatement:
                self.__visit_expression_statement(node)

            case NodeType.LetStatement:
                self.__visit_let_statement(node)

            case NodeType.InfixExpression:
                self.__visit_infixExpression(node)

            case NodeType.FunctionStatement:
                self.__visit_function_statement(node)

            case NodeType.BlockStatement:
                self.__visit_block_statement(node)

            case NodeType.ReturnStatement:
                self.__visit_return_statement(node)

            case NodeType.AssignStatement:
                self.__visit_assign_statement(node)

            case NodeType.IfStatement:
                self.__visit_if_statement(node)

    


    def __visit_program(self, node):
        for stmt in node.statements:
            self.compile(stmt)


    def __visit_expression_statement(self, node):
        self.compile(node.e)


    def __visit_let_statement(self, node):
        name=node.name.value
        value = node.value
        value_type=node.value_type  #TODO

        value, Type = self.__resolve_value(node=value)

        #variable
        if self.env.lookup(name)is None:
            ptr=self.builder.alloca(Type)
            #storeing the value at the pointer (ptr)
            self.builder.store(value, ptr)
            #Add the variable to the environment
            self.env.define(name, ptr, Type)
        else:
            ptr, _=self.env.lookup(name)
            self.builder.store(value, ptr)
        
    
    def __visit_block_statement(self, node):
        for stmt in node.statements:
            self.compile(stmt)

    
    def __visit_return_statement(self, node):
        value = node.return_value
        value, Type = self.__resolve_value(value)
        self.builder.ret(value)



    def __visit_function_statement(self, node):
        name = node.name.value
        body = node.body
        params=node.parameters
        params_names=[p.value for p in params]
        param_types = []
        return_type = self.type_map[node.return_type]

        fnty=ir.FunctionType(return_type, param_types)
        func = ir.Function(self.module, fnty, name=name)
        block = func.append_basic_block(f'{name}_entry')
        previous_builder = self.builder
        self.builder=ir.IRBuilder(block)
        previous_env=self.env
        self.env=Environment(parent=self.env)
        self.env.define(name, func, return_type)
        self.compile(body)
        self.env=previous_env
        self.env.define(name, func, return_type)
        self.builder = previous_builder


    def __visit_assign_statement(self, node):
        name = node.ident.value
        value = node.right_value
        value, Type = self.__resolve_value(value)
        if self.env.lookup(name) is None:
            self.errors.append(f"Compile Error: Identifier {name} has not been declared")
        else:
            ptr, _ = self.env.lookup(name)
            self.builder.store(value, ptr)


    def __visit_if_statement(self, node):
        #if condition = true  ==> if block
        #if condition false ==> else block
        condition = node.condition
        consequence = node.consequence
        alternative = node.alternative

        test, _ = self.__resolve_value(condition)

        if alternative is None:
            with self.builder.if_then(test):
                self.compile(consequence)
        else:
            with self.builder.if_else(test)as(true, otherwise):
                with true:
                    self.compile(consequence)
                with otherwise:
                    if alternative is not None:
                        self.compile(alternative)
                    else:
                        self.builder.ret_void() 



    def __visit_infixExpression(self, node):
        operator = node.operator
        left_value, left_type = self.__resolve_value(node.left_node)
        right_value, right_type=self.__resolve_value(node.right_node)
        value = None
        Type=None
        if isinstance(right_type, ir.IntType) and isinstance(left_type, ir.IntType):
            Type = self.type_map['int']
            match operator:
                case '+':
                    value = self.builder.add(left_value, right_value)
                case '-':
                    value = self.builder.sub(left_value, right_value)
                case '*':
                     value = self.builder.mul(left_value, right_value)
                case '/':
                    value = self.builder.sdiv(left_value, right_value)   
                case '%':
                    value= self.builder.srem(left_value, right_value) 
                case '^':
                    # TODO
                    pass
                case '<':
                    value = self.builder.icmp_signed('<',left_value, right_value)
                    Type = ir.IntType(1)
                case '<=':
                    value = self.builder.icmp_signed('<=',left_value, right_value)
                    Type = ir.IntType(1)
                case '>':
                    value = self.builder.icmp_signed('>',left_value, right_value)
                    Type = ir.IntType(1)
                case '>=':
                    value = self.builder.icmp_signed('>=',left_value, right_value) 
                    Type = ir.IntType(1)  
                case '==':
                    value= self.builder.icmp_signed('==',left_value, right_value) 
                    Type = ir.IntType(1) 
                case '!=':
                    value = self.builder.icmp_signed('!=', left_value, right_value)
                    Type = ir.IntType(1)

        elif isinstance(right_type, ir.FloatType) and isinstance(left_type, ir.FloatType):
            Type = ir.FloatType()
            match operator:
                case '+':
                    value = self.builder.fadd(left_value, right_value)
                case '-':
                    value = self.builder.fsub(left_value, right_value)
                case '*':
                    value = self.builder.fmul(left_value, right_value)
                case '/':
                    value = self.builder.fdiv(left_value, right_value)
                case '%':
                    value = self.builder.frem(left_value, right_value)
                case '^':
                    #TODO
                    pass
                case '<':
                    value = self.builder.fcmp_ordered('<',left_value, right_value)
                    Type = ir.IntType(1)
                case '<=':
                    value = self.builder.fcmp_ordered('<=',left_value, right_value)
                    Type = ir.IntType(1)
                case '>':
                    value = self.builder.fcmp_ordered('>',left_value, right_value)
                    Type = ir.IntType(1)
                case '>=':
                    value = self.builder.fcmp_ordered('>=',left_value, right_value) 
                    Type = ir.IntType(1)  
                case '==':
                    value= self.builder.fcmp_ordered('==',left_value, right_value) 
                    Type = ir.IntType(1) 
                case '!=':
                    value = self.builder.fcmp_ordered('!=', left_value, right_value)
                    Type = ir.IntType(1)

        return value, Type

    def __resolve_value(self, node, value_type=None):
        match node.type():
            case NodeType.IntegerLiteral:
                node=node
                value, Type = node.value, self.type_map['int' if value_type is None else value_type]
                return ir.Constant(Type, value), Type
            
            case NodeType.FloatLiteral:
                node=node
                value, Type = node.value, self.type_map['float' if value_type is None else value_type]
                return ir.Constant(Type, value), Type
            
            case NodeType.InfixExpression:
                return self.__visit_infixExpression(node)
            
            case NodeType.IdentifierLiteral:
                node=node
                ptr, Type = self.env.lookup(node.value)
                return self.builder.load(ptr), Type
            
            case NodeType.BooleanLiteral:
                node = node
                return ir.Constant(ir.IntType(1), 1 if node.value else 0), ir.IntType(1)