$(document).ready(function(){
    $('form').on('submit', function(event){
        console.log('hello')
        $.ajax({
            data : {
                query: $('#foodQuery').val()
            },
            type:'POST',
        })
        event.preventDefault();
    });
});


$(document).ready(function(){
    $('comment_form').on('submit', function(event){
        console.log('hello')
        $.ajax({
            data : {
                comment: $('#comment_content').val()
            },
            type:'POST',
        })
        event.preventDefault();
    });
});


$(document).ready(function(){
    $('form').on('submit', function(event){
        console.log('hello')
        $.ajax({
            data : {
                query_spage: $('#recipeText').val()
            },
            type:'POST',
        })
        event.preventDefault();
    });
});
