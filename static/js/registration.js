$(function() {
	// Deals with the code inscription button
    $('#student_form_link').click(function() {
        $('#menu').slideUp('fast');
        $('#student_form').slideDown('fast');
    });

    $('#hide_student_form').click(function() {
        $('#menu').slideDown('fast');
        $('#student_form').slideUp('fast');
    });


    //Deals with the code inscription form
    $('#student_registration').submit(function(e) {
    	e.preventDefault();
    	$('#id_code').removeClass('error');
        var code = $('#id_code').val();

    	$.post(
                '/register/',
                {
                    'code': code,
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                },
                function(data) {
                    if (data.success === 'true') {
                        location.replace('/register/code/'+code);
                    } else {
                    	$('#id_code').addClass('error');
                    }
                },
                'json'
            );
    });

    // Dealing with the choice to register with facebook or not
    if ($('.registration_form').length) {
        showPopup();

        $('#without_facebook').click(function() {
            hidePopup();
        });

        $('#with_facebook').click(function() {
            FB.login(
                function(response){
                    if (response.status == 'connected') {
                        FB.api(
                            '/me',
                            'get',
                            {fields: 'id,first_name,last_name,email'},
                            function(response) {
                                $('#id_firstName').val(response.first_name);
                                $('#id_lastName').val(response.last_name);
                                $('#id_email').val(response.email);

                                hidePopup();
                            }
                        );
                    } else {
                        alert('Une erreur est survenue');
                    }
                },
                {scope: 'email'}
            );
        })
    }

    function showPopup() {
        $('body').addClass('no-scroll');
        $('body').bind('touchmove', function(e){e.preventDefault()}); // For mobile devices

        $('#content, #banner, footer').addClass('blur');
        $('#registering_method').removeClass('hidden').addClass('full-size-popup');
    }

    function hidePopup() {
        $('body').removeClass('no-scroll');
        $('body').unbind('touchmove');

        $('#content, #banner, footer').removeClass('blur');
        $('#registering_method').removeClass('full-size-popup').hide();
    }

});
