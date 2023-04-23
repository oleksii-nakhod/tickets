$('#from, #to').autocomplete({
    source: function (request, response) {
        $.ajax({
            url: url_stations,
            dataType: "json",
            data: {
                q: request.term
            },
            success: function(data) {
                response($.map(data, function (item) {
                    return {
                        label: item.name,
                        value: item.name,
                        id: item.id
                    }
                }));
            }
        });
    },
    minLength: 0,
    cacheLength: 0,
    select: function (e, ui) {
        switch (e.target.id) {
            case 'from':
                $('#fromHidden').val(ui.item.id);
                break;
            case 'to':
                $('#toHidden').val(ui.item.id);
                break;
            default: {}
        }
        return true;
    }
});

function validateTicketForm() {
    if (!$('#fromHidden').val()) return false
    if (!$('#toHidden').val()) return false
    if (!$('#depart').val()) return false
    return true;
}

$('#from, #to').on('input', (e)=>{
    switch (e.target.id) {
        case 'from':
            $('#fromHidden').val('')
            break;
        case 'to':
            $('#toHidden').val('')
            break;
        default: { }
    }
})

function validateSignupForm() {
    const array = $("#form-signup").serializeArray();
    const json = {};
    $.each(array, function () {
        json[this.name] = this.value || "";
    });
    console.log(json);
    
    $.ajax({
            type: 'POST',
            url: url_signup,
            data: JSON.stringify(json),
            success: function (data, status, request) {
                $('#modal-signup').modal('hide')
                $('#message-signup-error').hide()
                location.reload()
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $('#message-signup-error').text(jqXHR.responseJSON['msg'])
                $('#message-signup-error').show()
            },
            dataType: 'json',
            contentType: 'application/json'
        })
    return false
}

function validateLoginForm() {
    const array = $("#form-login").serializeArray();
    const json = {};
    $.each(array, function () {
        json[this.name] = this.value || "";
    });
    console.log(json);
    
    $.ajax({
        type: 'POST',
        url: url_login,
        data: JSON.stringify(json),
        success: function (data, status, request) {
            $('#modal-login').modal('hide')
            $('#message-login-error').hide()
            location.reload()
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $('#message-login-error').text(jqXHR.responseJSON['msg'])
            $('#message-login-error').show()
        },
        dataType: 'json',
        contentType: 'application/json'
    });
    return false
}

function validateChangePasswordForm() {
    if ($('#password-new').val() != $('#password-confirm').val()) {
        $('#message-changepassword-error').text("Passwords don't match")
        $('#message-changepassword-error').show()
        return false
    }
    const array = $("#form-changepassword").serializeArray();
    const json = {'fields': {}};
    $.each(array, function () {
        if (this.name == 'password') {
            json['password'] = this.value || "";
        } else if (this.name == 'password-new') {
            json['fields']['password'] = this.value || "";
        } else {
            json['fields'][this.name] = this.value || "";
        }
    });
    console.log(json);
    
    $.ajax({
        type: 'PATCH',
        url: url_profile,
        data: JSON.stringify(json),
        success: function (data, status, request) {
            $('#message-changepassword-error').hide()
            location.reload()
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $('#message-changepassword-error').text(jqXHR.responseJSON['msg'])
            $('#message-changepassword-error').show()
        },
        dataType: 'json',
        contentType: 'application/json'
    });
    return false
}

$('#btn-update-profile').on('click', () => {
    const array = $("#form-profile").serializeArray();
    const json = {'fields': {}};
    $.each(array, function () {
        json['fields'][this.name] = this.value || "";
    });
    console.log(json);

    $.ajax({
        type: 'PATCH',
        url: url_profile,
        data: JSON.stringify(json),
        success: function (data, status, request) {
            location.reload()
        },
        error: function (jqXHR, textStatus, errorThrown) {
        },
        dataType: 'json',
        contentType: 'application/json'
    })
    return false
})

$('#link-login-modal').on('click', ()=>{
    $('#modal-signup').modal('hide');
    $('#modal-login').modal('show');
    return false;
})

$('#link-signup-modal').on('click', () => {
    $('#modal-login').modal('hide');
    $('#modal-signup').modal('show');
    return false;
})

$('input[name="radio-carriage"]').on('change', function(event){
    $('.carriage-seats').hide()
    $(`.${this.id}`).show()
})

$('.checkbox-seat').on('change', function (event) {
    if ($('.checkbox-seat:checked').length>0) {
        $('#hr-seat-ticket').collapse('show')
        $('#hr-ticket-total').collapse('show')
        $('#btn-pay').show()
        let total_price = 0
        $('.checkbox-seat:checked').each(()=>{
            total_price += Number($(this).data('seat-price'))
        })
        $('#total-price').text(`Total: ₴ ${(total_price/100).toFixed(2)}`)
        $('#total-price-row').collapse('show')
    } else {
        $('#btn-pay').hide()
        $('#hr-seat-ticket').collapse('hide')
        $('#hr-ticket-total').collapse('hide')
        $('#total-price-row').collapse('hide')
    }
})

$('#btn-pay').on('click', ()=>{
    $('#spinner-pay').show()
    seats = $('.checkbox-seat:checked').map(function(){
        return $(this).data('seat-id')
    }).get()
    json = {
        'trip_id': $('#btn-pay').data('trip-id'),
        'station_start_id': Number($('#btn-pay').data('station-start')),
        'station_end_id': Number($('#btn-pay').data('station-end')),
        'seats': seats
    }
    console.log(json)
    $.ajax({
        type: 'POST',
        url: url_order,
        data: JSON.stringify(json),
        success: function (data, status, request) {
            $('#spinner-pay').hide()
            window.location.href = data.url
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $('#spinner-pay').hide()
            console.log('error');
        },
        dataType: 'json',
        contentType: 'application/json'
    });
})