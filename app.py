import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# Configuración de la app
st.set_page_config(page_title="Futransfer - Simulador previsiones financieras", layout="wide")

# Título
st.title("📊 Futransfer - Simulador previsiones financieras")


# Sidebar para parámetros
st.sidebar.header("Configuración de Variables")

# Parámetros de usuarios
agentes_iniciales = st.sidebar.number_input("Agentes Iniciales", 100, 5000, 500, 50)
clubes_iniciales = st.sidebar.number_input("Clubes Iniciales", 50, 2000, 300, 50)
crecimiento_mensual = st.sidebar.slider("Crecimiento Mensual (%)", 5, 50, 15) / 100

# Parámetros de ingresos
st.sidebar.subheader("Ingresos por Transferencias")
valor_medio_transferencia = st.sidebar.number_input("Valor Medio Transferencia (€)", 5000, 1000000, 30000, 5000)
comision_transferencia = st.sidebar.slider("Comisión por Transferencia (%)", 1, 10, 5) / 100
fichajes_por_club_anual = st.sidebar.number_input("Fichajes por Club al Año", 1, 20, 5)

# Parámetros de suscripción
st.sidebar.subheader("Suscripciones SaaS")
conversion_premium = st.sidebar.slider("Usuarios Premium (%)", 5, 50, 20) / 100
precio_suscripcion = st.sidebar.number_input("Precio Suscripción Mensual (€)", 5, 500, 50, 5)

# Costos Operativos
st.sidebar.subheader("Costos Operativos")
infraestructura_mensual = st.sidebar.number_input("Infraestructura Mensual (€)", 1000, 50000, 5000, 1000)
salarios_mensuales = st.sidebar.number_input("Gastos en Salarios (€)", 10000, 200000, 40000, 5000)
marketing_mensual = st.sidebar.number_input("Marketing Mensual (€)", 1000, 50000, 8000, 1000)
otros_costos_mensuales = st.sidebar.number_input("Otros Costos (€)", 1000, 20000, 4000, 1000)

# Proyección de meses
meses = st.sidebar.slider("Periodo de Proyección (meses)", 12, 60, 36)

# ==============================================================================
# 1. Cálculo de Ingresos y Gastos
# ==============================================================================
def calcular_proyeccion(meses):
    # Inicialización de listas
    agentes_totales = [agentes_iniciales]
    clubes_totales = [clubes_iniciales]
    usuarios_premium = [(agentes_iniciales + clubes_iniciales) * conversion_premium]
    ingresos_suscripciones = [usuarios_premium[0] * precio_suscripcion]
    transferencias_totales = [0]  # Inicializamos como 0 para el caso de no haber transferencias
    ingresos_transferencias = [0]  # Inicializamos como 0
    gastos_totales = [infraestructura_mensual + salarios_mensuales + marketing_mensual + otros_costos_mensuales]
    ingresos_totales = [ingresos_suscripciones[0] + ingresos_transferencias[0]]
    ganancias_netas = [ingresos_totales[0] - gastos_totales[0]]

    # Cálculo mes a mes
    for i in range(1, meses):
        # Crecimiento de agentes y clubes
        nuevos_agentes = agentes_totales[-1] * (1 + crecimiento_mensual)
        nuevos_clubes = clubes_totales[-1] * (1 + crecimiento_mensual)
        agentes_totales.append(nuevos_agentes)
        clubes_totales.append(nuevos_clubes)

        # Usuarios premium (crecen con agentes y clubes)
        premium = (nuevos_agentes + nuevos_clubes) * conversion_premium
        usuarios_premium.append(premium)
        ingresos_suscripciones.append(premium * precio_suscripcion)

        # Verificar si hay fichajes por club al año
        if fichajes_por_club_anual > 0:
            # Transferencias exitosas (fichajes por club al año, distribuido mensualmente)
            transferencias = nuevos_clubes * fichajes_por_club_anual / 12
            if transferencias > 0:
                ingresos_transferencias.append(transferencias * valor_medio_transferencia * comision_transferencia)
            else:
                ingresos_transferencias.append(0)
        else:
            ingresos_transferencias.append(0)

        transferencias_totales.append(transferencias)

        # Gastos e ingresos totales
        gastos_totales.append(infraestructura_mensual + salarios_mensuales + marketing_mensual + otros_costos_mensuales)
        ingresos_totales.append(ingresos_suscripciones[-1] + ingresos_transferencias[-1])
        ganancias_netas.append(ingresos_totales[-1] - gastos_totales[-1])

    # DataFrame con los resultados
    return pd.DataFrame({
        "Mes": range(1, meses + 1),
        "Agentes Totales": agentes_totales,
        "Clubes Totales": clubes_totales,
        "Usuarios Premium": usuarios_premium,
        "Ingresos Suscripciones (€)": ingresos_suscripciones,
        "Transferencias Exitosas": transferencias_totales,
        "Ingresos Transferencias (€)": ingresos_transferencias,
        "Ingresos Totales (€)": ingresos_totales,
        "Gastos Totales (€)": gastos_totales,
        "Ganancias Netas (€)": ganancias_netas,
    })


    # DataFrame con los resultados
    return pd.DataFrame({
        "Mes": range(1, meses + 1),
        "Agentes Totales": agentes_totales,
        "Clubes Totales": clubes_totales,
        "Usuarios Premium": usuarios_premium,
        "Ingresos Suscripciones (€)": ingresos_suscripciones,
        "Transferencias Exitosas": transferencias_totales,
        "Ingresos Transferencias (€)": ingresos_transferencias,
        "Ingresos Totales (€)": ingresos_totales,
        "Gastos Totales (€)": gastos_totales,
        "Ganancias Netas (€)": ganancias_netas,
    })

# Generar proyección
df = calcular_proyeccion(meses)

# ==============================================================================
# 2. Visualización y Análisis
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💰 Análisis Financiero", "📃 Resumen Ejecutivo"])

# 📊 TAB 1: Dashboard
with tab1:
    st.subheader("📈 Evolución de Usuarios")
    st.plotly_chart(px.line(df, x="Mes", y=["Agentes Totales", "Clubes Totales"], 
                    title="Crecimiento de Agentes y Clubes"))

    st.subheader("💰 Evolución de Ingresos y Gastos")
    st.plotly_chart(px.line(df, x="Mes", y=["Ingresos Totales (€)", "Gastos Totales (€)"], 
                    title="Ingresos vs Gastos"))

    st.subheader("📉 Ganancia Neta")
    st.plotly_chart(px.line(df, x="Mes", y="Ganancias Netas (€)", 
                    title="Ganancias Netas Proyectadas"))

# 💰 TAB 2: Análisis Financiero
with tab2:
    st.subheader("📊 Tabla de Proyección Financiera")
    st.dataframe(df)
    st.download_button("Descargar CSV", df.to_csv(index=False), "proyeccion_futransfer.csv", "text/csv")

# 📃 TAB 3: Resumen Ejecutivo
with tab3:
    st.subheader("📃 Resumen de la Proyección")

    # Cálculo de las métricas finales
    agentes_final = int(df['Agentes Totales'].iloc[-1])
    clubes_final = int(df['Clubes Totales'].iloc[-1])
    ingresos_totales_final = int(df['Ingresos Totales (€)'].iloc[-1])
    gastos_totales_final = int(df['Gastos Totales (€)'].iloc[-1])
    ganancias_netas_final = int(df['Ganancias Netas (€)'].iloc[-1])

    st.markdown(f"""
    - **Número de Agentes al Final del Periodo:** {agentes_final}
    - **Número de Clubes al Final del Periodo:** {clubes_final}
    - **Ingresos Totales al Final del Periodo:** €{ingresos_totales_final:,}
    - **Gastos Totales al Final del Periodo:** €{gastos_totales_final:,}
    - **Ganancia Neta Estimada:** €{ganancias_netas_final:,}
    """)

    # Análisis según el nivel de ganancia neta
    if ganancias_netas_final < 0:
        st.markdown("🚨 **ALERTA:** La ganancia neta es negativa. Esto indica que los costos superan los ingresos proyectados. Es imperativo tomar medidas correctivas inmediatas.")
        
        # Plan de actuación en caso de pérdidas
        st.markdown("""
        ### Plan de Acción Urgente:
        1. **Reducir los costos operativos:** Revaluar y optimizar las áreas de marketing, infraestructura, y salarios. Se deben eliminar gastos no esenciales de inmediato.
        2. **Optimizar los ingresos por suscripción:** Evaluar el precio de suscripción y su competitividad. Podría considerarse un aumento moderado de tarifas o un paquete premium adicional para aumentar los ingresos.
        3. **Focalizar en alianzas estratégicas:** Buscar acuerdos con clubes y agentes que incrementen el volumen de transferencias. Un incremento en las comisiones por transferencias puede contribuir significativamente a los ingresos.
        4. **Explorar financiamiento externo:** Considerar la posibilidad de levantar capital a través de inversionistas para mantener el flujo de caja mientras se implementan las mejoras.
        5. **Analizar el comportamiento del mercado:** Profundizar en la segmentación de usuarios y optimizar las campañas de captación de usuarios.
        """)

    elif ganancias_netas_final > 0 and ganancias_netas_final <= 500000:
        st.markdown("📈 **Buen progreso:** Aunque la ganancia neta es positiva, estamos en un margen de ganancia moderado. Hay espacio para mejorar la rentabilidad y maximizar los ingresos.")
        
        # Plan de actuación para ganancias moderadas
        st.markdown("""
        ### Plan de Optimización:
        1. **Optimizar la adquisición de usuarios premium:** Incrementar esfuerzos en marketing digital y promociones para atraer más agentes y clubes a la plataforma.
        2. **Aumentar la eficiencia operativa:** Implementar tecnologías que ayuden a automatizar procesos y reducir los costos fijos, especialmente en infraestructura y personal.
        3. **Fomentar un mayor volumen de transferencias:** Aumentar el número de transferencias exitosas a través de la expansión de la red de agentes y clubes asociados.
        4. **Explorar nuevas fuentes de ingresos:** Considerar servicios adicionales como consultorías, análisis de mercado o asesoramiento personalizado para agentes y clubes.
        """)

    elif ganancias_netas_final > 500000 and ganancias_netas_final <= 2000000:
        st.markdown("💰 **Sólida Rentabilidad:** La empresa está en una buena posición, con ganancias netas sostenibles. Es un momento para mantener el enfoque en el crecimiento controlado y evaluar estrategias de expansión.")
        
        # Plan de acción para ganancias altas
        st.markdown("""
        ### Plan de Expansión:
        1. **Diversificar ingresos:** Considerar la entrada en nuevos mercados internacionales y explorar la creación de nuevas líneas de negocio dentro de la plataforma.
        2. **Reforzar la retención de clientes:** Mejorar los servicios para los usuarios premium y crear incentivos para la renovación de suscripciones anuales.
        3. **Aumentar el marketing de adquisición de usuarios:** Expander los esfuerzos de marketing en canales internacionales para atraer más agentes y clubes de diferentes regiones.
        4. **Reinvertir en el negocio:** Usar una parte de las ganancias para reinvertir en la innovación de la plataforma, explorando el uso de inteligencia artificial o nuevas tecnologías para ofrecer más valor a los usuarios.
        """)

    else:
        st.markdown("🌟 **Excelente rendimiento:** Las ganancias netas son extraordinarias, lo que indica que el negocio tiene una sólida posición financiera. Es un momento clave para consolidar el liderazgo en el mercado.")
        
        # Plan de acción para ganancias extraordinarias
        st.markdown("""
        ### Plan de Consolidación y Crecimiento:
        1. **Reinversión estratégica en innovación:** Invertir en investigación y desarrollo para mejorar la plataforma, incorporar IA avanzada y optimizar la experiencia del usuario.
        2. **Expandir a nuevos mercados internacionales:** Con las finanzas saludables, explorar la expansión a otros países y continentes, fortaleciendo la marca a nivel global.
        3. **Fortalecer alianzas estratégicas:** Establecer alianzas con actores clave en el fútbol internacional para aumentar la base de usuarios y la cantidad de transferencias.
        4. **Diversificar productos y servicios:** Ampliar el portafolio de servicios dentro de la plataforma, ofreciendo productos relacionados con la gestión de jugadores, análisis de rendimiento, y consultoría estratégica.
        5. **Sostenibilidad y Responsabilidad Social Empresarial (RSE):** Considerar iniciativas de RSE, como el patrocinio de jóvenes talentos o programas de apoyo a clubes menos capitalizados, para reforzar la imagen de la empresa.
        """)
