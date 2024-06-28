let tenicos=[]

function listarTecnico() {
    let url = "/listarTecnicos/"
    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    })
        .then(respuesta => respuesta.json())
        .then(resultado => {
            tecnicos = JSON.parse(resultado.tecnicos)
            console.log(tecnicos)
        })
        .catch(error => {
            console.error(error)
        })

}
    
function agregarIdCaso(id) {
    document.getElementById('idCaso').value = id
}