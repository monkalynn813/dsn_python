#!/usr/bin/env python3
from pykicad.sexpr import *
from dsn_rule import *
from dsn_module import Component,Footprint
import dsn_module as module

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


class Boundary(AST):
    tag='boundary'
    schema={
        'path pcb':{
            '0':{
                '_parser':integer,
                '_attr':'brd_index'
            },
            '1':{
                '_parser': number,
                '_attr': 'path'
            },

        }
    }

    index_ctr=0
    def __init__(self,path,brd_index=None):
        brd_index=Boundary.index_ctr
        Boundary.index_ctr+=1

        super(Boundary,self).__init__(path=path,brd_index=brd_index)

class Keepout(AST):
    tag='keepout'
    schema={
        '0':{
            '0':{
                '_parser':text,
                '_attr':'name'
            },

            ' ':{
                '0': {
                    '_parser':text,
                    '_attr':'shape'
                },
                '1':{
                    '_parser':text,
                    '_attr':'typex'
                },
                '2':{
                    '_parser':integer,
                    '_attr':'brd_index'
                },
                '3':{
                    '_parser': number,
                    '_attr':'path'
                },
            },
        },
    }
    def __init__(self,path,name='\"\"',brd_index=0,shape='polygon',typex='signal'):

        super(Keepout,self).__init__(path=path,name=name,brd_index=brd_index,shape=shape,typex=typex)



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
                        '_multiple':True
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
                        '_attr': 'via_txt'
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
                    'component':{
                        '_parser':Component,
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
                }

                # 'padstack':{
                #     '_parser':Padstack,
                #     '_multiple': True
                # }

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
        via_txt='"Via[0-1]_800:400_um"',
        rule=None,
        component=None,
        image=None
        ):

        layers=self.init_list(layers,[])
        parser=self.init_list(parser,[])
        boundary=self.init_list(boundary,[])
        keepout=self.init_list(keepout,[])
        component=self.init_list(component,[])
        image=self.init_list(image,[])
        

        super(Dsn,self).__init__(
            resolution=resolution,
            unit=unit,
            parser=parser,
            layers=layers,
            boundary=boundary,
            keepout=keepout,
            via_txt=via_txt,
            rule=rule,
            component=component,
            image=image
            )

    def to_file(self, path):
        if not path.endswith('.dsn'):
            path += '.dsn'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_string())     

