
function clean_dom()
{
    $("#id_consegna").text = "";
    $("#stato").text = "";
    $("#dataRitiro").text = "";
    $("#dataConsegna").text = "";
}


function set_error_message()
{
    $("#errorMessage").css({"display": "block"});
}


function panic()
{
    // questa funzione conterra' tutta la logica nel caso in cui non esiste la chiave
    clean_dom();
    set_error_message();
}


function get_api_content()
{
    /*
        // http://127.0.0.1:8000/tracking?chiaveConsegna=<chiave>

        if success:
        result = {
            "id_consegna": "<chiave>",
            "stato": <numero>,
            "dataRitiro": "<date>",
            "dataConsegna": <date|null>
        }

        else:

        response = {
            "errore": "non trovata"
        }
    */

    let key = document.getElementById("id_chiaveConsegna").value;
    
    console.log(key);
    $.getJSON("/tracking?chiaveConsegna=" + key, function (response) {
        console.log(response);

        if (response.errore) {
            panic();
            return;
        }

        $("#errorMessage").css({"display": "none"});
        $("#id_consegna").html(response.id_consegna);
        $("#stato").html(response.stato);
        $("#dataRitiro").html(response.dataRitiro);
        $("#dataConsegna").html(
            (response.dataConsegna == null)? "unknow" : response.dataConsegna
        );
    });
}
