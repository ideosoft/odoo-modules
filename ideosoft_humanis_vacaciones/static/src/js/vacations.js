$(function() {
      
    function adjustDecimals(val) {
        var dec = val.slice(-2);
        if(dec == '32' || dec == '65' || dec == '99') {
            if(val > 0) val = (parseFloat(val) + 0.01).toString();
            else        val = (parseFloat(val) - 0.01).toString();
        }
        if(dec == '34' || dec == '67' || dec == '01') {
            if(val > 0) val = (parseFloat(val) - 0.01).toString();
            else        val = (parseFloat(val) + 0.01).toString();
        }
        return val;
    }
    
    
    setInterval(function(){
        
        if($('#adjustDaysTable').length > 0) {
            
            if($('#adjustDaysTable').attr('data-ok'))
                return;
            $('#adjustDaysTable').attr('data-ok', true);
         
         
            $('#btnFullAddOne').click(function() {
                $('#adjustDays input')[0].value = (parseFloat($('#adjustDays input')[0].value) + 1).toFixed(2);
            });
            $('#btnFullRemoveOne').click(function() {
                $('#adjustDays input')[0].value = (parseFloat($('#adjustDays input')[0].value) - 1).toFixed(2);
            });
            $('#btnMorningAddOne').click(function() {
                var aux = (parseFloat($('#adjustDays input')[0].value) + 0.666666666).toFixed(2).toString();
                aux = adjustDecimals(aux);
                $('#adjustDays input')[0].value = parseFloat(aux);
            });
            $('#btnMorningRemoveOne').click(function() {
                var aux = (parseFloat($('#adjustDays input')[0].value) - 0.666666666).toFixed(2).toString();
                aux = adjustDecimals(aux);
                $('#adjustDays input')[0].value = parseFloat(aux);
            });
            $('#btnEveningAddOne').click(function() {
                var aux = (parseFloat($('#adjustDays input')[0].value) + 0.333333333).toFixed(2).toString();
                aux = adjustDecimals(aux);
                $('#adjustDays input')[0].value = parseFloat(aux);
            });
            $('#btnEveningRemoveOne').click(function() {
                var aux = (parseFloat($('#adjustDays input')[0].value) - 0.333333333).toFixed(2).toString();
                aux = adjustDecimals(aux);
                $('#adjustDays input')[0].value = parseFloat(aux);
            });
        }
        
    }, 500);
    
    
        

});