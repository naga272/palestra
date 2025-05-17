
/*
prossimamente è da inserire in questo modo
var name_sections_topbar = [
    "HomePage", 
    // "Forum", 
    "Library"
];
*/


var name_sections_topbar = [
    "HomePage", 
    "Library"
];


function init_page(name_page, comeback)
{
    /*
    * @name_page: str -> Titolo pagina 
    * @comeback: str  -> link pagina di ritorno (se l'argomento alla chiamata init_page non viene descritto, comeback sarà undefined: es init_page("Titolo pagina")) 
    * Generatore automatico di topbar per ogni pagine del sito web
    */
    head(name_page);
    topbar(name_page, comeback);
    $("main").css("background-color", "#fff");
    return ;
}


function head(name_page)
{
    /*
    * @name_page: str -> Titolo pagina 
    * setting head section for all the web page
    */
    $("head").append("<link rel=\"icon\" type=\"image/x-icon\" href=\"https://scaling.spaggiari.eu/VRIT0007/favicon/5223.png&rs=%2FtccTw2MgxYfdxRYmYOB6AaWDwig7Mjl0zrQBslusFLrgln8v1dFB63p5qTp4dENr3DeAajXnV%2F15HyhNhRR%2FG8iNdqZaJxyUtaPePHkjhBWQioJKGUGZCYSU7n9vRa%2FmjC9hNCI%2BhCFdoBQkMOnT4UzIQUf8IQ%2B8Qm0waioy5M%3D\"></link>"); // icon website
    $("head").append("<title>" + name_page + "</title>");
    $("head").append("<meta charset='utf-8'>");
    $("head").append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>");
    $("head").append("<meta name='author' content='Bastianello Federico'>");
    $("head").append("<meta name='KeyWords' content='forum marconi verona'>");
    return ;
}


function topbar(name_page, comeback)
{
    /*
    * @name_page: str -> Titolo pagina 
    * @comeback: str  -> link pagina di ritorno (se l'argomento alla chiamata init_page non viene descritto, comeback sarà undefined: es init_page("Titolo pagina")) 
    * Generatore automatico di topbar per ogni pagina del sito web
    */
    $("body").prepend("<header></header>");
    $("header").append("<div class='topbar'></div>");
    $(".topbar").append("<h2>" + name_page + "</h2>");
    $(".topbar").append("<div class='section'></div>");

    $(".section").append("<a href='/desktop'>" + name_sections_topbar[0] + "</a>");
    //$(".section").append("<a href='/forum'>" + name_sections_topbar[1] + "</a>");
    $(".section").append("<a href='/library'>" + name_sections_topbar[1] + "</a>");


    // per i dispositivi con una lunghezza < di 980 non mostro alcune opzioni della topbar
    if(name_sections_topbar[2] != undefined && comeback != undefined && window.innerWidth >= 980)
        $(".section").append("<a href='" + comeback +"'>" + name_sections_topbar[2] + "</a>");

    return ;
}


function add_partecipante(link, image, nome, nomesito)
{
    /*
    * @link:str          link per info sul partecipante
    * @image:str         immagine del sito che dipende dal sito che porta al link
    * @nome:str          nome partecipante
    * @nomesito:str      inserire il nome del sito
    * 
    * Funzione che una volta chiamata aggiunge in automatico il partecipante (all'interno del readme nella homepage)
    */ 
    return `
        <span>
            <a href="${link}" style="color:#333">
                ${nome} <img src="${image}" alt="${nomesito}" width="15px" height="auto">
            </a>
        <span>
        `;
}


// è ancora in fase di sperimentazione
function copySourceCode(str_to_copy) 
{
    // al click di un qualcosa viene copiato negli appunti la stringa passata come parametro
    if (navigator.clipboard) {
        navigator.clipboard.writeText(str_to_copy)
            .then(() => {
                console.log('Testo copiato negli appunti');
                alert('Testo copiato negli appunti');
            })
            .catch(err => {
                console.error('Errore durante la copia del testo: ', err);
                alert('Errore durante la copia del testo');
            });
    } else {
        // Fallback per browser che non supportano navigator.clipboard
        stringaCodeElement.select();
        document.execCommand('copy');
        console.log('Testo copiato utilizzando execCommand');
        alert('Testo copiato negli appunti (metodo fallback)');
    }
    return ;
}
