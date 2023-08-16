$image_select = $("#image-select")

//$("#register-imgur").on("click", async function(e) {
$("#image-search").on("focusout", async (e)=>{
    console.log("Getting URL list");
    let keyword = e.target.value;//"greatsword"
    console.log(e.target)
    if(keyword){
        const response = await axios({
            url: `https://customsearch.googleapis.com/customsearch/v1?cx=b74ccd7463d3745d4&q=${keyword}&key=AIzaSyA2Rd8vOelYi-lpm7M0-uTemD69LYlS4ys`,
            method: "GET",
        });
        //clear the image list just in case the user is changing their search terms
        $image_select.html("");
        for(item of response.data.items){
            console.log(item.pagemap.cse_image[0].src);
            let image_url =item.pagemap.cse_image[0].src;
            let input = document.createElement("input");
            input.type = "radio";
            input.name = "image_url";
            input.value = image_url;
            let preview = document.createElement("img");
            preview.src = image_url;
            $image_select.append(input);
            $image_select.append(preview);
            $image_select.append("<br>");
        }
    }
    console.log("Registration complete")
})