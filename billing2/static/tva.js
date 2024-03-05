$(function() {
    function vatrCalculator() {
        var vata = 0
        console.log('we are here!!');
        quantity_price = $(".qp").val();
        tva_selected = $(".vatr").val();
        vata = Number(quantity_price) * Number(tva_selected)
        $('.vata').val(vata);

    }
    $(".vatr").on( "change", function() {
          console.log('vatr changed!!');
          vatrCalculator();
    });
    $(".qp").on( "change keyup", function() {
          console.log('qp changed!!');
          vatrCalculator();
    })
});