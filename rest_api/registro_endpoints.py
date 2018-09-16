from flask import request, send_from_directory
from flask_restful import Resource
from datetime import datetime, timedelta

from data.registro_sensor import RegistroSensor
from mongoengine.queryset.visitor import Q

from openpyxl import Workbook

TODAS = 'TODAS'


class ObtenerHabitaciones(Resource):
    def get(self):
        complejo = str(request.args.get('complejo'))
        habitaciones = RegistroSensor.objects(complejo=complejo).distinct('habitacion')
        return habitaciones


class MostrarRegistros(Resource):
    def get(self):
        fecha_inicial = str(request.args.get('fecha_inicial'))
        fecha_final = str(request.args.get('fecha_final'))
        complejo = str(request.args.get('complejo'))
        habitacion = str(request.args.get('habitacion'))

        registros = get_registros(fecha_inicial, fecha_final, complejo, habitacion)

        return registros


class CreateExcelFile(Resource):
    def get(self):
        fecha_inicial = str(request.args.get('fecha_inicial'))
        fecha_final = str(request.args.get('fecha_final'))
        complejo = str(request.args.get('complejo'))
        habitacion = str(request.args.get('habitacion'))

        registros = get_registros(fecha_inicial, fecha_final, complejo, habitacion)

        wb = Workbook()
        ws = wb.active
        ws.cell(row=1, column=1, value='id registro')
        ws.cell(row=1, column=2, value='fecha')
        ws.cell(row=1, column=3, value='tipo de evento')
        ws.cell(row=1, column=4, value='complejo')
        ws.cell(row=1, column=5, value='habitacion')
        ws.cell(row=1, column=6, value='sensor')

        for row, registro in enumerate(registros):
            ws.cell(row=(row + 2), column=1, value=registro['id'])
            ws.cell(row=(row + 2), column=2, value=registro['fecha_creacion'])
            ws.cell(row=(row + 2), column=3, value=registro['tipo_evento'])
            ws.cell(row=(row + 2), column=4, value=registro['complejo'])
            ws.cell(row=(row + 2), column=5, value=registro['habitacion'])
            ws.cell(row=(row + 2), column=6, value=registro['sensor'])

        file_name = '{}_{}_{}_{}_{}.xlsx'.format(fecha_inicial, fecha_final, complejo, habitacion)

        wb.save('./static/{}'.format(file_name))

        return send_from_directory('static', file_name)
