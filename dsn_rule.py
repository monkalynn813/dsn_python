

from pykicad.sexpr import *
class Clearance(AST):
    tag='clearance'
    schema={
        '0':{
            '_parser':number,
            '_attr':'number'
        },
        '1':{
            'type':{
                '_parser':text,
                '_attr':'typex'
            },
            '_optional':True
        },
    }
    def __init__(self,number=200.1,typex=None):
        super(Clearance,self).__init__(number=number,typex=typex)

class Rule(AST):
    tag='rule'
    schema={
        '0':{
            'width':{
                '_parser': number
            },
        },
        '1':{
            'clearance':{
                '_parser':Clearance,
                '_multiple':True
            },
            
        },
    }

    def __init__(self,width=250,clearance=None):
        clearance=self.init_list(clearance,[])
       
        super(Rule,self).__init__(width=width,clearance=clearance)