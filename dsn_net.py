
from pykicad.sexpr import *

class Net(AST):
    tag='net'
    schema={
        '0':{
            '_parser': text,
            '_attr': 'net_name'
        },
        '1':{
            'pins':{
                '0':{
                    '_parser':text +text,
                    '_attr':'conn_pins'
                },              
            }
        }
    }
    def __init__(self,net_name,conn_pins=None):
        super(Net,self).__init__(net_name=net_name,conn_pins=conn_pins)

class NetClass(AST):
    tag='class'
    schema={
        '0':{
            '0':{
                '_parser':text,
                '_attr':'net_class_name'
            },
            '1':{
                '_parser':text+text,
                '_attr':'nets_name'
            },
        },
        'circuit':{
            '0':{
                'use_via':{
                    '_parser':text,
                    '_attr':'via_name'
                }
            }
        },
        'rule':{
            'width':{
                '_parser':integer
            },
            'clearance':{
                '_parser': number
            }
        }
    }
    def __init__(self,net_class_name='default',nets_name=None,
                via_name='',width=3000,clearance=200.1):

        super(NetClass,self).__init__(net_class_name=net_class_name,nets_name=nets_name,
                                    via_name=via_name,width=width,clearance=clearance)
                
