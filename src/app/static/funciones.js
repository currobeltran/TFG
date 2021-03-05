$(document).ready(function(){
    $('#selecciontipo').change(function(){
        let value = $(this).val()

        $.ajax({
            url: "api/buscarBBDD",
            type: "GET",
            data: {tipo: value},
            success: function(data){
                let lista = '<option value="nuevo">Crear nuevo elemento</option>'
                $.each(data, function(i,v){
                    lista += `
                        <option value=${v.id}>${v.nombre}</option>
                    `
                })
                $('#seleccionobjeto').html(lista)
            }
        })
    })

})