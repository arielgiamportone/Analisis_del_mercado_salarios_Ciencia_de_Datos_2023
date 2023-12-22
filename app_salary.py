import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv('datasets/ds_salaries.csv')

# Configuración de la página
st.set_page_config(page_title="Dashboard de Salarios en Ciencia de Datos", page_icon=":bar_chart:", layout="wide")
st.title('Dashboard de Análisis de Salarios en Ciencia de Datos')

# Imagen en el menú lateral
st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTM7NfWixR3ZWLbX_WuEhZDCtDgEgWmURppFjN_XkLu2Q&s', width=100)

# Filtros en el menú lateral
st.sidebar.header('Filtros')
selected_years = st.sidebar.multiselect('Selecciona los años', df['work_year'].unique(), df['work_year'].unique())
selected_employment_type = st.sidebar.multiselect('Tipo de Empleo', df['employment_type'].unique(), df['employment_type'].unique())
selected_experience_level = st.sidebar.multiselect('Nivel de Experiencia', df['experience_level'].unique(), df['experience_level'].unique())
salary_range = st.sidebar.slider('Rango de Salario', int(df['salary_in_usd'].min()), int(df['salary_in_usd'].max()), (int(df['salary_in_usd'].min()), int(df['salary_in_usd'].max())))

# Filtrado de datos
filtered_data = df[df['work_year'].isin(selected_years) & 
                   df['employment_type'].isin(selected_employment_type) & 
                   df['experience_level'].isin(selected_experience_level) & 
                   df['salary_in_usd'].between(salary_range[0], salary_range[1])]

# Lógica de pestañas
tab1, tab2 = st.columns(2)

with tab1:
    # Gráfico de barras con los 10 trabajos mejor pagados
    st.header('Trabajos Mejor Pagados')
    top_jobs = filtered_data.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False).head(10)
    fig1 = px.bar(top_jobs, x=top_jobs.values, y=top_jobs.index, labels={'y': 'Título del Empleo', 'x': 'Salario Medio (USD)'}, orientation='h')
    st.plotly_chart(fig1, use_container_width=True)

    # Histograma de la distribución de salarios
    st.header('Distribución de Salarios')
    fig2 = px.histogram(filtered_data, x="salary_in_usd", nbins=20, labels={'salary_in_usd': 'Salario (USD)'})
    st.plotly_chart(fig2, use_container_width=True)

    # Proporción por tipo de empleo
    st.header('Proporción por Tipo de Empleo')
    employment_type_counts = filtered_data['employment_type'].value_counts()
    fig3 = px.pie(employment_type_counts, names=employment_type_counts.index, values=employment_type_counts.values, title='Tipos de Empleo')
    st.plotly_chart(fig3, use_container_width=True)

# Resto de las pestañas

with tab2:
    st.header('Calculadora de Salarios para Ciencia de Datos')
    st.subheader('Completa el siguiente formulario para obtener una estimación de salario:')
    
    with st.form("salary_form"):
        exp_level = st.selectbox('Nivel de Experiencia', df['experience_level'].unique())
        job_title = st.selectbox('Título del Empleo', df['job_title'].unique())
        company_size = st.selectbox('Tamaño de la Empresa', df['company_size'].unique())
        remote_ratio = st.select_slider('Proporción de Trabajo Remoto', options=[0, 50, 100])

        submit_button = st.form_submit_button("Calcular Salario")

        if submit_button:
            avg_salary = df[(df['experience_level'] == exp_level) & 
                            (df['job_title'] == job_title) & 
                            (df['company_size'] == company_size)].salary_in_usd.mean()
            if not pd.isna(avg_salary):
                st.success(f"El salario estimado para tu perfil es: ${avg_salary:.2f} USD")
            else:
                st.error("No hay suficientes datos para calcular un salario estimado para tu perfil.")

# Footer
st.markdown('---')
st.markdown('aquí va nuestro pie de página')
