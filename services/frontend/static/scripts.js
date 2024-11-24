$('#from, #to').autocomplete({
    source: function (request, response) {
        fetch(`${url_frontend}?q=${encodeURIComponent(request.term)}`)
        .then(response => response.json())
        .then(data => {
            const mappedData = data.map(item => ({
                label: item.name,
                value: item.name,
                id: item.id
            }));
            response(mappedData);
        })
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
            default: { }
        }
        return true;
    }
});

function validateTicketForm() {
    if (!$('#fromHidden').val()) {
        $('#message-index-error').text('Please select a departure city from the dropdown menu')
        $('#message-index-error').show()
        return false
    }
    if (!$('#toHidden').val()) {
        $('#message-index-error').text('Please select a destination city from the dropdown menu')
        $('#message-index-error').show()
        return false
    }
    if (!$('#depart').val()) {
        $('#message-index-error').text('Please select a departure date')
        $('#message-index-error').show()
        return false
    }
    $('#message-index-error').hide()
    return true;
}

$('#from, #to').on('input', (e) => {
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

    fetch(url_signup, {
        method: 'POST',
        body: JSON.stringify(json),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            $('#message-signup-error').hide();
            return response.json()
        } else {
            $('#message-signup-success').hide();
            return response.json().then(data => {
                throw new Error(data.msg);
            });
        }
    })
    .then(data => {
        $('#message-signup-success').text(data.msg);
        $('#message-signup-success').show();
    })
    .catch(error => {
        $('#message-signup-error').text(error.message);
        $('#message-signup-error').show();
    });

    return false
}

function validateLoginForm() {
    const array = $("#form-login").serializeArray();
    const json = {};
    $.each(array, function () {
        json[this.name] = this.value || "";
    });

    fetch(url_login, {
        method: 'POST',
        body: JSON.stringify(json),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            $('#modal-login').modal('hide');
            $('#message-login-error').hide();
            location.reload();
        } else {
            return response.json().then(data => {
                throw new Error(data.msg);
            });
        }
    })
    .catch(error => {
        $('#message-login-error').text(error.message);
        $('#message-login-error').show();
    });

    return false
}

function validateSendPasswordResetForm() {
    const array = $("#form-send-password-reset").serializeArray();
    const json = {};
    $.each(array, function () {
        json[this.name] = this.value || "";
    });

    fetch(url_send_password_reset, {
        method: 'POST',
        body: JSON.stringify(json),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        } else {
            return response.json().then(data => {
                throw new Error(data.msg);
            });
        }
    })
    .then(data => {
        $('#message-send-password-reset-success').text(data.msg);
        $('#message-send-password-reset-success').show();
        $('#message-send-password-reset-error').hide();
    })
    .catch(error => {
        $('#message-send-password-reset-error').text(error.message);
        $('#message-send-password-reset-error').show();
        $('#message-send-password-reset-success').hide();
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
    const json = { 'fields': {} };
    $.each(array, function () {
        if (this.name == 'password') {
            json['password'] = this.value || "";
        } else if (this.name == 'password-new') {
            json['fields']['password'] = this.value || "";
        } else {
            json['fields'][this.name] = this.value || "";
        }
    });

    fetch(url_profile, {
        method: 'PATCH',
        body: JSON.stringify(json),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            $('#message-changepassword-error').hide();
            location.reload();
        } else {
            return response.json().then(data => {
                throw new Error(data.msg);
            });
        }
    })
    .catch(error => {
        $('#message-changepassword-error').text(error.message);
        $('#message-changepassword-error').show();
    });

    return false
}

$('#btn-update-profile').on('click', () => {
    const array = $("#form-profile").serializeArray();
    const json = { 'fields': {} };
    $.each(array, function () {
        json['fields'][this.name] = this.value || "";
    });
    console.log(json);

    fetch(url_profile, {
        method: 'PATCH',
        body: JSON.stringify(json),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                throw new Error('Profile update failed');
            }
        })
        .catch(error => {
            console.log(error);
        });

    return false
})

$('#link-login-modal').on('click', () => {
    $('#modal-signup').modal('hide');
    $('#modal-login').modal('show');
    return false;
})

$('#link-signup-modal').on('click', () => {
    $('#modal-login').modal('hide');
    $('#modal-signup').modal('show');
    return false;
})

$('#link-reset-password-modal').on('click', () => {
    $('#modal-login').modal('hide');
    $('#modal-send-password-reset').modal('show');
    return false;
})

$('input[name="radio-carriage"]').on('change', function () {
    $('.carriage-seats').hide()
    $(`.${this.id}`).show()
})

$('.checkbox-seat').on('change', function () {
    if ($('.checkbox-seat:checked').length > 0) {
        $('#hr-seat-ticket').collapse('show')
        $('#hr-ticket-total').collapse('show')
        $('#btn-pay').show()
        let total_price = 0
        $('.checkbox-seat:checked').each(() => {
            total_price += Number($(this).data('seat-price'))
        })
        $('#total-price').text(`Total: ₴ ${(total_price / 100).toFixed(2)}`)
        $('#total-price-row').collapse('show')
    } else {
        $('#btn-pay').hide()
        $('#hr-seat-ticket').collapse('hide')
        $('#hr-ticket-total').collapse('hide')
        $('#total-price-row').collapse('hide')
    }
})

$('#btn-pay').on('click', () => {
    $('#spinner-pay').show()

    seats = $('.checkbox-seat:checked').map(function() {
        return $(this).data('seat-id')
    }).get()

    json = {
        'trip_id': $('#btn-pay').data('trip-id'),
        'station_start_id': Number($('#btn-pay').data('station-start')),
        'station_end_id': Number($('#btn-pay').data('station-end')),
        'seats': seats
    }

    fetch(url_orders, {
        method: 'POST',
        body: JSON.stringify(json),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json()
        } else {
            $('#modal-signup').modal('show');
        }
    })
    .then(data => {
        window.location.href = data.url;
    })
    .finally(() => {
        $('#spinner-pay').hide();
    })
})

$('.btn-modal-qrcode').on('click', function() {
    fetch(`${url_qrcode}?ticket-id=${this.dataset.ticketId}`)
    .then(res => res.blob())
    .then(blob => {
        img = URL.createObjectURL(blob)
        $('#img-qrcode').attr('src', img)
    })
})