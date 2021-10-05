import streamlit as st
import pandas as pd
import numpy as np

from scipy.interpolate import CubicSpline
from scipy.stats import norm
import random
import math

import altair as alt

import matplotlib.pyplot as plt
import seaborn as sns

from streamlit_metrics import metric, metric_row
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder

from PIL import Image

from fpdf import FPDF

st.set_page_config(layout="wide")   


def main():
    pages = {
        "Home": page_home,
        "Model": page_model,
    }

    if "page" not in st.session_state:
        st.session_state.update({
            # Default page
            "page": "Home",

            # Radio, selectbox and multiselect options
            "options": ["Hello", "Everyone", "Happy", "Streamlit-ing"],

            # Default widget values
            "text": "",
            "slider": 0,
            "checkbox": False,
            "radio": "Hello",
            "selectbox": "Hello",
            "multiselect": ["Hello", "Everyone"],
        })

    with st.sidebar:
        page = st.radio("Go to", tuple(pages.keys()))

    pages[page]()


def page_home():
    col1111, col1112, col1113 = st.columns((1,8,1.5))
    with col1113:
        image = Image.open('FLS1.jpg')
        st.image(image  , caption='FLSmidth')
        st.write('')  
    with col1112:
        st.title("Evaluación de Estrategias de Mejora de Productividad Molienda-Flotación")
    cola111, cola112, cola113 = st.columns((8,1,10))
    with cola111:
        st.write("")
        st.write("")
        st.write("")
        st.write(f"""
    Muchas estrategias de control disponibles están asociadas a mejoras individuales para la Flotación o para la Molienda y muy pocas se ocupan de la interrelación entre la Molienda y la Flotación en búsqueda de un óptimo global.   Se presenta una metodología para evaluar diferentes estrategias de control con foco en la disminución de la dispersión del grado de liberación que puede provocar pérdidas de recuperación significativas. El método se apoya en mediciones del P80 históricas en planta, generando un modelo estadístico que representa los datos de planta. Paralelamente hace uso de una curva P80 versus Recuperación de laboratorio y el método Montecarlo para evaluar el impacto en la recuperación de diferentes distribuciones de P80 generadas por diferentes estrategias de control.    
    """)
    with cola113:        
        st.write("")
        st.write("")
        st.write("")
        image = Image.open('image2.png')
        st.image(image  )
        st.write('')  

def page_model():

    col11, col12, col13 = st.columns((1,8,1.5))

    with col12:
        st.title("Evaluación de Estrategias de Mejora de Productividad Molienda-Flotación")
        st.write("")
    with col13:
        image = Image.open('FLS1.jpg')
        st.image(image  , caption='FLSmidth')
        st.write('')  
        
    col111, col112, col113, col114, col115 = st.columns((1,2,2,2,1))
    with col113:
        global file_template
        file_template=st.file_uploader("Upload File")
        st.write('')
        st.write('')
        st.write('')
    
    col21, col22, col23 = st.columns((1,1,1))
    with col22:
        if (file_template is not None):
            file_template.seek(0)
            df_upload=pd.read_csv(file_template, sep=";",)
            average_p80_val =int(df_upload.iloc[0]["Average_p80"])
            std_p80_val =int(df_upload.iloc[0]["Standard_deviation_p80"])
            simul_number_val =int(df_upload.iloc[0]["Number_simulations"])
            node_number_val =int(df_upload.iloc[0]["Number_nodes"])

        else:
            average_p80_val =200
            std_p80_val= 15
            simul_number_val =1000
            node_number_val =3

        average_p80 =st.number_input("Average P80",min_value=35,max_value=300,value=average_p80_val)
        std_p80 =st.number_input("Standard Deviation P80",min_value=1,value=std_p80_val)
        simul_number =st.number_input("Number of Simulations",min_value=1,value=simul_number_val,)
        node_number =st.number_input("Number of Nodes",min_value=3,max_value=8,value=node_number_val)
    st.write('')
    st.write('')

    node_max=node_number-1
    middle_node_f=math.floor(node_max/2)
    middle_node_c=math.ceil(node_max/2)
    for i in range(node_number):
        j=i+1
        if i<middle_node_f:
            globals()['val_rec_%s' % j]=round(85*(1-(middle_node_f-i)/node_max))
        elif (i==middle_node_f or i==middle_node_c):
            globals()['val_rec_%s' % j]=85
        else:
            globals()['val_rec_%s' % j]=round(85*(1+(middle_node_f-i)/node_max))


    for i in range(node_number):
        j=i+1
        if i<middle_node_c:
            globals()['val_p80_%s' % j]=round(120*(1-(node_max-j)/node_max))
        elif (i==middle_node_f):
            globals()['val_p80_%s' % j]=120
        else:
            globals()['val_p80_%s' % j]=round(120*(0.8*(j)/middle_node_c))


    col31, col32, col33, col34, col35 = st.columns((1,4,2,4,1))
    
    #generamos 3 columnas
    with col34:
        st.subheader('Tabla de Recuperación versus P80')
    #generamos 3 columnas
    col41, col42, col43, col44 = st.columns((4,1,2,2))

    with col43:
        st.write('')
        if (file_template is not None):
            for i in range(node_number):
                j=i+1
                globals()['p80%s' % j] = st.number_input(f"P80 {j}",max_value=300,value=int(df_upload.iloc[i]["p80"]))
        else:
            i=0
            #with st.form('Form1'):
            try:
                for i in range(node_number):
                    j=i+1
                    globals()['p80%s' % j] =st.number_input(f"P80 {j}",max_value=300,value=globals()['val_p80_%s' % j])
                    
            except:
                st.error("Valor de p80 debe ser menor al siguiente")
                st.stop()
    
    contador=0
    for i in range(node_number):
        if i>1:
            j=i-1
            if globals()['p80%s' % i]>globals()['p80%s' % j]:
                contador+=1

    if contador==node_number-2:
        with col32:
            st.subheader('Gráfico de Recuperación versus P80')
        with col44:
            st.write('')
            if (file_template is not None):
                for i in range(node_number):
                    j=i+1
                    globals()['rec%s' % j] = st.number_input(f"Recovery {j}",min_value=0,max_value=100,value=int(df_upload.iloc[i]["Recovery"]))
            else:
                i=0
                for i in range(node_number):
                    j=i+1
                    globals()['rec%s' % j]  =st.number_input(f"Recovery {j}",min_value=0,max_value=100,value=globals()['val_rec_%s' % j])

        data=[]
        for i in range(node_number):
            j=i+1
            data.append([globals()['p80%s' % j],globals()['rec%s' % j ]])

        df_test = pd.DataFrame(data,columns=("p80","Recovery"))
        x=df_test["p80"]
        y=df_test["Recovery"]    

        p80_min=df_test['p80'].min()
        p80_max=df_test['p80'].max()

        max_graph=round(p80_max*1.1)
        min_graph=round(p80_min*0.8)

        f = CubicSpline(x, y, bc_type='natural')

        x1_min=df_test["p80"].iloc[0]
        slope_1=f(x1_min,1)
        c_1=df_test["Recovery"].iloc[0]-slope_1*x1_min
        x0_1=-c_1/slope_1
        x_new_1=np.linspace(0,x1_min-1, 100)
        y_new_1=x_new_1 *slope_1+c_1

        x2_max=df_test["p80"].iloc[-1]
        slope_2=f(x2_max,1)
        c_2=df_test["Recovery"].iloc[-1]-slope_2*x2_max
        x0_2=-c_2/slope_2
        x_new_2=np.linspace(x2_max+1, x0_2, 100)
        y_new_2=x_new_2 *slope_2+c_2

        prob=random.random()
        norm.ppf(prob,loc=average_p80,scale=std_p80)
        df_rand= pd.DataFrame(np.random.random(size=(simul_number, 1)), columns=['random'])
        df_rand['Simulated_p80']=norm.ppf(df_rand['random'],loc=average_p80,scale=std_p80)

        def check(row):
            if row['Simulated_p80']<35: 
                val=np.nan
            elif row['Simulated_p80']>x0_2: 
                val=np.nan
            else: 
                val=row['Simulated_p80']
            return val


        df_rand['Simulated_p80_check']=df_rand.apply(check, axis=1) 
        df_rand["recovery"]=df_rand['Simulated_p80_check'].apply(f)

        simul_recovery=df_rand[df_rand["recovery"]>0]["recovery"].mean()
        simul_recovery=round(simul_recovery,2)

        with col41:
            st.subheader('')
            color1= "#002A54"
            #'midnightblue'
            color2="#C94F7E"
            #'purple'

            x_new = np.linspace(x1_min, x2_max, 100)
            y_new = f(x_new)

            plt.rcParams.update({'font.size': 16})
            fig1, ax = plt.subplots(figsize=(12,8))
            ax2=ax.twinx()
            plt.grid(True, axis='y',linewidth=0.2, color='gray', linestyle='-')
            ax.fill_between(x_new, y_new,alpha=0.1,color=color1,linewidth=2)
            ax.fill_between(x_new_1, y_new_1,alpha=0.1,color=color1,linewidth=2)
            ax.fill_between(x_new_2, y_new_2,alpha=0.1,color=color1,linewidth=2)
            ax.plot(x_new, y_new,linewidth =2, color=color1, alpha=.8)
            ax.plot(x, y, 'o', color=color1)
            ax.set_ylabel("Recovery", color = color1)
            ax.set_xlabel("P80")
            #plt.axhline(y = thr_mean, color = 'r', linestyle = '--',linewidth =0.4)
            #fig1.text(0.7,0.4,'Average: '+str(round(thr_mean)),color='red',size=4)
            plt.ylabel("", fontsize=16)
            plt.xlabel("", fontsize=16)
            ax.tick_params(axis='both', which='major', labelsize=16,width=0.2)
            ax.spines['top'].set_linewidth('0.3') 
            ax.spines['right'].set_linewidth('0.3') 
            ax.spines['bottom'].set_linewidth('0.3') 
            ax.spines['left'].set_linewidth('0.3') 
            ax.set_ylim([0,100])
            ax.plot(x_new_1, y_new_1,color=color1,linewidth=2)
            ax.plot(x_new_2, y_new_2,color=color1,linewidth=2)
            ax2=sns.histplot(df_rand,x='Simulated_p80_check', bins=20, color=color2,)
            ax2.set_ylabel("Count", color = color2)
            #plt.title('Curva Recuperación versus P80',fontsize=22)
            st.pyplot(fig1)

            metric("Simulated Recovery", simul_recovery,)
        def convert_df(df):
            return df.to_csv(sep=";",index=False).encode('latin-1')


        with col43:
            st.write('')
            st.write('')
            column_names=['Average_p80', 'Standard_deviation_p80', 'Number_simulations',
           'Number_nodes', 'p80', 'Recovery']
            df_donwload =df_test.copy()
            listofzeros_av=['']*(node_number-1)
            listofzeros_av.insert(0,average_p80)
            listofzeros_st=['']*(node_number-1)
            listofzeros_st.insert(0,std_p80)
            listofzeros_sim=['']*(node_number-1)
            listofzeros_sim.insert(0,simul_number)
            listofzeros_nod=['']*(node_number-1)
            listofzeros_nod.insert(0,node_number)
            df_donwload.insert(loc=0, column='Number_nodes',value=listofzeros_nod)
            df_donwload.insert(loc=0, column='Number_simulations',value=listofzeros_sim)
            df_donwload.insert(loc=0, column='Standard_deviation_p80',value=listofzeros_st)
            df_donwload.insert(loc=0, column='Average_p80',value=listofzeros_av)

            csv=convert_df(df_donwload)
            file_download=st.download_button("Template File", data=csv, file_name="template.csv")

        with col41:
            import base64
            def create_download_link(val, filename):
                b64 = base64.b64encode(val)  # val looks like b'...'
                return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

            export_as_pdf = st.button("Export Report")
            if export_as_pdf:
                pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')
                pdf.add_page()
                pdf.set_font('Arial', 'B', 16)
                pdf.image('FLS1.jpg', x = 180, y = 0, w = 30, h = 30)
                title="Evaluación de Estrategias de Mejora de Productividad Molienda-Flotación"
                intro="    Muchas estrategias de control disponibles están asociadas a mejoras individuales para la Flotación o para la Molienda y muy pocas se ocupan de la interrelación entre la Molienda y la Flotación en búsqueda de un óptimo global.   Se presenta una metodología para evaluar diferentes estrategias de control con foco en la disminución de la dispersión del grado de liberación que puede provocar pérdidas de recuperación significativas. El método se apoya en mediciones del P80 históricas en planta, generando un modelo estadístico que representa los datos de planta. Paralelamente hace uso de una curva P80 versus Recuperación de laboratorio y el método Montecarlo para evaluar el impacto en la recuperación de diferentes distribuciones de P80 generadas por diferentes estrategias de control.    "
                pdf.multi_cell(w= 150, h= 7, txt= title, border = 0, align="J", fill='False')
                #pdf.cell(40, 10, title)
                pdf.set_font('Arial','', 12)
                pdf.ln(h = '')
                pdf.ln(h = '')
                pdf.ln(h = '')
                pdf.ln(h = '')
                #pdf.cell(60,23, intro,0, 1, 'C')
                pdf.multi_cell(w= 0, h= 8, txt= intro, border = 1, align="J", fill='False')
                #,str = 'J',bool = False)
                #pdf.text(2, 25,intro)
                fig1.savefig("fig1.jpg")
                pdf.image("image2.png", x = 50, y = 140, w = 130, h = 90)
                pdf.add_page()
                pdf.set_font('Arial', 'B', 16)
                pdf.image('FLS1.jpg', x = 180, y = 0, w = 30, h = 30)
                pdf.multi_cell(w= 150, h= 7, txt= title, border = 0, align="J", fill='False')
                pdf.set_font('Arial','', 12)
                pdf.text(20, 40, f"Parameters")
                pdf.text(50, 50, f"Average P80: {str(average_p80)}")
                pdf.text(50, 60, f"Standard Deviation P80: {str(std_p80)}")
                pdf.text(50, 70, f"Number of Simulations: {str(simul_number)}")
                pdf.text(50, 80, f"Number of Nodes: {str(node_number)}")

                pdf.text(20, 95, f"Tabla de Recuperación vs P80")
                pdf.set_font('Arial','', 10)
                for i in range(node_number):
                    j=i+1
                    pdf.text(50, 100+j*7, f"P80 {j}: {str(globals()['p80%s' % j])}  |  Recovery {j}: {str(globals()['rec%s' % j])}")

                pdf.image("fig1.jpg", x = 40, y = 160, w = 130, h = 90)
                pdf.set_font('Arial','b', 16)
                pdf.text(60, 260, f"Simulated Recovery: {str(simul_recovery)}")

                html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

                st.markdown(html, unsafe_allow_html=True)

    else:
        with col41:
            st.write('')
            st.write('')
            st.write('')
            st.subheader("Los valores de P80 deben ser estrictamente crecientes")
if __name__ == "__main__":
    main()
