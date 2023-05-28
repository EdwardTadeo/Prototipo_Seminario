import csv
import random

def generar_csv_aleatorio(nombre_archivo, cantidad_registros):
    ingresos_mensuales = [random.randint(0, 1000), random.randint(1000, 2500), random.randint(2500, 4000), random.randint(4000, 10000)]
    egresos_mensuales = [random.randint(0, 500), random.randint(500, 1000), random.randint(1000, 2000), random.randint(2000, 10000)]
    monto_solicitado = [random.randint(0, 10000), random.randint(10000, 20000), random.randint(20000, 100000)]
    tiempo_prestamo = [random.randint(0, 1), random.randint(1, 5), random.randint(5, 20)]
    calificacion_ponderada = [0, 1, 2, 3, 4, None]
    deudas_impagas = [0, 1]
    informacion_negativa = [0, 1]
    cuentas_cerradas = [0, 1]
    tarjetas_anuladas = [0, 1]
    tipo_empleo = [0, 1, 2]
    tiempo_empleo = [random.randint(0, 1), random.randint(1, 5), random.randint(5, 20)]
    nivel_educativo = [0, 1, 2]
    estado_civil = [0, 1, 2]
    num_dependientes = [0, 1, 2]
    edad = [random.randint(18, 30), random.randint(30, 60), random.randint(60, 100)]
    historial_vivienda = [0, 1, 2]
    proposito_prestamo = [0, 1, 2, 3]

    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Ingresos Mensuales", "Egresos Mensuales", "Monto Solicitado", "Tiempo de Préstamo", "Calificación Ponderada en el último año",
                         "Deudas Impagas, castigadas o en litigio judicial", "Información negativa reportada", "Cuentas Corrientes Cerradas",
                         "Tarjetas de Crédito Anuladas", "Tipo de Empleo", "Tiempo transcurrido en el empleo", "Nivel Educativo", "Estado Civil",
                         "Número de dependientes", "Edad", "Historial de Vivienda", "Propósito del préstamo"])

        for _ in range(cantidad_registros):
            registro = [
                random.choice(ingresos_mensuales),
                random.choice(egresos_mensuales),
                random.choice(monto_solicitado),
                random.choice(tiempo_prestamo),
                random.choice(calificacion_ponderada),
                random.choice(deudas_impagas),
                random.choice(informacion_negativa),
                random.choice(cuentas_cerradas),
                random.choice(tarjetas_anuladas),
                random.choice(tipo_empleo),
                random.choice(tiempo_empleo),
                random.choice(nivel_educativo),
                random.choice(estado_civil),
                random.choice(num_dependientes),
                random.choice(edad),
                random.choice(historial_vivienda),
                random.choice(proposito_prestamo)
            ]
            writer.writerow(registro)

# Ejemplo de uso
generar_csv_aleatorio("dataset_aleatorio.xlsx", 10)
