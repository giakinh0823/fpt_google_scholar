function getCookieSaveUpdateData(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftokenSaveUpdateData = getCookieSaveUpdateData('csrftoken');

$(document).on('click','#updateDataButton', function() {
    $('#progress-bar').addClass('progress-bar-animated')
    $('#progress-bar').addClass('bg-success')
    $('#progress-bar').addClass('progress-bar-striped')
    $('#progress-bar').removeClass('bg-warning')
    $('#progress-bar').removeClass('bg-danger')
    $('#progress-bar').text('Get Profile')
    $.ajax({
        type: 'GET',
        url: 'updateData/',
        data: '',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
            $('#progress-bar').removeClass('progress-bar-animated')
            $('#progress-bar').removeClass('bg-success')
            $('#progress-bar').removeClass('progress-bar-striped')
            $('#progress-bar').addClass('bg-warning')
            $('#progress-bar').text('Done')
        },
    })
});

$(document).on('click','#updateArticleButton', function() {
    $('#progress-bar').addClass('progress-bar-animated')
    $('#progress-bar').addClass('bg-danger')
    $('#progress-bar').addClass('progress-bar-striped')
    $('#progress-bar').removeClass('bg-warning')
    $('#progress-bar').removeClass('bg-success')
    $('#progress-bar').text('Get Article')
    $.ajax({
        type: 'GET',
        url: 'updateArticle/',
        data: '',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
            $('#progress-bar').removeClass('progress-bar-animated')
            $('#progress-bar').removeClass('bg-danger')
            $('#progress-bar').removeClass('progress-bar-striped')
            $('#progress-bar').addClass('bg-warning')
            $('#progress-bar').text('Done')
        },
    })
});