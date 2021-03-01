$(document).ready(function(){
    $('#selecciontipo').change(function(){
        let value = $(this).val()

        $.ajax({
            url: "api/buscarBBDD",
            type: "GET",
            data: {tipo: value},
            success: function(data){
                let lista = ''
                $.each(data, function(i,v){
                    lista += `
                        <option>${v}</option>
                    `
                })
                $('#seleccionobjeto').html(lista)
            }
        })
    })

})