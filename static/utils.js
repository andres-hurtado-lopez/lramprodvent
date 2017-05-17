"use strict";

function HTTP_DELETE_JSON(params)
{
    $.blockUI({
        message: params.wait_msg,
        onBlock: function() {
            $.ajax({
            url: params.url,
            type: 'DELETE',
            data: params.data,
            dataType: 'json',
            }).done(function(data){
                $.unblockUI();
                if(params.reload_url)
                {
                    if(data.response === true)
                        location.reload();
                    else
                        alert(data.message);
                }
                else if(params.done)
                {
                	params.done(data);
                }

            }).fail(function(xhr){
                if(params.fail)
                {
                	params.fail();
                }
                else
                {
                	document.write(xhr.responseText);
                }
            });
        }
    });
}

function HTTP_PUT_JSON(params)
{
    $.blockUI({
        message: params.wait_msg,
        onBlock: function() {
            $.ajax({
            url: params.url,
            type: 'PUT',
            data: params.data,
            dataType: 'json',
            }).done(function(data){
                $.unblockUI();
                if(params.reload_url)
                {
                    if(data.response === true)
                        location.reload();
                    else
                        alert(data.message);
                }
                else if(params.done)
                {
                	params.done(data);
                }

            }).fail(function(xhr){
                if(params.fail)
                {
                	params.fail();
                }
                else
                {
                	document.write(xhr.responseText);
                }
            });
        }
    });
}

function HTTP_POST_JSON(params)
{
    $.blockUI({
        message: params.wait_msg,
        onBlock: function() {
            $.ajax({
            url: params.url,
            type: 'POST',
            data: params.data,
            dataType: 'json',
            }).done(function(data){
                $.unblockUI();
                if(params.reload_url)
                {
                    if(data.response === true)
                        location.reload();
                    else
                        alert(data.message);
                }
                else if(params.done)
                {
                	params.done(data);
                }

            }).fail(function(xhr){
                if(params.fail)
                {
                	params.fail();
                }
                else
                {
                	document.write(xhr.responseText);
                }
            });
        }
    });
}

function HTTP_GET_JSON(params)
{
    $.blockUI({
        message: params.wait_msg,
        onBlock: function() {
            $.ajax({
            url: params.url,
            type: 'GET',
            data: params.data,
            dataType: 'json',
            }).done(function(data){
                $.unblockUI();
                if(params.reload_url)
                {
                    if(data.response === true)
                        location.reload();
                    else
                        alert(data.message);
                }
                else if(params.done)
                {
                	params.done(data);
                }

            }).fail(function(xhr){
                if(params.fail)
                {
                	params.fail();
                }
                else
                {
                	document.write(xhr.responseText);
                }
            });
        }
    });
}