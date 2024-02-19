$(function() {
    $(".vatr").change(vatrCalculator);
    $('.qp input').blur(vatrCalculator);
});

function vatrCalculator() {
    var vata = 0

    $(".vatr option:selected").each(function(){
        if ($('.vatr option:selected').val() == 0.19)
        {
            vata = Number($(this).val()) * (Number($('.qp input').val()));
        }
        else if ($('.vatr option:selected').val() == 0.09)
        {
            vata = Number($(this).val()) * (Number($('.qp input').val()));
        }
        else if ($('.vatr option:selected').val() == 0.05)
        {
            vata = Number($(this).val()) * (Number($('.qp input').val()));
        }
        else
        {
            vata = 0;
        }
    });
    $(".vata input").val(vata);
}