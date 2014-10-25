<script>

    hidden_columns = 1;
    // calculate % for OR questions
    function calculateORAverages(sCol, value) {
        var grid = $('#hot').handsontable('getInstance');
        sCol -= hidden_columns;
        questionData = grid.getDataAtCol(sCol);
        colLength = questionData.length;
        var pts_value = questionData[1];
        var total_points = 0;
        var possible = [];
        for (var a=0; a <= or_points; a++) {
            possible.push(0);
        }
        var total = 0;
        for (var a = (3 + maxQuestions); a < colLength; a++) {
            if (questionData[a] != "") {
                total += 1;
                var input = questionData[a];
                possible[parseInt(input)] += 1;
                total_points += parseInt(input);

            }
            //if (questionData[1] != "" && questionData[a] == questionData[1]) total_points += 1;
        }
        var changes = [];
        if (total == 0) {
            // blank out question % if no answers 
            grid.setDataAtCell((maxQuestions + 3), sCol, "", "calc");
            // blank out answer choice % if no answers 
            for (var a = 0; a < maxQuestions; a++) changes.push([a + 2,sCol,""]);
            grid.setDataAtCell(changes,"calc");
        }
        else {
            var qPercent = Math.round(((total_points/total) / pts_value) * 100);
            if (isNaN(qPercent)) qPercent = 0;
            grid.setDataAtCell((maxQuestions + 3), sCol, (qPercent + "%"), "calc");
            
            var aPercent = [];
            
            for (var a = 0; a < possible.length; a++) {
                aPercent[a] = Math.round((possible[a]/total) * 100);
            }
            
            for (var a = 0; a < aPercent.length; a++) {
                changes.push([(a+2),sCol,aPercent[a] + "%"]);
            } 
            grid.setDataAtCell(changes,"calc");
        }
    }
    function calculateQuestionAverage(sCol, value) {
        var grid = $('#hot').handsontable('getInstance');
        sCol -= hidden_columns;
        questionData = grid.getDataAtCol(sCol);
        colLength = questionData.length;
        var correct = 0;
        //var answers = questionData[2:mc_answers + 1];
        
        var answers = [];
        for (var a=0; a <= mc_answers; a++) {
            answers.push(0);
        }
        var total = 0;
        for (var a = (3 + maxQuestions); a < colLength; a++) {
            if (questionData[a] != "") {
                total += 1;
                var input = questionData[a];
                answers[parseInt(input)] += 1;

            }
            if (questionData[0] != "" && questionData[a] == questionData[0]) correct += 1;
        }
        var changes = [];
        if (total == 0) {
            // blank out question % if no answers 
            grid.setDataAtCell((maxQuestions + 2), sCol, "", "calc");
            // blank out answer choice % if no answers 
            for (var a = 0; a < maxQuestions; a++) changes.push([a + 2,sCol,""]);
            grid.setDataAtCell(changes,"calc");
        }
        else {
            var qPercent = Math.round((correct/total) * 100);
            if (isNaN(qPercent)) qPercent = 0;
            grid.setDataAtCell((maxQuestions + 3), sCol, (qPercent + "%"), "calc");
            var aPercent = [];
            for (var a = 0; a < answers.length; a++) {
                aPercent[a] = Math.round((answers[a]/total) * 100);
            }
            for (var a = 0; a < aPercent.length; a++) {
                changes.push([(a+2),sCol,aPercent[a] + "%"]);
            } 
            grid.setDataAtCell(changes,"calc");
        }
    };

    // calculate student percentages
    // sRow = row of changed answer, sCol = column of changed answer, value = value
    function calculateStudentAverage(sRow, sCol, value) {
        var grid = $('#hot').handsontable('getInstance');
        // columns where answers begin
        startAnswers = 3;
        sCol -= hidden_columns;
        var onlyRightAnswers = grid.getDataAtRow(0).slice(startAnswers);
        var pt_values = grid.getDataAtRow(1).slice(startAnswers);
        var onlyStudentAnswers = grid.getDataAtRow(sRow).slice(startAnswers);
        var numOfQuestions = onlyStudentAnswers.length;
        var points = 0;
        var total = 0;
        for (var a = 0; a < num_mc; a++) {
            if (onlyStudentAnswers[a] != "") total += parseInt(pt_values[a]);
            if ( onlyRightAnswers[a] != "" && onlyStudentAnswers[a] == onlyRightAnswers[a] ) points += parseInt(pt_values[a]);
        }
        console.log(points + " / " + total);
        for (var a = (num_mc + 1); a < (num_or + num_mc + 1); a++) {
            if ( onlyStudentAnswers[a] != "" && pt_values[a] != "" ) {
                points += parseInt(onlyStudentAnswers[a]);
                total += parseInt(pt_values[a]);
            }
        }
        console.log(points + " / " + total);
        if (total == 0) {
            grid.setDataAtCell(sRow, 1, "", "calc");
        }
        else {
            var sPercent = Math.round((points/total) * 100);
            if (isNaN(sPercent)) sPercent = 0;
            grid.setDataAtCell(sRow, 1, (sPercent + "%"), "calc");
        }
    };
    //conditional formatting for right vs wrong answers: check value against answer
    function negativeValueRenderer(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments); 
        var grid = $('#hot').handsontable('getInstance');
        
        
        // if cell is an answer input area
        if (col > 1 && row > (3 + maxQuestions) && value) {
            // if cell is a MC answer
            if (col < (num_mc + 2)) {
                var answers = grid.getDataAtRow(0);
                var answer = answers[col + 1];
                // if cell has incorrect answer
                if (value != answer) {
                    td.style.background = 'red';
                }
                // if cell has correct answer
                else {
                    td.style.background = '#00FF00';
                }
            }
            // if cell is a OR answer
            else if (col > (num_mc + 2)) {
                var pt_values = grid.getDataAtRow(1);
                var pt_value = pt_values[col + 1];
                var pt_valueINT = parseInt(pt_value);
                var valueINT = parseInt(value);
                // if cell points value is equal to pt value
                if (valueINT == pt_valueINT) {
                    td.style.background = '#00FF00';   
                }
                else if ((valueINT/pt_valueINT) > .79) {
                    td.style.background = '#FFFF00';
                }
                else {
                    td.style.background = 'red';
                }
            }
        }
        /*if (col > 1 && row > (2 + or_points) && value && value != answer) {
            td.style.background = 'red';
            console.log(answer);
        }
        else if (value && value == answer) {
            td.style.background = '#00FF00';
        }*/
    };
    //conditional formatting for % row
    function firstRowRenderer(instance, td, row, col, prop, value, cellProperties) {
        Handsontable.renderers.TextRenderer.apply(this, arguments);
        td.style.fontWeight = 'bold';
        td.style.color = 'black';
        td.style.background = '';
        if (row == (maxQuestions + 3) && col > 1 && value && value != "") {
            if (value.split('%')[0] > 79) {td.style.color = 'green'; td.style.background = 'white';}
            if (value.split('%')[0] < 80) {td.style.color = 'red'; td.style.background = 'white';}
        }
        if (row > (maxQuestions + 3) && col == 1 && value && value != "") {
            if (value.split('%')[0] > 79) {td.style.color = 'green'; td.style.background = 'white';}
            if (value.split('%')[0] < 80) {td.style.color = 'red'; td.style.background = 'white';}   
        }
        if (col == 0 || row == 0 || row == 1) {
            td.style.fontWeight = 'bold';
            td.style.color = 'black';
        }
    };
    Handsontable.renderers.registerRenderer('negativeValueRenderer', negativeValueRenderer); //maps function 
    var num_mc = {{test.num_mc}};
    var mc_answers = {{test.mc_answers}};
    var num_or = {{test.num_or}};
    var or_points = {{test.or_points}};
    var maxQuestions = Math.max(mc_answers, or_points);
    var total_questions = num_mc + num_or;
    var num_students = {{test.num_students}};
    var data = {{data|safe}};
    
    //create the headers
    var colHeaders = ["Student","%"];
    for (var b = 1; b <= num_mc; b++) colHeaders.push(b);
    colHeaders.push("MC %");
    for (var b = (num_mc + 1); b <= total_questions; b++) colHeaders.push(b);
    colHeaders.push("OR %");

    //set readonly columns
    var columns = [
        {data: 0, readOnly: true},
        {data: 2, readOnly: true},
    ]
    for (var a = 3; a < num_mc + 3; a++) columns.push({data: a});
    columns.push({data: num_mc + 3, readOnly: true});
    for (var a = (num_mc + 4); a < (num_mc + 4 + num_or); a++) columns.push({data: a});
    columns.push({data: total_questions + 5, readOnly: true});
    
    //column widths
    var colw = [200];
    for (var a = 1; a < total_questions + 3; a++) colw.push(50);

    var autosaveNotification;
    $('#hot').handsontable({
        data: data,
        colHeaders: colHeaders,
        //rowHeaders: true,
        minSpareRows: 0,
        minSpareCols: 0,
        fillHandle: false,
        enterMoves: {row: 0, col: 1},
        autoWrapRow: true,
        columns: columns,
        colWidths: colw,
        fixedColumnsLeft: 2,        
        fixedRowsTop: 3 + maxQuestions,
        enterBeginsEditing: false,
        cells: function (row, col, prop) {
            var cellProperties = {};
            if (row > 1 && row <= (maxQuestions + 3))  {
                cellProperties.readOnly = true; //make cell read-only if third row
                cellProperties.renderer = firstRowRenderer;
            }
            if (col == 1 || col == 0) {
                cellProperties.readOnly = true; //make cell read-only if third row
                cellProperties.renderer = firstRowRenderer;   
            }
            if (row < 2) {
                cellProperties.renderer = firstRowRenderer;
            }
            else if (row > (maxQuestions + 3) && col > 1) {
                cellProperties.renderer = "negativeValueRenderer"; 
            }
            return cellProperties;
        },
        afterChange: function (changes, source) {
            var grid = $('#hot').handsontable('getInstance');
            if (changes && source != 'calc') {
                sRow = changes[0][0];
                if (sRow > 2) {
                    sCol = changes[0][1];
                    value = changes[0][3];
                    if (sCol < num_mc + 3) {
                        calculateQuestionAverage(sCol, value);
                    }
                    else {
                        calculateORAverages(sCol, value);
                    }
                    calculateStudentAverage(sRow, sCol, value);
                    
                }
            }
            if (source === 'loadData') {
                return; //don't save this change
            }
            /*clearTimeout(autosaveNotification);
            console.log("AJAX");
            $.ajax({
                url: "#",
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                type: "POST",
                data: JSON.stringify(grid.getData()), //contains changed cells' data
                complete: function (data) {
                  console.log('Autosaved (' + changes.length + ' cell' + (changes.length > 1 ? 's' : '') + ')');
                  autosaveNotification = setTimeout(function () {
                    console.log('Changes will be autosaved');
                  }, 1000);
                }
            });
        }
    });

    $('#hot').addClass('table');
    $('#hot table').addClass('table-striped'); 


</script>