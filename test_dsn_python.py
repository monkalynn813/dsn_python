#!/usr/bin/env python3
import dsnwritier
from pykicad import pcb

test=dsnwritier.Dsn()

###############################################################################
##General
layers=[
    dsnwritier.Layer('F.Cu'),
    dsnwritier.Layer('B.Cu'),
    dsnwritier.Layer('F.Mask'),
    dsnwritier.Layer('B.Mask')
]

parsers= dsnwritier.Parser()

rule=dsnwritier.Rule()
clearance=[
    dsnwritier.Clearance(200.1),
    dsnwritier.Clearance(200.1,'default_smd'),
    dsnwritier.Clearance(50,'smd_smd')]
rule.clearance=clearance

###############################################################################
###manually
bdata=[137735, -31864.8,  165736, -31864.8,  165736, -113335,  137735, -113335,
            137735, -113864,  160735, -113864,  160735, -151336,  150736, -151336,
            150736, -151865,  160735, -151865,  160735, -211335,  150736, -211335,
            150736, -211865,  169735, -211865,  169735, -249335,  96264.4,-249335,
            96264.4, -211865,  138264, -211865,  138264, -211335,  37264.4, -211335,
            37264.4, -151865,  138264, -151865,  138264, -151336,  87264.4, -151336,
            87264.4, -113864,  119265, -113864,  119265, -113335,  264.583, -113335,
            264.583, -31864.8,  78264.5, -31864.8,  78264.5, -264.632,  137735, -264.632,
            137735, -31864.8]


kdata1=[138725, -221865,  138725, -244336,  150275, -244336,  150275, -221865,
            138725, -221865]
kdata2=[98235.3, -224531,  98764.5, -224531,  98764.5, -219905,  103236, -224376,
            103236, -236824,  98764.5, -241294,  98764.5, -236669,  98235.3, -236669,
            98235.3, -242572,  103610, -237198,  103765, -237198,  103765, -237043,
            103874, -236933,  103765, -236824,  103765, -224376,  103874, -224266,
            103765, -224157,  103765, -224002,  103610, -224002,  98235.3, -218628,
            98235.3, -224531]

#############
boundary=dsnwritier.Boundary(bdata)

keepout=[
    dsnwritier.Keepout(kdata1),
    dsnwritier.Keepout(kdata2)]

###############
image1_outline=[
    dsnwritier.module.Outline(width=120,outline_start=[-7620, 11430],outline_end=[7540, 11430]),
    dsnwritier.module.Outline(width=120,outline_start=[-7620, 11430],outline_end=[7540, -13570]),
    dsnwritier.module.Outline(width=120,outline_start=[-7620, -13570],outline_end=[-7620, -13570]),
    dsnwritier.module.Outline(width=120,outline_start=[-7620, -13570],outline_end=[-7620, 11430])]
# image1_outline=[dsnwritier.module.Outline(120)]
image1_pin=[
    dsnwritier.module.Pin(1,[-6350, 10160]),
    dsnwritier.module.Pin(2,[-6350, 7620])]

image1=dsnwritier.Footprint('U1',image1_outline,image1_pin)
image=[image1]
###############
pin_shape1=[dsnwritier.module.Shape(layer='F.Cu'),
            dsnwritier.module.Shape(layer='B.Cu')]
padstack1=dsnwritier.Padstack(shape=pin_shape1,attach='off')
pin_shape2=[dsnwritier.module.Shape(layer='F.Cu',size=800),
            dsnwritier.module.Shape(layer='B.Cu',size=800)]
padstack2=dsnwritier.Padstack(pin_type='"Via[0-1]_800:400_um"',shape=pin_shape2,attach='off')
#######################################################################################
###load from library

drawingclass=dsnwritier.load_drawing('/home/jingyan/Documents/summer_intern_lemur/roco_electrical/dsn_line_test.dxf')
ddata=drawingclass.load_polygon()
bdata=ddata[0]  #first element is boundary

#############
boundary=dsnwritier.Boundary(bdata)

#############
keepout=[] #load all the rest as outline 

for i in range(1,len(ddata)):
    kdata=dsnwritier.Keepout(ddata[i])
    keepout.append(kdata)

##########
libpath='/home/jingyan/Documents/summer_intern_lemur/roco_electrical/libraries/kicad-ESP8266/ESP8266.pretty/'

image=[dsnwritier.Footprint.from_file(libpath+'mpu-9250.kicad_mod',ref='J1'),
       dsnwritier.Footprint.from_file(libpath+'ESP12F-Devkit-V3.kicad_mod',ref='U1')]

padstack=dsnwritier.Padstack.auto_detect([libpath+'mpu-9250.kicad_mod',libpath+'ESP12F-Devkit-V3.kicad_mod'])

##########placement
placement=[dsnwritier.Placement('U1',[103000,48000],orientation=90,name='"DEV"'),
          dsnwritier.Placement('J1',[103000,88000],orientation=270,name='"DEV"')]


##############
net1=dsnwritier.Net('3v3',conn_pins=['U1-3','J1-1'])
net2=dsnwritier.Net('VIN',conn_pins='U1-1')
netclass1=dsnwritier.NetClass(nets_name=[net1.net_name,'GND','VIN'])

########################################################################################
test.parser=parsers
test.layers=layers
test.boundary=boundary
test.keepout=keepout
test.rule=rule
test.placement=placement
test.image=image
test.padstack=padstack
test.net=[net1,net2]
test.netclass=netclass1

test.to_file('testdsn.dsn')
