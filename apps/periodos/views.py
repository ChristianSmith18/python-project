from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from apps.periodos.forms import periodosForm, Seguimiento_cierreform, Seguimiento_abrirform, validacion_abrirform, valida_cierreform
from apps.periodos.models import Glo_Periodos, Glo_Seguimiento, Glo_validacion
from apps.controlador.models import Ges_Controlador
from apps.jefaturas.models import Ges_Jefatura
from apps.estado_seguimiento.models import Glo_EstadoSeguimiento

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.db.models.deletion import ProtectedError
from django.core.mail import EmailMessage,send_mass_mail

from django.db.models import Q
from datetime import date
from datetime import datetime
from django.utils import timezone
# Create your views here.


class PeriodosList(ListView):
    model = Glo_Periodos
    template_name = 'periodos/periodo_list.html'


class PeriodosCreate(SuccessMessageMixin, CreateView):
    model = Glo_Periodos
    form_class = periodosForm
    template_name = 'periodos/periodo_form.html'


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            form.instance.fecha_inicio= date.today()
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron creados correctamente!")
            return HttpResponseRedirect('/periodos/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha creado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar')



class PeriodosEdit(SuccessMessageMixin, UpdateView ):
    model = Glo_Periodos
    form_class = periodosForm
    template_name = 'periodos/periodo_form.html'

    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        id_periodo = kwargs['pk']
        instancia_nivel = self.model.objects.get(id=id_periodo)
        form = self.form_class(request.POST, instance=instancia_nivel)

        if form.is_valid():
            form.save()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "Los datos fueron actualizados correctamente!" )
            return HttpResponseRedirect('/periodos/listar')
        else:
            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha actualizado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar')


class PeriodosDelete(SuccessMessageMixin, DeleteView ):
    model = Glo_Periodos
    template_name = 'periodos/periodo_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
            request.session['message_class'] = "alert alert-success"
            messages.success(self.request, "El registro fue eliminado correctamente!")
            return HttpResponseRedirect('/periodos/listar')

        except ProtectedError as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error de integridad: Este nivel posee subniveles los que deben ser borrados antes de borrar este nivel.")
            return HttpResponseRedirect('/periodos/listar')

        except Exception  as e:
            request.session['message_class'] = "alert alert-danger"
            messages.error(request, "Error interno: No se ha eliminado el registro. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar')




class SeguimientoList(ListView):
    model = Glo_Seguimiento
    template_name = 'periodos/seguimiento_list.html'



    def get_context_data(self, **kwargs):
        context = super(SeguimientoList, self).get_context_data(**kwargs)
        #id_usuario_actual = self.request.user.id  # obtiene id usuario actual
        self.request.session['id_periodo']=self.kwargs['pk'] #guarda id  controlador


        queryset= Glo_Seguimiento.objects.filter(id_periodo=self.kwargs['pk'])


        context['object_list'] = queryset
        context['periodo'] = PeriodoActual()




        return context


class SeguimientoCerrarPeriodo(UpdateView):
    model = Glo_Seguimiento
    template_name = 'periodos/seguimiento_cerrar.html'
    form_class = Seguimiento_cierreform

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        instancia = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=instancia)

        id_nuevo_estado= Glo_EstadoSeguimiento.objects.get(id=2)

        id_periodo=self.request.session['id_periodo']

        if form.is_valid():

            form.instance.id_estado_seguimiento=id_nuevo_estado
            form.instance.fecha_termino= datetime.now(tz=timezone.utc)

            form.save()

            try:

                EnviarCorreoCierreSeguimiento()

                request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                messages.success(request, "La etapa de seguimiento fue cerrada y se le ha enviado un correo a las jefaturas que formulan.!")  # mensaje
                return HttpResponseRedirect('/periodos/listar_seguimiento/' + str(id_periodo))  # Redirije a la pantalla principal

            except:

                 request.session['message_class'] = "alert alert-warning" #Tipo mensaje
                 messages.success(request, "La etapa de seguimiento fue cerrada correctamente!, pero el servicio de correo tuvo un inconveniente favor comuníquese con las jefaturas que formulan para informar el cierre de esta etapa.") # mensaje
                 return HttpResponseRedirect('/periodos/listar_seguimiento/' + str(id_periodo)) # Redirije a la pantalla principal

        else:

            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha cerrado la etapa de seguimiento. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar_seguimiento' + str(id_periodo))



class SeguimientoAbrirPeriodo(SuccessMessageMixin, CreateView):
    model = Glo_Seguimiento
    template_name = 'periodos/seguimiento_abrir.html'
    form_class = Seguimiento_abrirform


    def get_context_data(self, **kwargs):
        context = super(SeguimientoAbrirPeriodo, self).get_context_data(**kwargs)

        try:
             estado= Glo_Seguimiento.objects.get(Q(id_estado_seguimiento=1) & Q(id_periodo=PeriodoActual()))
        except Glo_Seguimiento.DoesNotExist:
             estado = 0

        try:
             estadoValida= Glo_validacion.objects.get(Q(id_estado_periodo=1) & Q(id_periodo=PeriodoActual()))
        except Glo_validacion.DoesNotExist:
             estadoValida = 0

        try:
            planes_no_aprobados= Ges_Controlador.objects.filter(Q(id_periodo=PeriodoActual()) & (~Q(estado_flujo_id=7) & ~Q(estado_flujo_id=2))).count()
        except Ges_Controlador.DoesNotExist:
            planes_no_aprobados = 0

        context["estado_seguimiento"] = {'estadoValida': estadoValida, 'estado_seguimiento': estado, 'planes_no_aprobados':planes_no_aprobados}
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)


        id_nuevo_estado= Glo_EstadoSeguimiento.objects.get(id=1)
        periodo_actual = Glo_Periodos.objects.get(id_estado=1)

        id_periodo=self.request.session['id_periodo']

        if form.is_valid():
            form.instance.id_periodo= periodo_actual
            form.instance.id_estado_seguimiento=id_nuevo_estado
            form.instance.fecha_inicio= datetime.now(tz=timezone.utc)

            form.save()

            try:
                Ges_Controlador.objects.filter(id_periodo=PeriodoActual()).update(id_estado_plan=1)
                EnviarCorreoAbrirSeguimiento()

                request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                messages.success(request, "El periodo de seguimiento fue abierto correctamente! y se ha enviado un correo a las jefaturas que formulan!")  # mensaje
                return HttpResponseRedirect('/periodos/listar_seguimiento/' + str(id_periodo))  # Redirije a la pantalla principal

            except:

                 request.session['message_class'] = "alert alert-warning" #Tipo mensaje
                 messages.success(request, "El periodo de seguimiento fue abierto correctamente!, pero el servicio de correo tuvo un inconveniente favor comuníquese con la jefatura directa para informar de la apertura.") # mensaje
                 return HttpResponseRedirect('/periodos/listar_seguimiento/' + str(id_periodo)) # Redirije a la pantalla principal

        else:

            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha abierto la etapa de seguimiento. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar_seguimiento/' + str(id_periodo))

class ValidacionCerrarPeriodo(UpdateView):
    model = Glo_validacion
    template_name = 'periodos/validacion_cerrar.html'
    form_class = valida_cierreform

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        instancia = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, instance=instancia)

        id_nuevo_estado= Glo_EstadoSeguimiento.objects.get(id=2)

        id_periodo=self.request.session['id_periodo']

        if form.is_valid():

            form.instance.id_estado_periodo=id_nuevo_estado
            #form.instance.fecha_termino= datetime.now(tz=timezone.utc)

            form.save()

            try:

                #EnviarCorreoCierre()
                EnviarCorreoCierreValidacion()

                request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                messages.success(request, "La etapa de validación fue cerrada y se le ha enviado un correo a las jefaturas que formulan.!")  # mensaje
                return HttpResponseRedirect('/periodos/listar_validacion/' + str(id_periodo))  # Redirije a la pantalla principal

            except:

                 request.session['message_class'] = "alert alert-warning" #Tipo mensaje
                 messages.success(request, "La etapa de validación fue cerrada correctamente!, pero el servicio de correo tuvo un inconveniente favor comuníquese con las jefaturas que formulan para informar el cierre de esta etapa.") # mensaje
                 return HttpResponseRedirect('/periodos/listar_validacion/' + str(id_periodo)) # Redirije a la pantalla principal

        else:

            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha cerrado la etapa de validación. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar_validacion/' + str(id_periodo))


class ValidacionList(ListView):
    model = Glo_validacion
    template_name = 'periodos/validacion_list.html'

    def get_context_data(self, **kwargs):
        context = super(ValidacionList, self).get_context_data(**kwargs)
        #id_usuario_actual = self.request.user.id  # obtiene id usuario actual
        self.request.session['id_periodo']=self.kwargs['pk'] #guarda id  controlador


        queryset= Glo_validacion.objects.filter(id_periodo=self.kwargs['pk']).order_by('-id')


        context['object_list'] = queryset
        context['periodo'] = PeriodoActual()




        return context

class ValidacionAbrirPeriodo(SuccessMessageMixin, CreateView):
    model = Glo_validacion
    template_name = 'periodos/validacion_abrir.html'
    form_class = validacion_abrirform


    def get_context_data(self, **kwargs):
        context = super(ValidacionAbrirPeriodo, self).get_context_data(**kwargs)

        try:
             estadoValida= Glo_validacion.objects.get(Q(id_estado_periodo=1) & Q(id_periodo=PeriodoActual()))
        except Glo_validacion.DoesNotExist:
             estadoValida = 0

        try:
            estadoSeguimiento = Glo_Seguimiento.objects.get(Q(id_estado_seguimiento=1) & Q(id_periodo=PeriodoActual()))
        except Glo_Seguimiento.DoesNotExist:
            estadoSeguimiento = 0

        context["estado_seguimiento"] = {'estadoValida': estadoValida, 'estado_seguimiento': estadoSeguimiento}

        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)


        id_nuevo_estado= Glo_EstadoSeguimiento.objects.get(id=1)
        periodo_actual = Glo_Periodos.objects.get(id_estado=1)

        id_periodo=self.request.session['id_periodo']

        if form.is_valid():
            form.instance.id_periodo= periodo_actual
            form.instance.id_estado_periodo=id_nuevo_estado
            form.instance.fecha_inicio= datetime.now(tz=timezone.utc)

            form.save()

            try:

                EnviarCorreoAbrirValidacion()

                request.session['message_class'] = "alert alert-success"  # Tipo mensaje
                messages.success(request, "El periodo de validación fue abierto correctamente! y se ha enviado un correo a las jefaturas que formulan!")  # mensaje
                return HttpResponseRedirect('/periodos/listar_validacion/' + str(id_periodo))  # Redirije a la pantalla principal

            except:

                 request.session['message_class'] = "alert alert-warning" #Tipo mensaje
                 messages.success(request, "El periodo de validación fue abierto correctamente!, pero el servicio de correo tuvo un inconveniente favor comuníquese con la jefatura directa para informar de la apertura.") # mensaje
                 return HttpResponseRedirect('/periodos/listar_validacion/' + str(id_periodo)) # Redirije a la pantalla principal

        else:

            request.session['message_class'] = "alert alert-danger"
            messages.error(self.request, "Error interno: No se ha abierto la etapa de validación. Comuníquese con el administrador.")
            return HttpResponseRedirect('/periodos/listar_validacion/' + str(id_periodo))


def PeriodoActual():

    try:
        periodo_actual = Glo_Periodos.objects.get(id_estado=1)
    except Glo_Periodos.DoesNotExist:
        return None
    return periodo_actual


def EnviarCorreoCierreValidacion():

    controladorPlan = Ges_Jefatura.objects.values_list('id_user__email' , flat=True).filter(id_periodo=PeriodoActual())

    ahora = datetime.now()
    fecha = ahora.strftime("%d" + " de " + "%B" + " de " + "%Y")

    idcorreoJefatura=list(controladorPlan)

    subject = 'Cierre etapa Validación'
    messageHtml = '<b>Estimada(o) Usuaria(o) del Sistema Capacity Institucional</b> ,<br> Le informamos que con fecha  '+ str(fecha) +', el proceso de <b>Validación</B> ha sido cerrado. <br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)
    email.content_subtype='html'
    email.send()


def EnviarCorreoCierreSeguimiento():

    controladorPlan = Ges_Jefatura.objects.values_list('id_user__email' , flat=True).filter(id_periodo=PeriodoActual())

    ahora = datetime.now()
    fecha = ahora.strftime("%d" + " de " + "%B" + " de " + "%Y")

    idcorreoJefatura=list(controladorPlan)

    subject = 'Cierre etapa Seguimiento'
    messageHtml = '<b>Estimada(o) Usuaria(o) del Sistema Capacity Institucional</b> ,<br> Le informamos que con fecha  '+ str(fecha) +', el proceso de <b>seguimiento</B> ha sido cerrado. <br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)
    email.content_subtype='html'
    email.send()



def EnviarCorreoAbrirValidacion():



    controladorPlan = Ges_Jefatura.objects.values_list('id_user__email', flat=True).filter(
        id_periodo=PeriodoActual())

    ahora = datetime.now()
    fecha = ahora.strftime("%d" + " de " + "%B" + " de " + "%Y")

    idcorreoJefatura=list(controladorPlan)

    subject = 'Apertura etapa Validación'
    messageHtml = '<b>Estimada(o) Usuaria(o) del Sistema Capacity Institucional</b> ,<br> Le informamos que con fecha  '+ str(fecha) +', el proceso de <b>VALIDACIÓN</B> ha sido abierto para que valide las actividades reportadas por el equipo. <br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)
    email.content_subtype='html'
    email.send()


def EnviarCorreoAbrirSeguimiento():



    controladorPlan = Ges_Jefatura.objects.values_list('id_user__email', flat=True).filter(
        id_periodo=PeriodoActual())

    ahora = datetime.now()
    fecha = ahora.strftime("%d" + " de " + "%B" + " de " + "%Y")

    idcorreoJefatura=list(controladorPlan)

    subject = 'Apertura etapa Seguimiento'
    messageHtml = '<b>Estimada(o) Usuaria(o) del Sistema Capacity Institucional</b> ,<br> Le informamos que con fecha  '+ str(fecha) +', el proceso de <b>Seguimiento</B> ha sido abierto para que reporte el avance de sus actividades. <br><p style="font-size:12px;color:red;">correo generado automaticamente favor no responder.'

    email = EmailMessage(subject, messageHtml ,to=idcorreoJefatura)
    email.content_subtype='html'
    email.send()

