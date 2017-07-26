import re
import sys
import copy

operators = ['+', '-', '*', '/']
code = ""
class MainStatement:
    def __init__(self,main_code):
        main_code= main_code.split('\n')
        for i in range(len(main_code)):
                main_code[i] = main_code[i].strip()
        while(1):
                try:
                    main_code.remove('')
                except:
                    break;
        main_code = '\n'.join(main_code[:])            
        var = {}
        CompoundStatement(main_code,var)     

class CompoundStatement:
    def __init__(self, code_base,var):
        
        self.list = code_base.split('\n')
        k=0
        local = var.copy()
        while(k<len(self.list)):

            parse = LineParser(self.list[k].split(';')[0], k, code_base,var,local)
            k += parse.counter
            

class LineParser:
    def __init__(self, codesegment, k,code_base,var,local):
        self.line = codesegment
        self.code_base = code_base
        self.line = self.line.strip()
        self.counter=0
        self.k = k
        self.var = var
        self.local = local
        self.check()

    def check(self):
        if(self.line.count(':=')>0):
            self.assignment()
            self.counter+=1
        if(self.line.count('print')>0):
            self.print()
            self.counter+=1
        if(self.line.count('if')>0):
            self.buildif()
        if(self.line.count('while')>0):
            self.buildloop()

    def assignment(self):
        self.line = self.line.split(':=')
        newtemp = self.line[0].strip()
        if(newtemp in self.var): 
            self.var[newtemp] = Expression.eval_exp(self.line[1].strip(),self.var,self.local)
        else:
            newdict = {newtemp:Expression.eval_exp(self.line[1].strip(),self.var,self.local)}
            self.local.update(newdict)

    def print(self):
        self.line = self.line.split('print')
        newtemp = self.line[1].strip()
        flag=0
        for op in operators:
            if(newtemp.count(op)>0):
                flag=1
        if(flag==0):
            ktemp = checkVar.find(newtemp,self.var,self.local)
            if(ktemp=='Error!!'):
                print(newtemp)
            else:
                print(ktemp)

    def buildif(self):

        self.line = self.line.split('if')
        newtemp = self.line[1].strip()
        self.line = newtemp.split('then')
        newtemp = self.line[0].strip()
        codetemp = self.code_base.split('\n')
        block = '\n'.join(codetemp[self.k:])
        if_tuple = [(m.start(0), m.end(0)) for m in re.finditer('if', block)]
        fi_tuple = [(m.start(0), m.end(0)) for m in re.finditer('fi', block)]
        first_fi = fi_tuple[0][0]
        counter = 0
        for ele in if_tuple:
            counter += 1
            if (ele[0] > first_fi):
                counter-=1
                break
        last_fi = fi_tuple[counter - 1][0]

        n_tuple = [(m.start(0), m.end(0)) for m in re.finditer('\n', block[:last_fi])]
        else_tuple = [(m.start(0), m.end(0)) for m in re.finditer('else', block[:last_fi])]
        increment_line = len(n_tuple) + 1
        self.counter += increment_line
        if(ConditionalExpression.eval_exp(newtemp,self.var,self.local)):
            lowerlimit = else_tuple[counter-1][0]-1
            upperlimit = block[:lowerlimit].split('\n')
            upperlimit = '\n'.join(upperlimit[1:])
            CompoundStatement(upperlimit,self.local)
        else:
            lowerlimit = fi_tuple[counter-1][0]-1
            upperlimit = block[else_tuple[counter-1][1]:lowerlimit].split('\n')
            upperlimit = '\n'.join(upperlimit[1:])
            CompoundStatement(upperlimit,self.local)


    def buildloop(self):
        self.line = self.line.split('while')
        newtemp = self.line[1].strip()
        self.line = newtemp.split('do')
        newtemp = self.line[0].strip()
        codetemp = self.code_base.split('\n')
        block = '\n'.join(codetemp[self.k:])
        while_tuple = [(m.start(0), m.end(0)) for m in re.finditer('while', block)]
        done_tuple = [(m.start(0), m.end(0)) for m in re.finditer('done', block)]
        first_done = done_tuple[0][0]
        counter = 0
        for ele in while_tuple:
            counter += 1
            if (ele[0] > first_done):
                counter-=1
                break
        last_done = done_tuple[counter - 1][0]
        n_tuple = [(m.start(0), m.end(0)) for m in re.finditer('\n', block[:last_done])]
        increment_line = len(n_tuple) + 1
        self.counter += increment_line
        while(ConditionalExpression.eval_exp(newtemp,self.var,self.local)):
            lowerlimit = last_done -1
            upperlimit = block[:lowerlimit].split('\n')
            upperlimit = '\n'.join(upperlimit[1:])
            CompoundStatement(upperlimit,self.local)


class Expression:

    def eval_exp(codeline,var,local):
        if(codeline.count('-')>0):
            return SubstExp.eval_exp(codeline,var,local)
        elif(codeline.count('+')>0):
            return AddExp.eval_exp(codeline,var,local)
        elif(codeline.count('*')>0):
            return MultExp.eval_exp(codeline,var,local)
        elif(codeline.count('/')>0):
            return DivExp.eval_exp(codeline,var,local)
        else:
            decide = checkVar.find(codeline,var,local)
            if(decide == 'Error!!'):
                print('Error in assignment operation(s)')
                exit()
            else:
                return decide

class ConditionalExpression:
    def eval_exp(codeline,var,local):
        if(codeline.count('>')):
            return GreaterExp.eval_exp(codeline,var,local)
        elif(codeline.count('<')):
            return LesserExp.eval_exp(codeline,var,local)
        elif(codeline.count('==')):
            return EqualExp.eval_exp(codeline,var,local)
        elif(codeline.count('!=')):
            return NotEqualExp.eval_exp(codeline,var,local)
        else:
            if(codeline=='1'):
                return 1
            decide = checkVar.find(codeline,var,local)
            if(decide=='Error!!'):
                print('Error in conditional expression(s)')
                exit()
            else:
                return codeline

class GreaterExp:
    def eval_exp(codeline,var,local):
        codeline = codeline.split('>')
        leftexp = Expression.eval_exp(codeline[0].strip(),var,local)
        rightexp = Expression.eval_exp(codeline[1].strip(),var,local)
        if(leftexp>rightexp):
            return 1
        else:
            return 0

class LesserExp:
    def eval_exp(codeline,var,local):
        codeline = codeline.split('<')
        leftexp = Expression.eval_exp(codeline[0].strip(),var,local)
        rightexp = Expression.eval_exp(codeline[1].strip(),var,local)
        if(leftexp<rightexp):
            return 1
        else:
            return 0

class EqualExp:
    def eval_exp(codeline,var):
        codeline = codeline.split('==')
        leftexp = Expression.eval_exp(codeline[0].strip(),var,local)
        rightexp = Expression.eval_exp(codeline[1].strip(),var,local)
        if(leftexp==rightexp):
            return 1
        else:
            return 0

class NotEqualExp:
    def eval_exp(codeline,var,local):
        codeline = codeline.split('!=')
        leftexp = Expression.eval_exp(codeline[0].strip(),var,local)
        rightexp = Expression.eval_exp(codeline[1].strip(),var,local)
        if(leftexp!=rightexp):
            return 1
        else:
            return 0


class SubstExp:
    def eval_exp(codeline,var,local):
        codeline = codeline.split('-')
        leftexp = Expression.eval_exp(codeline[0].strip(),var,local)
        rightexp = Expression.eval_exp(codeline[1].strip(),var,local)
        return leftexp - rightexp

class AddExp:
    def eval_exp(codeline,var,local):
        codeline = codeline.split('+')
        leftexp = Expression.eval_exp(codeline[0].strip(),var,local)
        rightexp = Expression.eval_exp(codeline[1].strip(),var,local)
        return rightexp + leftexp

class MultExp:
    def eval_exp(codeline,var,local):
        codeline = codeline.split('*')
        leftexp = Expression.eval_exp(codeline[0].strip(),var,local)
        rightexp = Expression.eval_exp(codeline[1].strip(),var,local)
        return rightexp*leftexp

class DivExp:
    def eval_exp(codeline,var,local):
        codeline = codeline.split('/')
        leftexp = Expression.eval_exp(codeline[0].strip(),var,local)
        rightexp = Expression.eval_exp(codeline[1].strip(),var,local)
        return leftexp/rightexp


class checkVar:
    def find(codeline,var,local):
        if(codeline.isdigit()):
            return int(codeline)
        elif(codeline in var):
            return int(var[codeline])
        elif(codeline in local):
            return int(local[codeline])    
        else:
            return 'Error!!'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    text = open(filename).read()
    MainStatement(text)       
    
               
