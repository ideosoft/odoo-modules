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
        
        var calendario = $('#ideocalendar_vacaciones');
        
        if(calendario.length > 0) {
            
            if(calendario.attr('data-ok'))
                return;
            
            calendario.attr('data-ok', true);
            
            // Oculto la 'x' de la ventana del calendario para que cambie la url (id de empleado)
            $('button.close').css('display', 'none');
            
            // Obtengo los dias de vacaciones del usuario para este contrato
            if(!existsId) {
                
                var employee_id = getEmployeeIdFromUrl();
                if(employee_id) {
                    existsId = true;
                }
                
                var model = new openerp.Model('hr.employee.ideocalendar');
                model.call('getVacations', [employee_id])
				.then(function(result) {
                    
                    init();
                    
                    $('#contract input').val(result['contract_id']);
                    
                    var vacations = result['vacations'];
                    for(var i=0; i < vacations.length; i++) {
                        key = vacations[i]['date'];
                        DIAS[key] = vacations[i];

                        str_dias.push(vacations[i]['date'] + vacations[i]['type']);
					}
                    
                    var festivosc = result['festivosc'];
                    for(var i=0; i < festivosc.length; i++) {
                        FCONVENIO[festivosc[i]] = festivosc[i];
                    }
                    
                    var festivosg = result['generales'];
                    for(var i=0; i < festivosg.length; i++) {
                        FGENERALES[festivosg[i]['date']] = festivosg[i];
                    }

                    calendario.datepicker( "option", "beforeShowDay", setStyle );
                    $('#string_dates input').val(str_dias);

                });
                
            }
            
            // Actualizo los días solicitados, restantes...
            model.call('getDataDays', [employee_id])
            .then(function(result) {
                console.log(result);
                $('#convenio_days span').html(result.convenio_days);
                $('#personal_days span').html(result.personal_days);
                $('#annual_days span').html(result.annual_days);
                $('#previous_year_days span').html(result.previous_year_days.toFixed(2));
                $('#requested_days span').html(result.requested_days.toFixed(2));
                $('#hanging_days span').html(result.hanging_days.toFixed(2));
                
                $('#previous_days input').val(result.previous_year_days.toFixed(2));
            });
            
            $.datepicker.setDefaults($.datepicker.regional['es']);
            
            // No muestro el input de tipo texto
            $('#datepicker').css('display', 'none');
            

            calendario.datepicker({
                numberOfMonths: [3, 4],
                minDate: new Date('01/01/'+year.toString().substr(2,2)),
                maxDate: new Date('31/12/'+year.toString().substr(2,2)),
                beforeShowDay: setStyle,
                onSelect: function (date) {

                    // compruebo si es sabado o domingo y si se permite seleccionar
                    var date_date = $(this).datepicker('getDate');
                    var dayOfWeek = date_date.getUTCDay();    
                    switch(dayOfWeek) {
                        case 5: // sabados
                            if( !$('input[name="allow_saturdays"]').is(':checked')) return;
                            break;
                        case 6: // domingos
                            if( !$('input[name="allow_sundays"]').is(':checked')) return;
                            break;
                    }
                    
                    // compruebo si es festivo y si se permite seleccionar
                    if(FCONVENIO[date] || FGENERALES[date]) {
                        if (!$('input[name="allow_holidays"]').is(':checked')) return;
                    }
                    checkDay(date);
                    
                    $('#string_dates input').val(str_dias);
                    
                    // Actualizo los días solicitados, restantes...
                    model.call('getDataDays', [employee_id, aux])
                    .then(function(result) {
                        $('#convenio_days span').html(result.convenio_days);
                        $('#annual_days span').html(result.annual_days);
                        $('#personal_days span').html(result.personal_days);
                        $('#previous_year_days span').html(result.previous_year_days.toFixed(2));
                        $('#requested_days span').html(result.requested_days.toFixed(2));
                        $('#hanging_days span').html(result.hanging_days.toFixed(2));
                        
                        $('#previous_days input').val(result.previous_year_days.toFixed(2));
                    });

                },
            });
            
            $('.type_legend .btn').click(function(e){
                type = e.target.classList[1];
                $('.type_legend .selected').removeClass('selected');
                $('.'+type).addClass('selected');
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
            init();
        }
    }
    , 500);

    
    function init() {
        DIAS = [];
        FCONVENIO = [];
        FGENERALES = [];
        str_dias = [];
        contract_id = {};
        type = 'c';
        year = new Date().getFullYear();
        aux = 0;
    }
    
    // Get id from url
    function getEmployeeIdFromUrl() {
        var url = window.location.href;
        var start = url.indexOf('id=') + 3;
        var auxUrl = url.substr(start);
        var end = auxUrl.indexOf('&');
        var id = url.substr(start, end);
        return id;
    }
    
    function refreshCalendar(num) {
        $('#ideocalendar_vacaciones').datepicker('option', 'minDate', new Date('01/01/'+(parseInt(year.toString().substr(2,2))).toString()));
        $('#ideocalendar_vacaciones').datepicker('option', 'maxDate', new Date('31/12/'+(parseInt(year.toString().substr(2,2))).toString()));
        $('#ideocalendar_vacaciones').datepicker('refresh');
    }
    
    function _type2class(type) {
        var classes = [];
        classes['c'] = 'COMPLETO';
        classes['m'] = 'MAÑANA';
        classes['t'] = 'TARDE';
              
        return classes[type];
    }
    
    function _type2number(type) {
        var numbers = [];
        numbers['c'] = 1;
        numbers['m'] = 0.666666666;
        numbers['t'] = 0.333333333;
              
        return numbers[type];
    }
    
    function setStyle(date) {
        date_day = ("0" + date.getDate()).slice(-2);
        date_month = ("0" + (date.getMonth() + 1).toString()).slice(-2);
        date_year = date.getFullYear();
        
        strDate = (date_day + "/" + date_month + "/" + date_year).toString();
                
        if(DIAS[strDate]) {
            d = DIAS[strDate];
            if(FCONVENIO[strDate]) return [true, d['type'] + '-fc', _type2class(d['type'])];
            if(FGENERALES[strDate]) return [true, d['type'] + '-fg', _type2class(d['type']) + ' / ' + FGENERALES[strDate]['desc']];
            return [true, d['type'], _type2class(d['type'])];
        }
        else if(FCONVENIO[strDate]) return [true, 'fc', 'FESTIVO CONVENIO'];
        else if(FGENERALES[strDate]) return [true, 'fg', FGENERALES[strDate]['desc']];
        else return [true, ''];
    }
    
    function setDay(date) {         
        var newDay = [];
        newDay['date'] = date;
        newDay['type'] = type;
        DIAS[date] = newDay;
    }
    
    function checkDay(date) {
        if(DIAS[date]) {
            for(var i = 0; i < str_dias.length; i++) {
                if(str_dias[i].substr(0,10) === date) {
                    type_to_delete = str_dias[i].substr(10,1);
                    aux = aux - _type2number(type_to_delete);
                    str_dias.splice(i,1);
                    delete DIAS[date];
               
                    if(type !== 'd') {
                        setDay(date);
                        str_dias.push((date + type).toString());
                        aux = aux + _type2number(type);
                    }
                }
            }
        } else if(type !== 'd') {
            setDay(date);
            strDate = (date + type).toString();
            aux = aux + _type2number(type);
            str_dias.push(strDate);
        }
    }

});
