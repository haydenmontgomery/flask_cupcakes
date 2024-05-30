$(document).ready(function(){
    const $list = $("#cupcake-list");

    getCupcakes($list)
})

    async function getCupcakes($list) {

    res = await axios.get('/api/cupcakes');
    console.log(res.data.cupcakes)
    for (let i = 0; i < res.data.cupcakes.length; i++) {
        const li = document.createElement("li");
        const img = document.createElement("img");
        img.src = await res.data.cupcakes[i].image;
        img.loading = "lazy"
        li.innerText = `Flavor: ${res.data.cupcakes[i].flavor}, Size: ${res.data.cupcakes[i].size}, Rating: ${res.data.cupcakes[i].rating}`;
        li.append(img);
        $list.append(li);
    }
}