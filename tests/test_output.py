#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy

from gestionatr.output.messages import sw_a1_02 as a1_02
from gestionatr.output.messages import sw_a1_03 as a1_03
from gestionatr.output.messages import sw_a1_04 as a1_04
from gestionatr.output.messages import sw_a1_05 as a1_05
from gestionatr.output.messages import sw_a1_41 as a1_41
from gestionatr.output.messages import sw_a1_44 as a1_44
from gestionatr.output.messages import sw_a1_46 as a1_46
from gestionatr.output.messages import sw_a1_48 as a1_48
from gestionatr.output.messages import sw_a1 as a1
from gestionatr.output.messages import sw_a3 as a3
from gestionatr.output.messages import sw_b1 as b1
from gestionatr.output.messages import sw_c1 as c1
from gestionatr.output.messages import sw_c2 as c2
from gestionatr.output.messages import sw_d1 as d1
from gestionatr.output.messages import sw_f1 as f1
from gestionatr.output.messages import sw_m1 as m1
from gestionatr.output.messages import sw_q1 as q1
from gestionatr.output.messages import sw_r1 as r1
from gestionatr.output.messages import sw_w1 as w1
from . import unittest
from .utils import get_data, assertXmlEqual, get_header, get_cliente, get_contacto, get_medida


class test_C1(unittest.TestCase):

    def setUp(self):
        self.xml_c101_completo = open(get_data("c101.xml"), "r")
        self.xml_c102_accept = open(get_data("c102_accept.xml"), "r")
        self.xml_c102_reject = open(get_data("c102_reject.xml"), "r")
        self.xml_c105 = open(get_data("c105.xml"), "r")
        self.xml_c106 = open(get_data("c106.xml"), "r")
        self.xml_c109 = open(get_data("c109.xml"), "r")
        self.xml_c111 = open(get_data("c111.xml"), "r")
        self.xml_c112 = open(get_data("c112.xml"), "r")

        # RegistrosDocumento
        self.registros_documento = c1.RegistrosDocumento()
        # RegistroDoc
        registro_doc1 = c1.RegistroDoc()
        registro_doc_fields1 = {
            'tipo_doc_aportado': '08',
            'direccion_url': 'http://eneracme.com/docs/NIF11111111H.pdf'
        }
        registro_doc1.feed(registro_doc_fields1)

        registro_doc2 = c1.RegistroDoc()
        registro_doc_fields2 = {
            'tipo_doc_aportado': '07',
            'direccion_url': 'http://eneracme.com/docs/NIF11111111H.pdf'
        }
        registro_doc2.feed(registro_doc_fields2)
        registros_documento_fields = {
            'registro_doc_list': [registro_doc1, registro_doc2],
        }
        self.registros_documento.feed(registros_documento_fields)

        self.cliente = get_cliente()

        # PuntosDeMedida
        self.puntos_de_medida = c1.PuntosDeMedida()
        # PuntoDeMedida
        punto_de_medida = c1.PuntoDeMedida()
        # Aparatos
        aparatos = c1.Aparatos()
        # Aparato
        aparato = c1.Aparato()

        # ModeloAparato
        modelo_aparato = c1.ModeloAparato()
        modelo_aparato_fields = {
            'tipo_aparato': 'CG',
            'marca_aparato': '132',
            'modelo_marca': '011',
        }
        modelo_aparato.feed(modelo_aparato_fields)

        # DatosAparato
        datos_aparato = c1.DatosAparato()
        datos_aparato_fields = {
            'periodo_fabricacion': '2005',
            'numero_serie': '0000539522',
            'funcion_aparato': 'M',
            'num_integradores': '18',
            'constante_energia': '1.000',
            'constante_maximetro': '1.000',
            'ruedas_enteras': '08',
            'ruedas_decimales': '02',
        }
        datos_aparato.feed(datos_aparato_fields)

        # Medidas
        medidas = c1.Medidas()
        # Medida 1
        medida1 = c1.Medida()
        medida_fields = {
            'tipo_dhedm': '6',
            'periodo': '65',
            'magnitud_medida': 'PM',
            'procedencia': '30',
            'ultima_lectura_firme': '0.00',
            'fecha_lectura_firme': '2003-01-02',
            'anomalia': '01',
            'comentarios': 'Comentario sobre anomalia',
        }
        medida1.feed(medida_fields)
        # Medida 2
        medida2 = c1.Medida()
        medida_fields = {
            'tipo_dhedm': '6',
            'periodo': '66',
            'magnitud_medida': 'PM',
            'procedencia': '30',
            'ultima_lectura_firme': '6.00',
            'fecha_lectura_firme': '2003-01-03',
        }
        medida2.feed(medida_fields)
        medidas_fields = {
            'medida_list': [medida1, medida2],
        }
        medidas.feed(medidas_fields)

        aparato_fields = {
            'modelo_aparato': modelo_aparato,
            'tipo_movimiento': 'CX',
            'tipo_equipo_medida': 'L03',
            'tipo_propiedad_aparato': '1',
            'propietario': 'Desc. Propietario',
            'tipo_dhedm': '6',
            'modo_medida_potencia': '1',
            'lectura_directa': 'N',
            'cod_precinto': '02',
            'datos_aparato': datos_aparato,
            'medidas': medidas
        }

        aparato.feed(aparato_fields)
        aparatos_fields = {
            'aparato_list': [aparato],
        }
        aparatos.feed(aparatos_fields)

        punto_de_medida_fields = {
            'cod_pm': 'ES1234000000000001JN0F',
            'tipo_movimiento': 'A',
            'tipo_pm': '03',
            'cod_pm_principal': 'ES1234000000000002JN0F',
            'modo_lectura': '1',
            'funcion': 'P',
            'direccion_enlace': '39522',
            'direccion_punto_medida': '000000001',
            'num_linea': '12',
            'telefono_telemedida': '987654321',
            'estado_telefono': '1',
            'clave_acceso': '0000000007',
            'tension_pm': '0',
            'fecha_vigor': '2003-01-01',
            'fecha_alta': '2003-01-01',
            'fecha_baja': '2003-02-01',
            'aparatos': aparatos,
            'comentarios': 'Comentarios Varios',
        }
        punto_de_medida.feed(punto_de_medida_fields)

        puntos_de_medida_fields = {
            'punto_de_medida_list': [punto_de_medida],
        }
        self.puntos_de_medida.feed(puntos_de_medida_fields)

    def tearDown(self):
        self.xml_c101_completo.close()
        self.xml_c102_accept.close()
        self.xml_c102_reject.close()
        self.xml_c105.close()
        self.xml_c106.close()
        self.xml_c109.close()
        self.xml_c111.close()
        self.xml_c112.close()

    def test_create_pas01(self):
        # MensajeCambiodeComercializadorSinCambios
        mensaje = c1.MensajeCambiodeComercializadorSinCambios()

        # Cabecera
        cabecera = get_header(step='01')

        # CambiodeComercializadorSinCambios
        cambio_comer = c1.CambiodeComercializadorSinCambios()

        # DatosSolicitud
        datos_solicitud = c1.DatosSolicitud()
        datos_solicitud_fields = {
            'ind_activacion': 'L',
            'fecha_prevista_accion': '2016-06-06',
            'contratacion_incondicional_ps': 'S',
            'contratacion_incondicional_bs': 'S',
            'bono_social': '0',
        }
        datos_solicitud.feed(datos_solicitud_fields)

        # Cliente
        cliente = self.cliente

        # RegistrosDocumento
        registros_documento = self.registros_documento

        cambiode_comercializador_sin_cambios_fields = {
            'datos_solicitud': datos_solicitud,
            'cliente': cliente,
            'registros_documento': registros_documento,
        }
        cambio_comer.feed(
            cambiode_comercializador_sin_cambios_fields)

        mensaje_cambiode_comercializador_sin_cambios_fields = {
            'cabecera': cabecera,
            'cambiode_comercializador_sin_cambios': cambio_comer,
        }
        mensaje.feed(
            mensaje_cambiode_comercializador_sin_cambios_fields)

        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_c101_completo.read())

    def test_create_pas02(self):
        # MensajeAceptacionCambiodeComercializadorSinCambios
        mensaje = c1.MensajeAceptacionCambiodeComercializadorSinCambios()

        # Cabecera
        cabecera = get_header(step='02')

        # AceptacionCambiodeComercializadorSinCambios
        acept_cambio = c1.AceptacionCambiodeComercializadorSinCambios()

        # DatosAceptacion
        datos_aceptacion = c1.DatosAceptacion()
        datos_aceptacion_fields = {
            'fecha_aceptacion': '2016-06-06',
            'actuacion_campo': 'S',
            'fecha_ultima_lectura_firme': '2016-06-01',
            'bono_social': '0',
        }
        datos_aceptacion.feed(datos_aceptacion_fields)

        # Contrato
        contrato = c1.Contrato()

        # CondicionesContractuales
        condiciones_contractuales = c1.CondicionesContractuales()
        potencias_contratadas = c1.PotenciasContratadas()
        potencias_contratadas.feed({'p1': 1000, 'p2': 2000})
        condiciones_contractuales_fields = {
            'tarifa_atr': '003',
            'potencias_contratadas': potencias_contratadas,
        }
        condiciones_contractuales.feed(condiciones_contractuales_fields)

        contrato_fields = {
            'tipo_contrato_atr': '02',
            'condiciones_contractuales': condiciones_contractuales,
            'tipo_activacion_prevista': 'C0',
            'fecha_activacion_prevista': '2016-07-06',
        }
        contrato.feed(contrato_fields)

        aceptacion_cambiode_comercializador_sin_cambios_fields = {
            'datos_aceptacion': datos_aceptacion,
            'contrato': contrato,
        }
        acept_cambio.feed(
            aceptacion_cambiode_comercializador_sin_cambios_fields)

        mensaje_aceptacion_cambiode_comercializador_sin_cambios_fields = {
            'cabecera': cabecera,
            'aceptacion_cambiode_comercializador_sin_cambios': acept_cambio,
        }
        mensaje.feed(
            mensaje_aceptacion_cambiode_comercializador_sin_cambios_fields)

        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_c102_accept.read())

    def test_create_pas02_rej(self):
        # MensajeRechazo
        mensaje_rechazo = c1.MensajeRechazo()

        # Cabecera
        cabecera = get_header(step='02')

        # MensageRechazos
        rechazos = c1.Rechazos()

        # Rechazos
        r1 = c1.Rechazo()
        r1.feed({
            'secuencial': '1',
            'codigo_motivo': '01',
            'comentarios': 'Motiu de rebuig 01: No existe Punto de Suministro asociado al CUPS'
        })
        r2 = c1.Rechazo()
        r2.feed({
            'secuencial': '2',
            'codigo_motivo': '03',
            'comentarios': 'Cuando el CIF-NIF no coincide con el que figura en la base de datos del Distribuidor'
        })

        # RegistrosDocumento
        registros_documento = self.registros_documento

        rechazos_fields = {
            'fecha_rechazo': '2016-07-20',
            'rechazo_list': [r1, r2],
            'registros_documento': registros_documento,
        }
        rechazos.feed(rechazos_fields)

        mensaje_rechazo_fields = {
            'cabecera': cabecera,
            'rechazos': rechazos,
        }
        mensaje_rechazo.feed(mensaje_rechazo_fields)
        mensaje_rechazo.build_tree()
        xml = str(mensaje_rechazo)
        assertXmlEqual(xml, self.xml_c102_reject.read())

    def test_create_pas05(self):
        # MensajeActivacionCambiodeComercializadorSinCambios
        mensaje = c1.MensajeActivacionCambiodeComercializadorSinCambios()

        # Cabecera
        cabecera = get_header(step='05')

        # ActivacionCambiodeComercializadorSinCambios
        act_cambio = c1.ActivacionCambiodeComercializadorSinCambios()

        # DatosActivacion
        datos_activacion = c1.DatosActivacion()
        datos_activacion_fields = {
            'fecha': '2016-08-21',
            'bono_social': '1',
        }
        datos_activacion.feed(datos_activacion_fields)

        # Contrato
        contrato = c1.Contrato()

        # IdContrato
        id_contrato = c1.IdContrato()
        id_contrato_fields = {
            'cod_contrato': '00001',
        }
        id_contrato.feed(id_contrato_fields)

        # CondicionesContractuales
        condiciones_contractuales = c1.CondicionesContractuales()

        # PotenciasContratadas
        potencias_contratadas = c1.PotenciasContratadas()
        potencias_contratadas.feed({'p1': 1000, 'p2': 2000})

        condiciones_contractuales_fields = {
            'tarifa_atr': '003',
            'periodicidad_facturacion': '01',
            'tipode_telegestion': '01',
            'potencias_contratadas': potencias_contratadas,
            'modo_control_potencia': '1',
            'marca_medida_con_perdidas': 'S',
            'tension_del_suministro': '10',
            'vas_trafo': '50',
            'porcentaje_perdidas': '05',
        }
        condiciones_contractuales.feed(condiciones_contractuales_fields)

        contrato_fields = {
            'id_contrato': id_contrato,
            'tipo_autoconsumo': '00',
            'tipo_contrato_atr': '02',
            'condiciones_contractuales': condiciones_contractuales,
        }
        contrato.feed(contrato_fields)

        # Puntos de Medida
        puntos_de_medida = self.puntos_de_medida

        activacion_cambiode_comercializador_sin_cambios_fields = {
            'datos_activacion': datos_activacion,
            'contrato': contrato,
            'puntos_de_medida': puntos_de_medida,
        }
        act_cambio.feed(
            activacion_cambiode_comercializador_sin_cambios_fields)

        mensaje_activacion_cambiode_comercializador_sin_cambios_fields = {
            'cabecera': cabecera,
            'activacion_cambiode_comercializador_sin_cambios': act_cambio,
        }
        mensaje.feed(mensaje_activacion_cambiode_comercializador_sin_cambios_fields)
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_c105.read())

    def test_create_pas06(self):
        # MensajeActivacionComercializadorSaliente
        mensaje_activacion_comercializador_saliente = c1.MensajeActivacionComercializadorSaliente()

        # Cabecera
        cabecera = get_header(step='06')

        # NotificacionComercializadoraSaliente
        notificacion_comercializadora_saliente = c1.NotificacionComercializadorSaliente()

        # DatosNotificacion
        datos_notificacion = c1.DatosNotificacion()
        datos_notificacion_fields = {
            'fecha_activacion': '2016-08-21',
            'ind_bono_social': 'S'
        }
        datos_notificacion.feed(datos_notificacion_fields)

        # Contrato
        contrato = c1.Contrato()
        id_contrato = c1.IdContrato()
        id_contrato.feed({'cod_contrato': '00001'})
        contrato.feed({'id_contrato': id_contrato})

        # PuntosDeMedida
        puntos_de_medida = self.puntos_de_medida

        notificacion_comercializadora_saliente_fields = {
            'datos_notificacion': datos_notificacion,
            'contrato': contrato,
            'puntos_de_medida': puntos_de_medida,
        }
        notificacion_comercializadora_saliente.feed(
            notificacion_comercializadora_saliente_fields)

        mensaje_activacion_comercializador_saliente_fields = {
            'cabecera': cabecera,
            'notificacion_comercializador_saliente': notificacion_comercializadora_saliente,
        }
        mensaje_activacion_comercializador_saliente.feed(
            mensaje_activacion_comercializador_saliente_fields)
        mensaje_activacion_comercializador_saliente.build_tree()
        xml = str(mensaje_activacion_comercializador_saliente)
        assertXmlEqual(xml, self.xml_c106.read())

    def test_create_pas09(self):
        # MensajeAceptacionAnulacion
        mensaje_aceptacion_anulacion = c1.MensajeAceptacionAnulacion()

        # Cabecera
        cabecera = get_header(step='09')

        # AceptacionAnulacion
        aceptacion_anulacion = c1.AceptacionAnulacion()
        aceptacion_anulacion_fields = {
            'fecha_aceptacion': '2017-02-02',
        }
        aceptacion_anulacion.feed(aceptacion_anulacion_fields)

        mensaje_aceptacion_anulacion_fields = {
            'cabecera': cabecera,
            'aceptacion_anulacion': aceptacion_anulacion,
        }
        mensaje_aceptacion_anulacion.feed(mensaje_aceptacion_anulacion_fields)
        mensaje_aceptacion_anulacion.build_tree()
        xml = str(mensaje_aceptacion_anulacion)
        assertXmlEqual(xml, self.xml_c109.read())

    def test_create_pas11(self):
        # MensajeAceptacionCambiodeComercializadorSaliente
        mensaje_aceptacion_cambiode_comercializador_saliente = c1.MensajeAceptacionCambiodeComercializadorSaliente()

        # Cabecera
        cabecera = get_header(step='11')

        # AceptacionCambioComercializadorSaliente
        aceptacion_cambio_comercializador_saliente = c1.AceptacionCambioComercializadorSaliente()
        aceptacion_cambio_comercializador_saliente_fields = {
            'fecha_activacion_prevista': '2017-02-02',
            'ind_bono_social': 'N'
        }
        aceptacion_cambio_comercializador_saliente.feed(aceptacion_cambio_comercializador_saliente_fields)

        mensaje_aceptacion_cambiode_comercializador_saliente_fields = {
            'cabecera': cabecera,
            'aceptacion_cambio_comercializador_saliente': aceptacion_cambio_comercializador_saliente,
        }
        mensaje_aceptacion_cambiode_comercializador_saliente.feed(mensaje_aceptacion_cambiode_comercializador_saliente_fields)
        mensaje_aceptacion_cambiode_comercializador_saliente.build_tree()
        xml = str(mensaje_aceptacion_cambiode_comercializador_saliente)
        assertXmlEqual(xml, self.xml_c111.read())

    def test_create_pas12(self):
        # MensajeRechazoCambiodeComercializadorSaliente
        mensaje_rechazo_cambiode_comercializador_saliente = c1.MensajeRechazoCambiodeComercializadorSaliente()

        # Cabecera
        cabecera = get_header(step='12')

        # RechazoCambioComercializadorSaliente
        rechazo_cambio_comercializador_saliente = c1.RechazoCambioComercializadorSaliente()
        rechazo_cambio_comercializador_saliente_fields = {
            'fecha_rechazo': '2017-02-02',
        }
        rechazo_cambio_comercializador_saliente.feed(
            rechazo_cambio_comercializador_saliente_fields)

        mensaje_rechazo_cambiode_comercializador_saliente_fields = {
            'cabecera': cabecera,
            'rechazo_cambio_comercializador_saliente': rechazo_cambio_comercializador_saliente,
        }
        mensaje_rechazo_cambiode_comercializador_saliente.feed(
            mensaje_rechazo_cambiode_comercializador_saliente_fields)
        mensaje_rechazo_cambiode_comercializador_saliente.build_tree()
        xml = str(mensaje_rechazo_cambiode_comercializador_saliente)
        assertXmlEqual(xml, self.xml_c112.read())


class test_C2(unittest.TestCase):

    def setUp(self):
        self.xml_c201_completo = open(get_data("c201.xml"), "r")
        self.xml_c202_accept = open(get_data("c202_accept.xml"), "r")
        self.xml_c203 = open(get_data("c203.xml"), "r")

    def tearDown(self):
        self.xml_c201_completo.close()
        self.xml_c202_accept.close()
        self.xml_c203.close()

    def test_create_pas01(self):
        # MensajeCambiodeComercializadorConCambios
        mensage = c2.MensajeCambiodeComercializadorConCambios()

        # Cabecera
        cabecera = get_header(process='C2', step='01', date='2014-04-16T22:13:37', code='201412111009')

        # CambiodeComercializadorConCambios
        cambiode_comercializador_con_cambios = c2.CambiodeComercializadorConCambios()

        # DatosSolicitud
        datos_solicitud = c2.DatosSolicitud()
        datos_solicitud_fields = {
            'tipo_modificacion': 'S',
            'tipo_solicitud_administrativa': 'S',
            'cnae': '2222',
            'ind_activacion': 'L',
            'fecha_prevista_accion': '2016-06-06',
            'contratacion_incondicional_ps': 'S',
            'contratacion_incondicional_bs': 'N',
            'bono_social': '0',
            'solicitud_tension': 'T'
        }
        datos_solicitud.feed(datos_solicitud_fields)

        # Contrato
        contrato = c2.Contrato()

        # CondicionesContractuales
        condiciones_contractuales = c2.CondicionesContractuales()

        # PotenciasContratadas
        potencias_contratadas = c2.PotenciasContratadas()
        potencias_contratadas.feed({'p1': 1000, 'p2': 2000})

        condiciones_contractuales_fields = {
            'tarifa_atr': '003',
            'potencias_contratadas': potencias_contratadas,
            'modo_control_potencia': '1',
        }
        condiciones_contractuales.feed(condiciones_contractuales_fields)

        # Contacto
        contacto = get_contacto()

        contrato_fields = {
            'fecha_finalizacion': '2018-01-01',
            'tipo_autoconsumo': '00',
            'tipo_contrato_atr': '02',
            'condiciones_contractuales': condiciones_contractuales,
            'periodicidad_facturacion': '01',
            'consumo_anual_estimado': '5000',
            'contacto': contacto,
        }
        contrato.feed(contrato_fields)

        # Cliente
        cliente = get_cliente(dir=True, tipo_dir='F')

        # Medida
        medida = get_medida()

        # DocTecnica
        doc_tecnica = c2.DocTecnica()

        # DatosCie
        datos_cie = c2.DatosCie()

        # CIEPapel
        cie_papel = c2.CIEPapel()
        cie_papel_fields = {
            'codigo_cie': '1234567',
            'potencia_inst_bt': '3500',
            'potencia_no_interrumpible': '2000',
            'fecha_emision_cie': '2015-06-04',
            'fecha_caducidad_cie': '',
            'nif_instalador': '12345678Z',
            'tension_suministro_cie': '10',
            'tipo_suministro': 'VI',
        }
        cie_papel.feed(cie_papel_fields)

        datos_cie_fields = {
            'cie_papel': cie_papel,
            'validez_cie': 'ES',
        }
        datos_cie.feed(datos_cie_fields)

        # DatosAPM
        datos_apm = c2.DatosAPM()
        datos_apm_fields = {
            'codigo_apm': '1111111111',
            'potencia_inst_at': '5000',
            'fecha_emision_apm': '2015-06-04',
            'fecha_caducidad_apm': '2016-06-04',
            'tension_suministro_apm': '20',
            'codigo_instalador': '0550',
        }
        datos_apm.feed(datos_apm_fields)

        doc_tecnica_fields = {
            'datos_cie': datos_cie,
            'datos_apm': datos_apm,
        }
        doc_tecnica.feed(doc_tecnica_fields)

        cambiode_comercializador_con_cambios_fields = {
            'datos_solicitud': datos_solicitud,
            'contrato': contrato,
            'cliente': cliente,
            'medida': medida,
            'doc_tecnica': doc_tecnica,
            'comentarios': 'Comentario',
        }
        cambiode_comercializador_con_cambios.feed(
            cambiode_comercializador_con_cambios_fields)

        mensaje_fields = {
            'cabecera': cabecera,
            'cambiode_comercializador_con_cambios': cambiode_comercializador_con_cambios,
        }
        mensage.feed(mensaje_fields)
        mensage.build_tree()
        xml = str(mensage)
        assertXmlEqual(xml, self.xml_c201_completo.read())

    def test_create_pas02(self):
        # MensajeAceptacionCambiodeComercializadorConCambios
        mensaje_aceptacion_cambiode_comercializador_con_cambios = c2.MensajeAceptacionCambiodeComercializadorConCambios()

        # Cabecera
        cabecera = get_header(process='C2', step='02')

        # AceptacionCambiodeComercializadorConCambios
        aceptacion_cambiode_comercializador_con_cambios = c2.AceptacionCambiodeComercializadorConCambios()

        # DatosAceptacion
        datos_aceptacion = c2.DatosAceptacion()
        datos_aceptacion_fields = {
            'fecha_aceptacion': '2016-06-06',
            'potencia_actual': '5000',
            'actuacion_campo': 'S',
            'fecha_ultima_lectura_firme': '2016-06-01',
            'bono_social': '1',
        }
        datos_aceptacion.feed(datos_aceptacion_fields)

        # Contrato
        contrato = c2.Contrato()

        # CondicionesContractuales
        condiciones_contractuales = c2.CondicionesContractuales()

        # PotenciasContratadas
        potencias_contratadas = c2.PotenciasContratadas()
        potencias_contratadas.feed({'p1': 1000, 'p2': 2000})

        condiciones_contractuales_fields = {
            'tarifa_atr': '003',
            'potencias_contratadas': potencias_contratadas,
            'modo_control_potencia': '1',
        }
        condiciones_contractuales.feed(condiciones_contractuales_fields)

        contrato_fields = {
            'tipo_contrato_atr': '02',
            'condiciones_contractuales': condiciones_contractuales,
            'tipo_activacion_prevista': 'C0',
            'fecha_activacion_prevista': '2016-07-06',
        }
        contrato.feed(contrato_fields)

        aceptacion_cambiode_comercializador_con_cambios_fields = {
            'datos_aceptacion': datos_aceptacion,
            'contrato': contrato,
        }
        aceptacion_cambiode_comercializador_con_cambios.feed(
            aceptacion_cambiode_comercializador_con_cambios_fields)

        mensaje_aceptacion_cambiode_comercializador_con_cambios_fields = {
            'cabecera': cabecera,
            'aceptacion_cambiode_comercializador_con_cambios': aceptacion_cambiode_comercializador_con_cambios,
        }
        mensaje_aceptacion_cambiode_comercializador_con_cambios.feed(
            mensaje_aceptacion_cambiode_comercializador_con_cambios_fields)
        mensaje_aceptacion_cambiode_comercializador_con_cambios.build_tree()
        xml = str(mensaje_aceptacion_cambiode_comercializador_con_cambios)
        assertXmlEqual(xml, self.xml_c202_accept.read())

    def test_create_pas03(self):
        # MensajeIncidenciasATRDistribuidor
        mensaje = c2.MensajeIncidenciasATRDistribuidor()

        # Cabecera
        cabecera = get_header(process='C2', step='03')

        # IncidenciasATRDistribuidor
        incidencias_atr_distribuidor = c2.IncidenciasATRDistribuidor()
        i1 = c2.Incidencia()
        incidencia_fields = {
            'secuencial': '1',
            'codigo_motivo': '01',
            'comentarios': 'Com 1',
        }
        i1.feed(incidencia_fields)
        i2 = c2.Incidencia()
        incidencia_fields = {
            'secuencial': '2',
            'codigo_motivo': '08',
            'comentarios': 'Com 2',
        }
        i2.feed(incidencia_fields)

        incidencias_atr_distribuidor_fields = {
            'fecha_incidencia': '2016-07-21',
            'fecha_prevista_accion': '2016-07-22',
            'incidencia_list': [i1, i2],
        }
        incidencias_atr_distribuidor.feed(incidencias_atr_distribuidor_fields)

        mensaje_incidencias_atr_distribuidor_fields = {
            'cabecera': cabecera,
            'incidencias_atr_distribuidor': incidencias_atr_distribuidor,
        }
        mensaje.feed(mensaje_incidencias_atr_distribuidor_fields)
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_c203.read())


class test_A1(unittest.TestCase):

        def setUp(self):
            self.xml_a101 = open(get_data("a101.xml"), "r")
            self.xml_a102_accept = open(get_data("a102_accept.xml"), "r")
            self.xml_a102_reject = open(get_data("a102_reject.xml"), "r")

        def tearDown(self):
            self.xml_a101.close()
            self.xml_a102_accept.close()
            self.xml_a102_reject.close()

        def test_create_pas01(self):
            # InfoRegistroAutoconsA1
            mensaje = a1.A101()

            # Cabecera
            cabecera = a1.CabeceraAutoconsumo()
            cabecera_fields = {
                'codigo_empresa_emisora': '09',
                'codigo_ree_empresa_destino': '4321',
                'codigo_del_proceso': 'A1',
                'codigo_del_paso': '01',
                'codigo_de_solicitud': '201605219497',
                'secuencial_de_solicitud': '00',
                'fecha': '2016-06-08T04:24:09',
            }
            cabecera.feed(cabecera_fields)

            # Autoconsumo
            autoconsumo = d1.Autoconsumo()
            autoconsumo_fields = {
                'cau': 'ES1234000000000001JN0FA001',
                'seccion_registro': '1',
                # 'sub_seccion': 'a0',
                'colectivo': 'S',
            }
            autoconsumo.feed(autoconsumo_fields)

            # DatosSuministro
            suministro_1 = d1.DatosSuministro()
            suministro_fields = {
                'cups': 'ES1234000000000001JN0F',
                'tipo_cups': '01',
                'ref_catastro': '1234567890qwertyuiop',
            }
            suministro_1.feed(suministro_fields)

            suministro_2 = d1.DatosSuministro()
            suministro_fields = {
                'cups': 'ES1234000000000002JN0F',
                'tipo_cups': '01',
                'ref_catastro': '1234567890qwertyuiop',
            }
            suministro_2.feed(suministro_fields)

            suministro_3 = d1.DatosSuministro()
            suministro_fields = {
                'cups': 'ES1234000000000003JN0F',
                'tipo_cups': '01',
                'ref_catastro': '1234567890qwertyuiop',
            }
            suministro_3.feed(suministro_fields)

            # UTM
            utm = d1.UTM()
            utm_fields = {
                'x': '100',
                'y': '200',
                'huso': '40',
                'banda': 'E',
            }
            utm.feed(utm_fields)

            # IdTitular
            id_titular = d1.IdTitular()
            id_titular_fields = {
                'tipo_identificador': 'NI',
                'identificador': '111111111H',
            }
            id_titular.feed(id_titular_fields)

            # Nombre
            nombre = d1.Nombre()
            nombre_fields = {
                'nombre_de_pila': 'Juan',
                'primer_apellido': 'López',
                'segundo_apellido': 'Sánchez',
            }
            nombre.feed(nombre_fields)

            # Telefono
            telefono = d1.Telefono()
            telefono_fields = {
                'prefijo_pais': '0034',
                'numero': '933834841',
            }
            telefono.feed(telefono_fields)

            # Telefono 2
            telefono2 = d1.Telefono()
            telefono2_fields = {
                'prefijo_pais': '0034',
                'numero': '633834841',
            }
            telefono2.feed(telefono2_fields)

            # Telefono 3
            telefono3 = d1.Telefono()
            telefono3_fields = {
                'prefijo_pais': '0034',
                'numero': '683834841',
            }
            telefono3.feed(telefono3_fields)

            # Via
            via = d1.Via()
            via_fields = {
                'tipo_via': 'CL',
                'calle': 'Pau Casals',
                'numero_finca': '18',
                'duplicador_finca': '1',
                'escalera': 'D',
                'piso': '3',
                'puerta': '2',
                'tipo_aclarador_finca': 'BI',
                'aclarador_finca': 'Bar',
            }
            via.feed(via_fields)

            # Direccion
            direccion = d1.Direccion()
            direccion_fields = {
                'pais': 'España',
                'provincia': '17',
                'municipio': '171181',
                'poblacion': '17118000400',
                'cod_postal': '17230',
                'via': via
            }
            direccion.feed(direccion_fields)

            # TitularRepresentanteGen
            titular = d1.TitularRepresentanteGen()
            titular_representante_gen_fields = {
                'id_titular': id_titular,
                'nombre': nombre,
                'telefono': [telefono, telefono2, telefono3],
                'correo_electronico': 'mail_falso@dominio.com',
                'direccion': direccion,
            }
            titular.feed(titular_representante_gen_fields)

            # DatosInstGen
            datos_1 = d1.DatosInstGen()
            datos_inst_gen_fields = {
                'cil': 'ES1234000000000001JN0F001',
                'tec_generador': 'b12',
                'combustible': 'Diesel',
                'pot_instalada_gen': '100',
                'tipo_instalacion': '01',
                'esquema_medida': 'B',
                'ssaa': 'S',
                'ref_catastro': '1234567890qwertyuidf',
                'utm': utm,
                'titular_representante_gen': titular,
            }
            datos_1.feed(datos_inst_gen_fields)

            # utm2 = copy.deepcopy(utm)
            # titular2 = copy.deepcopy(titular)

            datos_2 = d1.DatosInstGen()
            datos_inst_gen_fields = {
                'cil': 'ES1234000000000002JN0F001',
                'tec_generador': 'b11',
                'pot_instalada_gen': '100',
                'tipo_instalacion': '01',
                'esquema_medida': 'B',
                'ssaa': 'S',
                'ref_catastro': '1234567890qwertyuidf',
                # 'utm': utm2,
                # 'titular_representante_gen': titular2,
            }
            datos_2.feed(datos_inst_gen_fields)

            # InfoRegistroAutocons
            info = a1.InfoRegistroAutoconsA1()
            info_registro_autocons_fields = {
                'movimiento': 'A',
                'autoconsumo': autoconsumo,
                'datos_suministro': [suministro_1, suministro_2, suministro_3],
                'datos_inst_gen': [datos_1, datos_2],
                'comentarios': 'Esto es un comentario'
            }
            info.feed(info_registro_autocons_fields)

            a101_fields = {
                'cabecera': cabecera,
                'info_registro_autocons': info,
            }
            mensaje.feed(a101_fields)
            mensaje.build_tree()
            xml = str(mensaje)
            assertXmlEqual(xml, self.xml_a101.read())

        def test_create_pas02_accept(self):
            # Cabecera
            cabecera = a1.CabeceraAutoconsumoRechazo()
            cabecera_fields = {
                'codigo_ree_empresa_emisora': '4321',
                'codigo_empresa_destino': '09',
                'codigo_del_proceso': 'A1',
                'codigo_del_paso': '02',
                'codigo_de_solicitud': '201605219497',
                'secuencial_de_solicitud': '00',
                'fecha': '2016-06-08T04:24:09',
            }
            cabecera.feed(cabecera_fields)

            # ActualizacionRegistroAutoconsumo
            datos_registro = a1.ActualizacionDatosRegistro()
            actualizacion_datos_registro_fields = {
                'sub_seccion': 'a0',
            }
            datos_registro.feed(actualizacion_datos_registro_fields)

            # ActualizacionRegistroAutoconsumo
            registro = a1.ActualizacionRegistroAutoconsumo()
            actualizacion_registro_autoconsumo_fields = {
                'cau': 'ES1234000000000001JN0FA001',
                'actualizacion_datos_registro': datos_registro,
                'comentarios': 'Esto es un comentario',

            }
            registro.feed(actualizacion_registro_autoconsumo_fields)

            # MensajeActualizacionRegistroAutoconsumo
            mensaje = a1.MensajeActualizacionRegistroAutoconsumo()
            mensaje_actualizacion_registro_autoconsumo_fields = {
                'cabecera': cabecera,
                'actualizacion_registro_autoconsumo': registro,
            }
            mensaje.feed(mensaje_actualizacion_registro_autoconsumo_fields)

            mensaje.build_tree()
            xml = str(mensaje)
            assertXmlEqual(xml, self.xml_a102_accept.read())

        def test_create_pas02_rej(self):
            # Cabecera
            cabecera = a1.CabeceraAutoconsumoRechazo()
            cabecera_fields = {
                'codigo_ree_empresa_emisora': '4321',
                'codigo_empresa_destino': '09',
                'codigo_del_proceso': 'A1',
                'codigo_del_paso': '02',
                'codigo_de_solicitud': '201605219497',
                'secuencial_de_solicitud': '00',
                'fecha': '2016-06-08T04:24:09',
            }
            cabecera.feed(cabecera_fields)

            # Rechazo 1
            rechazo1 = a1.Rechazo()
            rechazo1_fields = {
                'fecha_rechazo': '2016-06-08',
                'secuencial': '00',
                'codigo_motivo': '01',
                'cups': 'ES1234000000000001JN0F',
                'comentarios': 'Comentario del rechazo',
            }
            rechazo1.feed(rechazo1_fields)
            # Rechazo 2
            rechazo2 = a1.Rechazo()
            rechazo2_fields = {
                'fecha_rechazo': '2016-06-08',
                'secuencial': '00',
                'codigo_motivo': 'F1',
                'cups': 'ES1234000000000001JN0F',
                'comentarios': 'Comentario del rechazo',
            }
            rechazo2.feed(rechazo2_fields)
            # Rechazo 3
            rechazo3 = a1.Rechazo()
            rechazo3_fields = {
                'fecha_rechazo': '2016-06-08',
                'secuencial': '00',
                'codigo_motivo': 'F4',
                'cups': 'ES1234000000000001JN0F',
                'comentarios': 'Comentario del rechazo',
            }
            rechazo3.feed(rechazo3_fields)

            # Rechazos
            rechazos = d1.Rechazos()
            rechazos_fields = {
                'rechazos': [rechazo1, rechazo2, rechazo3],
            }
            rechazos.feed(rechazos_fields)

            # ActualizacionRegistroAutoconsumo
            registro = a1.ActualizacionRegistroAutoconsumo()
            actualizacion_registro_autoconsumo_fields = {
                'cau': 'ES1234000000000001JN0FA001',
                'rechazos': rechazos,
                'comentarios': 'Esto es un comentario',

            }
            registro.feed(actualizacion_registro_autoconsumo_fields)

            # MensajeActualizacionRegistroAutoconsumo
            mensaje = a1.MensajeActualizacionRegistroAutoconsumo()
            mensaje_actualizacion_registro_autoconsumo_fields = {
                'cabecera': cabecera,
                'actualizacion_registro_autoconsumo': registro,
            }
            mensaje.feed(mensaje_actualizacion_registro_autoconsumo_fields)

            mensaje.build_tree()
            xml = str(mensaje)
            assertXmlEqual(xml, self.xml_a102_reject.read())


class test_A3(unittest.TestCase):
    def setUp(self):
        self.xml_a301 = open(get_data("a301.xml"), "r")
        self.xml_a301_correos = open(get_data("a301_correos.xml"), "r")

    def tearDown(self):
        self.xml_a301.close()
        self.xml_a301_correos.close()

    def test_create_pas01(self):
        # MensajeAlta
        mensaje_alta = a3.MensajeAlta()

        # Cabecera
        cabecera = get_header(process='A3', step='01', date='2014-04-16T22:13:37', code='201412111009')

        # Alta
        alta = a3.Alta()

        # DatosSolicitud
        datos_solicitud = a3.DatosSolicitud()
        datos_solicitud_fields = {
            'cnae': '2222',
            'ind_activacion': 'L',
            'fecha_prevista_accion': '2016-06-06',
        }
        datos_solicitud.feed(datos_solicitud_fields)


        # Contrato
        contrato = a3.Contrato()

        # CondicionesContractuales
        condiciones_contractuales = a3.CondicionesContractuales()

        # PotenciasContratadas
        potencias_contratadas = a3.PotenciasContratadas()
        potencias_contratadas.feed({'p1': 1000, 'p2': 2000})

        condiciones_contractuales_fields = {
            'tarifa_atr': '003',
            'potencias_contratadas': potencias_contratadas,
            'modo_control_potencia': '1'
        }
        condiciones_contractuales.feed(condiciones_contractuales_fields)

        # Contacto
        contacto = get_contacto(email=False)

        contrato_fields = {
            'fecha_finalizacion': '2018-01-01',
            'tipo_autoconsumo': '00',
            'tipo_contrato_atr': '02',
            'condiciones_contractuales': condiciones_contractuales,
            'consumo_anual_estimado': '5000',
            'contacto': contacto,
        }
        contrato.feed(contrato_fields)

        # Cliente
        cliente = get_cliente(dir=True, tipo_dir='F')

        # Medida
        medida = get_medida()

        # DocTecnica
        doc_tecnica = a3.DocTecnica()

        # DatosCie
        datos_cie = a3.DatosCie()

        # CIEElectronico
        cie_electronico = a3.CIEElectronico()
        cie_electronico_fields = {
            'codigo_cie': '1234567',
            'sello_electronico': '11111',
        }
        cie_electronico.feed(cie_electronico_fields)

        datos_cie_fields = {
            'cie_electronico': cie_electronico,
            'validez_cie': 'ES',
        }
        datos_cie.feed(datos_cie_fields)


        # DatosAPM
        datos_apm = a3.DatosAPM()
        datos_apm_fields = {
            'codigo_apm': '1111111111',
            'potencia_inst_at': '5000',
            'fecha_emision_apm': '2015-06-04',
            'fecha_caducidad_apm': '2016-06-04',
            'tension_suministro_apm': '20',
            'codigo_instalador': '0550',
        }
        datos_apm.feed(datos_apm_fields)

        doc_tecnica_fields = {
            'datos_cie': datos_cie,
            'datos_apm': datos_apm,
        }
        doc_tecnica.feed(doc_tecnica_fields)

        alta_fields = {
            'datos_solicitud': datos_solicitud,
            'contrato': contrato,
            'cliente': cliente,
            'medida': medida,
            'doc_tecnica': doc_tecnica,
            'comentarios': 'Comentario',
        }
        alta.feed(alta_fields)

        mensaje_alta_fields = {
            'cabecera': cabecera,
            'alta': alta,
        }
        mensaje_alta.feed(mensaje_alta_fields)
        mensaje_alta.build_tree()
        xml = str(mensaje_alta)
        assertXmlEqual(xml, self.xml_a301.read())

    def test_create_pas01_correos(self):
        # MensajeAlta
        mensaje_alta = a3.MensajeAlta()

        # Cabecera
        cabecera = get_header(process='A3', step='01', date='2014-04-16T22:13:37', code='201412111009')

        # Alta
        alta = a3.Alta()

        # DatosSolicitud
        datos_solicitud = a3.DatosSolicitud()
        datos_solicitud_fields = {
            'cnae': '2222',
            'ind_activacion': 'L',
            'fecha_prevista_accion': '2016-06-06',
        }
        datos_solicitud.feed(datos_solicitud_fields)


        # Contrato
        contrato = a3.Contrato()

        # CondicionesContractuales
        condiciones_contractuales = a3.CondicionesContractuales()

        # PotenciasContratadas
        potencias_contratadas = a3.PotenciasContratadas()
        potencias_contratadas.feed({'p1': 1000, 'p2': 2000})

        condiciones_contractuales_fields = {
            'tarifa_atr': '003',
            'potencias_contratadas': potencias_contratadas,
            'modo_control_potencia': '1'
        }
        condiciones_contractuales.feed(condiciones_contractuales_fields)

        # Contacto
        contacto = get_contacto(email=False)

        contrato_fields = {
            'fecha_finalizacion': '2018-01-01',
            'tipo_autoconsumo': '00',
            'tipo_contrato_atr': '02',
            'condiciones_contractuales': condiciones_contractuales,
            'consumo_anual_estimado': '5000',
            'contacto': contacto,
        }
        contrato.feed(contrato_fields)

        # Cliente
        cliente = get_cliente(dir="correo", tipo_dir='F')

        # Medida
        medida = get_medida()

        # DocTecnica
        doc_tecnica = a3.DocTecnica()

        # DatosCie
        datos_cie = a3.DatosCie()

        # CIEElectronico
        cie_electronico = a3.CIEElectronico()
        cie_electronico_fields = {
            'codigo_cie': '1234567',
            'sello_electronico': '11111',
        }
        cie_electronico.feed(cie_electronico_fields)

        datos_cie_fields = {
            'cie_electronico': cie_electronico,
            'validez_cie': 'ES',
        }
        datos_cie.feed(datos_cie_fields)


        # DatosAPM
        datos_apm = a3.DatosAPM()
        datos_apm_fields = {
            'codigo_apm': '1111111111',
            'potencia_inst_at': '5000',
            'fecha_emision_apm': '2015-06-04',
            'fecha_caducidad_apm': '2016-06-04',
            'tension_suministro_apm': '20',
            'codigo_instalador': '0550',
        }
        datos_apm.feed(datos_apm_fields)

        doc_tecnica_fields = {
            'datos_cie': datos_cie,
            'datos_apm': datos_apm,
        }
        doc_tecnica.feed(doc_tecnica_fields)

        alta_fields = {
            'datos_solicitud': datos_solicitud,
            'contrato': contrato,
            'cliente': cliente,
            'medida': medida,
            'doc_tecnica': doc_tecnica,
            'comentarios': 'Comentario',
        }
        alta.feed(alta_fields)

        mensaje_alta_fields = {
            'cabecera': cabecera,
            'alta': alta,
        }
        mensaje_alta.feed(mensaje_alta_fields)
        mensaje_alta.build_tree()
        xml = str(mensaje_alta)
        assertXmlEqual(xml, self.xml_a301_correos.read())


class test_M1(unittest.TestCase):
    def setUp(self):
        self.xml_m101 = open(get_data("m101.xml"), "r")

    def tearDown(self):
        self.xml_m101.close()

    def test_create_pas01(self):
        # MensajeModificacionDeATR
        mensaje_modificacion_de_atr = m1.MensajeModificacionDeATR()

        # Cabecera
        cabecera = get_header(process='M1', step='01', date='2014-04-16T22:13:37', code='201412111009')

        # ModificacionDeATR
        modificacion_de_atr = m1.ModificacionDeATR()

        # DatosSolicitud
        datos_solicitud = m1.DatosSolicitud()
        datos_solicitud_fields = {
            'tipo_modificacion': 'S',
            'tipo_solicitud_administrativa': 'S',
            'periodicidad_facturacion': '01',
            'ind_activacion': 'L',
            'fecha_prevista_accion': '2016-06-06',
            'cnae': '2222',
            'bono_social': '1'
        }
        datos_solicitud.feed(datos_solicitud_fields)

        # Contrato
        contrato = m1.Contrato()

        # CondicionesContractuales
        condiciones_contractuales = m1.CondicionesContractuales()

        # PotenciasContratadas
        potencias_contratadas = a3.PotenciasContratadas()
        potencias_contratadas.feed({'p1': 1000, 'p2': 2000})

        condiciones_contractuales_fields = {
            'tarifa_atr': '003',
            'potencias_contratadas': potencias_contratadas,
            'modo_control_potencia': '1',
        }
        condiciones_contractuales.feed(condiciones_contractuales_fields)


        # Contacto
        contacto = get_contacto(email=False)

        contrato_fields = {
            'fecha_finalizacion': '2018-01-01',
            'tipo_autoconsumo': '00',
            'tipo_contrato_atr': '02',
            'condiciones_contractuales': condiciones_contractuales,
            'contacto': contacto,
        }
        contrato.feed(contrato_fields)

        # Cliente
        cliente = get_cliente(dir=False, tipo_dir='S')

        # Medida
        medida = m1.Medida()
        medida_fields = {
            'propiedad_equipo': 'C',
            'tipo_equipo_medida': 'L00',
        }
        medida.feed(medida_fields)

        modificacion_de_atr_fields = {
            'datos_solicitud': datos_solicitud,
            'contrato': contrato,
            'cliente': cliente,
            'medida': medida,
        }
        modificacion_de_atr.feed(modificacion_de_atr_fields)

        mensaje_modificacion_de_atr_fields = {
            'cabecera': cabecera,
            'modificacion_de_atr': modificacion_de_atr,
        }
        mensaje_modificacion_de_atr.feed(mensaje_modificacion_de_atr_fields)
        mensaje_modificacion_de_atr.build_tree()
        xml = str(mensaje_modificacion_de_atr)
        assertXmlEqual(xml, self.xml_m101.read())


class test_D1(unittest.TestCase):

    def setUp(self):
        self.xml_d101 = open(get_data("d101.xml"), "r")
        self.xml_d102_accept = open(get_data("d102_accept.xml"), "r")
        self.xml_d102_reject = open(get_data("d102_reject.xml"), "r")

    def tearDown(self):
        self.xml_d101.close()
        self.xml_d102_accept.close()
        self.xml_d102_reject.close()

    def test_create_pas01(self):
        # MensajeNotificacionCambiosATRDesdeDistribuidor
        mensaje = d1.MensajeNotificacionCambiosATRDesdeDistribuidor()

        # Cabecera
        cabecera = d1.Cabecera()
        cabecera_fields = {
            'codigo_ree_empresa_emisora': '1234',
            'codigo_ree_empresa_destino': '4321',
            'codigo_del_proceso': 'D1',
            'codigo_del_paso': '01',
            'codigo_de_solicitud': '201605219497',
            'secuencial_de_solicitud': '00',
            'fecha': '2016-06-08T04:24:09',
            'cups': 'ES0116000000011531LK0F',
        }
        cabecera.feed(cabecera_fields)

        # Autoconsumo
        autoconsumo = d1.Autoconsumo()
        autoconsumo_fields = {
            'cau': 'ES1234000000000001JN0FA001',
            'seccion_registro': '2',
            'sub_seccion': 'a0',
            'colectivo': 'S',
        }
        autoconsumo.feed(autoconsumo_fields)

        # DatosSuministro
        suministro = d1.DatosSuministro()
        suministro_fields = {
            'cups': 'ES1234000000000001JN0F',
            'tipo_cups': '01',
            'ref_catastro': '1234567890qwertyuiop',
        }
        suministro.feed(suministro_fields)

        # UTM
        utm = d1.UTM()
        utm_fields = {
            'x': '100',
            'y': '200',
            'huso': '40',
            'banda': 'E',
        }
        utm.feed(utm_fields)

        # IdTitular
        id_titular = d1.IdTitular()
        id_titular_fields = {
            'tipo_identificador': 'NI',
            'identificador': '111111111H',
        }
        id_titular.feed(id_titular_fields)

        # Nombre
        nombre = d1.Nombre()
        nombre_fields = {
            'nombre_de_pila': 'Juan',
            'primer_apellido': 'López',
            'segundo_apellido': 'Sánchez',
        }
        nombre.feed(nombre_fields)

        # Telefono
        telefono = d1.Telefono()
        telefono_fields = {
            'prefijo_pais': '0034',
            'numero': '933834841',
        }
        telefono.feed(telefono_fields)

        # Telefono 2
        telefono2 = d1.Telefono()
        telefono2_fields = {
            'prefijo_pais': '0034',
            'numero': '633834841',
        }
        telefono2.feed(telefono2_fields)

        # Telefono 3
        telefono3 = d1.Telefono()
        telefono3_fields = {
            'prefijo_pais': '0034',
            'numero': '683834841',
        }
        telefono3.feed(telefono3_fields)

        # Via
        via = d1.Via()
        via_fields = {
            'tipo_via': 'CL',
            'calle': 'Pau Casals',
            'numero_finca': '18',
            'duplicador_finca': '1',
            'escalera': 'D',
            'piso': '3',
            'puerta': '2',
            'tipo_aclarador_finca': 'BI',
            'aclarador_finca': 'Bar',
        }
        via.feed(via_fields)

        # Direccion
        direccion = d1.Direccion()
        direccion_fields = {
            'pais': 'España',
            'provincia': '17',
            'municipio': '171181',
            'poblacion': '17118000400',
            'cod_postal': '17230',
            'via': via
        }
        direccion.feed(direccion_fields)

        # TitularRepresentanteGen
        titular = d1.TitularRepresentanteGen()
        titular_representante_gen_fields = {
            'id_titular': id_titular,
            'nombre': nombre,
            'telefono': [telefono, telefono2, telefono3],
            'correo_electronico': 'mail_falso@dominio.com',
            'direccion': direccion,
        }
        titular.feed(titular_representante_gen_fields)

        # DatosInstGen
        datos_1 = d1.DatosInstGen()
        datos_inst_gen_fields = {
            'cil': 'ES1234000000000001JN0F001',
            'tec_generador': 'b12',
            'combustible': 'Diesel',
            'pot_instalada_gen': '100',
            'tipo_instalacion': '01',
            'esquema_medida': 'B',
            'ssaa': 'S',
            'ref_catastro': '1234567890qwertyuidf',
            'utm': utm,
            'titular_representante_gen': titular,
        }
        datos_1.feed(datos_inst_gen_fields)

        utm2 = copy.deepcopy(utm)
        titular2 = copy.deepcopy(titular)

        datos_2 = d1.DatosInstGen()
        datos_inst_gen_fields = {
            'cil': 'ES1234000000000001JN0F002',
            'tec_generador': 'b11',
            'pot_instalada_gen': '100',
            'tipo_instalacion': '01',
            'esquema_medida': 'B',
            'ssaa': 'S',
            'ref_catastro': '1234567890qwertyuidf',
            'utm': utm2,
            'titular_representante_gen': titular2,
        }
        datos_2.feed(datos_inst_gen_fields)

        # InfoRegistroAutocons
        info = d1.InfoRegistroAutocons()
        info_registro_autocons_fields = {
            'movimiento': 'A',
            'autoconsumo': autoconsumo,
            'datos_suministro': suministro,
            'datos_inst_gen': [datos_1, datos_2],
            'comentarios': 'Esto es un comentario'
        }
        info.feed(info_registro_autocons_fields)

        # NotificacionCambiosATRDesdeDistribuidor
        notificacion = d1.NotificacionCambiosATRDesdeDistribuidor()
        notificacion_cambios_atr_desde_distribuidor_fields = {
            'motivo_cambio_atr_desde_distribuidora': '01',
            'fecha_prevista_aplicacion_cambio_atr': '2016-06-09',
            'periodicidad_facturacion': '01',
            'info_registro_autocons': info,
        }
        notificacion.feed(notificacion_cambios_atr_desde_distribuidor_fields)

        mensaje_notificacion_cambios_atr_desde_distribuidor_fields = {
            'cabecera': cabecera,
            'notificacion_cambios_atr_desde_distribuidor': notificacion,
        }
        mensaje.feed(mensaje_notificacion_cambios_atr_desde_distribuidor_fields)
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_d101.read())

    def test_create_pas02_accept(self):
        # Cabecera
        cabecera = d1.Cabecera()
        cabecera_fields = {
            'codigo_ree_empresa_emisora': '1234',
            'codigo_ree_empresa_destino': '4321',
            'codigo_del_proceso': 'D1',
            'codigo_del_paso': '02',
            'codigo_de_solicitud': '201607211259',
            'secuencial_de_solicitud': '01',
            'fecha': '2016-07-21T12:59:47',
            'cups': 'ES1234000000000001JN0F',
        }
        cabecera.feed(cabecera_fields)

        # DatosAceptacion
        datos_aceptacion = d1.DatosAceptacion()
        datos_aceptacion_fields = {
            'fecha_aceptacion': '2016-06-06',
        }
        datos_aceptacion.feed(datos_aceptacion_fields)

        # AceptacionNotificacionCambiosATRDesdeDistribuidor
        acept_cambio = d1.AceptacionNotificacionCambiosATRDesdeDistribuidor()
        aceptacion_notificacion_cambios_atr_desde_distribuidor_fields = {
            'datos_aceptacion': datos_aceptacion,
        }
        acept_cambio.feed(aceptacion_notificacion_cambios_atr_desde_distribuidor_fields)

        # MensajeAceptacionCambiodeComercializadorSinCambios
        mensaje = d1.MensajeAceptacionNotificacionCambiosATRDesdeDistribuidor()
        mensaje_aceptacion_notificacion_cambios_atr_desde_distribuidor_fields = {
            'cabecera': cabecera,
            'aceptacion_notificacion_cambios_atr_desde_distribuidor': acept_cambio,
        }
        mensaje.feed(mensaje_aceptacion_notificacion_cambios_atr_desde_distribuidor_fields)

        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_d102_accept.read())

    def test_create_pas02_rej(self):
        # Cabecera
        cabecera = d1.Cabecera()
        cabecera_fields = {
            'codigo_ree_empresa_emisora': '1234',
            'codigo_ree_empresa_destino': '4321',
            'codigo_del_proceso': 'D1',
            'codigo_del_paso': '02',
            'codigo_de_solicitud': '201607211259',
            'secuencial_de_solicitud': '01',
            'fecha': '2016-07-21T12:59:47',
            'cups': 'ES1234000000000001JN0F',
        }
        cabecera.feed(cabecera_fields)

        # Rechazos
        rechazo = d1.Rechazo()
        rechazo_fields = {
            'secuencial': '1',
            'codigo_motivo': 'F1',
            'comentarios': 'Motiu de rebuig F1'
        }
        rechazo.feed(rechazo_fields)

        # RegistroDoc
        doc1 = d1.RegistroDoc()
        registro_doc_fields1 = {
            'tipo_doc_aportado': '08',
            'direccion_url': 'http://eneracme.com/docs/NIF11111111H.pdf',
        }
        doc1.feed(registro_doc_fields1)

        # RegistroDoc
        doc2 = d1.RegistroDoc()
        registro_doc_fields2 = {
            'tipo_doc_aportado': '07',
            'direccion_url': 'http://eneracme.com/docs/NIF11111111H.pdf',
        }
        doc2.feed(registro_doc_fields2)

        # RegistrosDocumento
        registros = d1.RegistrosDocumento()
        registros_documento_fields = {
            'registro_doc': [doc1, doc2],
        }
        registros.feed(registros_documento_fields)

        # Rechazos
        rechazos = d1.Rechazos()
        rechazos_fields = {
            'fecha_rechazo': '2016-07-20',
            'rechazo': rechazo,
            'registros_documento': registros,
        }
        rechazos.feed(rechazos_fields)

        # MensajeRechazo
        mensaje_rechazo = d1.MensajeRechazo()
        mensaje_rechazo_fields = {
            'cabecera': cabecera,
            'rechazos': rechazos,
        }
        mensaje_rechazo.feed(mensaje_rechazo_fields)

        mensaje_rechazo.build_tree()
        xml = str(mensaje_rechazo)
        assertXmlEqual(xml, self.xml_d102_reject.read())


class test_Q1(unittest.TestCase):

    def setUp(self):
        self.xml_q101 = open(get_data("q101.xml"), "r")

    def tearDown(self):
        self.xml_q101.close()

    def test_create_pas01(self):
        # MensajeSaldoLecturasFacturacion
        mensaje = q1.MensajeSaldoLecturasFacturacion()

        # Cabecera
        cabecera = get_header(process='Q1', step='01', date='2014-04-16T22:13:37', code='201412111009')

        # Medidas
        medidas = q1.Medidas()

        # ModeloAparato 1
        ma1 = q1.ModeloAparato()

        # Integrador 1
        i1 = q1.Integrador()

        # LecturaDesde
        lectura_desde = q1.LecturaDesde()
        lectura_desde_fields = {
            'fecha': '2014-04-18',
            'procedencia': '20',
            'lectura': '500',
        }
        lectura_desde.feed(lectura_desde_fields)

        # LecturaHasta
        lectura_hasta = q1.LecturaHasta()
        lectura_hasta_fields = {
            'fecha': '2014-05-18',
            'procedencia': '20',
            'lectura': '1500',
        }
        lectura_hasta.feed(lectura_hasta_fields)

        integrador_fields = {
            'magnitud': 'R2',
            'codigo_periodo': '20',
            'constante_multiplicadora': '1',
            'numero_ruedas_enteras': '10',
            'numero_ruedas_decimales': '20',
            'consumo_calculado': '5000',
            'lectura_desde': lectura_desde,
            'lectura_hasta': lectura_hasta,
        }
        i1.feed(integrador_fields)

        modelo_aparato_fields = {
            'tipo_aparato': 'CG',
            'marca_aparato': '135',
            'numero_serie': '012',
            'tipo_dhedm': '2',
            'integrador_list': [i1],
        }
        ma1.feed(modelo_aparato_fields)

        # ModeloAparato 2
        ma2 = q1.ModeloAparato()
        # Integrador 1
        i1 = q1.Integrador()

        # LecturaDesde
        lectura_desde = q1.LecturaDesde()
        lectura_desde_fields = {
            'fecha': '2014-04-18',
            'procedencia': '30',
            'lectura': '500',
        }
        lectura_desde.feed(lectura_desde_fields)

        # LecturaHasta
        lectura_hasta = q1.LecturaHasta()
        lectura_hasta_fields = {
            'fecha': '2014-05-18',
            'procedencia': '30',
            'lectura': '1500',
        }
        lectura_hasta.feed(lectura_hasta_fields)

        integrador_fields = {
            'magnitud': 'R3',
            'codigo_periodo': '30',
            'constante_multiplicadora': '1',
            'numero_ruedas_enteras': '10',
            'numero_ruedas_decimales': '20',
            'consumo_calculado': '5000',
            'lectura_desde': lectura_desde,
            'lectura_hasta': lectura_hasta,
        }
        i1.feed(integrador_fields)

        # Integrador 2
        i2 = q1.Integrador()

        # LecturaDesde
        lectura_desde = q1.LecturaDesde()
        lectura_desde_fields = {
            'fecha': '2014-04-18',
            'procedencia': '30',
            'lectura': '500',
        }
        lectura_desde.feed(lectura_desde_fields)

        # LecturaHasta
        lectura_hasta = q1.LecturaHasta()
        lectura_hasta_fields = {
            'fecha': '2014-05-18',
            'procedencia': '40',
            'lectura': '1500',
        }
        lectura_hasta.feed(lectura_hasta_fields)

        # Ajuste
        ajuste = q1.Ajuste()
        ajuste_fields = {
            'codigo_motivo_ajuste': '01',
            'ajuste_por_integrador': '1500',
            'comentarios': 'Comentario Ajuste',
        }
        ajuste.feed(ajuste_fields)

        # Anomalia
        anomalia = q1.Anomalia()
        anomalia_fields = {
            'tipo_anomalia': '05',
            'comentarios': 'Comentarios Anomalia',
        }
        anomalia.feed(anomalia_fields)

        integrador_fields = {
            'magnitud': 'R3',
            'codigo_periodo': '30',
            'constante_multiplicadora': '1',
            'numero_ruedas_enteras': '10',
            'numero_ruedas_decimales': '20',
            'consumo_calculado': '5000',
            'lectura_desde': lectura_desde,
            'lectura_hasta': lectura_hasta,
            'ajuste': ajuste,
            'anomalia': anomalia,
            'fecha_hora_maximetro': '2014-05-18T22:13:37',
        }
        i2.feed(integrador_fields)

        modelo_aparato_fields = {
            'tipo_aparato': 'CG',
            'marca_aparato': '136',
            'numero_serie': '012',
            'tipo_dhedm': '3',
            'integrador_list': [i1, i2],
        }
        ma2.feed(modelo_aparato_fields)

        medidas_fields = {
            'cod_pm': '1112223334445556667779',
            'modelo_aparato_list': [ma1, ma2],
        }
        medidas.feed(medidas_fields)

        mensaje_saldo_lecturas_facturacion_fields = {
            'cabecera': cabecera,
            'medidas': medidas,
        }
        mensaje.feed(mensaje_saldo_lecturas_facturacion_fields)
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_q101.read())


class test_W1(unittest.TestCase):

    def setUp(self):
        self.xml_w101 = open(get_data("w101.xml"), "r")
        self.xml_w102_accept = open(get_data("w102_accept.xml"), "r")
        self.xml_w102_reject = open(get_data("w102_reject.xml"), "r")

    def tearDown(self):
        self.xml_w101.close()
        self.xml_w102_accept.close()
        self.xml_w102_reject.close()

    def test_create_pas01(self):
        # MensajeSolicitudAportacionLectura
        mensaje_aportacion_lectura = w1.MensajeSolicitudAportacionLectura()

        # Cabecera
        cabecera = get_header(process='W1', step='01',  date='2014-04-16T22:13:37', code='201412111009')

        # DatosSolicitudAportacionLectura
        datos_solicitud = w1.DatosSolicitudAportacionLectura()
        datos_solicitud_aportacion_lectura_fields = {
            'fecha_lectura': '2015-02-18',
            'tipo_dhedm': '2',
        }
        datos_solicitud.feed(datos_solicitud_aportacion_lectura_fields)

        # LecturaAportada
        la1 = w1.LecturaAportada()
        lectura_aportada_fields = {
            'integrador': 'AE',
            'tipo_codigo_periodo_dh': '21',
            'lectura_propuesta': '0000001162.00',
        }
        la1.feed(lectura_aportada_fields)

        la2 = w1.LecturaAportada()
        lectura_aportada_fields = {
            'integrador': 'AE',
            'tipo_codigo_periodo_dh': '22',
            'lectura_propuesta': '0000003106.00',
        }
        la2.feed(lectura_aportada_fields)

        mensaje_aportacion_lectura_fields = {
            'cabecera': cabecera,
            'datos_solicitud_aportacion_lectura': datos_solicitud,
            'lectura_aportada_list': [la1, la2],
        }
        mensaje_aportacion_lectura.feed(mensaje_aportacion_lectura_fields)
        mensaje_aportacion_lectura.build_tree()
        xml = str(mensaje_aportacion_lectura)
        assertXmlEqual(xml, self.xml_w101.read())

    def test_create_pas02(self):
        # AceptacionAportacionLectura
        mensaje = w1.AceptacionAportacionLectura()

        # Cabecera
        cabecera = get_header(process='W1', step='02',
                              date='2014-04-16T22:13:37', code='201412111009')
        # DatosAceptacionLectura
        datos_aceptacion_lectura = w1.DatosAceptacionLectura()
        datos_aceptacion_lectura_fields = {
            'fecha_aceptacion': '2016-06-06',
        }
        datos_aceptacion_lectura.feed(datos_aceptacion_lectura_fields)

        aceptacion_aportacion_lectura_fields = {
            'cabecera': cabecera,
            'datos_aceptacion_lectura': datos_aceptacion_lectura,
        }
        mensaje.feed(aceptacion_aportacion_lectura_fields)
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_w102_accept.read())

    def test_create_pas02_rej(self):
        # MensajeRechazo
        mensaje_rechazo = w1.MensajeRechazo()

        # Cabecera
        cabecera = get_header(process='W1', step='02')

        # Rechazos
        rechazos = w1.Rechazos()

        # Rechazo
        r1 = w1.Rechazo()
        rechazo_fields = {
            'secuencial': '1',
            'codigo_motivo': '01',
            'comentarios': 'Motiu de rebuig 01: No existe Punto de Suministro asociado al CUPS',
        }
        r1.feed(rechazo_fields)

        # RegistrosDocumento
        registros_documento = w1.RegistrosDocumento()

        # RegistroDoc
        rd1 = w1.RegistroDoc()
        registro_doc_fields = {
            'tipo_doc_aportado': '08',
            'direccion_url': 'http://eneracme.com/docs/NIF11111111H.pdf',
        }
        rd1.feed(registro_doc_fields)

        registros_documento_fields = {
            'registro_doc_list': [rd1],
        }
        registros_documento.feed(registros_documento_fields)

        rechazos_fields = {
            'fecha_rechazo': '2016-07-20',
            'rechazo_list': [r1],
            'registros_documento': registros_documento,
        }
        rechazos.feed(rechazos_fields)

        mensaje_rechazo_fields = {
            'cabecera': cabecera,
            'rechazos': rechazos,
        }
        mensaje_rechazo.feed(mensaje_rechazo_fields)
        mensaje_rechazo.build_tree()
        xml = str(mensaje_rechazo)
        assertXmlEqual(xml, self.xml_w102_reject.read())


class test_B1(unittest.TestCase):

    def setUp(self):
        self.xml_b101 = open(get_data("b101.xml"), "r")
        self.xml_b102_accept = open(get_data("b102_accept.xml"), "r")
        self.xml_b104_accept = open(get_data("b104_accept.xml"), "r")
        self.xml_b105 = open(get_data("b105.xml"), "r")

    def tearDown(self):
        self.xml_b101.close()
        self.xml_b102_accept.close()
        self.xml_b104_accept.close()
        self.xml_b105.close()

    def test_create_pas01(self):
        # MensajeBajaSuspension
        mensaje_baja_suspension = b1.MensajeBajaSuspension()

        # Cabecera
        cabecera = d1.Cabecera()
        cabecera_fields = {
            'codigo_ree_empresa_emisora': '1234',
            'codigo_ree_empresa_destino': '4321',
            'codigo_del_proceso': 'B1',
            'codigo_del_paso': '01',
            'codigo_de_solicitud': '201605219497',
            'secuencial_de_solicitud': '00',
            'fecha': '2016-06-08T04:24:09',
            'cups': 'ES0116000000011531LK0F',
        }
        cabecera.feed(cabecera_fields)

        # BajaSuspension
        baja_suspension = b1.BajaSuspension()

        # DatosSolicitud
        datos_solicitud = b1.DatosSolicitud()
        datos_solicitud_fields = {
            'ind_activacion': 'L',
            'motivo': '03',
        }
        datos_solicitud.feed(datos_solicitud_fields)

        # Cliente
        cliente = get_cliente()

        baja_suspension_fields = {
            'datos_solicitud': datos_solicitud,
            'cliente': cliente,
            'iban': '444555666',
        }
        baja_suspension.feed(baja_suspension_fields)

        mensaje_baja_suspension_fields = {
            'cabecera': cabecera,
            'baja_suspension': baja_suspension,
        }
        mensaje_baja_suspension.feed(mensaje_baja_suspension_fields)
        mensaje_baja_suspension.build_tree()
        xml = str(mensaje_baja_suspension)
        assertXmlEqual(xml, self.xml_b101.read())

    def test_create_pas02(self):
        # MensajeAceptacionBajaSuspension
        mensaje_aceptacion_baja_suspension = b1.MensajeAceptacionBajaSuspension()

        # Cabecera
        cabecera = get_header(process='B1', step='02')

        # AceptacionBajaSuspension
        aceptacion_baja_suspension = b1.AceptacionBajaSuspension()

        # DatosAceptacion
        datos_aceptacion = b1.DatosAceptacion()
        datos_aceptacion_fields = {
            'fecha_aceptacion': '2016-06-06',
            'actuacion_campo': 'S',
            'fecha_ultima_lectura_firme': '2016-06-01',
            'tipo_activacion_prevista': 'B1',
            'fecha_activacion_prevista': '2016-06-08',
        }
        datos_aceptacion.feed(datos_aceptacion_fields)

        aceptacion_baja_suspension_fields = {
            'datos_aceptacion': datos_aceptacion,
        }
        aceptacion_baja_suspension.feed(aceptacion_baja_suspension_fields)

        mensaje_aceptacion_baja_suspension_fields = {
            'cabecera': cabecera,
            'aceptacion_baja_suspension': aceptacion_baja_suspension,
        }
        mensaje_aceptacion_baja_suspension.feed(mensaje_aceptacion_baja_suspension_fields)
        mensaje_aceptacion_baja_suspension.build_tree()
        xml = str(mensaje_aceptacion_baja_suspension)
        assertXmlEqual(xml, self.xml_b102_accept.read())

    def test_create_pas04(self):
        # MensajeAceptacionAnulacionBaja
        mensaje = b1.MensajeAceptacionAnulacionBaja()

        # Cabecera
        cabecera = get_header(process='B1', step='04')

        # AceptacionAnulacion
        aceptacion_anulacion = b1.AceptacionAnulacion()
        aceptacion_anulacion_fields = {
            'fecha_aceptacion': '2017-02-02',
            'hora_aceptacion': '20:05:10',
        }
        aceptacion_anulacion.feed(aceptacion_anulacion_fields)

        mensaje_aceptacion_anulacion_baja_fields = {
            'cabecera': cabecera,
            'aceptacion_anulacion': aceptacion_anulacion,
        }
        mensaje.feed(mensaje_aceptacion_anulacion_baja_fields)
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_b104_accept.read())

    def test_create_pas05(self):
        # MensajeActivacionBajaSuspension
        mensaje = b1.MensajeActivacionBajaSuspension()

        # Cabecera
        cabecera = get_header(process='B1', step='05')

        # ActivacionBaja
        activacion_baja = b1.ActivacionBaja()

        # DatosActivacionBaja
        datos_activacion_baja = b1.DatosActivacionBaja()
        datos_activacion_baja_fields = {
            'fecha_activacion': '2016-08-21',
        }
        datos_activacion_baja.feed(datos_activacion_baja_fields)

        # Contrato
        contrato = b1.Contrato()

        # IdContrato
        id_contrato = b1.IdContrato()
        id_contrato.feed({'cod_contrato': '00001'})
        contrato.feed({'id_contrato': id_contrato})

        # PuntosDeMedida
        puntos_de_medida = c1.PuntosDeMedida()
        # PuntoDeMedida
        punto_de_medida = c1.PuntoDeMedida()
        # Aparatos
        aparatos = c1.Aparatos()
        # Aparato
        aparato = c1.Aparato()

        # ModeloAparato
        modelo_aparato = c1.ModeloAparato()
        modelo_aparato_fields = {
            'tipo_aparato': 'CG',
            'marca_aparato': '132',
            'modelo_marca': '011',
        }
        modelo_aparato.feed(modelo_aparato_fields)

        # DatosAparato
        datos_aparato = c1.DatosAparato()
        datos_aparato_fields = {
            'periodo_fabricacion': '2005',
            'numero_serie': '0000539522',
            'funcion_aparato': 'M',
            'num_integradores': '18',
            'constante_energia': '1.000',
            'constante_maximetro': '1.000',
            'ruedas_enteras': '08',
            'ruedas_decimales': '02',
        }
        datos_aparato.feed(datos_aparato_fields)

        # Medidas
        medidas = c1.Medidas()
        # Medida 1
        medida1 = c1.Medida()
        medida_fields = {
            'tipo_dhedm': '6',
            'periodo': '65',
            'magnitud_medida': 'PM',
            'procedencia': '30',
            'ultima_lectura_firme': '6.00',
            'fecha_lectura_firme': '2003-01-02',
            'anomalia': '01',
            'comentarios': 'Comentario sobre anomalia',
        }
        medida1.feed(medida_fields)
        # Medida 2
        medida2 = c1.Medida()
        medida_fields = {
            'tipo_dhedm': '6',
            'periodo': '66',
            'magnitud_medida': 'PM',
            'procedencia': '30',
            'ultima_lectura_firme': '6.00',
            'fecha_lectura_firme': '2003-01-03',
        }
        medida2.feed(medida_fields)
        medidas_fields = {
            'medida_list': [medida1, medida2],
        }
        medidas.feed(medidas_fields)

        aparato_fields = {
            'modelo_aparato': modelo_aparato,
            'tipo_movimiento': 'CX',
            'tipo_equipo_medida': 'L03',
            'tipo_propiedad_aparato': '1',
            'propietario': 'Desc. Propietario',
            'tipo_dhedm': '6',
            'modo_medida_potencia': '1',
            'lectura_directa': 'N',
            'cod_precinto': '02',
            'datos_aparato': datos_aparato,
            'medidas': medidas,
        }
        aparato.feed(aparato_fields)
        aparatos_fields = {
            'aparato_list': [aparato],
        }
        aparatos.feed(aparatos_fields)

        punto_de_medida_fields = {
            'cod_pm': 'ES1234000000000001JN0F',
            'tipo_movimiento': 'A',
            'tipo_pm': '03',
            'cod_pm_principal': 'ES1234000000000002JN0F',
            'modo_lectura': '1',
            'funcion': 'P',
            'direccion_enlace': '39522',
            'direccion_punto_medida': '000000001',
            'num_linea': '12',
            'telefono_telemedida': '987654321',
            'estado_telefono': '1',
            'clave_acceso': '0000000007',
            'tension_pm': '0',
            'fecha_vigor': '2003-01-01',
            'fecha_alta': '2003-01-01',
            'fecha_baja': '2003-02-01',
            'aparatos': aparatos,
            'comentarios': 'Comentarios Varios',
        }
        punto_de_medida.feed(punto_de_medida_fields)

        puntos_de_medida_fields = {
            'punto_de_medida_list': [punto_de_medida],
        }
        puntos_de_medida.feed(puntos_de_medida_fields)

        activacion_baja_fields = {
            'datos_activacion_baja': datos_activacion_baja,
            'contrato': contrato,
            'puntos_de_medida': puntos_de_medida,
        }
        activacion_baja.feed(activacion_baja_fields)

        mensaje_activacion_baja_suspension_fields = {
            'cabecera': cabecera,
            'activacion_baja': activacion_baja,
        }
        mensaje.feed(mensaje_activacion_baja_suspension_fields)
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_b105.read())


class test_R1(unittest.TestCase):

    def setUp(self):
        self.xml_r101 = open(get_data("r101.xml"), "r")
        self.xml_r102_accept = open(get_data("r102_accept.xml"), "r")
        self.xml_r103 = open(get_data("r103.xml"), "r")
        self.xml_r103_intervenciones = open(get_data("r103_intervenciones.xml"), "r")
        self.xml_r104 = open(get_data("r104.xml"), "r")
        self.xml_r105 = open(get_data("r105.xml"), "r")

    def tearDown(self):
        self.xml_r101.close()
        self.xml_r102_accept.close()
        self.xml_r103.close()
        self.xml_r103_intervenciones.close()
        self.xml_r104.close()
        self.xml_r105.close()

    def test_create_pas01(self):
        # MensajeReclamacionPeticion
        mensaje_reclamacion_peticion = r1.MensajeReclamacionPeticion()

        # CabeceraReclamacion
        cabecera_reclamacion = r1.CabeceraReclamacion()
        cabecera_reclamacion_fields = {
            'codigo_ree_empresa_emisora': '0321',
            'codigo_ree_empresa_destino': '0123',
            'codigo_del_proceso': 'R1',
            'codigo_del_paso': '01',
            'codigo_de_solicitud': '201650008314',
            'secuencial_de_solicitud': '01',
            'fecha': '2016-01-22T10:09:41',
            'cups': 'ES1234000000000001JN0F',
        }
        cabecera_reclamacion.feed(cabecera_reclamacion_fields)

        # SolicitudReclamacion
        solicitud_reclamacion = r1.SolicitudReclamacion()

        # DatosSolicitud
        datos_solicitud = r1.DatosSolicitud()
        datos_solicitud_fields = {
            'tipo': '02',
            'subtipo': '003',
            'referencia_origen': '01',
            'fecha_limite': '2016-02-22',
            'prioritario': 'S',
        }
        datos_solicitud.feed(datos_solicitud_fields)

        # VariablesDetalleReclamacion
        variables_detalle_reclamacion = r1.VariablesDetalleReclamacion()

        # VariableDetalleReclamacion
        vdr1 = r1.VariableDetalleReclamacion()

        # LecturasAportadas
        lecturas_aportadas = r1.LecturasAportadas()

        # LecturaAportada
        la1 = r1.LecturaAportada()
        lectura_aportada_fields = {
            'integrador': 'AE',
            'codigo_periodo_dh': '21',
            'lectura_propuesta': '0000001162.00',
        }
        la1.feed(lectura_aportada_fields)

        la2 = r1.LecturaAportada()
        lectura_aportada_fields = {
            'integrador': 'AE',
            'codigo_periodo_dh': '22',
            'lectura_propuesta': '0000003106.00',
        }
        la2.feed(lectura_aportada_fields)

        lecturas_aportadas_fields = {
            'lectura_aportada_list': [la1, la2],
        }
        lecturas_aportadas.feed(lecturas_aportadas_fields)

        # Contacto
        contacto = r1.Contacto()

        # Telefono
        telefono1 = r1.Telefono()
        telefono_fields = {
            'prefijo_pais': '34',
            'numero': '666777888',
        }
        telefono1.feed(telefono_fields)
        telefono2 = r1.Telefono()
        telefono_fields = {
            'prefijo_pais': '34',
            'numero': '55512345',
        }
        telefono2.feed(telefono_fields)
        telefonos = [telefono1, telefono2]

        contacto_fields = {
            'persona_de_contacto': 'Perico Palotes Largos',
            'telefonos': telefonos,
            'correo_electronico': 'perico@acme.com',
        }
        contacto.feed(contacto_fields)

        # UbicacionIncidencia
        ubicacion_incidencia = r1.UbicacionIncidencia()
        ubicacion_incidencia_fields = {
            'des_ubicacion_incidencia': 'Destino',
            'provincia': '17',
            'municipio': '17079',
            'poblacion': '17079',
            'cod_postal': '17001',
        }
        ubicacion_incidencia.feed(ubicacion_incidencia_fields)

        variable_detalle_reclamacion_fields = {
            'num_expediente_acometida': '11111',
            'num_expediente_fraude': '22222',
            'fecha_incidente': '2016-02-10',
            'num_factura_atr': '243615',
            'tipo_concepto_facturado': '01',
            'fecha_lectura': '2016-01-20',
            'tipo_dhedm': '1',
            'lecturas_aportadas': lecturas_aportadas,
            'codigo_incidencia': '01',
            'codigo_solicitud': '33333',
            'parametro_contratacion': '01',
            'concepto_disconformidad': '100',
            'tipo_de_atencion_incorrecta': '05',
            'iban': '4444222211113333',
            'contacto': contacto,
            'codigo_solicitud_reclamacion': '11111',
            'fecha_desde': '2017-02-05',
            'fecha_hasta': '2017-04-05',
            'importe_reclamado': '5000',
            'ubicacion_incidencia': ubicacion_incidencia,
        }
        vdr1.feed(variable_detalle_reclamacion_fields)

        # VariableDetalleReclamacion 2
        vdr2 = r1.VariableDetalleReclamacion()
        variable_detalle_reclamacion_fields = {
            'num_expediente_acometida': '22222',
        }
        vdr2.feed(variable_detalle_reclamacion_fields)

        variables_detalle_reclamacion_fields = {
            'variable_detalle_reclamacion_list': [vdr1, vdr2],
        }
        variables_detalle_reclamacion.feed(variables_detalle_reclamacion_fields)

        # Cliente
        cliente = get_cliente(dir=True, tipo_dir='F')

        # Reclamante
        reclamante = r1.Reclamante()

        # IdReclamante
        id_reclamante = r1.IdReclamante()
        id_reclamante_fields = {
            'tipo_identificador': 'NI',
            'identificador': 'B36385870',
            'tipo_persona': 'J',
        }
        id_reclamante.feed(id_reclamante_fields)

        # Nombre
        nombre = r1.Nombre()
        nombre_fields = {
            'nombre_de_pila': '',
            'primer_apellido': '',
            'segundo_apellido': '',
            'razon_social': u'ACC Y COMP DE COCINA MILLAN Y MUÑOZ',
        }
        nombre.feed(nombre_fields)

        # Telefono
        telefono1 = r1.Telefono()
        telefono_fields = {
            'prefijo_pais': '34',
            'numero': '666777888',
        }
        telefono1.feed(telefono_fields)
        telefono2 = r1.Telefono()
        telefono_fields = {
            'prefijo_pais': '34',
            'numero': '666777999',
        }
        telefono2.feed(telefono_fields)
        telefono3 = r1.Telefono()
        telefono_fields = {
            'prefijo_pais': '34',
            'numero': '666777555',
        }
        telefono3.feed(telefono_fields)
        telefonos = [telefono1, telefono2, telefono3]

        reclamante_fields = {
            'id_reclamante': id_reclamante,
            'nombre': nombre,
            'telefonos': telefonos,
            'correo_electronico': 'email@host',
        }
        reclamante.feed(reclamante_fields)

        solicitud_reclamacion_fields = {
            'datos_solicitud': datos_solicitud,
            'variables_detalle_reclamacion': variables_detalle_reclamacion,
            'cliente': cliente,
            'tipo_reclamante': '01',
            'reclamante': reclamante,
            'comentarios': 'no calcula sus consumos desea revisio y facturas',
        }
        solicitud_reclamacion.feed(solicitud_reclamacion_fields)

        mensaje_reclamacion_peticion_fields = {
            'cabecera_reclamacion': cabecera_reclamacion,
            'solicitud_reclamacion': solicitud_reclamacion,
        }
        mensaje_reclamacion_peticion.feed(mensaje_reclamacion_peticion_fields)
        mensaje_reclamacion_peticion.build_tree()
        xml = str(mensaje_reclamacion_peticion)
        assertXmlEqual(xml, self.xml_r101.read())

    def test_create_pas02(self):
        # MensajeAceptacionReclamacion
        mensaje_aceptacion_reclamacion = r1.MensajeAceptacionReclamacion()

        # CabeceraReclamacion
        cabecera_reclamacion = r1.CabeceraReclamacion()
        cabecera_reclamacion_fields = {
            'codigo_del_proceso': 'R1',
            'codigo_del_paso': '02',
            'codigo_de_solicitud': '201607211259',
            'secuencial_de_solicitud': '01',
            'cups': 'ES1234000000000001JN0F',
            'codigo_ree_empresa_emisora': '1234',
            'codigo_ree_empresa_destino': '4321',
            'fecha': '2016-07-21T12:59:47',
        }
        cabecera_reclamacion.feed(cabecera_reclamacion_fields)

        # AceptacionReclamacion
        aceptacion_reclamacion = r1.AceptacionReclamacion()

        # DatosAceptacion
        datos_aceptacion = r1.DatosAceptacion()
        datos_aceptacion_fields = {
            'fecha_aceptacion': '2016-06-06',
            'codigo_reclamacion_distribuidora': '1234',
        }
        datos_aceptacion.feed(datos_aceptacion_fields)

        aceptacion_reclamacion_fields = {
            'datos_aceptacion': datos_aceptacion,
        }
        aceptacion_reclamacion.feed(aceptacion_reclamacion_fields)

        mensaje_aceptacion_reclamacion_fields = {
            'cabecera_reclamacion': cabecera_reclamacion,
            'aceptacion_reclamacion': aceptacion_reclamacion,
        }
        mensaje_aceptacion_reclamacion.feed(
            mensaje_aceptacion_reclamacion_fields)
        mensaje_aceptacion_reclamacion.build_tree()
        xml = str(mensaje_aceptacion_reclamacion)
        assertXmlEqual(xml, self.xml_r102_accept.read())

    def test_create_pas03(self):
        # MensajePeticionInformacionAdicionalReclamacion
        mensaje_peticion_informacion_adicional_reclamacion = r1.MensajePeticionInformacionAdicionalReclamacion()

        # CabeceraReclamacion
        cabecera_reclamacion = r1.CabeceraReclamacion()
        cabecera_reclamacion_fields = {
            'codigo_ree_empresa_emisora': '1234',
            'codigo_ree_empresa_destino': '4321',
            'codigo_del_proceso': 'R1',
            'codigo_del_paso': '03',
            'codigo_de_solicitud': '201412111009',
            'secuencial_de_solicitud': '01',
            'fecha': '2016-06-10T08:50:43',
            'cups': 'ES1234000000000001JN0F',
        }
        cabecera_reclamacion.feed(cabecera_reclamacion_fields)

        # InformacionAdicional
        informacion_adicional = r1.InformacionAdicional()

        # DatosInformacion
        datos_informacion = r1.DatosInformacion()
        datos_informacion_fields = {
            'num_expediente_acometida': '1111122222',
            'tipo_comunicacion': '01',
            'codigo_reclamacion_distribuidora': '12345678',
        }
        datos_informacion.feed(datos_informacion_fields)

        # InformacionIntermedia
        informacion_intermedia = r1.InformacionIntermedia()

        informacion_intermedia_fields = {
            'desc_informacion_intermedia': 'Descripcion de la informacion intermedia aportada.',
        }
        informacion_intermedia.feed(informacion_intermedia_fields)

        # Retipificacion
        retipificacion = r1.Retipificacion()
        retipificacion_fields = {
            'tipo': '02',
            'subtipo': '003',
            'desc_retipificacion': 'descripcio de la retipificacio.',
        }
        retipificacion.feed(retipificacion_fields)

        # SolicitudesInformacionAdicional
        solicitudes_informacion_adicional = r1.SolicitudesInformacionAdicional()

        # SolicitudInformacionAdicional 1
        sia1 = r1.SolicitudInformacionAdicional()
        solicitud_informacion_adicional_fields = {
            'tipo_informacion_adicional': '01',
            'desc_peticion_informacion': 'Descripcion de la peticion.',
            'fecha_limite_envio': '2016-07-10',
        }
        sia1.feed(solicitud_informacion_adicional_fields)

        # SolicitudInformacionAdicional 2
        sia2 = r1.SolicitudInformacionAdicional()
        solicitud_informacion_adicional_fields = {
            'tipo_informacion_adicional': '02',
            'desc_peticion_informacion': 'Descripcion de la peticion.',
            'fecha_limite_envio': '2016-07-10',
        }
        sia2.feed(solicitud_informacion_adicional_fields)

        # SolicitudInformacionAdicionalParaRetipificacion
        siar = r1.SolicitudInformacionAdicionalParaRetipificacion()
        solicitud_informacion_adicional_para_retipificacion_fields = {
            'tipo': '03',
            'subtipo': '003',
            'fecha_limite_envio': '2016-08-10',
        }
        siar.feed(solicitud_informacion_adicional_para_retipificacion_fields)

        solicitudes_informacion_adicional_fields = {
            'solicitud_informacion_adicional_list': [sia1, sia2],
            'solicitud_informacion_adicional_para_retipificacion': siar
        }
        solicitudes_informacion_adicional.feed(solicitudes_informacion_adicional_fields)

        informacion_adicional_fields = {
            'datos_informacion': datos_informacion,
            'informacion_intermedia': informacion_intermedia,
            'retipificacion': retipificacion,
            'solicitudes_informacion_adicional': solicitudes_informacion_adicional,
            'comentarios': 'R1 03.',
        }
        informacion_adicional.feed(informacion_adicional_fields)

        mensaje_peticion_informacion_adicional_reclamacion_fields = {
            'cabecera_reclamacion': cabecera_reclamacion,
            'informacion_adicional': informacion_adicional,
        }
        mensaje_peticion_informacion_adicional_reclamacion.feed(mensaje_peticion_informacion_adicional_reclamacion_fields)
        mensaje_peticion_informacion_adicional_reclamacion.build_tree()
        xml = str(mensaje_peticion_informacion_adicional_reclamacion)
        assertXmlEqual(xml, self.xml_r103.read())

    def test_create_pas03_intervenciones(self):
        # MensajePeticionInformacionAdicionalReclamacion
        mensaje = r1.MensajePeticionInformacionAdicionalReclamacion()

        # CabeceraReclamacion
        cabecera_reclamacion = r1.CabeceraReclamacion()
        cabecera_reclamacion_fields = {
            'codigo_ree_empresa_emisora': '1234',
            'codigo_ree_empresa_destino': '4321',
            'codigo_del_proceso': 'R1',
            'codigo_del_paso': '03',
            'codigo_de_solicitud': '201412111009',
            'secuencial_de_solicitud': '01',
            'fecha': '2016-06-10T08:50:43',
            'cups': 'ES1234000000000001JN0F',
        }
        cabecera_reclamacion.feed(cabecera_reclamacion_fields)

        # InformacionAdicional
        informacion_adicional = r1.InformacionAdicional()

        # DatosInformacion
        datos_informacion = r1.DatosInformacion()
        datos_informacion_fields = {
            'num_expediente_acometida': '1111122222',
            'tipo_comunicacion': '01',
            'codigo_reclamacion_distribuidora': '12345678',
        }
        datos_informacion.feed(datos_informacion_fields)

        # InformacionIntermedia
        informacion_intermedia = r1.InformacionIntermedia()

        # Intervenciones
        intervenciones = r1.Intervenciones()

        # Intervencion
        i1 = r1.Intervencion()
        intervencion_fields = {
            'tipo_intervencion': '01',
            'fecha': '2016-06-10',
            'hora_desde': '08:00:00',
            'hora_hasta': '09:00:00',
            'numero_visita': '10',
            'resultado': '001',
            'detalle_resultado': 'Descripcion de los resultados obtenidos.',
        }
        i1.feed(intervencion_fields)

        i2 = r1.Intervencion()
        intervencion_fields = {
            'tipo_intervencion': '02',
            'fecha': '2016-06-10',
            'hora_desde': '08:00:00',
            'hora_hasta': '09:00:00',
            'numero_visita': '10',
            'resultado': '001',
            'detalle_resultado': 'Descripcion de los resultados obtenidos.',
        }
        i2.feed(intervencion_fields)

        intervenciones_fields = {
            'intervencion_list': [i1, i2],
        }
        intervenciones.feed(intervenciones_fields)

        informacion_intermedia_fields = {
            'intervenciones': intervenciones,
        }
        informacion_intermedia.feed(informacion_intermedia_fields)

        informacion_adicional_fields = {
            'datos_informacion': datos_informacion,
            'informacion_intermedia': informacion_intermedia,
            'comentarios': "R1 03 with 'Intervenciones'.",
        }
        informacion_adicional.feed(informacion_adicional_fields)

        mensaje_peticion_informacion_adicional_reclamacion_fields = {
            'cabecera_reclamacion': cabecera_reclamacion,
            'informacion_adicional': informacion_adicional,
        }
        mensaje.feed(mensaje_peticion_informacion_adicional_reclamacion_fields)
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_r103_intervenciones.read())

    def test_create_pas04(self):
        # MensajeEnvioInformacionReclamacion
        mensaje = r1.MensajeEnvioInformacionReclamacion()

        # CabeceraReclamacion
        cabecera_reclamacion = r1.CabeceraReclamacion()
        cabecera_reclamacion_fields = {
            'codigo_ree_empresa_emisora': '1234',
            'codigo_ree_empresa_destino': '4321',
            'codigo_del_proceso': 'R1',
            'codigo_del_paso': '04',
            'codigo_de_solicitud': '201650008314',
            'secuencial_de_solicitud': '01',
            'fecha': '2016-01-22T10:09:41',
            'cups': 'ES1234000000000001JN0F',
        }
        cabecera_reclamacion.feed(cabecera_reclamacion_fields)

        # EnvioInformacionReclamacion
        envio_informacion_reclamacion = r1.EnvioInformacionReclamacion()

        # DatosEnvioInformacion
        datos_envio_informacion = r1.DatosEnvioInformacion()
        datos_envio_informacion_fields = {
            'num_expediente_acometida': '0123456789ABCD',
            'fecha_informacion': '2016-01-20',
        }
        datos_envio_informacion.feed(datos_envio_informacion_fields)

        # VariablesAportacionInformacion
        variables_aportacion_informacion = r1.VariablesAportacionInformacion()

        # VariableAportacionInformacion
        vai1 = r1.VariableAportacionInformacion()
        variable_aportacion_informacion_fields = {
            'tipo_informacion': '01',
            'desc_peticion_informacion': 'Informacio per fer testos.',
            'variable': '01',
            'valor': '125',
        }
        vai1.feed(variable_aportacion_informacion_fields)

        vai2 = r1.VariableAportacionInformacion()
        variable_aportacion_informacion_fields = {
            'tipo_informacion': '02',
        }
        vai2.feed(variable_aportacion_informacion_fields)

        variables_aportacion_informacion_fields = {
            'variable_aportacion_informacion_list': [vai1, vai2],
        }
        variables_aportacion_informacion.feed(variables_aportacion_informacion_fields)

        # VariablesAportacionInformacionParaRetipificacion
        variables_retipificacion = r1.VariablesAportacionInformacionParaRetipificacion()

        vair1 = r1.VariableAportacionInformacionParaRetipificacion()

        # LecturasAportadas
        lecturas_aportadas = r1.LecturasAportadas()

        # LecturaAportada
        la1 = r1.LecturaAportada()
        lectura_aportada_fields = {
            'integrador': 'AE',
            'codigo_periodo_dh': '21',
            'lectura_propuesta': '0000001162.00',
        }
        la1.feed(lectura_aportada_fields)

        la2 = r1.LecturaAportada()
        lectura_aportada_fields = {
            'integrador': 'AE',
            'codigo_periodo_dh': '22',
            'lectura_propuesta': '0000003106.00',
        }
        la2.feed(lectura_aportada_fields)

        lecturas_aportadas_fields = {
            'lectura_aportada_list': [la1, la2],
        }
        lecturas_aportadas.feed(lecturas_aportadas_fields)

        # Contacto
        contacto = r1.Contacto()

        # Telefono
        telefono1 = r1.Telefono()
        telefono_fields = {
            'prefijo_pais': '34',
            'numero': '666777888',
        }
        telefono1.feed(telefono_fields)
        telefono2 = r1.Telefono()
        telefono_fields = {
            'prefijo_pais': '34',
            'numero': '55512345',
        }
        telefono2.feed(telefono_fields)
        telefonos = [telefono1, telefono2]

        contacto_fields = {
            'persona_de_contacto': 'Perico Palotes Largos',
            'telefonos': telefonos,
            'correo_electronico': 'perico@acme.com',
        }
        contacto.feed(contacto_fields)

        # UbicacionIncidencia
        ubicacion_incidencia = r1.UbicacionIncidencia()
        ubicacion_incidencia_fields = {
            'des_ubicacion_incidencia': 'Destino',
            'provincia': '17',
            'municipio': '17079',
            'poblacion': '17079',
            'cod_postal': '17001',
        }
        ubicacion_incidencia.feed(ubicacion_incidencia_fields)

        vair_fields = {
            'num_expediente_acometida': '11111',
            'num_expediente_fraude': '22222',
            'fecha_incidente': '2016-02-10',
            'num_factura_atr': '243615',
            'tipo_concepto_facturado': '01',
            'fecha_lectura': '2016-01-20',
            'tipo_dhedm': '1',
            'lecturas_aportadas': lecturas_aportadas,
            'codigo_incidencia': '01',
            'codigo_solicitud': '33333',
            'parametro_contratacion': '01',
            'concepto_disconformidad': '100',
            'tipo_de_atencion_incorrecta': '05',
            'iban': '4444222211113333',
            'contacto': contacto,
            'codigo_solicitud_reclamacion': '11111',
            'fecha_desde': '2017-02-05',
            'fecha_hasta': '2017-04-05',
            'importe_reclamado': '5000',
            'ubicacion_incidencia': ubicacion_incidencia,
        }
        vair1.feed(vair_fields)

        variables_retipificacion_fields = {
            'variable_aportacion_informacion_para_retipificacion_list': [vair1],
        }
        variables_retipificacion.feed(variables_retipificacion_fields)

        # Cliente
        cliente = get_cliente(dir=True, tipo_dir='F')

        # RegistrosDocumento
        registros_documento = r1.RegistrosDocumento()
        # RegistroDoc
        rd1 = w1.RegistroDoc()
        registro_doc_fields = {
            'tipo_doc_aportado': '01',
            'direccion_url': 'http://eneracme.com/docs/CIE0100001.pdf',
        }
        rd1.feed(registro_doc_fields)
        rd2 = w1.RegistroDoc()
        registro_doc_fields = {
            'tipo_doc_aportado': '06',
            'direccion_url': 'http://eneracme.com/docs/INV201509161234.pdf',
        }
        rd2.feed(registro_doc_fields)
        rd3 = w1.RegistroDoc()
        registro_doc_fields = {
            'tipo_doc_aportado': '08',
            'direccion_url': 'http://eneracme.com/docs/NIF11111111H.pdf',
        }
        rd3.feed(registro_doc_fields)

        registros_documento_fields = {
            'registro_doc_list': [rd1, rd2, rd3],
        }
        registros_documento.feed(registros_documento_fields)

        envio_informacion_reclamacion_fields = {
            'datos_envio_informacion': datos_envio_informacion,
            'variables_aportacion_informacion': variables_aportacion_informacion,
            'variables_aportacion_informacion_para_retipificacion': variables_retipificacion,
            'cliente': cliente,
            'comentarios': 'R104 test with VariablesAportacionInformacion.',
            'registros_documento': registros_documento,
        }
        envio_informacion_reclamacion.feed(envio_informacion_reclamacion_fields)

        mensaje_envio_informacion_reclamacion_fields = {
            'cabecera_reclamacion': cabecera_reclamacion,
            'envio_informacion_reclamacion': envio_informacion_reclamacion,
        }
        mensaje.feed(mensaje_envio_informacion_reclamacion_fields)
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_r104.read())


    def test_create_pas05(self):
        # MensajeCierreReclamacion
        mensaje_cierre_reclamacion = r1.MensajeCierreReclamacion()

        # CabeceraReclamacion
        cabecera_reclamacion = r1.CabeceraReclamacion()
        cabecera_reclamacion_fields = {
            'codigo_ree_empresa_emisora': '1234',
            'codigo_ree_empresa_destino': '4321',
            'codigo_del_proceso': 'R1',
            'codigo_del_paso': '05',
            'codigo_de_solicitud': '201604111738',
            'secuencial_de_solicitud': '01',
            'fecha': '2014-04-16T22:13:37',
            'cups': 'ES1234000000000001JN0F',
        }
        cabecera_reclamacion.feed(cabecera_reclamacion_fields)

        # CierreReclamacion
        cierre_reclamacion = r1.CierreReclamacion()

        # DatosCierre
        datos_cierre = r1.DatosCierre()
        datos_cierre_fields = {
            'num_expediente_acometida': '11111',
            'fecha': '2016-04-12',
            'hora': '16:02:25',
            'tipo': '03',
            'subtipo': '013',
            'codigo_reclamacion_distribuidora': '3291970',
            'resultado_reclamacion': '02',
            'detalle_resultado': '0010101',
            'observaciones': 'Observaciones generales',
            'indemnizacion_abonada': '0.0',
            'num_expediente_anomalia_fraude': '22222',
            'fecha_movimiento': '2016-04-12',
        }
        datos_cierre.feed(datos_cierre_fields)

        cierre_reclamacion_fields = {
            'datos_cierre': datos_cierre,
            'cod_contrato': '383922379',
            'comentarios': 'Comentarios generales',
        }
        cierre_reclamacion.feed(cierre_reclamacion_fields)

        mensaje_cierre_reclamacion_fields = {
            'cabecera_reclamacion': cabecera_reclamacion,
            'cierre_reclamacion': cierre_reclamacion,
        }
        mensaje_cierre_reclamacion.feed(mensaje_cierre_reclamacion_fields)
        mensaje_cierre_reclamacion.build_tree()
        xml = str(mensaje_cierre_reclamacion)
        assertXmlEqual(xml, self.xml_r105.read())


class test_F1(unittest.TestCase):

    def setUp(self):
        self.xml_f101_factura_atr = open(get_data("f101_factura_atr.xml"), "r")
        self.xml_f101_factura_otros = open(
            get_data("f101_factura_otros.xml"), "r"
        )
        self.xml_f101_factura_atr_direccion_suministro = open(
            get_data("f101_factura_atr_direccion_suministro.xml"), "r"
        )
        self.xml_f101_factura_atr_medidas_baja = open(
            get_data("f101_factura_atr_medidas_baja.xml"), "r"
        )

        direccion_suministro = f1.DireccionSuministro()

        direccion_suministro.feed(
            {
                'pais': u'España',
                'provincia': '17',
                'municipio': '17079',
                'poblacion': None,
                'tipo_via': None,
                'cod_postal': '17003',
                'calle': 'Nom carrer',
                'numero_finca': '3',
                'duplicador_finca': None,
                'escalera': '1',
                'piso': 1,
                'puerta': 1,
                'tipo_aclarador_finca': None,
                'alcarador_finca': None,
            }
        )

        self.direccion_suministro_bad_lengths = f1.DireccionSuministro()

        self.direccion_suministro_bad_lengths.feed(
            {
                'pais': u'España',
                'provincia': '17',
                'municipio': '17079',
                'poblacion': None,
                'tipo_via': None,
                'cod_postal': '17003',
                'calle': u'Virgen Serenísima del Santo Socorro',
                'numero_finca': '1234567890',
                'duplicador_finca': '1',
                'escalera': '1234567890',
                'piso': '1234567890',
                'puerta': '12 4567890',
                'tipo_aclarador_finca': False,
                'alcarador_finca': None,
            }
        )

        datos_generales_factura_atr = f1.DatosGeneralesFacturaATR()

        cliente = f1.Cliente()

        cliente.feed(
            {
                'tipo_identificador': 'NI',
                'identificador': '70876712G',
                'tipo_persona': 'F',
            }
        )

        datos_generales_factura_for_atr = f1.DatosGeneralesFactura()

        datos_generales_factura_for_atr.feed(
            {
                'codigo_fiscal_factura': 'F0001',
                'tipo_factura': 'N',
                'motivo_facturacion': '01',
                'codigo_factura_rectificada_anulada': None,
                'expediente': None,
                'fecha_factura': '2017-05-01',
                'identificador_emisora': 'B11254455',
                'comentarios': '. ',
                'importe_total_factura': 100,
                'saldo_factura': 100,
                'tipo_moneda': '02',
            }
        )

        datos_generales_factura_for_otros = f1.DatosGeneralesFactura()

        datos_generales_factura_for_otros.feed(
            {
                'codigo_fiscal_factura': 'F0001',
                'tipo_factura': 'N',
                'motivo_facturacion': '01',
                'codigo_factura_rectificada_anulada': None,
                'expediente': None,
                'fecha_factura': '2017-05-01',
                'identificador_emisora': 'B11254455',
                'comentarios': '. ',
                'importe_total_factura': 21.84,
                'saldo_factura': 21.84,
                'tipo_moneda': '02',
            }
        )

        periodo = f1.Periodo()

        periodo.feed(
            {
                'fecha_desde_factura': '2017-03-31',
                'fecha_hasta_factura': '2017-04-30',
                'numero_dias': 30,
            }
        )

        atr_data = f1.DatosFacturaATR()

        atr_data.feed(
            {
                'fecha_boe': '2016-01-01',
                'tarifa_atr_fact': '001',
                'modo_control_potencia': 1,
                'marca_medida_con_perdidas': 'N',
                'vas_trafo': None,
                'porcentaje_perdidas': None,
                'indicativo_curva_carga': '02',
                'periodo_cch': None,
                'periodo': periodo,
            }
        )

        self.atr_data_lb = f1.DatosFacturaATR()

        self.atr_data_lb.feed(
            {
                'fecha_boe': '2016-01-01',
                'tarifa_atr_fact': '001',
                'modo_control_potencia': 1,
                'marca_medida_con_perdidas': 'S',
                'vas_trafo': 50000.0,
                'porcentaje_perdidas': 4.00,
                'indicativo_curva_carga': '02',
                'periodo_cch': None,
                'periodo': periodo,
            }
        )

        datos_generales_factura_atr.feed(
            {
                'direccion_suministro': direccion_suministro,
                'cliente': cliente,
                'cod_contrato': '111111',
                'datos_generales_factura': datos_generales_factura_for_atr,
                'datos_factura_atr': atr_data,
            }
        )

        periodo_pot = f1.PeriodoPotencia()

        periodo_pot.feed(
            {
                'potencia_contratada': 1000,
                'potencia_max_demandada': 1000,
                'potencia_a_facturar': 1000,
                'precio_potencia': 0.05,
            }
        )

        periodos_potencia = [periodo_pot]

        term_potencia = f1.TerminoPotencia()

        term_potencia.feed(
            {
                'fecha_desde': '2017-03-31',
                'fecha_hasta': '2017-04-30',
                'periodo': periodos_potencia,
            }
        )

        terminos_potencia = [term_potencia]

        power = f1.Potencia()

        power.feed(
            {
                'termino_potencia': terminos_potencia,
                'penalizacion_no_icp': 'N',
                'importe_total_termino_potencia': 50,
            }
        )

        periodo_act = f1.PeriodoEnergiaActiva()

        periodo_act.feed(
            {
                'valor_energia_activa': 300,
                'precio_energia': 0.044027,
            }
        )

        periodos_activa = [periodo_act]

        term_activa = f1.TerminoEnergiaActiva()

        term_activa.feed(
            {
                'fecha_desde': '2017-03-31',
                'fecha_hasta': '2017-04-30',
                'periodos': periodos_activa,
            }
        )

        terminos_activa = [term_activa]

        energia_activa = f1.EnergiaActiva()

        energia_activa.feed(
            {
                'termino_energia_activa': terminos_activa,
                'importe_total_energia_activa': 13.21,
            }
        )

        impuesto_electrico = f1.ImpuestoElectrico()

        impuesto_electrico.feed(
            {
                'base_imponible': 0,
                'porcentaje': 0,
                'importe': 0,
            }
        )

        iva_atr = f1.IVA()

        iva_atr.feed(
            {
                'base_imponible': 63.21,
                'porcentaje': 21,
                'importe': 13.27,
            }
        )

        lectura_desde = f1.LecturaDesde()

        lectura_desde.feed(
            {
                'fecha': '2017-03-31',
                'procedencia': '30',
                'lectura': 100,
            }
        )

        lectura_hasta = f1.LecturaHasta()

        lectura_hasta.feed(
            {
                'fecha': '2017-04-30',
                'procedencia': '30',
                'lectura': 400,
            }
        )

        ivas_atr = [iva_atr]

        integrador = f1.Integrador()

        integrador.feed(
            {
                'magnitud': 'AE',
                'codigo_periodo': '10',
                'constante_multiplicadora': 1.0,
                'numero_ruedas_enteras': 5,
                'numero_ruedas_decimales': 0,
                'consumo_calculado': 300,
                'lectura_desde': lectura_desde,
                'lectura_hasta': lectura_hasta,
                'ajuste': None,
                'anomalia': None,
                'fecha_hora_maximetro': None,
            }
        )

        integradores = [integrador]

        aparato = f1.ModeloAparato()

        aparato.feed(
            {
                'tipo_aparato': 'CC',
                'marca_aparato': 199,
                'numero_serie': 'C99999',
                'tipo_dhedm': 1,
                'integrador': integradores
            }
        )

        aparatos = [aparato]

        medidas = f1.Medidas()

        medidas.feed(
            {
                'cod_pm': 'ES1234000000000001JN0F',
                'modelo_aparato': aparatos
            }
        )

        self.factura_atr = f1.FacturaATR()

        self.factura_atr.feed(
            {
                'datos_generales_factura_atr': datos_generales_factura_atr,
                'potencia': power,
                'exceso_potencia': None,
                'energia_activa': energia_activa,
                'energia_reactiva': None,
                'impuesto_electrico': impuesto_electrico,
                'alquileres': None,
                'importe_intereses': None,
                'concepto_repercutible': None,
                'iva': ivas_atr,
                'iva_reducido': None,
                'medidas': medidas,
            }
        )

        datos_gen_otras_facturas = f1.DatosGeneralesOtrasFacturas()

        datos_gen_otras_facturas.feed(
            {
                'direccion_suministro': direccion_suministro,
                'cliente': cliente,
                'cod_contrato': '111111',
                'datos_generales_factura': datos_generales_factura_for_otros,
                'fecha_boe': '2016-01-01',
            }
        )

        concepto_repercutible_enganche = f1.ConceptoRepercutible()

        concepto_repercutible_enganche.feed(
            {
                'concepto_repercutible': '04',
                'tipo_impositivo_concepto_repercutible': 1,
                'fecha_operacion': '2016-09-01',
                'unidades_concepto_repercutible': 1.0,
                'precio_unidad_concepto_repercutible': 9.04476,
                'importe_total_concepto_repercutible': 9.04,
                'comentarios': 'Cuota de enganche / Act. en equipos BT',
            }
        )

        concepto_repercutible_verificacion = f1.ConceptoRepercutible()

        concepto_repercutible_verificacion.feed(
            {
                'concepto_repercutible': '05',
                'tipo_impositivo_concepto_repercutible': 1,
                'fecha_operacion': '2016-09-01',
                'unidades_concepto_repercutible': 1.0,
                'precio_unidad_concepto_repercutible': 8.011716,
                'importe_total_concepto_repercutible': 8.01,
                'comentarios': u'Cuota de verificación BT',
            }
        )

        concepto_repercutible_demora = f1.ConceptoRepercutible()

        concepto_repercutible_demora.feed(
            {
                'concepto_repercutible': '11',
                'tipo_impositivo_concepto_repercutible': 1,
                'fecha_desde': '2016-09-01',
                'fecha_hasta': '2016-10-01',
                'unidades_concepto_repercutible': 1.0,
                'precio_unidad_concepto_repercutible': 1.0,
                'importe_total_concepto_repercutible': 1.0,
                'comentarios': 'Intereses de demora',
            }
        )

        conceptos_repercutibles = [
            concepto_repercutible_enganche, concepto_repercutible_verificacion,
            concepto_repercutible_demora
        ]

        iva_otros = f1.IVA()

        iva_otros.feed(
            {
                'base_imponible': 18.05,
                'porcentaje': 21,
                'importe': 3.79,
            }
        )

        ivas_otros = [iva_otros]

        self.factura_otros = f1.OtrasFacturas()
        self.factura_otros.feed(
            {
                'datos_generales_otras_facturas': datos_gen_otras_facturas,
                'concepto_repercutible': conceptos_repercutibles,
                'iva': ivas_otros,
                'iva_reducido': None,
            }
        )

    def tearDown(self):
        self.xml_f101_factura_atr.close()

    def with_factura_atr(self):
        cabecera = get_header(process='F1', step='01')

        facturacion = f1.Facturacion()

        facturas = f1.Facturas()

        registo_fin = f1.RegistroFin()
        registo_fin.feed(
            {
                'importe_total': 76.48,
                'saldo_total_facturacion': 76.48,
                'total_recibos': 1,
                'tipo_moneda': '02',
                'fecha_valor': '2017-05-01',
                'fecha_limite_pago': '2017-06-01',
                'iban': 'ES7712341234161234567890',
                'id_remesa': '0',
            }
        )

        facturas.feed(
            {
                'factura_atr': self.factura_atr,
                'registro_fin': registo_fin
            }
        )

        facturacion.feed(
            {
                'cabecera': cabecera,
                'facturas': facturas,
            }
        )

        return facturacion

    def with_factura_otros(self):
        cabecera = get_header(process='F1', step='01')

        facturacion = f1.Facturacion()

        facturas = f1.Facturas()

        registo_fin = f1.RegistroFin()
        registo_fin.feed(
            {
                'importe_total': 21.84,
                'saldo_total_facturacion': 21.84,
                'total_recibos': 1,
                'tipo_moneda': '02',
                'fecha_valor': '2016-11-01',
                'fecha_limite_pago': '2016-11-21',
                'iban': 'ES7712341234161234567890',
                'id_remesa': '0',
            }
        )

        facturas.feed(
            {
                'otras_facturas': self.factura_otros,
                'registro_fin': registo_fin
            }
        )

        facturacion.feed(
            {
                'cabecera': cabecera,
                'facturas': facturas,
            }
        )

        return facturacion

    def test_create_pas01_atr_invoice(self):
        mensaje = self.with_factura_atr()

        mensaje.build_tree()

        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_f101_factura_atr.read())

    def test_create_pas01_atr_invoice_direccion_suministro(self):
        mensaje = self.with_factura_atr()

        mensaje.facturas.factura_atr.datos_generales_factura_atr.direccion_suministro = self.direccion_suministro_bad_lengths

        mensaje.build_tree()

        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_f101_factura_atr_direccion_suministro.read())

    def test_create_pas01_atr_invoice_medidas_baja(self):
        mensaje = self.with_factura_atr()

        mensaje.facturas.factura_atr.datos_generales_factura_atr.datos_factura_atr = self.atr_data_lb

        mensaje.build_tree()

        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_f101_factura_atr_medidas_baja.read())

    def test_create_pas01_other_invoice(self):
        mensaje = self.with_factura_otros()

        mensaje.build_tree()

        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_f101_factura_otros.read())


class test_A1_41(unittest.TestCase):

    def setUp(self):
        self.xml_a141 = open(get_data("a141.xml"), "r")

    def tearDown(self):
        self.xml_a141.close()

    def test_create_a141(self):
        # MensajeA141
        mensaje_a141 = a1_41.MensajeA141()

        # Heading
        heading = a1_41.Heading()
        heading_fields = {
            'dispatchingcode': 'GML',
            'dispatchingcompany': '1234',
            'destinycompany': '4321',
            'communicationsdate': '2018-05-01',
            'communicationshour': '12:00:00',
            'processcode': '41',
            'messagetype': 'A1'
        }
        heading.feed(heading_fields)

        # A141
        a141 = a1_41.A141()

        # RegistrosDocumento
        registros_documento = a1_41.Registerdoclist()
        rd1 = a1_41.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-02',
            'doctype': 'CC',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': '404 page not found'
        }
        rd1.feed(registro_doc_fields)
        rd2 = a1_41.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-03',
            'doctype': '01',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': '404 page not found'
        }
        rd2.feed(registro_doc_fields)
        registros_documento.feed({
            'registerdoc_list': [rd1, rd2],
        })

        a141_fields = {
            'comreferencenum': '000123456789',
            'reqdate': '2018-05-01',
            'reqhour': '13:00:00',
            'nationality': 'ES',
            'documenttype': '01',
            'documentnum': '11111111H',
            'cups': 'ES1234000000000001JN',
            'modeffectdate': '05',
            'reqtransferdate': '2018-06-01',
            'updatereason': '01',
            'surrogacy': 'S',
            'newnationality': 'AF',
            'newdocumenttype': '03',
            'newdocumentnum': '00000000T',
            'newfirstname': 'Gas',
            'newfamilyname1': 'Al',
            'newfamilyname2': 'Matalas',
            'newtitulartype': 'F',
            'newregularaddress': 'S',
            'newtelephone1': '999888777',
            'newtelephone2': '666555444',
            'newemail': 'gasalmatalas@atr',
            'newlanguage': '02',
            'newprovinceowner': '17',
            'newcityowner': '17001',
            'newzipcodeowner': '17002',
            'newstreettypeowner': 'ACCE',
            'newstreetowner': 'Carrer inventat',
            'newstreetnumberowner': '1',
            'newportal': '2',
            'newstaircase': '3',
            'newfloor': '4',
            'newdoor': '5',
            'newreqqd': '987654321.1234567',
            'disconnectedserviceaccepted': 'N',
            'extrainfo': 'comentarios extras',
            'registerdoclist': registros_documento,
        }
        a141.feed(a141_fields)

        mensaje_a141_fields = {
            'heading': heading,
            'a141': a141,
        }
        mensaje_a141.feed(mensaje_a141_fields)
        mensaje_a141.build_tree()
        xml = str(mensaje_a141)
        assertXmlEqual(xml, self.xml_a141.read())


class test_A1_02(unittest.TestCase):

    def setUp(self):
        self.xml_a102 = open(get_data("a102.xml"), "r")

    def tearDown(self):
        self.xml_a102.close()

    def test_create_a102(self):
        # MensajeA102
        mensaje_a102 = a1_02.MensajeA102()

        # Heading
        heading = a1_02.Heading()
        heading_fields = {
            'dispatchingcode': 'GML',
            'dispatchingcompany': '1234',
            'destinycompany': '4321',
            'communicationsdate': '2018-05-01',
            'communicationshour': '12:00:00',
            'processcode': '02',
            'messagetype': 'A1'
        }
        heading.feed(heading_fields)

        # A102
        a102 = a1_02.A102()
        a102_fields = {
            'comreferencenum': '000123456789',
            'reqdate': '2018-05-01',
            'reqhour': '13:00:00',
            'titulartype': 'F',
            'nationality': 'ES',
            'documenttype': '01',
            'documentnum': '11111111H',
            'cups': 'ES1234000000000001JN',
            'modeffectdate': '05',
            'reqtransferdate': '2018-06-01',
            'disconnectedserviceaccepted': 'N',
            'extrainfo': 'comentarios extras',
            'reqqd': 654321.1234,
            'reqestimatedqa': 987654,
        }
        a102.feed(a102_fields)
        mensaje_a102_fields = {
            'heading': heading,
            'a102': a102,
        }
        mensaje_a102.feed(mensaje_a102_fields)
        mensaje_a102.build_tree()
        xml = str(mensaje_a102)
        assertXmlEqual(xml, self.xml_a102.read())


class test_A1_05(unittest.TestCase):

    def setUp(self):
        self.xml_a105 = open(get_data("a105.xml"), "r")

    def tearDown(self):
        self.xml_a105.close()

    def test_create_a105(self):
        # MensajeA105
        mensaje_a105 = a1_05.MensajeA105()

        # Heading
        heading = a1_05.Heading()
        heading_fields = {
            'dispatchingcode': 'GML',
            'dispatchingcompany': '1234',
            'destinycompany': '4321',
            'communicationsdate': '2018-05-01',
            'communicationshour': '12:00:00',
            'processcode': '05',
            'messagetype': 'A1'
        }
        heading.feed(heading_fields)

        # A141
        a105 = a1_05.A105()

        # RegistrosDocumento
        registros_documento = a1_05.Registerdoclist()
        rd1 = a1_05.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-02',
            'doctype': 'CC',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': '404 page not found'
        }
        rd1.feed(registro_doc_fields)
        rd2 = a1_05.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-03',
            'doctype': '01',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': '404 page not found'
        }
        rd2.feed(registro_doc_fields)
        registros_documento.feed({
            'registerdoc_list': [rd1, rd2],
        })

        a105_fields = {
            'comreferencenum': '000123456789',
            'reqdate': '2018-05-01',
            'reqhour': '13:00:00',
            'nationality': 'ES',
            'documenttype': '01',
            'documentnum': '11111111H',
            'cups': 'ES1234000000000001JN',
            'modeffectdate': '05',
            'reqtransferdate': '2018-06-01',
            'updatereason': '01',
            'surrogacy': 'S',
            'newnationality': 'AF',
            'newdocumenttype': '03',
            'newdocumentnum': '00000000T',
            'newfirstname': 'Gas',
            'newfamilyname1': 'Al',
            'newfamilyname2': 'Matalas',
            'newtitulartype': 'F',
            'newregularaddress': 'S',
            'newtelephone': '999888777',
            'newfax': '111222333',
            'newemail': 'gasalmatalas@atr',
            'newcaecode': '9988',
            'newprovinceowner': '17',
            'newcityowner': '17001',
            'newzipcodeowner': '17002',
            'newstreettypeowner': 'ACCE',
            'newstreetowner': 'Carrer inventat',
            'newstreetnumberowner': '1',
            'newportalowner': '2',
            'newstaircaseowner': '3',
            'newfloorowner': '4',
            'newdoorowner': '5',
            'newreqqd': '987654321.1234567',
            'newtolltype': '31',
            'extrainfo': 'comentarios extras',
            'registerdoclist': registros_documento,
        }
        a105.feed(a105_fields)

        mensaje_a105_fields = {
            'heading': heading,
            'a105': a105,
        }
        mensaje_a105.feed(mensaje_a105_fields)
        mensaje_a105.build_tree()
        xml = str(mensaje_a105)
        assertXmlEqual(xml, self.xml_a105.read())


class test_A1_44(unittest.TestCase):

    def setUp(self):
        self.xml_a144 = open(get_data("a144.xml"), "r")

    def tearDown(self):
        self.xml_a144.close()

    def test_create_a144(self):
        # MensajeA144
        mensaje_a144 = a1_44.MensajeA144()

        # Heading
        heading = a1_44.Heading()
        heading_fields = {
            'dispatchingcode': 'GML',
            'dispatchingcompany': '1234',
            'destinycompany': '4321',
            'communicationsdate': '2018-05-01',
            'communicationshour': '12:00:00',
            'processcode': '44',
            'messagetype': 'A1'
        }
        heading.feed(heading_fields)

        # A144
        a144 = a1_44.A144()

        # RegistrosDocumento
        registros_documento = a1_05.Registerdoclist()
        rd1 = a1_44.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-02',
            'doctype': 'CC',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': '404 page not found'
        }
        rd1.feed(registro_doc_fields)
        rd2 = a1_05.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-03',
            'doctype': '01',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': '404 page not found'
        }
        rd2.feed(registro_doc_fields)
        registros_documento.feed({
            'registerdoc_list': [rd1, rd2],
        })

        a144_fields = {
            'comreferencenum': '000123456789',
            'sourcetype': '01',
            'firstname': 'Gas',
            'lastname': 'Al',
            'secondname': 'Matalas',
            'cups': 'ES1234000000000001JN',
            'operationtype': 'A10001',
            'description': 'Desc',
            'operationnum': '111111',
            'prefixtel1': '34',
            'telephone1': '987654321',
            'prefixtel2': '33',
            'telephone2': '123456789',
            'reqdate': '2018-05-01',
            'reqhour': '13:00:00',
            'readingdate': '2018-06-01',
            'readingvalue': '25',
            'extrainfo': 'comentarios extras',
            'registerdoclist': registros_documento,
        }
        a144.feed(a144_fields)
        mensaje_a144_fields = {
            'heading': heading,
            'a1': a144,
        }
        mensaje_a144.feed(mensaje_a144_fields)
        mensaje_a144.build_tree()
        xml = str(mensaje_a144)
        assertXmlEqual(xml, self.xml_a144.read())


class test_A1_03(unittest.TestCase):

    def setUp(self):
        self.xml_a103 = open(get_data("a103.xml"), "r")

    def tearDown(self):
        self.xml_a103.close()

    def test_create_a103(self):
        # MensajeA103
        mensaje_a103 = a1_03.MensajeA103()

        # Heading
        heading = a1_03.Heading()
        heading_fields = {
            'dispatchingcode': 'GML',
            'dispatchingcompany': '1234',
            'destinycompany': '4321',
            'communicationsdate': '2018-05-01',
            'communicationshour': '12:00:00',
            'processcode': '03',
            'messagetype': 'A1'
        }
        heading.feed(heading_fields)

        # A103
        a103 = a1_03.A103()

        a103_fields = {
            'comreferencenum': '000123456789',
            'titulartype': 'F',
            'nationality': 'ES',
            'documenttype': '01',
            'documentnum': 'ES11111111H',
            'annulmentreason': '002',
            'cups': 'ES1234000000000001JN',
            'reqdate': '2018-05-01',
            'reqhour': '13:00:00',
            'extrainfo': 'comentarios extras',
        }
        a103.feed(a103_fields)
        mensaje_a103_fields = {
            'heading': heading,
            'a103': a103,
        }
        mensaje_a103.feed(mensaje_a103_fields)
        mensaje_a103.build_tree()
        xml = str(mensaje_a103)
        assertXmlEqual(xml, self.xml_a103.read())


class test_A1_04(unittest.TestCase):

    def setUp(self):
        self.xml_a104 = open(get_data("a104.xml"), "r")

    def tearDown(self):
        self.xml_a104.close()

    def test_create_a104(self):
        # MensajeA104
        mensaje_a104 = a1_04.MensajeA104()

        # Heading
        heading = a1_04.Heading()
        heading_fields = {
            'dispatchingcode': 'GML',
            'dispatchingcompany': '4321',
            'destinycompany': '1234',
            'communicationsdate': '2018-05-01',
            'communicationshour': '12:00:00',
            'processcode': '04',
            'messagetype': 'A1'
        }
        heading.feed(heading_fields)

        # A104
        a104 = a1_04.A104()

        a104_fields = {
            'comreferencenum': '000123456789',
            'reqdate': '2018-05-01',
            'reqhour': '12:00:00',
            'titulartype': 'F',
            'nationality': 'ES',
            'documenttype': '07',
            'documentnum': '11111111H',
            'cups': 'ES1234000000000001JN',
            'cancelreason': '04',
            'modeffectdate': '03',
            'reqcanceldate': '2018-03-08',
            'contactphonenumber': '555123456',
            'extrainfo': (
                'Información adicional con la ubicación '
                'del tesoro de Mary Read'
            )
        }

        a104.feed(a104_fields)

        mensaje_a104_fields = {
            'heading': heading,
            'a104': a104,
        }
        mensaje_a104.feed(mensaje_a104_fields)
        mensaje_a104.build_tree()
        xml = str(mensaje_a104)
        assertXmlEqual(xml, self.xml_a104.read())


class test_A1_48(unittest.TestCase):

    def setUp(self):
        self.xml_a148 = open(get_data("a148.xml"), "r")
        self.xml_a2648 = open(get_data("a2648.xml"), "r")

    def tearDown(self):
        self.xml_a148.close()
        self.xml_a2648.close()

    def test_create_a148(self):
        # A148
        mensaje = a1_48.MensajeA148()
        heading = a1_48.Heading()
        heading_fields = {
            'dispatchingcode': 'GML',
            'dispatchingcompany': '1234',
            'destinycompany': '4321',
            'communicationsdate': '2018-05-01',
            'communicationshour': '12:00:00',
            'processcode': '48',
            'messagetype': 'A1'
        }
        heading.feed(heading_fields)
        a148 = a1_48.A148()

        # claimer
        claimer = a1_48.claimer()

        # claimerid
        claimerid = a1_48.claimerid()
        claimerid_fields = {
            'claimerdocumenttype': '01',
            'claimerdocumentnum': 'ES00000000T',
        }
        claimerid.feed(claimerid_fields)


        # claimername
        claimername = a1_48.claimername()
        claimername_fields = {
            'claimerfirstname': 'gas',
            'claimerlastname': 'al',
            'claimersecondname': 'matalas',
        }
        claimername.feed(claimername_fields)


        # claimertelephone
        claimertelephone = a1_48.claimertelephone()
        claimertelephone_fields = {
            'claimerprefixtel1': '34',
            'claimertelephone1': '999888777',
        }
        claimertelephone.feed(claimertelephone_fields)

        claimer_fields = {
            'claimerid': claimerid,
            'claimername': claimername,
            'claimertelephone': claimertelephone,
            'claimeremail': 'gas@matalas',
        }
        claimer.feed(claimer_fields)

        # claimreference
        claimreference = a1_48.claimreference()
        # contact
        contact = a1_48.contact()
        # contacttelephone
        contacttelephone = a1_48.contacttelephone()
        contacttelephone_fields = {
            'telephoneprefix': '+34',
            'telephonenumber': '666555444',
        }
        contacttelephone.feed(contacttelephone_fields)
        contact_fields = {
            'contactname': 'mortdegana',
            'contacttelephone': contacttelephone,
            'contactemail': 'matalas@gas',
        }
        contact.feed(contact_fields)
        # incidentperiod
        incidentperiod = a1_48.incidentperiod()
        incidentperiod_fields = {
            'datefrom': '2018-09-21',
            'dateto': '2018-09-21',
        }
        incidentperiod.feed(incidentperiod_fields)
        # incidentlocation
        incidentlocation = a1_48.incidentlocation()
        incidentlocation_fields = {
            'incidentlocationdesc': 'calle pequeña',
            'incidentlocationprovince': '01',
            'incidentlocationcity': '000001',
            'incidentlocationcitysubdivision': '20AA',
            'incidentlocationzipcode': '17888',
        }
        incidentlocation.feed(incidentlocation_fields)
        # reading
        reading = a1_48.reading()
        reading_fields = {
            'readingdate': '2018-09-21',
            'readingvalue': '4.89',
        }
        reading.feed(reading_fields)
        # incident
        incident = a1_48.incident()
        incident_fields = {
            'incidentdate': '2018-09-21',
        }
        incident.feed(incident_fields)
        # client
        client = a1_48.client()
        # document
        document = a1_48.document()
        document_fields = {
            'documenttype': '01',
            'documentnum': 'ES11111111T',
        }
        document.feed(document_fields)
        # name
        name = a1_48.cname()
        name_fields = {
            'firstname': 'nom',
            'familyname1': 'cognom',
            'familyname2': 'cognom 2',
        }
        name.feed(name_fields)
        # telephone
        telephone = a1_48.telephone()
        telephone_fields = {
            'telephoneprefix': '34',
            'telephonenumber': '999111222',
        }
        telephone.feed(telephone_fields)
        # clientAddress
        clientAddress = a1_48.clientAddress()
        clientAddress_fields = {
            'province': '01',
            'city': '000001',
            'zipcode': '16001',
            'streettype': 'ACCE',
            'street': 'inventat',
            'streetnumber': '4_ce',
            'portal': '5_TE2',
            'staircase': '5_mIh',
            'floor': '5_e6A',
            'door': '5_40T',
        }
        clientAddress.feed(clientAddress_fields)
        client_fields = {
            'document': document,
            'titulartype': 'F',
            'cname': name,
            'telephone': telephone,
            'email': 'a@a',
            'clientAddress': clientAddress,
        }
        client.feed(client_fields)
        claimreference_fields = {
            'wrongattentiontype': '01',
            'comreferencenum': '0000001',
            'targetclaimcomreferencenum': '9999998',
            'conceptcontract': '01',
            'conceptfacturation': '02',
            'contact': contact,
            'nnssexpedient': '45666666',
            'fraudrecordnum': '888888888',
            'incidentperiod': incidentperiod,
            'invoicenumber': 'F5555',
            'incidentlocation': incidentlocation,
            'reading': reading,
            'incident': incident,
            'client': client,
            'claimedcompensation': '520176666.24',
            'iban': 'ES0000000000000000000000000000000',
        }
        claimreference.feed(claimreference_fields)
        claimreferencelist = a1_48.claimreferencelist()
        claimreference_fields = {
            'claimreference_list': [claimreference],
        }
        claimreferencelist.feed(claimreference_fields)

        # Registerdoclist
        rd1 = a1_44.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-02',
            'doctype': 'CC',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': '404 page not found'
        }
        rd1.feed(registro_doc_fields)
        rd2 = a1_05.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-03',
            'doctype': '01',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': 'Comments'
        }
        rd2.feed(registro_doc_fields)
        registerdoclist = a1_48.Registerdoclist()
        registerdoclist_fields = {
            'registerdoclist': [rd1, rd2],
        }
        registerdoclist.feed(registerdoclist_fields)

        a148_fields = {
            'reqdate': '2018-05-01',
            'reqhour': '13:00:00',
            'comreferencenum': '000123456789',
            'claimertype': '01',
            'claimer': claimer,
            'claimtype': '01',
            'claimsubtype': '001',
            'originreference': 'AB999888',
            'claimreferencelist': claimreferencelist,
            'cups': 'ES1234000000000001JN',
            'legallimitdate': '2018-09-21',
            'priority': '1',
            'extrainfo': 'comentarios extra',
            'registerdoclist': registerdoclist,
        }
        a148.feed(a148_fields)
        mensaje_a148_fields = {
            'heading': heading,
            'a1': a148,
        }
        mensaje.feed(mensaje_a148_fields)
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_a148.read())

    def test_create_a2648(self):
        # A2648
        mensaje = a1_48.MensajeA2648()
        heading = a1_48.Heading()
        heading_fields = {
            'dispatchingcode': 'GML',
            'dispatchingcompany': '1234',
            'destinycompany': '4321',
            'communicationsdate': '2018-05-01',
            'communicationshour': '12:00:00',
            'processcode': '48',
            'messagetype': 'A26'
        }
        heading.feed(heading_fields)

        # A2648
        a2648 = a1_48.A2648()

        # claimreference
        claimreference = a1_48.claimreference()
        # contact
        contact = a1_48.contact()
        # contacttelephone
        contacttelephone = a1_48.contacttelephone()
        contacttelephone_fields = {
            'telephoneprefix': '+34',
            'telephonenumber': '666555444',
        }
        contacttelephone.feed(contacttelephone_fields)
        contact_fields = {
            'contactname': 'mortdegana',
            'contacttelephone': contacttelephone,
            'contactemail': 'matalas@gas',
        }
        contact.feed(contact_fields)
        # incidentperiod
        incidentperiod = a1_48.incidentperiod()
        incidentperiod_fields = {
            'datefrom': '2018-09-21',
            'dateto': '2018-09-21',
        }
        incidentperiod.feed(incidentperiod_fields)
        # incidentlocation
        incidentlocation = a1_48.incidentlocation()
        incidentlocation_fields = {
            'incidentlocationdesc': 'calle pequeña',
            'incidentlocationprovince': '01',
            'incidentlocationcity': '000001',
            'incidentlocationcitysubdivision': '20AA',
            'incidentlocationzipcode': '17888',
        }
        incidentlocation.feed(incidentlocation_fields)
        # reading
        reading = a1_48.reading()
        reading_fields = {
            'readingdate': '2018-09-21',
            'readingvalue': '4.89',
        }
        reading.feed(reading_fields)
        # incident
        incident = a1_48.incident()
        incident_fields = {
            'incidentdate': '2018-09-21',
        }
        incident.feed(incident_fields)
        # client
        client = a1_48.client()
        # document
        document = a1_48.document()
        document_fields = {
            'documenttype': '01',
            'documentnum': 'ES11111111T',
        }
        document.feed(document_fields)
        # name
        name = a1_48.cname()
        name_fields = {
            'firstname': 'nom',
            'familyname1': 'cognom',
            'familyname2': 'cognom 2',
        }
        name.feed(name_fields)
        # telephone
        telephone = a1_48.telephone()
        telephone_fields = {
            'telephoneprefix': '34',
            'telephonenumber': '999111222',
        }
        telephone.feed(telephone_fields)
        # clientAddress
        clientAddress = a1_48.clientAddress()
        clientAddress_fields = {
            'province': '01',
            'city': '000001',
            'zipcode': '16001',
            'streettype': 'ACCE',
            'street': 'inventat',
            'streetnumber': '4_ce',
            'portal': '5_TE2',
            'staircase': '5_mIh',
            'floor': '5_e6A',
            'door': '5_40T',
        }
        clientAddress.feed(clientAddress_fields)
        client_fields = {
            'document': document,
            'titulartype': 'F',
            'cname': name,
            'telephone': telephone,
            'email': 'a@a',
            'clientAddress': clientAddress,
        }
        client.feed(client_fields)
        claimreference_fields = {
            'wrongattentiontype': '01',
            'comreferencenum': '0000001',
            'targetclaimcomreferencenum': '9999998',
            'conceptcontract': '01',
            'conceptfacturation': '02',
            'contact': contact,
            'nnssexpedient': '45666666',
            'fraudrecordnum': '888888888',
            'incidentperiod': incidentperiod,
            'invoicenumber': 'F5555',
            'incidentlocation': incidentlocation,
            'reading': reading,
            'incident': incident,
            'client': client,
            'claimedcompensation': '520176666.24',
            'iban': 'ES0000000000000000000000000000000',
        }
        claimreference.feed(claimreference_fields)
        claimreferencelist = a1_48.claimreferencelist()
        claimreference_fields = {
            'claimreference_list': [claimreference],
        }
        claimreferencelist.feed(claimreference_fields)

        # Registerdoclist
        rd1 = a1_44.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-02',
            'doctype': 'CC',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': '404 page not found'
        }
        rd1.feed(registro_doc_fields)
        rd2 = a1_05.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-03',
            'doctype': '01',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': 'Comments'
        }
        rd2.feed(registro_doc_fields)
        registerdoclist = a1_48.Registerdoclist()
        registerdoclist_fields = {
            'registerdoclist': [rd1, rd2],
        }
        registerdoclist.feed(registerdoclist_fields)

        # variableinf
        variableinf_list = []
        variableinf = a1_48.variableinf()
        variableinf_fields = {
            'moreinformationtype': '01',
            'description': 'desc',
            'variabletype': '01',
            'variablevalue': 'val',
        }
        variableinf.feed(variableinf_fields)
        variableinf_list.append(variableinf)

        variableinflist = a1_48.variableinflist()
        variableinflist.feed({'variableinf_list': variableinf_list})

        a2648_fields = {
            'reqdate': '2018-05-01',
            'reqhour': '13:00:00',
            'comreferencenum': '000123456789',
            'claimtype': '01',
            'claimsubtype': '001',
            'originreference': 'AB999888',
            'claimreferencelist': claimreferencelist,
            'cups': 'ES1234000000000001JN',
            'legallimitdate': '2018-09-21',
            'priority': '1',
            'extrainfo': 'comentarios extra',
            'registerdoclist': registerdoclist,
            'reqcode': '7777',
            'sequential': '01',
            'informationdate': '2018-09-24',
            'informationtype': '01',
            'variableinflist': variableinflist,
        }
        a2648.feed(a2648_fields)
        mensaje.feed({
            'heading': heading,
            'a26': a2648,
        })
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_a2648.read())


class test_A1_46(unittest.TestCase):

    def setUp(self):
        self.xml_a146 = open(get_data("a146.xml"), "r")

    def tearDown(self):
        self.xml_a146.close()

    def test_create_a146(self):
        # A146
        mensaje = a1_46.MensajeA146()
        heading = a1_46.Heading()
        heading_fields = {
            'dispatchingcode': 'GML',
            'dispatchingcompany': '1234',
            'destinycompany': '4321',
            'communicationsdate': '2018-05-01',
            'communicationshour': '12:00:00',
            'processcode': '46',
            'messagetype': 'A1'
        }
        heading.feed(heading_fields)
        a146 = a1_46.A146()

        # Registerdoclist
        rd1 = a1_44.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-02',
            'doctype': 'CC',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': '404 page not found'
        }
        rd1.feed(registro_doc_fields)
        rd2 = a1_05.Registerdoc()
        registro_doc_fields = {
            'date': '2018-05-03',
            'doctype': '01',
            'url': 'http://www.gasalmatalas.com',
            'extrainfo': 'Comments'
        }
        rd2.feed(registro_doc_fields)
        registerdoclist = a1_46.Registerdoclist()
        registerdoclist_fields = {
            'registerdoclist': [rd1, rd2],
        }
        registerdoclist.feed(registerdoclist_fields)

        a146_fields = {
            'reqdate': '2018-05-01',
            'reqhour': '13:00:00',
            'comreferencenum': '000123456789',
            'cups': 'ES1234000000000001JN',
            'operationtype': 'A20002',
            'extrainfo': 'comentarios extra',
            'registerdoclist': registerdoclist,
        }
        a146.feed(a146_fields)
        mensaje_a146_fields = {
            'heading': heading,
            'a1': a146,
        }
        mensaje.feed(mensaje_a146_fields)
        mensaje.build_tree()
        xml = str(mensaje)
        assertXmlEqual(xml, self.xml_a146.read())
