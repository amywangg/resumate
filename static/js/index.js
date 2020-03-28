var setDefaultActive = function() {
    var path = window.location.pathname;
    var element = $(".navlist li > a[href='" + path + "']");
    element.addClass("active");
}
$(document).ready(function(){
    setDefaultActive()
});


    $('#jobtable tbody').on('click', 'button#editskill',function () {
        var x = this.value
        $.ajax({
            url: '/popskills',
            data: {
                a: x,
            },
            type: 'GET',
            success: function (response) {
                var input = document.querySelector('.editskilltag'+x)
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
                tagify.addTags(response)
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
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    $('.close').on('click', function(){
        $(".tagify").remove();
        $(".tagify").removeData();
        $(".suggestions").remove();
    });

    $('.close2').on('click', function(){
        $(".tagify").remove();
        $(".tagify").removeData();
        $(".suggestions").remove();
    });