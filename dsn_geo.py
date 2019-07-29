

from pykicad.sexpr import *
import numpy as np

class load_drawing():
    def __init__(self,afile):
        import ezdxf
        self.dwg=ezdxf.readfile(afile)
        self.msp=self.dwg.modelspace()
    
    def load_all(self):
        return [self.load_line,self.load_polygon]
    
    def load_line(self):
        startlist=[]
        endlist=[]
        line_list=[]
        for e in self.msp.query('LINE'):
            startlist.append(e.dxf.start[:2])
            endlist.append(e.dxf.end[:2])
        
        for i in range(len(startlist)):
            line_list.append(startlist[i])
            line_list.append(endlist[i])
        
        line_list=np.array(line_list)
        line_list[:,1]*=-1
        line_list*=1000
        line_list=line_list.flatten()
        line_list=list(line_list)

        return line_list
    def load_polygon(self):
        pts_list=[]
        for e in self.msp.query('LWPOLYLINE'):
            pts_list.append(np.array(e.get_points()))

        for i in range(len(pts_list)):
            pts_list[i]=pts_list[i][:,:2]
            pts_list[i][:,1]*=-1

            ##Unit = um
            pts_list[i]=pts_list[i]*1000
            pts_list[i]=pts_list[i].flatten()
            pts_list[i]=list(pts_list[i])
        return pts_list  
    def load_line_as_polygon(self):
        pts_list=self.load_polygon()
        ply_list=[]
        for i in range(len(pts_list)):
            for j in range(len(pts_list[i])):
                ply_list.append(pts_list[i][j])
        return ply_list

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