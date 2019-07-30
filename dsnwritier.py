#!/usr/bin/env python3
from pykicad.sexpr import *
from dsn_rule import *
from dsn_module import Placement,Footprint, Padstack
import dsn_module as module
from dsn_net import *
from dsn_geo import *

class Parser(AST):
    tag = 'parser'
    schema = {
        'string_quote' : {
            '_parser' : text,
            '_attr' : 'quote_char'
        },
        'space_in_quoted_tokens' : {
            '_parser': yes_no,
            '_attr' : 'tokens_on_off'
        },
        'host_cad':{
            '_parser': text
        },
        'host_version':{
            '_parser':text
        }
    }
    def __init__(self,
        quote_char='\"',
        tokens_on_off='on',
        host_cad= "KiCad's Pcbnew",
        host_version="5.1.3-ffb9f22~84~ubuntu18.04.1"):

        super(Parser,self).__init__(quote_char=quote_char,
                                    tokens_on_off=tokens_on_off,
                                    host_cad=host_cad,
                                    host_version=host_version)

                         
class Layer(AST):
    tag='layer'
    schema={
        '0':{
            '_parser': text,
            '_attr': 'name'
        },
        'type':{
            '_parser': Literal('signal') | 'power' | 'mixed' | 'jumper' | 'user',
            '_attr': 'typex'
        },
        'property':{
            'index':{
                '_parser':text,
                '_attr':'index'
            },
        },
    }
    index_ctr=0

    def __init__(self,name,typex='signal',index=None):
        index=Layer.index_ctr
        Layer.index_ctr+=1
        super(Layer,self).__init__(name=name,typex=typex,index=index)

class Dsn(AST):
    tag = 'PCB "kicad_board"'
    schema = {
        '0':{
            'parser' : {
            '_parser': Parser
            },
        },
        '1':{
            'resolution':{
                '_parser': text + integer
            },
        },
        '2':{    
            'unit':{
                '_parser': text
            },
        },
        '3':{
            'structure':{
                '0':{
                    'layers':{
                        '_parser':Layer,
                        '_multiple':True
                    },
                },
                '1':{
                    'boundary':{
                        '_parser':Boundary, 
                        '_multiple':False
                    },                    
                },
                '2':{
                    'keepout':{
                        '_parser': Keepout,
                        '_multiple': True
                    },
                },
                '3':{
                    'via':{
                        '_parser': text,
                        '_attr': 'via_type'
                    },
                },
                '4':{
                    'rule':{
                        '_parser': Rule
                    }
                }
            },
            '_optional':True
        },
        '4':{
            'placement':{
                '0':{
                    'placement':{
                        '_parser':Placement,
                        '_multiple':True
                    },
                },
            },
        },
        '5':{
            'library':{
                '0':{
                    'image':{
                        '_parser': Footprint,
                        '_multiple': True
                    },
                },

                '1':{
                    '_parser':Padstack,
                    '_multiple': True,
                    '_attr':'padstack'
                }

            }
        },
        '6':{
            'network':{
                'net':{
                    '_parser':Net,
                    '_multiple':True
                },
                'netclass':{
                    '_parser':NetClass,
                    '_multiple':True
                }
            }
        },
        '7':{
            'wiring':{
                '_parser':text,  #not available before auto-routing, code can be modificed if want to set route from script manually
                
            }
        }


           
    }

    def __init__(self,
        resolution=['um',10],
        unit='um',
        parser=None,
        layers=None,
        boundary=None,
        keepout=None,
        via_type=None,
        rule=None,
        placement=None,
        image=None,
        padstack=None,
        net=None,
        netclass=None,
        wiring= None
        ):

        layers=self.init_list(layers,[])
        parser=self.init_list(parser,[])
        boundary=self.init_list(boundary,[])
        keepout=self.init_list(keepout,[])
        placement=self.init_list(placement,[])
        image=self.init_list(image,[])
        padstack=self.init_list(padstack,[])
        net=self.init_list(net,[])
        net=self.init_list(netclass,[])

        super(Dsn,self).__init__(
            resolution=resolution,
            unit=unit,
            parser=parser,
            layers=layers,
            boundary=boundary,
            keepout=keepout,
            via_type=via_type,
            rule=rule,
            placement=placement,
            image=image,
            padstack=padstack,
            net=net,
            netclass=netclass,
            wiring=wiring
            )

    def to_file(self, path):
        if not path.endswith('.dsn'):
            path += '.dsn'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_string())     

