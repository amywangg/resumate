// FOR SEARCH
$('.js-example-basic-single').select2();
// DATATABLE
$(document).ready(function(){
    var table = $('#jobtable').DataTable();
})
$(function () {
    $('#get-rankings').bind('click', function () {
        $.getJSON('/getrankings', {
            a: $('select').val()
        }, function (data) {
            var rank_data = '';
            var count = 0;
            $.each(data, function (k, v) {
                count++;
                rank_data += '<tr>'
                rank_data += '<td>' + count + '</td>'
                rank_data += '<td>' + v.Name + '</td>'
                rank_data += '<td>' + v.Email + '</td>'
                rank_data += '<td>' + v.Phone_Number + '</td>'
                rank_data += '<td>' + v.Score + '</td>'
                rank_data += '<td>' + v.Matched_Skills.replace(/[\[\]"]+/g, "") + '</td>'
                rank_data += '<td style="width:325px;">' +
                    '<button value="' + v.Resume + '" class="btn btn-info btn-xs" id="viewres">View Resume</button>' +
                    '  <button value="' + v.Applicant_ID + '" class="btn btn-success btn-xs" id="selectint">Select for Interview</button>' +
                    '  <button value="' + v.Applicant_ID + '" class="btn btn-danger btn-xs" id="unmatch" id="unmatch" style="width:177.06px; text-align:center;">Unmatch</button>' +
                    '</td>'
                rank_data += '</tr>'
            });
            $('#rankbody').append(rank_data)
            var table = $('#ranktable').DataTable();

            $.each(data, function (k, v) {
                if (v.Match == 'False') {
                    $('button[id="selectint"][value="' + v.Applicant_ID + '"]').show()
                    $('button[id="unmatch"][value="' + v.Applicant_ID + '"]').hide()
                } else {
                    $('button[id="selectint"][value="' + v.Applicant_ID + '"]').hide()
                    $('button[id="unmatch"][value="' + v.Applicant_ID + '"]').show()
                }
            });
        });
    });
    // AJAX FOR VIEW RESUME
    $('#ranktable tbody').on('click', 'button#viewres', function () {
        var buttonlink = this;
        $.ajax({
            url: '/drive',
            data: {
                a: $(buttonlink).val(),
                b: $('select').val()
            },
            type: 'GET',
            success: function (response) {
                window.open(response)
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
    // AJAX FOR SELECT FOR INTERVIEW
    $('#ranktable tbody').on('click', 'button#selectint', function () {
        var buttonlink = this;
        $.ajax({
            url: '/match',
            data: {
                a: $(buttonlink).val(),
                b: $('select').val()
            },
            type: 'GET',
            success: function (response) {
                $('button[id="selectint"][value="' + response + '"]').hide()
                $('button[id="unmatch"][value="' + response + '"]').show()
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
    // AJAX FOR UNMATCH
    $('#ranktable tbody').on('click', 'button#unmatch', function () {
        var buttonlink = this;
        $.ajax({
            url: '/unmatch',
            data: {
                a: $(buttonlink).val(),
                b: $('select').val()
            },
            type: 'GET',
            success: function (response) {
                $('button[id="unmatch"][value="' + response + '"]').hide()
                $('button[id="selectint"][value="' + response + '"]').show()
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    $('#get-rankings').on('click', function () {
        $('.rankplaceholder').hide()
        $("#rankbody").empty();
        $('.rankdiv').show()
    });
});