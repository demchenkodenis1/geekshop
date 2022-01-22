window.onload = function () {

    $('.basket_list').on('click', 'input[type="number"]', function (event) {
        let t_href = event.target
        console.log(t_href)
        $.ajax(
            {
                url: "/baskets/edit/" + t_href.name + "/" + t_href.value + "/",
                success: function (data) {
                    $('.basket_list').html(data.result)
                },
                error: function (data){
                    console.log(data)
                }
            });
        event.preventDefault();
    });

    // var csrf = $('meta[name="csrf_token"]').attr('content');
    // $('.button_basket').on('click', 'button', function (event) {
    //     let t_href = event.target.value
    //     console.log(t_href)
    //     $.ajax(
    //         {
    //             type: 'POST',
    //             headers: {'X-CSRFToken': csrf},
    //             url: "/baskets/add/" + t_href + "/",
    //             success: function (data) {
    //                 $('.card_add_basket').html(data.result)
    //                 swal('Спасибо!', 'Товар, успешно добавлен в корзину!', 'success')
    //
    //             },
    //             error: function (data){
    //                 console.log(data)
    //             }
    //         });
    //     event.preventDefault()
    // })
}