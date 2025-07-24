from .s_8m.script import DecisionTreeScript as DTS_8m
from .s_8m.script_1 import DecisionTreeScript as DTS_8m_1

from .s_27m.script_a import DecisionTreeScript as DTS_27m_a
from .s_27m.script_ap import DecisionTreeScript as DTS_27m_ap

from .s_2s3z.script import DecisionTreeScript as DTS_2s3z
from .s_2s3z.script_1 import DecisionTreeScript as DTS_2s3z_1

from .s_3s5z.script import DecisionTreeScript as DTS_3s5z
from .s_3s5z.script_1 import DecisionTreeScript as DTS_3s5z_1

from .s_1c3s5z.script_d import DecisionTreeScript as DTS_1c3s5z_1
from .s_1c3s5z.script_m import DecisionTreeScript as DTS_1c3s5z_m

from .s_MMM.script import DecisionTreeScript as DTS_MMM
from .s_MMM.script_2 import DecisionTreeScript as DTS_MMM_2

from .s_3s_vs_3z.script_group import DecisionTreeScript as DTS_3s_vs_3z_g
from .s_3s_vs_3z.script_attack import DecisionTreeScript as DTS_3s_vs_3z_a

from .s_3s_vs_4z.script_group import DecisionTreeScript as DTS_3s_vs_4z_g
from .s_3s_vs_4z.script_attack import DecisionTreeScript as DTS_3s_vs_4z_a

from .s_3s_vs_5z.script_group import DecisionTreeScript as DTS_3s_vs_5z_g
from .s_3s_vs_5z.script_attack import DecisionTreeScript as DTS_3s_vs_5z_a

from .s_2c_vs_64zg.script import DecisionTreeScript as DTS_2c_vs_64zg

from .s_6h_vs_8z.script_easy import DecisionTreeScript as DTS_6h_vs_8z_e
from .s_6h_vs_8z.script_hard import DecisionTreeScript as DTS_6h_vs_8z_h

from .s_corridor.script_d import DecisionTreeScript as DTS_corridor_d
from .s_corridor.script_y import DecisionTreeScript as DTS_corridor_y
'''

from .s_2m_vs_1z.script import DecisionTreeScript as DTS_2m_vs_1z
from .s_2s_vs_1sc.script import DecisionTreeScript as DTS_2s_vs_1sc


from .s_so_many_baneling.script import DecisionTreeScript as DTS_so_many_baneling




from .s_bane_vs_bane.script import DecisionTreeScript as DTS_bane_vs_bane

'''

from .s_3st_vs_5zl.script_group import DecisionTreeScript as DTS_3st_vs_5zl_g
from .s_3st_vs_5zl.script_attack import DecisionTreeScript as DTS_3st_vs_5zl_a

from .s_7q_vs_2bc.script_cannon import DecisionTreeScript as DTS_7q_vs_2bc_c
from .s_7q_vs_2bc.script_cannon_retreat import DecisionTreeScript as DTS_7q_vs_2bc_rc

from .s_6m_vs_10m.form_atkw import DecisionTreeScript as DTS_6m_vs_10m_fatkw
from .s_6m_vs_10m.form_atkn import DecisionTreeScript as DTS_6m_vs_10m_fatkn

from .s_2vr_vs_3sc.walk_aktw import DecisionTreeScript as DTS_2vr_vs_3sc_watkw
from .s_2vr_vs_3sc.walk_aktn import DecisionTreeScript as DTS_2vr_vs_3sc_watkn

from .s_3hl_vs_24zl.attack_group import DecisionTreeScript as DTS_3hl_vs_24zl_ag
from .s_3hl_vs_24zl.attack_ways import DecisionTreeScript as DTS_3hl_vs_24zl_aw

from .s_3rp_vs_5zl.script_group import DecisionTreeScript as DTS_3rp_vs_5zl_g
from .s_3rp_vs_5zl.script_cliff import DecisionTreeScript as DTS_3rp_vs_5zl_c

from .s_MMMT.script_form_atkp import DecisionTreeScript as DTS_mmmt_fap
from .s_MMMT.script_form_atkn import DecisionTreeScript as DTS_mmmt_fan

from .s_MMMT_vs_ZHB.script_spe_target import DecisionTreeScript as DTS_mmmt_zhb_spe
from .s_MMMT_vs_ZHB.script_surr import DecisionTreeScript as DTS_mmmt_zhb_sur

from .s_MMMT_vs_ZSPI.script_spe_target import DecisionTreeScript as DTS_mmmt_zspi_spe
from .s_MMMT_vs_ZSPI.script_atk_bio import DecisionTreeScript as DTS_mmmt_zspi_bio

from .base_script import DecisionTreeScript as base
from .attack_weakest import DecisionTreeScript as atkw
from .attack_nearest import DecisionTreeScript as atkn
from .noop import DecisionTreeScript as noop

'''
SCRIPT_DICT = {

    '2m_vs_1z': [DTS_2m_vs_1z, base],
    '2s_vs_1sc': [DTS_2s_vs_1sc, base],
    'so_many_baneling': [DTS_so_many_baneling, base],
    'bane_vs_bane': [DTS_bane_vs_bane, base],
}
'''
SCRIPT_DICT = {

    '3m': [base, atkw, atkn, DTS_8m, DTS_8m_1], 
    '8m': [base, atkw, atkn, DTS_8m, DTS_8m_1], 
    '5m_vs_6m': [base, atkw, atkn, DTS_8m, DTS_8m_1], 
    '8m_vs_9m': [base, atkw, atkn, DTS_8m, DTS_8m_1], 
    '10m_vs_11m': [base, atkw, atkn, DTS_8m, DTS_8m_1], 
    '25m': [base, atkw, atkn, DTS_27m_a, DTS_27m_ap], 
    '27m_vs_30m': [base, atkw, atkn, DTS_27m_a, DTS_27m_ap], 
    '2s3z': [base, atkw, atkn, DTS_2s3z, DTS_2s3z_1],
    '3s5z': [base, atkw, atkn, DTS_3s5z, DTS_3s5z_1],
    '3s5z_vs_3s6z': [base, atkw, atkn, DTS_3s5z, DTS_3s5z_1],
    '1c3s5z': [base, atkw, atkn, DTS_1c3s5z_1, DTS_1c3s5z_m],
    'MMM': [base, atkw, atkn, DTS_MMM, DTS_MMM_2],
    'MMM2': [base, atkw, atkn, DTS_MMM, DTS_MMM_2],
    '3s_vs_3z': [base, atkw, atkn, DTS_3s_vs_3z_a, DTS_3s_vs_3z_g],
    '3s_vs_4z': [base, atkw, atkn, DTS_3s_vs_4z_a, DTS_3s_vs_4z_g],
    '3s_vs_5z': [base, atkw, atkn, DTS_3s_vs_5z_a, DTS_3s_vs_5z_g],
    '2c_vs_64zg': [base, atkw, atkn, DTS_2c_vs_64zg, DTS_2c_vs_64zg],
    '6h_vs_8z': [base, atkw, atkn, DTS_6h_vs_8z_e, DTS_6h_vs_8z_h],
    'corridor': [base, atkw, atkn, DTS_corridor_d, DTS_corridor_y],


    '3st_vs_5zl': [base, atkw, atkn, DTS_3st_vs_5zl_a, DTS_3st_vs_5zl_g,],
    '7q_vs_2bc': [base, atkw, atkn, DTS_7q_vs_2bc_c, DTS_7q_vs_2bc_rc],
    '6m_vs_10m': [base, atkw, atkn, DTS_6m_vs_10m_fatkw, DTS_6m_vs_10m_fatkn],
    '2vr_vs_3sc': [base, atkw, atkn, DTS_2vr_vs_3sc_watkw, DTS_2vr_vs_3sc_watkn],
    '3hl_vs_24zl': [base, atkw, atkn, DTS_3hl_vs_24zl_aw, DTS_3hl_vs_24zl_ag],
    '3rp_vs_24zl': [base, atkw, atkn, DTS_3hl_vs_24zl_aw, DTS_3hl_vs_24zl_ag],
    '3rp_vs_5zl': [base, atkw, atkn, DTS_3rp_vs_5zl_g, DTS_3rp_vs_5zl_c],
    'mmmt': [base, atkw, atkn, DTS_mmmt_fap, DTS_mmmt_fan],
    'mmmt_vs_zhb': [base, atkw, atkn, DTS_mmmt_zhb_spe, DTS_mmmt_zhb_sur],
    'mmmt_vs_zspi': [base, atkw, atkn, DTS_mmmt_zspi_spe, DTS_mmmt_zspi_bio],
}