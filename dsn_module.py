#!/usr/bin/env python3
from pykicad.sexpr import *

class Component(AST):
    tag='component'
    schema={
        '0':{
            '_parser':text,
            '_attr':'ref1',
            # '_multiple':True
        },
        'place':{
            '0':{
                '_parser':text,
                '_attr':'ref2',
            },
            '1':{
                '_parser':number + number,
                '_attr':'at'
            },
            '2':{
                '_parser':text,
                '_attr':'flip'
            },
            '3':{
                '_parser':integer,
                '_attr':'orientation'
            },
            'PN':{
                '_parser':text,
                '_attr':'name'
            }
        }
    }  
    def __init__(self,ref1,at,ref2=None,flip='front',orientation=0,name=None):
        at[1]=-at[1] #flip y for dsn
        ref2=ref1
        super(Component,self).__init__(ref1=ref1,ref2=ref2,at=at,flip=flip,orientation=orientation,name=name)

class Outline(AST):
    tag='outline'
    schema={
        '0':{
            'path signal':{
                '0':{
                    '_parser':integer,
                    '_attr':'width'
                },
                '1':{
                    '_parser':number,
                    '_attr':'outline_start'
                },
                '2':{
                    '_parser':number,
                    '_attr':'outline_end'
                }
            }

        }
    }
    def __init__(self,width=None,outline_start=None,outline_end=None):
        super(Outline,self).__init__(width=width,outline_start=outline_start,outline_end=outline_end)

class Pin(AST):
    tag='pin'
    schema={
        '0':{
            '_parser':text,
            '_attr':'pin_type',
        },
        '1':{
            '_parser':integer,
            '_attr':'pin_index',
        },
        '2':{
            '_parser':number+number,
            '_attr':'pin_at',
        }
    }
    def __init__(self,pin_index=None,pin_at=None,pin_type='Round[A]Pad_1524_um'):
        super(Pin,self).__init__(pin_type=pin_type,pin_index=pin_index,pin_at=pin_at)

class Shape(AST):
    tag='shape'
    schema={
        ' ':{
            '0':{
                '_parser': text,
                '_attr':'shape'
                
            },
            '1':{
                '_parser': text,
                '_attr':'layer'
            },
            '2':{
                '_parser': integer,
                '_attr': 'size'
            }
        }
    }
    def __init__(self,shape='circle',layer=None,size=1524):
        super(Shape,self).__init__(shape=shape,layer=layer,size=size)
class Padstack(AST):
    tag='padstack'
    schema={
        '0':{
            '_parser': text,
            '_attr': 'pin_type'
        },
        '1':{
            'shape':{
                '_parser':Shape,
                '_multiple':True
            },
        },

        'attach':{
            '_parser': text
        }
    }
    def __init__(self,pin_type='Round[A]Pad_1524_um',shape=None,attach='off'):
        shape=self.init_list(shape,[])
        super(Padstack,self).__init__(pin_type=pin_type,shape=shape,attach=attach)

class Footprint(AST):
    tag='image'
    schema={
        '0':{
            '_parser':text,
            '_attr':'ref',
        },
        'outline':{
            '_parser':Outline,
            '_multiple':True
        },
        'pin':{
            '_parser':Pin,
            '_multiple':True

        }

    }
    def __init__(self,ref=None,outline=None,pin=None):
        outline=self.init_list(outline,[])
        pin=self.init_list(pin,[])
        super(Footprint,self).__init__(ref=ref,outline=outline,pin=pin)



# def load_module(file)