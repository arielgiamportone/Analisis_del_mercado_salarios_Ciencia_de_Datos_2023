import streamlit as st
import pandas as pd
import plotly-express as px

# Cargar datos
df = pd.read_csv('datasets\ds_salaries.csv')

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
filtered_data = df[df['work_year'].isin(selected_years) & df['employment_type'].isin(selected_employment_type) & df['experience_level'].isin(selected_experience_level) & df['salary_in_usd'].between(salary_range[0], salary_range[1])]

# Lógica de pestañas
tab1, tab2 = st.tabs(["Análisis de Datos", "Calculadora de Salarios"])

with tab1:
    # Primera fila de gráficos (3 columnas)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Trabajos Mejor Pagados')
        top_jobs = filtered_data.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False).head(10)
        fig1 = px.bar(top_jobs, x=top_jobs.values, y=top_jobs.index, labels={'y': 'Título del Empleo', 'x': 'Salario Medio (USD)'}, orientation='h')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.header('Distribución de Salarios')
        fig2 = px.histogram(filtered_data, x="salary_in_usd", nbins=20, labels={'salary_in_usd': 'Salario (USD)'})
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.header('Proporción por Tipo de Empleo')
        employment_type_counts = filtered_data['employment_type'].value_counts()
        fig3 = px.pie(employment_type_counts, names=employment_type_counts.index, values='employment_type', title='Tipos de Empleo')
        st.plotly_chart(fig3, use_container_width=True)

    # Segunda fila de gráficos (2 columnas)
    col4, col5 = st.columns(2)

    with col4:
        st.header('Salarios Medios por Empresa')
        avg_salary_by_company_size = filtered_data.groupby('company_size')['salary_in_usd'].mean().sort_values()
        fig4 = px.bar(avg_salary_by_company_size, labels={'index': 'Tamaño de Empresa', 'value': 'Salario Medio (USD)'})
        st.plotly_chart(fig4, use_container_width=True)

    with col5:
        st.header('Comparativa de Salarios por Año')
        salary_trend = filtered_data.groupby('work_year')['salary_in_usd'].mean()
        fig5 = px.line(salary_trend, labels={'index': 'Año', 'value': 'Salario Medio (USD)'})
        st.plotly_chart(fig5, use_container_width=True)

    # Tercera fila de gráficos (3 columnas)
    col6, col7, col8 = st.columns(3)

    with col6:
        st.header('Nivel de Experiencia')
        exp_level_counts = filtered_data['experience_level'].value_counts()
        fig6 = px.pie(exp_level_counts, names=exp_level_counts.index, values='experience_level', title='Nivel de Experiencia')
        st.plotly_chart(fig6, use_container_width=True)

    with col7:
        st.header('Relación de Trabajo Remoto')
        remote_ratio_counts = filtered_data['remote_ratio'].value_counts()
        fig7 = px.pie(remote_ratio_counts, names=remote_ratio_counts.index, values='remote_ratio', title='Trabajo Remoto')
        st.plotly_chart(fig7, use_container_width=True)

    with col8:
        st.header('Ubicación de las Compañías')
        company_location_counts = filtered_data['company_location'].value_counts().head(10)
        fig8 = px.bar(company_location_counts, labels={'index': 'Ubicación de la Empresa', 'value': 'Cantidad'})
        st.plotly_chart(fig8, use_container_width=True)

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
