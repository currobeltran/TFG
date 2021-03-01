$(document).ready(function(){
    $('#selecciontipo').change(function(){
        let value = $(this).val()
        let search = "null"

        switch (value){
            case "Asignatura":
                search = "Asignatura" 
                break;
            case "Área":
                search = "Area"
                break;
            case "Título":
                search = "Titulo"
                break;
            case "Mención":
                search = "Mencion"
                break;
            case "Año Asignatura":
                search = "AñoAsignatura"
                break;
            case "Grupo":
                search = "Grupo"
                break;
        }

        $.ajax({
            // Aquí se realizaría una consulta a la base de datos a través de una nueva
            // ruta que debemos crear, y que dará acceso a realizar esta operación.
        })
    })

})