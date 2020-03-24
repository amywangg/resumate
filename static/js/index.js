// FOR SEARCH
$('.js-example-basic-single').select2();

$(function () {
    $('#get-rankings').bind('click', function () {
        $.getJSON('/getrankings', {
            a: $('select').val()
        }, function (data) {
            console.log(data)
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
                    '</td>'
                rank_data += '</tr>'
            });
            $('#rankbody').append(rank_data)
            var table = $('#ranktable').DataTable();
        });
    });
    // AJAX FOR VIEW RESUME
    $('#ranktable tbody').on( 'click', 'button#viewres', function () {
        var buttonlink = this;
        $.ajax({
			url: '/drive',
			data: {a: $(buttonlink).val(),
                b: $('select').val()},
			type: 'GET',
			success: function(response){
				window.open(response)
			},
			error: function(error){
				console.log(error);
			}
		});
    });

      // AJAX FOR SELECT FOR INTERVIEW
      $('#ranktable tbody').on( 'click', 'button#selectint', function () {
        var buttonlink = this;
        $.ajax({
			url: '/match',
			data: {a: $(buttonlink).val(),
                b: $('select').val()},
			type: 'GET',
			success: function(response){
				window.open(response)
			},
			error: function(error){
				console.log(error);
			}
		});
    });

    $('#get-rankings').on('click', function () {
        $('.rankplaceholder').hide()
        $("#rankbody").empty();
        $('.rankdiv').show()
    });
    // FOR TAGIFY
    var tagify2;

    $("#skillmodal").on("click", function () {
        var input2 = document.querySelector('.createskilltag')
        window.tagify2 = new Tagify(input2, {
            whitelist: ["A# .NET", "A# (Axiom)", "A-0 System", "A+", "A++", "ABAP", "ABC", "ABC ALGOL", "ABSET", "ABSYS", "ACC", "Accent", "Ace DASL", "ACL2", "Avicsoft", "ACT-III", "Action!", "ActionScript", "Ada", "Adenine", "Agda", "Agilent VEE", "Agora", "AIMMS", "Alef", "ALF", "ALGOL 58", "ALGOL 60", "ALGOL 68", "ALGOL W", "Alice", "Alma-0", "AmbientTalk", "Amiga E", "AMOS", "AMPL", "Apex (Salesforce.com)", "APL", "AppleScript", "Arc", "ARexx", "Argus", "AspectJ", "Assembly language", "ATS", "Ateji PX", "AutoHotkey", "Autocoder", "AutoIt", "AutoLISP / Visual LISP", "Averest", "AWK", "Axum", "Active Server Pages", "ASP.NET", "B", "Babbage", "Bash", "BASIC", "bc", "BCPL", "BeanShell", "Batch", "Bertrand", "BETA", "Bigwig", "Bistro", "BitC", "BLISS", "Blockly", "BlooP", "Blue", "Boo", "Boomerang", "Bourne shell (including bash and ksh)", "BREW", "BPEL", "B", "C--", "C++ – ISO/IEC 14882", "C# – ISO/IEC 23270", "C/AL", "Caché ObjectScript", "C Shell", "Caml", "Cayenne", "CDuce", "Cecil", "Cesil", "Céu", "Ceylon", "CFEngine", "CFML", "Cg", "Ch", "Chapel", "Charity", "Charm", "Chef", "CHILL", "CHIP-8", "chomski", "ChucK", "CICS", "Cilk", "Citrine (programming language)", "CL (IBM)", "Claire", "Clarion", "Clean", "Clipper", "CLIPS", "CLIST", "Clojure", "CLU", "CMS-2", "COBOL – ISO/IEC 1989", "CobolScript – COBOL Scripting language", "Cobra", "CODE", "CoffeeScript", "ColdFusion", "COMAL", "Combined Programming Language (CPL)", "COMIT", "Common Intermediate Language (CIL)", "Common Lisp (also known as CL)", "COMPASS", "Component Pascal", "Constraint Handling Rules (CHR)", "COMTRAN", "Converge", "Cool", "Coq", "Coral 66", "Corn", "CorVision", "COWSEL", "CPL", "CPL", "Cryptol", "csh", "Csound", "CSP", "CUDA", "Curl", "Curry", "Cybil", "Cyclone", "Cython", "Java", "Javascript", "M2001", "M4", "M#", "Machine code", "MAD (Michigan Algorithm Decoder)", "MAD/I", "Magik", "Magma", "make", "Maple", "MAPPER now part of BIS", "MARK-IV now VISION:BUILDER", "Mary", "MASM Microsoft Assembly x86", "MATH-MATIC", "Mathematica", "MATLAB", "Maxima (see also Macsyma)", "Max (Max Msp – Graphical Programming Environment)", "Maya (MEL)", "MDL", "Mercury", "Mesa", "Metafont", "Microcode", "MicroScript", "MIIS", "Milk (programming language)", "MIMIC", "Mirah", "Miranda", "MIVA Script", "ML", "Model 204", "Modelica", "Modula", "Modula-2", "Modula-3", "Mohol", "MOO", "Mortran", "Mouse", "MPD", "Mathcad", "MSIL – deprecated name for CIL", "MSL", "MUMPS", "Mystic Programming L"],
            dropdown: {
                position: "manual",
                maxItems: Infinity,
                enabled: 0,
                classname: "suggestions2"
            },
            duplicates: false
        });
        tagify2.on("dropdown:show", onSuggestionsListUpdate2)
            .on("dropdown:hide")
            .on('dropdown:scroll')

        renderSuggestionsList2()
    });
    // ES2015 argument destructuring
    function onSuggestionsListUpdate2({ detail: suggestionsElm }) {
    }
    function renderSuggestionsList2() {
        tagify2.dropdown.show.call(tagify2) // load the list
        tagify2.DOM.scope.parentNode.appendChild(tagify2.DOM.dropdown)
    }
});
    $("#close").on("click", function () {
        $(".tagify").remove();
        $(".tagify").removeData();
        $(".suggestions2").remove();
    })
    $("#close2").on("click", function () {
        $(".tagify").remove();
        $(".tagify").removeData();
        $(".suggestions2").remove();
    })

    // FOR JOB CREATION
    $(".nav-link").on("click", function () {
        $(".nav").find(".active").removeClass("active");
        $(this).addClass("active");
    });

    var title;
    var description;
    var tagify;

    $("#job-next").click(function () {
        setTimeout(function () {
            window.title = $("#title").val()
            window.description = $("#description").val(), 100
        });
        $("#job-page").hide();
        $("#skills-page").show();
        $("#loading-gif").show();
        $("#circ-2").addClass("active-step");
        $("#lab-2").addClass("active-step-text");
        $("#line-1-2").addClass("active-step");
    });

    $("#skills-next").click(function () {
        var skills = "";
        window.tagify["value"].forEach(function (e) {
            skills += e.value + ", "
        });
        skills = skills.replace(/,\s*$/, "");
        $("#skills-page").hide();
        $("#summary-page").show();
        $("#circ-3").addClass("active-step");
        $("#lab-3").addClass("active-step-text");
        $("#line-2-3").addClass("active-step");
        $("#summary-title").text(window.title)
        $("#summary-desc").text(window.description)
        $("#summary-skills").text(skills)
        //    extract only values from object
        $('.skilltag').val(JSON.stringify(window.tagify["value"].map(a => a.value)))

    });

    $("#skills-prev").click(function () {
        $("#skills-page").hide();
        $("#job-page").show();
        $("#circ-2").removeClass("active-step");
        $("#lab-2").removeClass("active-step-text");
        $("#circ-1").addClass("active-step");
        $("#lab-1").addClass("active-step-text");
        $("#line-1-2").removeClass("active-step");
        $(".tagify").remove();
        $(".tagify").removeData();
        $(".suggestions").remove();
    });

    $("#summary-prev").click(function () {
        $("#summary-page").hide();
        $("#skills-page").show();
        $("#circ-3").removeClass("active-step");
        $("#lab-3").removeClass("active-step-text");
        $("#circ-2").addClass("active-step");
        $("#lab-2").addClass("active-step-text");
        $("#line-2-3").removeClass("active-step");

    });


    $(function () {
        $('#job-next').bind('click', function () {
            $.getJSON('/getskills', {
                a: $('textarea[name="description"]').val(),
            }, function (data) {
                var input = document.querySelector('.skilltag')
                window.tagify = new Tagify(input, {
                    whitelist: ["A# .NET", "A# (Axiom)", "A-0 System", "A+", "A++", "ABAP", "ABC", "ABC ALGOL", "ABSET", "ABSYS", "ACC", "Accent", "Ace DASL", "ACL2", "Avicsoft", "ACT-III", "Action!", "ActionScript", "Ada", "Adenine", "Agda", "Agilent VEE", "Agora", "AIMMS", "Alef", "ALF", "ALGOL 58", "ALGOL 60", "ALGOL 68", "ALGOL W", "Alice", "Alma-0", "AmbientTalk", "Amiga E", "AMOS", "AMPL", "Apex (Salesforce.com)", "APL", "AppleScript", "Arc", "ARexx", "Argus", "AspectJ", "Assembly language", "ATS", "Ateji PX", "AutoHotkey", "Autocoder", "AutoIt", "AutoLISP / Visual LISP", "Averest", "AWK", "Axum", "Active Server Pages", "ASP.NET", "B", "Babbage", "Bash", "BASIC", "bc", "BCPL", "BeanShell", "Batch", "Bertrand", "BETA", "Bigwig", "Bistro", "BitC", "BLISS", "Blockly", "BlooP", "Blue", "Boo", "Boomerang", "Bourne shell (including bash and ksh)", "BREW", "BPEL", "B", "C--", "C++ – ISO/IEC 14882", "C# – ISO/IEC 23270", "C/AL", "Caché ObjectScript", "C Shell", "Caml", "Cayenne", "CDuce", "Cecil", "Cesil", "Céu", "Ceylon", "CFEngine", "CFML", "Cg", "Ch", "Chapel", "Charity", "Charm", "Chef", "CHILL", "CHIP-8", "chomski", "ChucK", "CICS", "Cilk", "Citrine (programming language)", "CL (IBM)", "Claire", "Clarion", "Clean", "Clipper", "CLIPS", "CLIST", "Clojure", "CLU", "CMS-2", "COBOL – ISO/IEC 1989", "CobolScript – COBOL Scripting language", "Cobra", "CODE", "CoffeeScript", "ColdFusion", "COMAL", "Combined Programming Language (CPL)", "COMIT", "Common Intermediate Language (CIL)", "Common Lisp (also known as CL)", "COMPASS", "Component Pascal", "Constraint Handling Rules (CHR)", "COMTRAN", "Converge", "Cool", "Coq", "Coral 66", "Corn", "CorVision", "COWSEL", "CPL", "CPL", "Cryptol", "csh", "Csound", "CSP", "CUDA", "Curl", "Curry", "Cybil", "Cyclone", "Cython", "Java", "Javascript", "M2001", "M4", "M#", "Machine code", "MAD (Michigan Algorithm Decoder)", "MAD/I", "Magik", "Magma", "make", "Maple", "MAPPER now part of BIS", "MARK-IV now VISION:BUILDER", "Mary", "MASM Microsoft Assembly x86", "MATH-MATIC", "Mathematica", "MATLAB", "Maxima (see also Macsyma)", "Max (Max Msp – Graphical Programming Environment)", "Maya (MEL)", "MDL", "Mercury", "Mesa", "Metafont", "Microcode", "MicroScript", "MIIS", "Milk (programming language)", "MIMIC", "Mirah", "Miranda", "MIVA Script", "ML", "Model 204", "Modelica", "Modula", "Modula-2", "Modula-3", "Mohol", "MOO", "Mortran", "Mouse", "MPD", "Mathcad", "MSIL – deprecated name for CIL", "MSL", "MUMPS", "Mystic Programming L"],
                    dropdown: {
                        position: "manual",
                        maxItems: Infinity,
                        enabled: 0,
                        classname: "suggestions"
                    },
                    duplicates: false
                })
                tagify.addTags(data)
                tagify.on("dropdown:show", onSuggestionsListUpdate)
                    .on("dropdown:hide")
                    .on('dropdown:scroll')

                renderSuggestionsList()

                // ES2015 argument destructuring
                function onSuggestionsListUpdate({ detail: suggestionsElm }) {
                }
                function renderSuggestionsList() {
                    tagify.dropdown.show.call(tagify) // load the list
                    tagify.DOM.scope.parentNode.appendChild(tagify.DOM.dropdown)
                }
                $("#loading-gif").hide();
            });

            return false;
        });
    });
    // GET EXISTING SKILL
    $(function () {
        $('a#calculate').bind('click', function () {
            $.getJSON($SCRIPT_ROOT + '/getexistingskills', {
                a: $('input[name="a"]').val(),
                b: $('input[name="b"]').val()
            }, function (data) {

                $("#result").text(data.result);
            });
            return false;
        });
    });