from asts import AbstractVisitor


def getBuiltinProcedures():
    return """.method public static _out : (Ljava/lang/String;)V
.code stack 2 locals 1
   getstatic Field java/lang/System out Ljava/io/PrintStream;
   aload_0
   invokevirtual Method java/io/PrintStream println (Ljava/lang/String;)V
   return
.end code
.end method

.method public static _int : (F)I
.code stack 2 locals 1
   fload_0
   f2i
   ireturn
.end code
.end method

.method public static _float : (I)F
.code stack 2 locals 1
   iload_0
   i2f
   freturn
.end code
.end method

.method public static _string : (F)Ljava/lang/String;
.code stack 2 locals 1
   fload_0
   invokestatic Method java/lang/Float toString (F)Ljava/lang/String;
   areturn
.end code
.end method

"""
# def getname(node):
#     return node.id


def generateClass(BuiltinProcedures, declarations, body):
        class_template = (
            ".version 49 0\n"
            ".class public super Mamba\n"
            ".super java/lang/Object\n\n"
            ".method public <init> : ()V\n"
            ".code stack 1 locals 1\n"
            "aload_0\n"
            "invokespecial Method java/lang/Object <init> ()V\n"
            "return\n"
            ".end code\n"
            ".end method\n\n"
            "{0}"  # BuiltinMehods
            "{1}"  # Placeholder for declarations
            "{2}"  # Placeholder for body
            ".sourcefile 'Mamba.java'\n"
            ".end class\n"
        )

        return class_template.format(BuiltinProcedures, declarations, body)



def generateMethod(self, name, args, ret, body):
        method_template = (
            ".method static public {0} : ({1}){2}\n"
            ".code stack 32 locals 32"
            "{3} "
            ".end code\n"
            ".end method\n"
            ""
        )

        # Fill in the template with the provided details
        return method_template.format(name, args, ret, body)

def translate_type(type):
        if type == "int":
            return 'I'
        elif type == "float":
            return 'F'
        elif type == "bool":
            return 'Z'
        elif type == "string":
            return 'Ljava/lang/String;'
        
class Project4Visitor(AbstractVisitor):

    declarations = "" #Keeps track of field declarations
    label_counter = 0 # Counter for generating labels
    scope_stack = []  # Stack to keep track of scopes

    def push_scope(self, scope_name):
        self.scope_stack.append(scope_name)

    def pop_scope(self):
        return self.scope_stack.pop()

    def getname(self, identifier):
        # If the identifier at top level, returns as is
        if not self.scope_stack:
            return identifier

        # If nested scope, prefix with the scope
        current_scope = self.scope_stack[-1]
        return f"{current_scope}_{identifier}"

    def visitProgram(self, node, *args):
        block_code = node.b.accept(self, *args)

        BuiltinProcedures = getBuiltinProcedures()

        class_code = generateClass(BuiltinProcedures, self.declarations, block_code)

        return class_code


    def visitBlock(self, node, *args):
        # Translate each declaration/statement
        block_code = ""
        for child in node.children:
            block_code += child.accept(self, *args)
        
        #TOP BLOCK..

        # Return all of them concatenated together
        return block_code


    def visitVariableDeclaration(self, node, *args):
        jvm_type = translate_type(node.type)
        self.declarations += f".field static public {node.id} {jvm_type}\n"

        #Translate the RHS expression
        rhs_code = node.rhs.accept(self, *args)

        # Store the result into the field for this variable
        initialization_code = f"putstatic Mamba {node.id} {jvm_type}\n"

        # Return the concatenated code
        return rhs_code + initialization_code
        

    def visitProcedureDeclaration(self, node, *args):
        # Translate the parameters
        params_code = ""
        if node.params:
            params_code = node.params.accept(self, *args)

        # Translate the body to get nested procedures
        nested_procedures_code = ""
        if node.b:
            nested_procedures_code = node.b.accept(self, *args)

        # Translate the body to get the current procedure's statements
        statements_code = ""
        if node.b:
            statements_code = node.b.accept(self, *args)

        # Call "generateMethod" to create the current method
        method_declaration_code = generateMethod(self, node.id, params_code, node.ret, f"{nested_procedures_code}{statements_code}")

        # Return the code for the method declaration
        return method_declaration_code

    
    def visitFormalParameters(self, node, *args):
        params_code = ""

        # generate field declaration
        for param, param_type in zip(node.params, node.types):


            param_type = "I"
            #translate_type(node.vt.lookup(param))
            self.declarations += f".field static public {param} {param_type}\n"

        return params_code


    def visitAssignmentStatement(self, node, *args):

        # Translate the expression
        expression_code = node.e.accept(self, *args)

        ID = node.id
        assignment_type = node.vt.lookup(ID)

        # Use "putstatic" to store into the field
        # Be sure to use the correct type for the field
        assignment_code = f"putstatic Mamba {ID} {assignment_type}\n" 

        # Return the concatenated code
        return expression_code + assignment_code

    def visitReturnStatement(self, node, *args):
        # Translate the expression
        expression_code = node.e.accept(self, *args)

        # Use "ireturn" #Here #Type
        return f"{expression_code}ireturn\n"

    def visitCallExpression(self, node, *args):
        # Translate the actual parameters
        actual_parameters_code = ""
        if node.params:
            actual_parameters_code = node.params.accept(self, *args)

        # Return the code for the arguments, followed by a "invokestatic" to the method being called
        invokestatic_code = f"invokestatic Mamba {node.id}({actual_parameters_code})\n"

        return actual_parameters_code + invokestatic_code

    def visitIfStatement(self, node, *args):
        # Create labels for the true and false branches
        true_label = self.getLabel()
        false_label = self.getLabel()
        end_label = self.getLabel()

        # Translate the condition
        condition_code = node.c.accept(self, true_label, *args)

        true_branch_code = f"{true_label}:\n{node.t.accept(self, *args)}goto {end_label}\n"

        false_branch_code = f"{false_label}:\n{node.f.accept(self, *args)}"

        return f"{condition_code}ifeq {false_label}\n{true_branch_code}{false_branch_code}{end_label}:\n"

    def getLabel(self):
        label_name = f'L{self.label_counter}'
        self.label_counter += 1
        return label_name

    
    def visitWhileStatement(self, node, *args):
        # Create labels for the start and end of the loop
        start_label = self.getLabel()
        end_label = self.getLabel()

        # Translate the condition
        condition_code = node.c.accept(self, start_label, *args)

        while_start_code = f"{start_label}:\n"

        # Translate the statement
        statement_code = node.s.accept(self, *args)

        while_end_code = f"goto {start_label}\n{end_label}:\n"

        return f"{while_start_code}{condition_code}ifeq {end_label}\n{statement_code}{while_end_code}"

    
    def visitActualParameters(self, node, *args):
        parameters_code = ""

        # Iterate through each parameter and translate it
        for param in node.params:
            param_code = param.accept(self, *args)
            parameters_code += param_code

        return parameters_code



    def visitExpression(self, node, *args):
        # Translate the left-hand side
        lhs_code = node.t.accept(self, *args)

        # Translate the right-hand side
        rhs_code = ""
        if node.e:
            rhs_code = node.e.accept(self, *args)

        operator_code = "" #call transop
        if node.op:
            operator_code = self.transop(node.op, operand_type="int")  #type

        return f"{lhs_code}{rhs_code}{operator_code}"



    def visitTerm(self, node, *args):
        # Translate the left-hand side
        lhs_code = node.f.accept(self, *args)

        # Translate the right-hand sideif there
        rhs_code = ""
        if node.t:
            rhs_code = node.t.accept(self, *args)

        #how to get operand_type 
        operator_code = ""
        if node.op:
            operator_code = self.transop(node.op, operand_type = "int")  

        # Operator comes last
        return f"{lhs_code}{rhs_code}{operator_code}"


    def visitFactor(self, node, *args): #how do types looklike when they return
        #ft, vt = args
        if node.f:
            return node.f.accept(self, *args) #keep
        if node.call:
            return node.call.accept(self, *args) #keep
        if node.id:
            ID = node.id #keep

            # Look up the variable name
            t = node.vt.lookup(ID)

            jas_type = translate_type(t)
            return "getstatic " + "Mamba" + ID + str(jas_type) + '\n'
            
        if node.int:
            return "ldc " + node.int + '\n'
        if node.float:
            return "ldc " + node.float + '\n'
        if node.str:
            return "ldc " + node.str + '\n'

    def visitParenthesisFactor(self, node, *args):
        return node.e.accept(self, *args)
    

    def visitCondition(self, node, label, *args):
        # Translate Expression1 and Expression2
        expression1_code = node.lhs.accept(self, *args)
        expression2_code = node.rhs.accept(self, *args)

        # transop
        op_code = self.transop(node.op, label, operand_type="int")  #type

        return f"{expression1_code}\n{expression2_code}\n{op_code}\n"


    #conditional and others
    def transop(self, op, label=None, operand_type="int"):
    # Dictionary of equivalent instructions for each operator depennding on type
        operators = {
            "*": {"int": "imul", "float": "fmul"},
            "/": {"int": "idiv", "float": "fdiv"},
            "+": {"int": "iadd", "float": "fadd"},
            "-": {"int": "isub", "float": "fsub"},
            "<>": {"int": "ifne", "float": "ifne"},
            "==": {"int": "ifeq", "float": "ifeq"},
            "<": {"int": "iflt", "float": "iflt"},
            ">": {"int": "ifgt", "float": "ifgt"},
            "<=": {"int": "ifle", "float": "ifle"},
            ">=": {"int": "ifge", "float": "ifge"},
        }

        op_code = operators[op].get(operand_type, "nop")

        # If label(comparators), use it; otherwise, return the operator code
        return f"{op_code} {label}\n" if label else op_code