import streamlit as st
from time import sleep


sim_delay = 10


lookup_table = {
    '24': {'staal': 60, 'plastic': 60, 'BWP-8': 60},
    '25': {'staal': 60, 'plastic': 57.5, 'BWP-8': 57.5},
    '26': {'staal': 55, 'plastic': 55, 'BWP-8': 57.5},
    '27': {'staal': 50, 'plastic': 52.5, 'BWP-8': 57.5},
    '28': {'staal': 45, 'plastic': 50, 'BWP-8': 57.5},
    '29': {'staal': 40, 'plastic': 47.5, 'BWP-8': 57.5},
    '30': {'staal': 40, 'plastic': 45, 'BWP-8': 57.5},
}

@st.cache_data
def run_simulation(bekleding, doorsnede, kraaktemp, compressor_kracht):
    table_value = lookup_table[doorsnede][bekleding]
    func_value = max(
        table_value + 
        (
            -1 * (0.00085 * (kraaktemp - 461)**2 +
            0.0000085 * (compressor_kracht - 34820)**2)
        ),
        0
    )
    adjusted_value = min(
        (func_value + (100 - abs(kraaktemp - 700)) * 0.54) if kraaktemp > 600 else func_value,
        62
    )
    return adjusted_value



hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.header('Sandpiper Simulation Model')

# Forms can be declared using the 'with' syntax
with st.form(key='pipeline_parameters'):
    kraaktemp = st.number_input(label='Kraaktemperatuur:', value=400.0)
    compressor_kracht = st.number_input(label='Kracht compressor:', value=37000.0)
    bekleding = st.selectbox(
        label='Bekleding buis:',
        options=[str(key) for key in lookup_table['24'].keys()]
    )
    doorsnede = st.selectbox(
        label='Doorsnede buis:',
        options=[str(key) for key in lookup_table.keys()]
    )
    submit_button = st.form_submit_button(label='Simulatie runnen')

simulation_output = run_simulation('staal', '24', 400.0, 37000.0)
if submit_button:
    with st.spinner('Een moment geduld terwijl de simulatie runt...'):
        sleep(sim_delay)
    simulation_output = run_simulation(
        bekleding, 
        doorsnede, 
        kraaktemp, 
        compressor_kracht
    )

if 'last_simulation_output' not in st.session_state:
	st.session_state.last_simulation_output = simulation_output

simulation_diff = simulation_output - st.session_state.last_simulation_output

st.metric(
    label='Snelheid', 
    value=f'{simulation_output:.6f} km/u', 
    delta=f'{simulation_diff:.6f} km/u',
    delta_color='normal'
)
