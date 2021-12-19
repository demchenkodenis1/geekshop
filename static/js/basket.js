window.onload = () => {
    $('.basket_list').on('click', 'input[type="number"]', (e) => {
        let t_href = e.target
        // console.log(t_href.name)
        // console.log(t_href.value)
        $.ajax({
            url: "/baskets/edit/" + t_href.name + "/" + t_href.value + "/",
            success: (data) =>{
                $('.basket_list').html(data.result)
            }
        });
    e.preventDefault()

    })

        $('.card_add_basket').on('click', 'button[type="button"]', (e) => {
        let t_href = e.target.value
        $.ajax({
            url: "/baskets/add/" + t_href + "/",
            success: (data) =>{
                $('.card_add_basket').html(data.result)
            }
        });
    e.preventDefault()

    })
}
