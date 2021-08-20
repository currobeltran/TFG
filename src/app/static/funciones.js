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

    $('#seleccionsemestre').change(function(){
        let value = $(this).val()
        
        $.ajax({
            url: "api/buscarAsignaturaSemestre",
            type: "GET",
            data: {semestre: value},
            success:function(data){
                let lista = ''
                $.each(data,function(i,v){
                    lista += `
                        <li class="check-group-item">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value=${v.PK} id=${v.PK} name="asignaturas[]">
                                <label class="form-check-label" for=${v.PK}>
                                    ${v.Nombre}
                                </label>
                            </div>
                        </li>
                    `
                })
                $("#listaAsignaturasPrediccion").html(lista)
            }
        })
    })
})