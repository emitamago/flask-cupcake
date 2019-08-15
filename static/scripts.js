const BASE_API_URL = "http://localhost:5000"


$(document).ready( async function() {
    // on page load, make AJAX request to get all cupcake and add to DOM
    let response = await axios.get(`${BASE_API_URL}/cupcakes`);

    for (i = 0; i < response.data.cupcakes.length; i ++){
        $("#cupcakes-list").append(createHTML(response.data.cupcakes[i]))
    }
})


$("#cupcake-form").on('submit', async function(evt){
    // on submit, take user's input and make AJAX post request and append newly created cupcapke into DOM
    evt.preventDefault()
    let flavor = $("#flavor").val()
    let size = $("#size").val()
    let rating = $("#rating").val()
    let image = $("#image").val()
    let response = await axios.post('/cupcakes', {
                                'flavor': flavor,
                                'size': size,
                                'rating': rating,
                                'image' : image
                            })
   
    $("#cupcakes-list").append(createHTML(response.data.cupcake)) 

})

function createHTML(cupcake){
    //create html for a cupcake
  return    `<div class="d-inline-block mr-5">
                <img src="${cupcake.image}" height=200 width=200>
                <p>${cupcake.flavor}</p>
                <p>${cupcake.size}</p>
                <p>${cupcake.rating}</p>
            </div>`    
}