window.onresize = function() {
    gd = Plotly.d3.select('#Tab2-contents > div').node();
    if ( gd ){
        Plotly.Plots.resize( gd );
    }
};

function performClick(elemId) {
   var elem = document.getElementById(elemId);
   if(elem && document.createEvent) {
      var evt = document.createEvent("MouseEvents");
      evt.initEvent("click", true, false);
      elem.dispatchEvent(evt);
   }
}

$body = $("body");
$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
    ajaxStop:  function() { $body.removeClass("loading"); }
});

$( function() {
    var tabs = $( "#tabs" ).tabs();
    tabs.find( ".ui-tabs-nav" ).sortable({
        axis: "x",
        stop: function() {
            tabs.tabs( "refresh" );
        }
    });
});


$( function() {
    $( "#tabs input[type=submit]" ).button();
});


$( function() {
    $( ".btnLoad" ).on( "click", function( event ) {
        var target = $( event.target );
        $body.addClass("loading");
    });
});

// ============================================================= //

$(document).ready(function() {
    $( '#Tab0 input' ).bind( 'click', function(){
        return false;
    });

    $( '#buildModel' ).bind( 'click', function(){
        buildModel();
        return false;
    });

    $( '#predict' ).bind( 'click', function(){
        predict('miniset.txt');
        return false;
    });

    $( '#Tab2 input' ).bind( 'click', function(){
        getKSDist();
        return false;
    });

    $( '#upload' ).bind( 'click', function(){
        $('#form').submit();
        return false;
    });
});

function getKSDist( inpt ){
    $.getJSON( $SCRIPT_ROOT + '/_getKSDist', {
        inpt: JSON.stringify( 'tesT' )
    }, function( data ){
        var WIDTH_IN_PERCENT_OF_PARENT = 100,
        HEIGHT_IN_PERCENT_OF_PARENT = 100;

        $('#Tab2-contents').empty();
        $('#Tab2-contents').addClass('hidden');
        $('#Tab2-contents').append( data.result );
        $('#Tab2-contents > div').css({
            width: WIDTH_IN_PERCENT_OF_PARENT + '%',
            'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',
            height: HEIGHT_IN_PERCENT_OF_PARENT + 'vh',
            'margin-top': (100 - HEIGHT_IN_PERCENT_OF_PARENT) / 2 + 'vh'
        });
        Plotly.Plots.resize( Plotly.d3.select('#Tab2-contents > div').node() );
        $('#Tab2-contents').removeClass('hidden');

        $body.removeClass("loading");
    });
};

function buildModel(){
    $.getJSON( $SCRIPT_ROOT + '/_buildModel', {
    }, function( data ){
        alert( 'Accuracy score: ' + data.score )
        $('<img src="static/Clf.png">').load(function() {
            $(this).width('3000px').appendTo('#tree');
        });

        $body.removeClass("loading");
    })
};

function predict( input ){
    $.getJSON( $SCRIPT_ROOT + '/_predict', {
        file: input
    }, function( data ){
        $( '#predictResult' ).append( data.result );
        $body.removeClass("loading");
    })
};
