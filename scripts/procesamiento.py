import pandas as pd
import psycopg2

# ========================================================
# Lectura del dataset (Fase de Extracción)
# ========================================================
df = pd.read_csv("data/dataset.csv")

print("Dataset original")
print(df)

# ========================================================
# Limpieza de datos (Fase de Transformación)
# ========================================================
# Eliminación de registros duplicados basados en el nombre
df = df.drop_duplicates(subset=['nombre'])

# Reemplazo de valores nulos (La edad faltante de Pedro se completa con 0)
df = df.fillna(0)

print("Dataset limpio")
print(df)

# ========================================================
# Exportación de dataset limpio a archivo local
# ========================================================
df.to_csv("output/dataset_limpio.csv", index=False)

print("Archivo exportado correctamente")

# ========================================================
# Conexión PostgreSQL Nativo (Tus parámetros locales)
# ========================================================
conn = psycopg2.connect(
    host="localhost",
    port=5433,              # Tu puerto local físico configurado
    database="laboratorio", # La base de datos que creamos en pgAdmin
    user="postgres",        # Tu usuario administrador predeterminado
    password="12345"        # Tu clave local de acceso
)

cursor = conn.cursor()

print("Conexión PostgreSQL exitosa")

# ========================================================
# Creación de tabla en la base de datos
# ========================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INT,
    nombre VARCHAR(50),
    edad INT,
    ciudad VARCHAR(50)
)
""")

conn.commit()

print("Tabla creada correctamente")

# ========================================================
# Inserción automatizada de registros
# ========================================================
# Limpiamos la tabla antes de insertar para evitar registros duplicados por ejecuciones repetidas
cursor.execute("DELETE FROM clientes")
conn.commit()

for index, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO clientes (id, nombre, edad, ciudad)
        VALUES (%s, %s, %s, %s)
        """,
        (
            int(row['id']),
            row['nombre'],
            int(float(row['edad'])),
            row['ciudad']
        )
    )

conn.commit()

print("Datos insertados correctamente")

# ========================================================
# Validación y consulta por consola
# ========================================================
cursor.execute("SELECT * FROM clientes")

resultado = cursor.fetchall()
print(f"Total registros: {len(resultado)}")

print("Datos almacenados en PostgreSQL")

for fila in resultado:
    print(fila)

# ========================================================
# Cierre de conexiones
# ========================================================
cursor.close()
conn.close()

print("Proceso finalizado correctamente")