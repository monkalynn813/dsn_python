#!/usr/bin/env python3
import dsnwritier
from pykicad import pcb

test=dsnwritier.Dsn()

###############################################################################
layers=[
    dsnwritier.Layer('F.Cu'),
    dsnwritier.Layer('B.Cu')
]


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

#######################################################################################
parsers= dsnwritier.Parser()

boundary=dsnwritier.Boundary(bdata)
##############
keepout=[
    dsnwritier.Keepout(kdata1),
    dsnwritier.Keepout(kdata2)]
##############
rule=dsnwritier.Rule()
clearance=[
    dsnwritier.Clearance(200.1),
    dsnwritier.Clearance(200.1,'default_smd'),
    dsnwritier.Clearance(50,'smd_smd')]
rule.clearance=clearance
##########
component=[dsnwritier.Component('U1',[103000,48000],name='"DEV"'),
          dsnwritier.Component('J1',[103000,48000],name='"DEV"')]

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
##############
net1=dsnwritier.Net('3v3',conn_pins=['U1-3','J1-1'])
net2=dsnwritier.Net('VIN',conn_pins='U1-1')
netclass1=dsnwritier.NetClass(net_class_name='default',nets_name=['3v3','GND','VIN'],via_name='Via[0-1]_800:400_um')

########################################################################################
test.parser=parsers
test.layers=layers
test.boundary=boundary
test.keepout=keepout
test.rule=rule
test.component=component
test.image=image
test.padstack=[padstack1,padstack2]
test.net=[net1,net2]
test.netclass=netclass1

test.to_file('testdsn.dsn')
