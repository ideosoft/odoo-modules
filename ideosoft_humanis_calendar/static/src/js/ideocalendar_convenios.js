$(function() {
    
    // "use strict";
    
    // Initial data for calendar
    $.datepicker.regional['es'] = {
        closeText: 'Cerrar',
        prevText: '<Ant',
        nextText: 'Sig>',
        currentText: 'Hoy',
        monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        monthNamesShort: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep', 'Oct','Nov','Dic'],
        dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
        dayNamesShort: ['Dom','Lun','Mar','Mié','Juv','Vie','Sáb'],
        dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','Sá'],
        weekHeader: 'Sm',
        dateFormat: 'dd/mm/yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: ''
    };
    
    init();
    
    var existsId = false;
    
    
    var interv = setInterval(function(){
        
        var calendario = $('#ideocalendar_convenios');
        
        if(calendario.length > 0) {
            
            if(calendario.attr('data-ok'))
                return;
            
            calendario.attr('data-ok', true);
            
            // Oculto la 'x' de la ventana del calendario para que cambie la url (id de convenio)
            $('button.close').css('display', 'none');
            
            if(!existsId) {
                
                var convenio_id = getConvenioIdFromUrl();
                if(convenio_id) {
                    existsId = true;
                }
                
                var model = new openerp.Model('hr.employee.ideocalendar');
                model.call('getFestivosconvenio', [convenio_id])
				.then(function(result) {
                    
                    init();
                    
                    var diasGenerales = result['generales'];
                    for(var i=0; i < diasGenerales.length; i++) {
                        GENERALES[diasGenerales[i]['date']] = diasGenerales[i];
					}
                    
                    var festivosc = result['festivosc'];
                    for(var i=0; i < festivosc.length; i++) {
                        FESTIVOS[festivosc[i]] = festivosc[i];
                        str_fest.push(festivosc[i]);
                    }

                    $('#ideocalendar_convenios').datepicker( "option", "beforeShowDay", setStyle );
                    $('#string_dates input').val(str_fest);
                    $('#aux_convenio input').val(convenio_id);
  
                });
            }
            
           
            $.datepicker.setDefaults($.datepicker.regional['es']);
            
            // No muestro el input de tipo texto
            $('#datepicker').css('display', 'none');
            

            $('#ideocalendar_convenios').datepicker({
                numberOfMonths: [3, 4],
                minDate: new Date('01/01/'+year.toString().substr(2,2)),
                maxDate: new Date('31/12/'+year.toString().substr(2,2)),
                beforeShowDay: setStyle,
                onSelect: function (date) {
                    
                    // compruebo si es festivo general y si se permite seleccionar
                    if(GENERALES[date]) {
                        if (!$('input[name="allow_generals"]').is(':checked')) return;
                    }
                    checkDay(date);
                    
                    $('#string_dates input').val(str_fest);
                    console.log(str_fest);
                },
            });
            
            $('.btn-prev-next .prev').click(function(e) {
                year--;
                refreshCalendar();
            });
            
            $('.btn-prev-next .next').click(function(e) {
                year++;
                refreshCalendar();
            });
            
        } else {
            // Reinicializo variables por si se guardan nuevas vacaciones o se cambia de empleado
            existsId = false;
        }
    }
    , 500);
    
    
    function init() {
        GENERALES = [];
        FESTIVOS = [];
        str_fest = [];
        convenio_id = {};
        year = new Date().getFullYear();
    }   
    
    // Get id from url
    function getConvenioIdFromUrl() {
        var url = window.location.href;
        var start = url.indexOf('id=') + 3;
        var auxUrl = url.substr(start);
        var end = auxUrl.indexOf('&');
        var id = url.substr(start, end);
        return id;
    }
    
    function setStyle(date) {
        date_day = ("0" + date.getDate()).slice(-2);
        date_month = ("0" + (date.getMonth() + 1).toString()).slice(-2);
        date_year = date.getFullYear();
        
        strDate = (date_day + "/" + date_month + "/" + date_year).toString();
        
        if(GENERALES[strDate]) {
            if(FESTIVOS[strDate]) {
                return [true, 'g-fc', 'CONVENIO / ' + GENERALES[strDate]['desc']];
            } else {
                return [true, 'g', GENERALES[strDate]['desc']];
            }
        } else if(FESTIVOS[strDate]) {
            return [true, 'fc', 'FEST CONVENIO'];
        }
        return [true, ''];
    }
    
    function setDay(date) {         
        var newDay = [];
        newDay['date'] = date;
        newDay['type'] = type;
        FESTIVOS[date] = newDay;
    }
    
    function checkDay(date) {
        if(FESTIVOS[date]) {
            for(var i = 0; i < str_fest.length; i++) {
                if(str_fest[i] === date) {
                    str_fest.splice(i,1);
                    delete FESTIVOS[date];
                }
            }
        } else {
            setDay(date);
            strDate = date.toString();
            str_fest.push(strDate);
        }
    }
    
    function refreshCalendar(num) {
        $('#ideocalendar_convenios').datepicker('option', 'minDate', new Date('01/01/'+(parseInt(year.toString().substr(2,2))).toString()));
        $('#ideocalendar_convenios').datepicker('option', 'maxDate', new Date('31/12/'+(parseInt(year.toString().substr(2,2))).toString()));
        $('#ideocalendar_convenios').datepicker('refresh');
    }

});
