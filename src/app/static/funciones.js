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
        
        document.getElementById('eliminar').style.display = 'none';
    })

    $('#seleccionobjeto').change(function(){
        let value = $(this).val()

        if(value != "nuevo"){
            document.getElementById('eliminar').style.display = 'block';
        }
        else{
            document.getElementById('eliminar').style.display = 'none';
        }
    })

    $('#ayuda').click(function(){
        var elemento = document.getElementById("parrafoayuda")

        if(window.getComputedStyle(elemento).display === "none"){
            $('#parrafoayuda').show()
        }
        else{
            $('#parrafoayuda').hide()
        }
    })
})