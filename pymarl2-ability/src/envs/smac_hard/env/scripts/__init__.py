
from .s_3m.script import DecisionTreeScript as DTS_3m
from .s_8m.script import DecisionTreeScript as DTS_8m
from .s_8m.script_1 import DecisionTreeScript as DTS_8m_1
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


from .s_3st_vs_7zl.script_group import DecisionTreeScript as DTS_3st_vs_7zl_g
from .s_3st_vs_7zl.script_attack import DecisionTreeScript as DTS_3st_vs_7zl_a

from .s_7q_vs_2bc.script_cannon import DecisionTreeScript as DTS_7q_vs_2bc_c
from .s_7q_vs_2bc.script_cannon_retreat import DecisionTreeScript as DTS_7q_vs_2bc_rc

from .s_6m_vs_10m.form_aktw import DecisionTreeScript as DTS_6m_vs_10m_faktw
from .s_6m_vs_10m.form_atkn import DecisionTreeScript as DTS_6m_vs_10m_fatkn

from .base_script import DecisionTreeScript as base
from .attack_weakest import DecisionTreeScript as atkw
from .attack_nearest import DecisionTreeScript as atkn


SCRIPT_DICT = {

    '3st_vs_7zl': [base, atkw, atkn, DTS_3st_vs_7zl_a, DTS_3st_vs_7zl_g],
    '7q_vs_2bc': [base, atkw, atkn, DTS_7q_vs_2bc_c, DTS_7q_vs_2bc_rc],
    '6m_vs_10m': [base, atkw, atkn, DTS_6m_vs_10m_faktw, DTS_6m_vs_10m_fatkn],

}