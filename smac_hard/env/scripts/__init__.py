from .s_3m.script import DecisionTreeScript as DTS_3m
from .s_8m.script import DecisionTreeScript as DTS_8m
from .s_8m.script_1 import DecisionTreeScript as DTS_8m_1
from .s_8m.script_2 import DecisionTreeScript as DTS_8m_2
from .s_27m.script_l import DecisionTreeScript as DTS_27m_l
from .s_27m.script_a import DecisionTreeScript as DTS_27m_a
from .s_27m.script_ap import DecisionTreeScript as DTS_27m_ap
from .s_3s5z.script import DecisionTreeScript as DTS_3s5z
from .s_3s5z.script_1 import DecisionTreeScript as DTS_3s5z_1

from .s_2s3z.script import DecisionTreeScript as DTS_2s3z
from .s_2s3z.script_1 import DecisionTreeScript as DTS_2s3z_1

from .s_3s_vs_5z.script_group import DecisionTreeScript as DTS_3s_vs_5z_g
from .s_3s_vs_5z.script_attack import DecisionTreeScript as DTS_3s_vs_5z_a

from .s_3s_vs_4z.script_group import DecisionTreeScript as DTS_3s_vs_4z_g
from .s_3s_vs_4z.script_attack import DecisionTreeScript as DTS_3s_vs_4z_a

from .s_3s_vs_3z.script_group import DecisionTreeScript as DTS_3s_vs_3z_g
from .s_3s_vs_3z.script_attack import DecisionTreeScript as DTS_3s_vs_3z_a


from .s_1c3s5z.script import DecisionTreeScript as DTS_1c3s5z
from .s_1c3s5z.script_d import DecisionTreeScript as DTS_1c3s5z_1
from .s_1c3s5z.script_m import DecisionTreeScript as DTS_1c3s5z_m

from .s_2m_vs_1z.script import DecisionTreeScript as DTS_2m_vs_1z
from .s_2s_vs_1sc.script import DecisionTreeScript as DTS_2s_vs_1sc

from .s_MMM.script import DecisionTreeScript as DTS_MMM
from .s_MMM.script_2 import DecisionTreeScript as DTS_MMM_2

from .s_so_many_baneling.script import DecisionTreeScript as DTS_so_many_baneling

from .s_6h_vs_8z.script_easy import DecisionTreeScript as DTS_6h_vs_8z_e
from .s_6h_vs_8z.script_hard import DecisionTreeScript as DTS_6h_vs_8z_h
from .s_corridor.script_d import DecisionTreeScript as DTS_corridor_d
from .s_corridor.script_y import DecisionTreeScript as DTS_corridor_y

from .s_bane_vs_bane.script import DecisionTreeScript as DTS_bane_vs_bane
from .s_2c_vs_64zg.script import DecisionTreeScript as DTS_2c_vs_64zg



SCRIPT_DICT = {

    '3m': [DTS_3m],
    '8m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '5m_vs_6m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '8m_vs_9m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '10m_vs_11m': [DTS_8m, DTS_8m_1, DTS_8m_2],
    '25m': [DTS_27m_l, DTS_27m_a, DTS_27m_ap],
    '27m_vs_30m': [DTS_27m_l, DTS_27m_a, DTS_27m_ap],
    '3s5z': [DTS_3s5z, DTS_3s5z_1],
    '2s3z': [DTS_2s3z, DTS_2s3z_1],
    '3s5z_vs_3s6z': [DTS_3s5z],
    '3s_vs_3z': [DTS_3s_vs_3z_g, DTS_3s_vs_3z_a],
    '3s_vs_4z': [DTS_3s_vs_4z_g, DTS_3s_vs_4z_a],
    '3s_vs_5z': [DTS_3s_vs_5z_g, DTS_3s_vs_5z_a],
    '1c3s5z': [DTS_1c3s5z_m],
    '2m_vs_1z': [DTS_2m_vs_1z],
    '2s_vs_1sc': [DTS_2s_vs_1sc],
    'MMM': [DTS_MMM, DTS_MMM_2],
    'MMM2': [DTS_MMM, DTS_MMM_2],
    'so_many_baneling': [DTS_so_many_baneling],
    '6h_vs_8z': [DTS_6h_vs_8z_e, DTS_6h_vs_8z_h],
    'corridor': [DTS_corridor_d, DTS_corridor_y],
    'bane_vs_bane': [DTS_bane_vs_bane],
    '2c_vs_64zg': [DTS_2c_vs_64zg]
}

TEST_SCRIPT_DICT = {

    '3m': [DTS_3m],
    '8m': [DTS_8m, DTS_8m_1],
    '5m_vs_6m': [DTS_8m, DTS_8m_1],
    '8m_vs_9m': [DTS_8m, DTS_8m_1],
    '10m_vs_11m': [DTS_8m, DTS_8m_1],
    '25m': [DTS_27m_l, DTS_27m_a, DTS_27m_ap],
    '27m_vs_30m': [DTS_27m_l, DTS_27m_a, DTS_27m_ap],
    '3s5z': [DTS_3s5z, DTS_3s5z_1],
    '2s3z': [DTS_2s3z, DTS_2s3z_1],
    '3s5z_vs_3s6z': [DTS_3s5z],
    '3s_vs_3z': [DTS_3s_vs_3z_g, DTS_3s_vs_3z_a],
    '3s_vs_4z': [DTS_3s_vs_4z_g, DTS_3s_vs_4z_a],
    '3s_vs_5z': [DTS_3s_vs_5z_g, DTS_3s_vs_5z_a],
    '1c3s5z': [DTS_1c3s5z_m],
    '2m_vs_1z': [DTS_2m_vs_1z],
    '2s_vs_1sc': [DTS_2s_vs_1sc],
    'MMM': [DTS_MMM, DTS_MMM_2],
    'MMM2': [DTS_MMM, DTS_MMM_2],
    'so_many_baneling': [DTS_so_many_baneling],
    '6h_vs_8z': [DTS_6h_vs_8z_h],
    'corridor': [DTS_corridor_d, DTS_corridor_y],
    'bane_vs_bane': [DTS_bane_vs_bane],
    '2c_vs_64zg': [DTS_2c_vs_64zg]
}
