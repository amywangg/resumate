
$(document).ready(function(){
    var table = $('#jobtable').DataTable();
    $('#apply').on('click', function(){
        $('li#posting').removeClass('active')
        $('li#upload').addClass('active')
    });
    $('#submitres').on('click', function(){
        $('li#upload').removeClass('active')
        $('li#review').addClass('active')
    });
    $('#summary-prev').on('click', function(){
        $('li#upload').removeClass('active')
        $('li#posting').addClass('active')
    });
});